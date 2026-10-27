"""Download the evidence for one server (runs outside the Codex sandbox, where HTTPS works):
OAuth metadata, full copies of web pages, and GitHub repositories pinned to their latest commit."""

import html, io, json, re, urllib.error, urllib.parse, urllib.request, zipfile

HEADERS = {"User-Agent": "Mozilla/5.0 (mcp-research)"}
CATALOGUES = ["https://composio.dev/toolkits/{}", "https://composio.dev/toolkits/{}_mcp",
              "https://agentdiscoverability.com/track/chatgpt/{}", "https://martechdb.com/vendors/{}",
              "https://claude.com/connectors/{}"]
MAX_PAGES = 100
MAX_SUBPAGES = 60             # sub-pages followed from official tool reference / docs pages (counted in MAX_PAGES)
MAX_ORIGIN_LINKS = 10         # same-host links followed from the endpoint's origin pages
MAX_REPOS = 3
MAX_ZIP = 40_000_000          # bytes; bigger repositories are not downloaded
MAX_CODE_FILE = 1_000_000     # bytes; bigger files (data, bundles) are skipped
BINARY = re.compile(r"\.(png|jpe?g|gif|ico|svg|webp|pdf|zip|gz|tgz|woff2?|ttf|eot|mp4|mov|wasm|jar|exe|dll|so|lock)$", re.I)
GITHUB_REPO = re.compile(r"github\.com/([\w.-]+/[\w.-]+?)(?:\.git)?(?=[/\"'#?\s)<\]]|$)")
NOT_REPOS = ("orgs/", "sponsors/", "features/", "login", "about", "pricing", "topics/", "marketplace",
             "settings/", "apps/", "collections/", "enterprise", "security", "site/", "contact")


# ---------- OAuth metadata ----------

def fetch(url: str, method: str = "GET") -> str:
    """Raw HTTP status, WWW-Authenticate header and body (shortened) - or the error."""
    req = urllib.request.Request(url, method=method, headers={**HEADERS, "Accept": "application/json"})
    try:
        resp = urllib.request.urlopen(req, timeout=20)
    except urllib.error.HTTPError as err:
        resp = err
    except Exception as err:
        return f"ERROR: {err}"
    auth = resp.headers.get("WWW-Authenticate")
    body = resp.read(6000).decode("utf-8", "replace")
    return f"HTTP {resp.status}" + (f"\nWWW-Authenticate: {auth}" if auth else "") + f"\n{body}"


def well_known(base: str, name: str) -> str:
    """RFC 8414/9728: https://host/path -> https://host/.well-known/<name>/path"""
    u = urllib.parse.urlsplit(base)
    return f"{u.scheme}://{u.netloc}/.well-known/{name}{u.path.rstrip('/')}"


def oauth_metadata(endpoint: str) -> str:
    origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(endpoint))
    urls = [endpoint, well_known(origin, "oauth-protected-resource"), well_known(endpoint, "oauth-protected-resource")]
    results = {url: fetch(url, "POST" if url == endpoint else "GET") for url in dict.fromkeys(urls)}
    servers = []
    for text in results.values():
        match = re.search(r'"authorization_servers"\s*:\s*\[([^\]]*)\]', text)
        if match:
            servers += re.findall(r'"([^"]+)"', match.group(1))
    for server in dict.fromkeys(servers or [origin]):
        for name in ("oauth-authorization-server", "openid-configuration"):
            results[well_known(server, name)] = fetch(well_known(server, name))
    return "\n\n".join(f"--- {url}\n{text}" for url, text in results.items())


# ---------- web pages ----------

INLINE_TAGS = r"(?:a|abbr|b|bdi|bdo|cite|code|data|dfn|em|i|kbd|mark|q|s|samp|small|span|strong|sub|sup|time|u|var|wbr)"


def to_text(page: str) -> str:
    """Plain text of an HTML page. Inline tags (code, span, wbr, a, ...) are removed WITHOUT a line break,
    so tool names such as getOrchestrate<wbr>JourneySteps stay in one piece; block tags become line breaks."""
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", page)
    # a line break between two code spans splits one name: <code>acquisition</code><br><code>Trend</code>
    text = re.sub(r"(?is)</code>\s*<br\s*/?>\s*<code\b[^>]*>", "", text)
    text = re.sub(r"(?is)</?" + INLINE_TAGS + r"\b[^>]*>", "", text)
    text = html.unescape(re.sub(r"<[^>]+>", "\n", text))
    return re.sub(r"\n\s*\n+", "\n", text).strip()


# a string literal used as a value: preceded by : [ , ( and followed by , } ] ) - e.g. name:`get_crm_objects`
# or children:[`Search CRM records ...`, _jsx(...)]. Requiring both neighbours keeps the pairing of backticks
# correct even when the script also contains template literals with ${...}.
SCRIPT_STRING = re.compile(r"(?<=[:\[,(])\s*`([^`$]{2,3000})`(?=\s*[,}\])])"
                           r"|\"(?:children|name|title|description|content|value|text)\"\s*:\s*\"((?:[^\"\\]|\\.){2,3000})\"")
CODE_LIKE = re.compile(r"[{};]|=>|\bfunction\b|\$\{|\bvar\b|\bconst\b|\breturn\b")


def script_text(page: str) -> str:
    """Readable text that a JavaScript-rendered docs page keeps INSIDE its scripts (e.g. compiled MDX:
    _jsx(Parameter,{name:`get_crm_objects`,children:...`Fetch one or more CRM objects`})). Plain to_text()
    drops all scripts, so such tool lists vanish from pageN.txt. Returns string literals that look like text."""
    parts = []
    for block in re.findall(r"(?is)<script[^>]*>(.*?)</script>", page):
        for tick, quoted in SCRIPT_STRING.findall(block):
            s = (tick or quoted).replace("\\n", "\n").replace('\\"', '"').strip()
            if re.search(r"[A-Za-z]{2}", s) and not CODE_LIKE.search(s):
                parts.append(s)
    return "\n".join(dict.fromkeys(parts))


def base_domain(host: str) -> str:
    """support.airtable.com -> airtable.com (good enough for vendor domains; co.uk-style suffixes are rare here)."""
    return ".".join(host.lower().split(":")[0].split(".")[-2:])


def sub_pages(page: str, base: str, any_tool_page: bool) -> list:
    """Links on an official page that lead deeper into the vendor's MCP documentation:
    - same host and a path below the page's own path (e.g. /tools -> /tools/deployments);
    - any page of the vendor's domain (also another subdomain, e.g. support. -> www.) whose path contains 'mcp'
      (e.g. a support article linking to /developers/agents/mcp/tools);
    - for tool reference pages also same-host paths containing 'tool'.
    Reads HTML href attributes and Markdown links, since some docs sites serve Markdown."""
    split = urllib.parse.urlsplit(base)
    prefix = split.path.rstrip("/") + "/"
    hrefs = re.findall(r"""href\s*=\s*["']([^"'#]+)""", page) + re.findall(r"\]\((/[^)\s#]*|https?://[^)\s#]+)", page)
    found = []
    for href in hrefs:
        url = urllib.parse.urljoin(base, html.unescape(href.strip()))
        u = urllib.parse.urlsplit(url)
        if u.scheme not in ("http", "https") or base_domain(u.netloc) != base_domain(split.netloc):
            continue
        path = u.path.rstrip("/")
        if re.search(r"\.(js|css|png|svg|ico|jpe?g|gif|webp|woff2?|pdf|zip|xml)$", path, re.I) or path + "/" == prefix:
            continue
        same_host = u.netloc == split.netloc
        if (same_host and path.startswith(prefix)) or "mcp" in path.lower() \
                or (any_tool_page and same_host and "tool" in path.lower()):
            found.append(f"{u.scheme}://{u.netloc}{path or '/'}")
    return list(dict.fromkeys(found))


def concrete_url(text: str) -> str | None:
    """The endpoint as a usable URL, or None if the CSV only describes it (per-customer, not published,
    or a template such as https://<tenant>.example.com/mcp)."""
    match = re.search(r"https?://[^\s)]+", text or "")
    if not match or re.search(r"[<>{}]", match.group(0)):
        return None
    return match.group(0).rstrip("/.,;")


def save_pages(row: dict, links: dict, folder) -> tuple[set, dict]:
    """Save full copies (.html + .txt) of: endpoint pages, docs URL, catalogue guesses, all links found
    in phase 1, and same-host URLs mentioned on the first pages.
    Returns (GitHub repos seen on the pages, {url: (HTTP status or "ERROR", plain text)})."""
    endpoint = concrete_url(row["endpoint"])
    origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlsplit(endpoint)) if endpoint else None
    seeds = [origin + "/", endpoint, endpoint + "/install"] if endpoint else []
    # modes: "origin" = follow same-host links of the endpoint origin; "tools" / "docs" = follow sub-pages
    queue = [(url, "origin") for url in seeds] + [(row.get("docs") or "", "docs")]
    for key in ("tool_reference_pages", "official_docs"):              # official tool lists first
        queue += [(url, "tools" if key == "tool_reference_pages" else "docs")
                  for url in links.get(key, []) if isinstance(url, str)]
    for key, urls in links.items():
        if key not in ("unofficial_servers", "github_repos", "tool_reference_pages", "official_docs") \
                and isinstance(urls, list):
            queue += [(url, None) for url in urls if isinstance(url, str)]
    queue += [(url.format(row["name"]), None) for url in CATALOGUES]
    seen, index, repos, fetched = set(), [], set(), {}
    subpages = origin_links = 0
    folder.mkdir(parents=True, exist_ok=True)
    while queue and len(seen) < MAX_PAGES:
        url, mode = queue.pop(0)
        url = url.strip()
        if not url.startswith("http") or url in seen:
            continue
        seen.add(url)
        n = len(seen)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=30) as resp:
                status, raw = resp.status, resp.read(5_000_000)
        except urllib.error.HTTPError as err:
            status, raw = err.code, err.read(200_000)
        except Exception as err:
            index.append(f"{url} -> ERROR: {err}")
            fetched[url] = ("ERROR", "")
            continue
        page = raw.decode("utf-8", "replace")
        text = to_text(page)
        fetched[url] = (status, text)
        (folder / f"page{n}.html").write_text(page, encoding="utf-8")
        (folder / f"page{n}.txt").write_text(text, encoding="utf-8")
        line = f"{url} -> HTTP {status}, page{n}.html ({len(page)} chars), page{n}.txt ({len(text)} chars)"
        extra = script_text(page)
        if len(extra) >= 500:                    # text that the page renders with JavaScript (e.g. tool lists)
            (folder / f"page{n}.script.txt").write_text(extra, encoding="utf-8")
            line += f", page{n}.script.txt ({len(extra)} chars, text found inside the page's scripts)"
        index.append(line)
        repos.update(r.rstrip(".") for r in GITHUB_REPO.findall(page) if not r.startswith(NOT_REPOS))
        # sub-pages of official tool reference / docs pages (one level), fetched before the catalogues
        if mode in ("tools", "docs") and isinstance(status, int) and status < 400:
            children = [u for u in sub_pages(page, url, mode == "tools") if u not in seen][:MAX_SUBPAGES - subpages]
            subpages += len(children)
            queue[0:0] = [(u, None) for u in children]
        # same-host links on the endpoint's origin pages (one level deep), e.g. a newer documented endpoint path
        for link in re.findall(re.escape(origin) + r"/[\w\-./]*", page) if mode == "origin" and origin else []:
            link = link.rstrip("./")
            if link == origin or "/.well-known/" in link or re.search(r"\.(js|css|png|svg|ico|jpg|woff2?)$", link):
                continue
            if origin_links >= MAX_ORIGIN_LINKS:
                break
            origin_links += 1
            queue.append((link, None))
            if not link.endswith("/install"):
                queue.append((link + "/install", None))
    (folder / "INDEX.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    return repos, fetched


# ---------- GitHub ----------

def latest_commit(repo: str) -> tuple[str, str]:
    """(full hash, YYYY-MM-DD) of the newest commit on the default branch.
    Uses the public Atom feed first (no API rate limit), then the GitHub API."""
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://github.com/{repo}/commits.atom",
                                                           headers=HEADERS), timeout=20) as resp:
            feed = resp.read().decode("utf-8", "replace")
        entry = feed[feed.index("<entry>"):]
        sha = re.search(r"Commit/([0-9a-f]{40})", entry).group(1)
        day = re.search(r"<updated>(\d{4}-\d\d-\d\d)", entry).group(1)
        return sha, day
    except Exception:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/commits?per_page=1",
                                     headers={**HEADERS, "Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            commit = json.loads(resp.read())[0]
        return commit["sha"], commit["commit"]["committer"]["date"][:10]


def download_repo(repo: str, sha: str, folder) -> str:
    """Unzip the repository at commit `sha` into folder (text files only). Returns a short status."""
    req = urllib.request.Request(f"https://codeload.github.com/{repo}/zip/{sha}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(MAX_ZIP + 1)
    if len(data) > MAX_ZIP:
        return f"not downloaded (archive larger than {MAX_ZIP // 1_000_000} MB)"
    files = 0
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for info in archive.infolist():
            inner = info.filename.split("/", 1)[-1]       # drop the "<repo>-<sha>/" top folder
            if info.is_dir() or not inner or info.file_size > MAX_CODE_FILE or BINARY.search(inner):
                continue
            target = folder / inner
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
            files += 1
    return f"{files} files"


def save_repos(repos: list, folder) -> None:
    """Download up to MAX_REPOS repositories into folder/<org>__<repo>/ and write GITHUB_COMMITS.txt."""
    lines, shas = [], set()
    for repo in list(dict.fromkeys(repos))[:MAX_REPOS]:
        target = folder / repo.replace("/", "__")
        try:
            sha, day = latest_commit(repo)
            if sha in shas:                       # renamed/redirected repository already downloaded
                lines.append(f"https://github.com/{repo} -> same commit {sha} as a repository above (redirect); not downloaded again")
                continue
            shas.add(sha)
            status = download_repo(repo, sha, target)
            lines.append(f"https://github.com/{repo} -> latest commit {sha} ({day}); local copy: code/{target.name}/ ({status})")
        except Exception as err:
            lines.append(f"https://github.com/{repo} -> ERROR: {err}")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "GITHUB_COMMITS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def repo_names(urls) -> list:
    return [m.removesuffix(".git").rstrip(".") for url in urls for m in GITHUB_REPO.findall(str(url) + " ")
            if not m.startswith(NOT_REPOS)]


# ---------- choosing and checking sources ----------

OFFICIAL_KEYS = ("tool_reference_pages", "official_docs", "hosted_server_pages", "pricing", "legal",
                 "other_official_endpoints")
MCP_DEPENDENCY = re.compile(r"modelcontextprotocol|fastmcp|mark3labs/mcp-go|\brmcp\b|[\"'\s]mcp[\"'\s=<>~\[]", re.I)
MANIFESTS = ("package.json", "pyproject.toml", "go.mod", "Cargo.toml", "setup.py", "pom.xml", "build.gradle")


def vendor_tokens(row: dict) -> set:
    """Words that identify the vendor: domain stem and server name parts (e.g. 'tavily', 'launchdarkly')."""
    stem = row.get("vendor_domain", "").lower().split(".")[0]
    parts = re.split(r"[-_ ]", row["name"].lower())
    tokens = {t for t in [row["name"].lower(), *parts] if len(t) >= 4}
    return tokens | ({stem} if len(stem) >= 2 else set())       # short brand names such as "quo" count too


def pick_repos(row: dict, links: dict, page_repos: set) -> list:
    """Official repos from step 1 (minus those it also called unofficial), then repos seen on the pages
    only if their organisation is the vendor's (by name or same org as an official repo)."""
    unofficial = set(repo_names(links.get("unofficial_servers", [])))
    official = [r for r in repo_names(links.get("github_repos", [])) if r not in unofficial]
    orgs = {r.split("/")[0].lower() for r in official}
    tokens = vendor_tokens(row)
    extra = [r for r in sorted(page_repos) if r not in unofficial and not r.startswith("_")
             and (r.split("/")[0].lower() in orgs or any(t in r.split("/")[0].lower() for t in tokens))]
    return list(dict.fromkeys(official + extra))


def has_mcp_dependency(folder) -> bool:
    for path in folder.rglob("*"):
        if path.name in MANIFESTS or path.name.startswith("requirements") and path.suffix == ".txt":
            if MCP_DEPENDENCY.search(path.read_text(encoding="utf-8", errors="replace")):
                return True
    return False


def check_links(row: dict, links: dict, fetched: dict, repos: list, folder) -> None:
    """Write links_check.txt: is every link reachable, on the vendor's domain, about the product?"""
    tokens = vendor_tokens(row)
    vendor_domain = row.get("vendor_domain", "").lower()
    lines = ["Automatic plausibility check of the collected links (OK = no warning). Warnings do not prove a",
             "link is wrong, but such sources must be verified before they are used as evidence.", ""]
    for key, urls in links.items():
        if not isinstance(urls, list):
            continue
        for url in urls:
            status, text = fetched.get(str(url).strip(), ("not downloaded", ""))
            host = urllib.parse.urlsplit(str(url)).netloc.lower()
            warnings = []
            if status == "ERROR" or (isinstance(status, int) and status >= 400):
                warnings.append(f"HTTP {status}")
            official_repo = host == "github.com" and any(r.split("/")[0].lower() in {x.split("/")[0].lower() for x in repos}
                                                          for r in repo_names([url]))
            if key in OFFICIAL_KEYS and not (host.endswith(vendor_domain) or any(t in host for t in tokens) or official_repo):
                warnings.append("not on the vendor's domain")
            if key == "github_repos":
                for repo in repo_names([url]):
                    if not any(t in repo.split("/")[0].lower() for t in tokens):
                        warnings.append("GitHub organisation does not contain the vendor name")
                    if repo in set(repo_names(links.get("unofficial_servers", []))):
                        warnings.append("also listed as unofficial - not downloaded")
            if text and not any(t in text.lower() for t in tokens):
                warnings.append("product name not mentioned on the page")
            if text and key in ("tool_reference_pages", "official_docs", "hosted_server_pages", "tool_catalogues") and "mcp" not in text.lower():
                warnings.append("'MCP' not mentioned on the page")
            lines.append(f"[{key}] {url} -> {'; '.join(warnings) or 'OK'}")
    lines.append("")
    for repo in repos[:MAX_REPOS]:
        local = folder / "code" / repo.replace("/", "__")
        warnings = []
        if not any(t in repo.split("/")[0].lower() for t in tokens):
            warnings.append("organisation name does not contain the vendor name - check that it is official")
        if local.exists() and not has_mcp_dependency(local):
            warnings.append("no MCP SDK dependency found in manifests - may not be an MCP server")
        if repo in set(repo_names(links.get("unofficial_servers", []))):
            warnings.append("listed as unofficial")
        lines.append(f"[repo] https://github.com/{repo} -> {'; '.join(warnings) or 'OK'}")
    (folder / "links_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
