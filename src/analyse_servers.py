"""
Analyse MCP servers in three steps per server. Run: python main.py --analyse (or --links-only).
"""

import csv, json, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime

import config
from src import sources


def load_prompt(path) -> str:
    """The prompt file contains only the prompt text (with {{placeholders}})."""
    return path.read_text(encoding="utf-8").strip()


def fill_prompt(template: str, row: dict, oauth: str = "") -> str:
    for key, value in row.items():
        template = template.replace("{{" + key + "}}", value or "(none)")
    return (template.replace("{{YYYY-MM-DD}}", date.today().isoformat())
                    .replace("{{English}}", config.LANGUAGE)
                    .replace("{{prefetched_oauth}}", oauth))


def extract_json(text: str) -> dict:
    text = text[text.find("{"):text.rfind("}") + 1]
    text = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)   # drop // comments
    for _ in range(100):      # repair unescaped quotes inside strings, e.g. "use "get_x" when ..."
        try:
            return json.loads(text, strict=False)
        except json.JSONDecodeError as err:
            if err.msg.startswith("Extra data"):      # valid object followed by junk, e.g. one extra "}" at the end
                return json.JSONDecoder(strict=False).raw_decode(text)[0]
            if not err.msg.startswith(("Expecting ',' delimiter", "Expecting ':' delimiter")):
                raise
            quote = text.rfind('"', 0, err.pos)              # the quote that ended the string too early
            if quote <= 0:
                raise
            text = text[:quote] + '\\"' + text[quote + 1:]
    return json.loads(text, strict=False)


def run_codex(prompt: str, answer_file, work_dir, effort: str, timeout_min: int) -> subprocess.CompletedProcess:
    codex = shutil.which("codex") or sys.exit("Codex CLI not found. Install it and run `codex login`.")
    cmd = [codex, "--search", "-s", "workspace-write",
           "-c", "sandbox_workspace_write.network_access=true", "-C", str(work_dir),
           "-m", config.MODEL, "-c", f'model_reasoning_effort="{effort}"',
           "exec", "--skip-git-repo-check", "-o", str(answer_file), "-"]
    answer_file.unlink(missing_ok=True)      # never parse an answer left over from an earlier run
    return subprocess.run(cmd, input=prompt, text=True, encoding="utf-8", capture_output=True,
                          timeout=timeout_min * 60)


def collect_links(name: str, row: dict, work_dir) -> dict:
    """Step 1: ask Codex only for URLs. Reused if links.json already exists."""
    links_file = work_dir / "links.json"
    if links_file.exists():
        links = json.loads(links_file.read_text(encoding="utf-8"))
        if links.get("_prompt") == config.LINKS_PROMPT_FILE.name:     # reuse only if made by the same prompt
            return links
    prompt = fill_prompt(load_prompt(config.LINKS_PROMPT_FILE), row)
    answer_file = work_dir / "links.answer.txt"
    try:
        run_codex(prompt, answer_file, work_dir, config.LINKS_EFFORT, config.LINKS_TIMEOUT_MIN)
        links = extract_json(answer_file.read_text(encoding="utf-8"))
        assert isinstance(links, dict)
    except Exception as err:
        log(f"{name}: link collection failed ({type(err).__name__}) - continuing with default pages")
        return {}
    links["_prompt"] = config.LINKS_PROMPT_FILE.name
    links_file.write_text(json.dumps(links, ensure_ascii=False, indent=2), encoding="utf-8")
    return links


def fill_commit(result: dict) -> None:
    """If Codex named a GitHub repository but no full commit hash, look it up ourselves."""
    general = result.get("A_general", {})
    repos = sources.repo_names([general.get("repository_url", "")])
    if not repos or re.fullmatch(r"[0-9a-f]{40}", str(general.get("commit_hash", "")).strip()):
        return
    try:
        sha, day = sources.latest_commit(repos[0])
    except Exception:
        return
    general["commit_hash"], general["commit_date"] = sha, day
    general["commit_note"] = "commit hash/date filled in by the research script (latest commit on the default branch)"


def save_result(name: str, answer: str, work_dir, minutes) -> bool:
    """Parse Codex's answer, insert actions.json, save data/<version>/<server>.json."""
    try:
        result = extract_json(answer)
        assert isinstance(result, dict)
    except (ValueError, AssertionError):
        return False
    try:   # the complete action list is written to a separate file (too long for the answer)
        actions = json.loads((work_dir / "actions.json").read_text(encoding="utf-8"))
        if isinstance(actions, list) and actions:
            result.setdefault("E_aggregated", {})["actions"] = actions
    except (OSError, json.JSONDecodeError):
        log(f"{name}: no valid actions.json - keeping the actions from the answer")
    fill_commit(result)
    result["_run"] = {"model": config.MODEL, "reasoning_effort": config.REASONING_EFFORT,
                      "prompt": config.PROMPT_FILE.name, "links_prompt": config.LINKS_PROMPT_FILE.name,
                      "date": date.today().isoformat(), "duration_min": minutes}
    (config.DATA_DIR / f"{name}.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for leftover in (f"{name}.answer.txt", f"{name}.error.txt"):
        (config.DATA_DIR / leftover).unlink(missing_ok=True)
    return True


def analyse(name: str, row: dict, template: str, stop: threading.Event) -> bool | None:
    """All three steps for one server. Returns True (saved), False (failed) or None (skipped)."""
    out = config.DATA_DIR / f"{name}.json"
    if stop.is_set() or (out.exists() and not config.OVERWRITE and not config.LINKS_ONLY):
        return None
    work_dir = config.WORK_DIR / name
    answer_file = config.DATA_DIR / f"{name}.answer.txt"
    if answer_file.exists() and not config.LINKS_ONLY and \
            save_result(name, answer_file.read_text(encoding="utf-8"), work_dir, "n/a (answer of an earlier run repaired)"):
        log(f"{name}: earlier answer repaired and saved (no new Codex run)")
        return True

    start = time.monotonic()
    log(f"{name}: started")
    work_dir.mkdir(parents=True, exist_ok=True)

    links = collect_links(name, row, work_dir)                                   # step 1
    for old in ("pages", "code"):                                                # fresh downloads every run
        shutil.rmtree(work_dir / old, ignore_errors=True)
    endpoint = sources.concrete_url(row["endpoint"])                             # step 2
    oauth = sources.oauth_metadata(endpoint) if endpoint else (
        f"NOT FETCHED: the input endpoint is not a concrete public URL ({row['endpoint']}). "
        "It is per customer or not published, so there is no public OAuth metadata to fetch; "
        "use the documentation to describe how customers obtain and authorise their endpoint.")
    (work_dir / "oauth_metadata.txt").write_text(oauth, encoding="utf-8")
    page_repos, fetched = sources.save_pages(row, links, work_dir / "pages")
    repos = sources.pick_repos(row, links, page_repos)
    sources.save_repos(repos, work_dir / "code")
    sources.check_links(row, links, fetched, repos, work_dir)
    log(f"{name}: sources downloaded after {round((time.monotonic() - start) / 60, 1)} min")
    if config.LINKS_ONLY:                                                        # steps 1-2 only
        return True

    (work_dir / "actions.json").unlink(missing_ok=True)                          # step 3
    prompt = fill_prompt(template, row, oauth)
    (config.PROMPTS_DIR / f"{name}.md").write_text(prompt, encoding="utf-8")
    try:
        proc = run_codex(prompt, answer_file, work_dir, config.REASONING_EFFORT, config.TIMEOUT_MIN)
    except subprocess.TimeoutExpired:
        log(f"{name}: timeout after {config.TIMEOUT_MIN} min")
        return False
    minutes = round((time.monotonic() - start) / 60, 1)
    answer = answer_file.read_text(encoding="utf-8") if answer_file.exists() else ""
    if not save_result(name, answer, work_dir, minutes):
        (config.DATA_DIR / f"{name}.error.txt").write_text(proc.stderr[-20000:] + "\n\n" + answer, encoding="utf-8")
        log(f"{name}: no valid JSON after {minutes} min -> {name}.error.txt")
        return False
    log(f"{name}: saved in {minutes} min")
    return True


PRINT_LOCK = threading.Lock()


def log(message: str):
    with PRINT_LOCK:
        print(f"[{datetime.now():%H:%M:%S}] {message}", flush=True)


def main():
    with open(config.CSV_FILE, encoding="utf-8") as f:
        rows = {row["name"]: row for row in csv.DictReader(f)}
    names = config.SERVERS
    chosen = config.CHOSEN_FILE.read_text(encoding="utf-8").split()
    if names == "remaining":
        names = [n for n in rows if n not in set(chosen)]
    elif names == "chosen":                     # the 20 manually analysed servers
        names = chosen

    template = load_prompt(config.PROMPT_FILE)
    config.PROMPTS_DIR.mkdir(exist_ok=True)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    stop = threading.Event()     # set after 3 failures in a row (usually: usage limit reached)
    failures = done = 0
    start = time.monotonic()

    with ThreadPoolExecutor(max_workers=config.PARALLEL) as pool:
        jobs = {pool.submit(analyse, n, rows[n], template, stop): n for n in names}
        for job in as_completed(jobs):
            try:
                ok = job.result()
            except Exception as err:             # a bug for one server must not stop the others
                log(f"{jobs[job]}: unexpected error {err!r} - skipped, please report")
                continue                         # not counted as a usage-limit failure
            if ok is None:
                continue
            done += ok
            failures = 0 if ok else failures + 1
            if failures >= 3 and not stop.is_set():
                stop.set()
                log("3 failures in a row (usage limit reached?) - finishing running jobs, starting no new ones")

    log(f"finished: {done} saved in {round((time.monotonic() - start) / 60, 1)} min. "
        "Failed servers: see data/*.error.txt; run again later - finished servers are skipped.")
