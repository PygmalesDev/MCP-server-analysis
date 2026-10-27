# Prompt Log

| Version       | Date       | Model                                                                                                                      | File                          | Status                                                              |
| ------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ------------------------------------------------------------------- |
| v1            | 2026-10-23 | GPT Sol (with web search)                                                                                                  | `prompt_v1.md`                | Tested on 3 servers on 2026-10-23, replaced by v2                   |
| v2            | 2026-10-24 | GPT-6 Luna (Codex, web search + shell with internet access)                                                                | `prompt_v2.md`                | Tested on 3 servers on 2026-10-24, replaced by v3                   |
| v3            | 2026-10-24 | GPT-6 Luna, effort high (Codex; OAuth metadata and pages are downloaded by the script)                                     | `prompt_v3.md`                | Tested on 3 servers on 2026-10-24, replaced by v4                   |
| v4            | 2026-10-24 | GPT-6 Luna, effort high (+ latest GitHub commits are fetched by the script)                                                | `prompt_v4.md`                | Tested on 4 servers on 2026-10-24, replaced by v5                   |
| v5            | 2026-10-24 | GPT-6 Luna, effort high (+ catalogue pages are downloaded and the commit hash is filled in by the script)                  | `prompt_v5.md`                | Not run: immediately replaced by the three-step pipeline of v6      |
| links_v1 + v6 | 2026-10-26 | Step 1: GPT-6 Luna, effort low (link collection); step 3: GPT-6 Luna, effort high (analysis)                               | `links_v1.md`, `prompt_v6.md` | Tested on 4 servers on 2026-10-26, replaced by links_v2 + v7        |
| links_v2 + v7 | 2026-10-26 | as above + automatic link check (`links_check.txt`); link collection with effort `medium`                                  | `links_v2.md`, `prompt_v7.md` | Tested on 4 servers on 2026-10-26                                   |
| links_v3 + v8 | 2026-10-26 | Step 1: GPT-6 Luna, effort medium; step 3: GPT-6 Luna, effort high; + sub-pages of official tool references are downloaded | `links_v3.md`, `prompt_v8.md` | Re-run of 14 servers whose tool lists were wrong in the v7 full run |
| links_v3 + v9 | 2026-10-27 | as v8 (GPT-6 Luna); + text of JavaScript-rendered pages (`pageN.script.txt`), `<br>` inside code names joined              | `links_v3.md`, `prompt_v9.md` | Re-run of 3 servers (hubspot, pendo, vercel) after the v8 check     |

---

## v1

Based on the findings of the manual analysis of 20 servers. The prompt incorporates the errors and pitfalls found during the manual analysis:

| Observation from the manual analysis | How the prompt addresses it |
|---|---|
| Public code often ≠ the server at the CSV endpoint (Tavily, Grafana, Basic Memory, Heroku, LaunchDarkly, Braze) | Step 2 + field `open_code_equals_deployed_server` |
| Public OAuth metadata (`/.well-known/...`) reveals permissions (scopes) that are not in the documentation (Quo, Brex, Airwallex) | Step 1.3 + comparison of scopes with the tool list |
| For closed servers, tool lists exist only in third-party catalogues, and they disagree (Lucid: 30 vs 35) | Step 1.7: THIRD-PARTY label and snapshot date |
| Third-party wrappers and unofficial servers get confused with official ones (Shapes/Knit, Tripadvisor, GoCardless) | Step 2 |
| Identical names for different products (motion.dev ≠ Motion calendar) | Step 2 |
| Contradictions: documentation ↔ tools ↔ scopes ↔ code (ClickUp, Brex, Heroku, Similarweb) | Separate field `contradictions` |
| The model tends to "paraphrase" instead of copying verbatim | Strict rule for the verbatim field |
| Mechanisms important for the research (server-side confirmation, masking, vendor interests, skills, nested agents, "universal" tools) | 13-item checklist in step 4 |
| Compatibility with the Excel template `MCP_manual_analysis.xlsx` is needed | The JSON schema mirrors its sheets: Servers, Capabilities (15 rows), Actions, Observations |

**Format decisions.**
- One server per conversation: less confusion and fewer truncated answers.
- The result is strictly JSON so that it can later be transferred to Excel automatically.

---

### Test results v1
Run: Codex CLI, `gpt-6.1-sol`, reasoning effort `medium`, sandbox `read-only`, 2023-10-26.

| Server | Missing | Invented / wrong | Without source | Other |
| --- | --- | --- | --- | --- |
| tavily | **The entire analysis of the public code.** No tool parameters ("NOT PUBLISHED"), no commit hash, no verbatim descriptions, no token estimate. Not found: the AI's parameters being overridden via `DEFAULT_PARAMETERS`, crawl results truncated to 200 characters, the hard-coded `chunks_per_source: 3`, the texts of keyless responses (x402, bonus credits). | No obvious inventions. Debatable: structure "Non-standard" (because of the Tavily research agent; manual analysis: "standard"). Capabilities are almost all "Unknown", although the code clearly shows "No". | None: every field has links. But code links are not pinned to a commit (branch `main`). | **Pros:** found more documentation than the manual analysis! EU endpoint `mcp.eu.tavily.com`, the keyless-mode header, `/logs` and `/usage`, the promise of "PII redaction and prompt injection protection" in the Anthropic catalogue, the model-training clauses in the Terms. Correctly separated the documentation server `docs.tavily.com/mcp` from the product server. **Cons:** very long text; the model could not download the code because the shell has no internet access in the `read-only` sandbox. |
| gocardless | **Almost the entire tool list.** Only 2 names were taken from the Claude catalogue (manual analysis: 24 tools from Composio, with scopes). The model deliberately did not use the third-party catalogue because "an official list exists". No OAuth metadata retrieved (manual analysis: Dynamic Client Registration, PKCE S256, `registration_endpoint`). Not found: the £50 liability cap, the tools "Submit feedback" and "Get environment". | None. | None. | **Pros:** correctly found the confirmation of payment operations, data masking, the "App (GoCardless MCP)" event log, the limit of 25 payments, the contradiction "terms prohibit personal data ↔ the server returns it". Found US prices and GoCardless's broad rights to inputs and outputs (not in the manual analysis). **Cons:** network blocked, as for tavily. |
| launchdarkly | **All actions (empty list).** The CSV path `/mcp/v1` differs from the documented path `/mcp/launchdarkly`, and the model refused to transfer data from one to the other. Therefore almost all capabilities are "Unknown", although the install page publishes the tools with annotations. | None. | None. | **Pros:** found that the install page now lists **170 tools** (manual analysis from 24.10: about 97; verified on 26.10: the page says "Available Tools (170)"; manual analysis `18_launchdarkly.md` updated on 26.10). Found a second endpoint `/mcp/fm` (111 tools), the tool `vent` for complaints to the vendor, a server instruction about agent skills, a token lifetime of 2 hours and re-authorisation every 90 days. |

The model does not invent anything and cites sources carefully; it finds documentation even better than the manual analysis. However, at the slightest doubt ("this is a different path", "this is local code", "this is a third-party catalogue") it leaves the field empty. That is why sections C and E are almost empty.

The Codex `read-only` sandbox blocks network access for commands: `git clone` and `curl` to `/.well-known/...` do not work. Only the built-in web search remains, which does not open JSON files and does not give a commit hash.

---

### Changes for v2

| Problem in v1 | Change in v2 |
| --- | --- |
| Fields left empty "out of caution" | New principle "best available evidence, labelled with its source": `[LOCAL CODE @hash]`, `[DOCS]`, `[ENDPOINT path]`, `[THIRD-PARTY catalogue, date]`. `NOT FOUND` only if nothing at all exists |
| Public code not analysed (tavily) | If official public code of the same product exists, it should be downloaded (`git clone`) and analysed in full, with the commit hash |
| CSV path ≠ documented path (launchdarkly) | Describe the documented endpoint on the same host with a label and record the path difference in `contradictions` |
| Third-party catalogue not used although the official list is incomplete (gocardless) | Catalogues are allowed if the official list is incomplete (names only, no descriptions or parameters) |
| "Unknown" where the code clearly shows "no" | New value `No (public code)` |
| No network for commands, OAuth metadata not retrieved | Prompt section "YOUR TOOLS" (`curl`, `git clone`). In the script: sandbox `workspace-write` with network access and a separate working folder `code/work/<server>` |
| Very long answers | Length limits for every field |
| Debatable "Non-standard" because of the research agent (tavily) | Clarified definition: a single tool that calls the vendor's AI does not by itself make the structure non-standard (recorded in D, item 12) |
| Sol usage limit consumption (14 % for 3 servers) | Model changed to GPT-6 Luna (medium) |

### Test results v2
Run: Codex CLI, `gpt-6-luna`, reasoning effort `medium`, sandbox `workspace-write` with network, 2026-10-24.

| Server | Better than v1                                                                                                                                                                                                                                                                                                  | Remaining / worse |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tavily | **Public code analysed:** 6 tools with parameters (search 15, extract 6, crawl 10, map 6, research 2, feedback 10 - almost identical to the manual analysis), licence, SDK, capabilities "No (public code)", verbatim instructions from the description of `tavily_feedback`. The answer is noticeably shorter. | No commit hash. Not found: override of the AI's parameters via `DEFAULT_PARAMETERS` (described as "merges"), crawl truncation to 200 characters, `chunks_per_source: 3`, promotional texts of the keyless mode. Prices taken from a third-party catalogue although an official page exists. Information from v1 lost: EU endpoint, keyless-mode header, `/logs`. |
| gocardless | Found verbatim advice to the user ("Some LLMs have a tendency to search the web instead of using an MCP"), the event log, masking, the limit of 25 payments.                                                                                                                                                    | Still 2 tools plus the placeholder "[account management tools: names not published]". Composio not used, although the rule allowed it. OAuth metadata not retrieved. |
| launchdarkly | Used the documented endpoint `/mcp/launchdarkly`: **170 tools**, the full server instruction verbatim ("…ask the user if they want them installed from https://github.com/launchdarkly/ai-tooling"), the rules `confirm=true` and the `safe` check, `update-alert` with 20 parameters.                          | Only 12 of 170 tools in `actions`. **Errors:** "No rating/feedback mechanism found", although `vent` exists; "no tool filtering configuration found", although the documentation describes `toolsets` and `writes`. |

On Windows, HTTPS does not work in the shell inside the Codex sandbox: `curl` and `git` fail with the error `SEC_E_NO_CREDENTIALS` (Schannel). Therefore no OAuth metadata or commit hashes were retrieved for any server.

---
### Changes for v3

| Problem in v2                                                                                                   | Change in v3                                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HTTPS does not work in the Codex sandbox                                                                        | OAuth metadata is requested **by the Python script itself** before Codex starts: POST to the endpoint (status and `WWW-Authenticate`), `oauth-protected-resource` (with and without the path), then `oauth-authorization-server` and `openid-configuration` of the authorization server found. The responses are inserted into the prompt and saved in `work/<server>/oauth_metadata.txt` |
| No commit hash                                                                                                  | Read GitHub via the browser; take the hash from the `/commits/<branch>` page                                                                                                                                                                                                                                                                                                              |
| Only examples in `actions` (launchdarkly: 12 of 170)                                                            | Requirement to list ALL tools, in compact form if there are more than 60; state how many names could be read                                                                                                                                                                                                                                                                              |
| Composio not used (gocardless)                                                                                  | Third-party catalogues are **mandatory** if the official list is clearly incomplete; placeholders are forbidden                                                                                                                                                                                                                                                                           |
| `vent` and `toolsets` not found (launchdarkly)                                                                  | Explicit search of the complete list in the checklist: feedback, vent, rate, report…; filter parameters `toolsets`, `writes`, `readonly`                                                                                                                                                                                                                                                  |
| Parameter override, truncation and promotional texts not found (tavily)                                         | Read the request handlers, not only the tool descriptions; a concrete list of what to look for                                                                                                                                                                                                                                                                                            |
| Third-party prices instead of official ones; hosted-server specifics lost                                       | Official pricing page first; read the hosted-server documentation even when code is available                                                                                                                                                                                                                                                                                             |
| The Codex browser truncates long pages (the LaunchDarkly page has 114,000 characters, ≈86 of 170 names visible) | The script itself downloads **complete** copies of the pages: host root, endpoint, `<endpoint>/install`, the documentation from the CSV and same-host links found there (e.g. the new path `/mcp/launchdarkly` and its `/install`). Saved in `work/<server>/pages/` as `.html` and `.txt` with an index `INDEX.txt`; Codex reads them locally, without truncation                         |
| Long answer with 170+ tools                                                                                     | Codex writes the complete action list to `work/<server>/actions.json`; the script inserts it into the final JSON                                                                                                                                                                                                                                                                          |

---
### Test results v3
Run: Codex CLI, `gpt-6-luna`, reasoning effort `high`, 5 in parallel, 2026-10-24.

| Server       | Better than v2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Remaining                                                                                                                                                                                                                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| tavily       | **OAuth metadata retrieved** (scopes `openid offline_access`, DCR `/register`, PKCE S256, `/revoke`). **Override of the AI's parameters via `DEFAULT_PARAMETERS` found** (also recorded as a contradiction: the README calls them "defaults"). Crawl (11) and map (8) parameters now match the manual analysis. Commit hash present, prices from the official page.                                                                                                                                                                                      | Hash is not the latest (`d57bbe3`, 2026-09-02; current: `688b0f7`, 2026-10-15), hence SDK 1.30.0 instead of 1.31.0. Not found: crawl truncation to 200 characters, `chunks_per_source: 3`, keyless promotional texts. Tokens taken from a third-party catalogue.                                 |
| gocardless   | **24 tools** (Agent Discoverability catalogue) - as in the manual analysis, including `submit_feedback` and `get_environment`. **OAuth metadata matches the manual analysis** (DCR, S256, `none`, no scopes). **New:** a verbatim instruction from the tool descriptions about two-step confirmation: "first call with confirmed=false returns a preview; second call with confirmed=true executes after the user has explicitly confirmed in their next message". This reveals the confirmation mechanism that remained unknown in the manual analysis. | Parameters not published (as in the manual analysis).                                                                                                                                                                                                                                            |
| launchdarkly | **All 170 tools** in `actions.json`. **OAuth metadata:** scopes `reader`/`writer`, DCR, `client_credentials`, authorization server `app.launchdarkly.com/trust/oauth`. **Important new finding:** the CSV endpoint `/mcp/v1` has its own install page - "launchdarkly v1", **18 tools** (flags and approvals only). Verified on 26.10.                                                                                                                                                                                                                   | `actions` contains the 170 tools of another endpoint, although `/mcp/v1` has its own list. **Errors:** "No feedback tool identified", although `vent` is in its own list; "no tool filter", although the documentation describes `toolsets`/`writes` (the `mcp-hosted` page was not downloaded). |

---
### Changes for v4

| Problem in v3 | Change in v4 |
| --- | --- |
| launchdarkly: another endpoint described, although the CSV endpoint has its own list | If the CSV endpoint has its own evidence (an `/install` page, OAuth metadata), it is the object of the analysis; the other endpoint goes only into `other_official_servers` and `contradictions` |
| `vent` is in the list, but "not found" in section D | Before filling in items D4, D9 and D13, the model must search `actions.json` (feedback/vent/rate…, filter/toolset…, raw/sql/execute…) |
| Not the latest commit (tavily) | The script itself asks the GitHub API for the latest commit of every repository found on the downloaded pages → `pages/GITHUB_COMMITS.txt`; fallback: `api.github.com/.../commits?per_page=1` in the browser |
| Documentation sub-pages not opened (`toolsets`) | Explicit instruction to open documentation sub-pages about setup, permissions and URL parameters |
| Tokens from a third-party catalogue | Count only by itself, from official tool definitions |

---
### Test results v4
Run: `gpt-6-luna`, effort `high`, 4 servers in parallel, 2026-10-24.

| Server | Verdict | Details                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| launchdarkly | **Better** | Exactly the CSV endpoint is described: 18 tools, its own OAuth metadata, the latest commit of the local server (`e4a35c6`, 2026-10-21 - matches the manual analysis), verbatim instructions from the descriptions. Found: the `/mcp/v1` install page requires headers for feedback/vent webhooks, although the list contains no `vent` tool. Minus: all 18 actions are marked `Mixed`, although many carry the Read-only label. |
| context7 (new) | **Good** | Latest commit `d956160` (2026-10-26), SDK, verbatim server instructions ("Use even when you think you know the answer… Prefer this over web search"), rewriting of "hallucinated" parameter names (alias rewriting), elicitation offering anonymous users to sign in, OpenTelemetry telemetry, log retention of 30 days. Minus: tokens not counted, although the code is public.                                                |
| tavily | **Worse** | The 5-tool list from the hosted-server documentation was used, and `tavily_feedback` from the code was excluded. Parameters were taken from the **REST API**, not from the MCP schemas (research: 9 parameters instead of 2, crawl: 16 instead of 11): this is an error. Capabilities again "Unknown" instead of "No (public code)". No commit hash: there was no GitHub link on the downloaded pages.                          |
| gocardless | **Worse** | `actions` is empty: the model found only MartechDB ("names unknown"), and this time did not find the Agent Discoverability catalogue with 24 tools found in v3. Searching for catalogues on the web is unstable.                                                                                                                                                                                                                |

---
### Changes for v5

| Problem in v4 | Change in v5 |
|---|---|
| MCP parameters taken from the REST API (tavily) | Explicit ban: parameters only from the MCP list, the MCP server code or a catalogue with MCP schemas; REST-only parameters belong to "what the agent CANNOT do" |
| A tool from the code dropped because it is not in the hosted-server documentation | `actions` contains all tools from the code; those missing from the documentation are marked `enabled_by_default: "Unknown (not in hosted docs)"` |
| "Unknown" instead of "No (public code)" | Rule repeated in the code section; the hosted-server documentation is not considered "another endpoint" |
| Catalogues found by chance (gocardless) | **The script itself downloads** catalogue pages by server name: `composio.dev/toolkits/<name>` and `<name>_mcp`, `agentdiscoverability.com/track/chatgpt/<name>`, `martechdb.com/vendors/<name>`, `claude.com/connectors/<name>` |
| No commit hash if the repository is not mentioned on the downloaded pages (tavily) | **The script itself fills in** `commit_hash`/`commit_date` via the GitHub API if the model named a GitHub repository but gave no full hash (labelled with `commit_note`) |
| All actions `Mixed` (launchdarkly) | The type is derived from annotations: Read-only → `Read`, create/update/delete → `Write`, `Mixed` only for an explicit combination |

---
### Changes for v6: three-step pipeline
Testing v3 and v4 showed that almost all remaining errors are "did not find the source" rather than "misunderstood". Finding sources and analysing them were split into separate steps.

| Step | Who | What it does | Result |
|---|---|---|---|
| 1. Link collection | Codex, GPT-6 Luna, effort `low`, prompt `links_v1.md` | Only searches for URLs by category: documentation and sub-pages, pages on the endpoint host, official GitHub repositories, packages, pricing, legal pages, third-party tool catalogues, other endpoints, unofficial servers. Analyses nothing | `work/<server>/links.json` |
| 2. Download | Python (`sources.py`), no model | Downloads in full all pages from step 1, the endpoint pages, guessed catalogue pages and the OAuth metadata; official GitHub repositories as an archive at the latest commit (hash and date from the commits Atom feed, no API limit) | `oauth_metadata.txt`, `pages/`, `code/` |
| 3. Analysis | Codex, GPT-6 Luna, effort `high`, prompt `prompt_v6.md` | Analyses the local files first (searches code with `rg`/`findstr`/`python`), uses the internet only for what is missing | `data/prompt_v6/<server>.json` |

**Differences between `prompt_v6.md` and v5:** the evidence folder is described (`links.json`, `pages/`, `code/` with `GITHUB_COMMITS.txt`); __code is read locally__ instead of in the GitHub browser; code links are pinned to the hash from `GITHUB_COMMITS.txt` with line numbers from the local files; unofficial servers from `links.json` are used only for notes.

**Additional benefit for the research:** the folder `work/<server>/` is a snapshot of all sources on the analysis date, against which every conclusion can be re-checked even if the vendor's website changes.

---
### Test results links_v1 + v6
Run: 4 servers in parallel.

**Link collection (step 1).** Found 9–15 official documentation pages per server, including sub-pages, legal pages, pricing, 5–6 catalogues per server, and the second LaunchDarkly endpoint `/mcp/fm`. **Errors:** for GoCardless, the unofficial repository `jmceleney/gocardless-mcp` ended up in `github_repos` (and at the same time in `unofficial_servers`); unrelated repositories were picked up from the downloaded pages (`apideck-libraries/portman`, `composiohq/composio`, `chatmcp/mcp-directory`).

| Server | Verdict | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|---|---|---|
| tavily | **Best result of all versions** | Latest commit `514e56c` (2026-10-26), SDK 1.32.0; 6 tools with parameters from the code, `tavily_feedback` marked "not in hosted docs"; capabilities "No (public code)". **Everything key from the manual analysis was found:** override of the AI's parameters via `DEFAULT_PARAMETERS`, crawl truncation to 200 characters, keyless messages with sign-up, "agentic payment" and bonus credits, the headers `X-Client-Source`/`X-Session-Id`/`X-Human-Id`. Not found: the hard-coded `chunks_per_source: 3`; tokens not counted. |
| gocardless | Good | 24 tools from Composio (with "human-readable" names rather than machine names), `Submit feedback` found. Lost the instruction about two-step confirmation `confirmed=false/true`, which is on the downloaded Agent Discoverability page with machine names.                                                                                                                                                                                                                                                                        |
| launchdarkly | Partial | The 18 tools of the CSV endpoint are correct, OAuth and instructions are correct. **Error:** 20 tools from the public code were added to `actions`, although that is a different server (local, for EU/Federal) - the rule "all tools from the code" was applied to a different server variant.                                                                                                                                                                                                                                    |
| context7 | Good | As in v4, plus tokens counted from the code (≈1140) and plan-upgrade messages in API responses found.                                                                                                                                                                                                                                                                                                                                                                                                                              |

---
### Changes for links_v2 + v7

| Problem | Change |
| --- | --- |
| Unofficial repository among the official ones; unrelated repositories from pages | `links_v2.md`: `github_repos` contains only the vendor's organisation or links from its documentation. The script (`pick_repos`): does not download repositories marked as unofficial; repositories from pages only if the organisation matches an official one or contains the vendor's name |
| No check that links are correct | The script writes `links_check.txt`: HTTP errors, foreign domain for "official" links, product or "MCP" not mentioned on the page, GitHub organisation not the vendor's, no MCP SDK dependency in the manifests, link listed as both official and unofficial. `prompt_v7`: sources with warnings must not be used without the model's own verification |
| Tools of a different server variant in `actions` (launchdarkly) | `prompt_v7`: tools from the code are added only if the code is the same server or its direct local equivalent; otherwise only in `other_official_servers` with their count |
| Human-readable names instead of machine names; confirmation instruction lost (gocardless) | `prompt_v7`: prefer the catalogue with exact machine names; quote behavioural instructions from tool descriptions in catalogues verbatim, labelled with the catalogue |
| Tokens not counted although code is public (tavily) | `prompt_v7`: if code of the same server is available, tokens must be counted from the code |


---
### Test results links_v2 + v7
Run: 4 servers in parallel, 2026-10-26.

| Server | Verdict | Details |
|---|---|---|
| launchdarkly | **Fixed** | Exactly the 18 tools of the endpoint `/mcp/v1`; the code of the local EU/Federal server (20 tools) and the server `/mcp/launchdarkly` (170) are described only in `other_official_servers` and `contradictions`. Types: 7 Read, 10 Write, 1 Mixed. |
| context7 | Good | As in v6; tokens from the code ≈1450; found that telemetry can be disabled with `OTEL_SDK_DISABLED=true`. |
| tavily | Good, with fluctuations | Commit, SDK, 6 tools from the code, "No (public code)", crawl truncation to 200 characters. But this time: the parameter override is described as "merging" (correctly described as an override in v6), tokens not counted (the model considered the code only "partially equivalent"). |
| gocardless | Unchanged | 24 tools from Composio with "human-readable" names; the rule to prefer the catalogue with machine names did not take effect. |

**Shortcomings found:**
- with effort `low`, the collector did not find in this run some key official pages that had been found in the previous run;
- a parsing error for a link with a trailing dot (`context7-mcp.`) and repeated download of the same repository under its old name;
- a false "foreign domain" warning for a link to the vendor's GitHub repository in the documentation.

**Fixes:** link collection switched to effort `medium`.


---
### Changes for links_v3 + v8 
Reason: a check of the v7 full run against official sources (41 servers whose actions came from third-party catalogues). For 14 of them the vendor publishes an official tool list, but `actions` was built from a catalogue, was incomplete or carried wrong names.

| Problem (servers)                                                                                                                                                                       | Cause                                                                                                                                                   | Change                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Official list existed and was downloaded, but `actions` came from a catalogue (hubspot, jam, mixpanel, amplitude, clerk, kindora-funder-discovery, microsoft-learn, vybe-solana, pendo) | `prompt_v7` step 1.7 told the model to prefer the catalogue with machine names and full descriptions; the model rejected official lists without schemas | `prompt_v8`: new section "Source hierarchy for actions" - the official list is the base, catalogues only add tools (marked "Unknown (not in official list)")                                                                                                                                                                   |
| Official tool names labelled "Third-party" (airtable, hubspot, jam, mixpanel, microsoft-learn, vybe-solana, kindora-funder-discovery)                                                   | `source_type` followed the source of the description/parameters                                                                                         | `prompt_v8`: `source_type` = where the tool NAME is confirmed; borrowed descriptions/parameters are prefixed with the catalogue; python check before writing `actions.json`                                                                                                                                                    |
| claude.com/connectors labelled "Official" for some servers and "Third-party" for others                                                                                                 | no rule                                                                                                                                                 | `prompt_v8`: always `Third-party (Claude connector directory, <date>)`                                                                                                                                                                                                                                                         |
| Tool names with proxy prefixes `liltmcp_`, `metaviewmcp_` (lilt, metaview)                                                                                                              | Scalekit renames the tools it proxies                                                                                                                   | `prompt_v8`: record native names, remove platform prefixes, mark proxy-only helpers                                                                                                                                                                                                                                            |
| Only part of a split tool reference read (vercel: 27 category pages, 217 + 31 tools)                                                                                                    | the script followed links only from the endpoint origin; the collector listed only the overview page                                                    | `links_v3`: new category `tool_reference_pages` incl. every sub-page; `sources.py`: follows sub-pages of official tool reference/docs pages (also other vendor subdomains with "mcp" in the path, HTML and Markdown links), up to 60, before the catalogues; `MAX_PAGES` 40 → 100; endpoint-origin crawling capped at 10 links |
| Official tool list on another subdomain not downloaded (airtable: support article → airtable.com/developers/agents/mcp/tools)                                                           | see above                                                                                                                                               | see above                                                                                                                                                                                                                                                                                                                      |
| Tool names broken across lines in `pageN.txt` (pendo: `getOrchestrateJourney` / `StepVisitors`)                                                                                         | `to_text` replaced every tag, also `<wbr>`/`<span>`/`<code>` inside a name, by a line break                                                             | `sources.py`: inline tags removed without a line break; `prompt_v8`: extract names from `.html` if a table looks broken                                                                                                                                                                                                        |
| Wrong official page / mirror (mintlify: docs-search MCP page instead of the Admin MCP page; the Admin page only on a mirror)                                                            | collector did not check the endpoint host; mirrors accepted                                                                                             | `links_v3` and `prompt_v8`: identity rules (search the endpoint host, docs-search MCP trap, mirrors are not official)                                                                                                                                                                                                          |
| Stated totals not checked (vercel 217, pendo ~100)                                                                                                                                      | -                                                                                                                                                       | `prompt_v8`: stated totals and per-category counts are a checklist                                                                                                                                                                                                                                                             |

---
### Test results links_v3 + v8
Run: 14 servers, GPT-6 Luna, effort high. Each action list was compared with the vendor's official tool list (where one exists).

| Server | Verdict | Details |
| --- | --- | --- |
| airtable | **Fixed** | All 40 official tools, labelled Official; 7 more from Agent Discoverability, labelled third-party. |
| amplitude | **Fixed** | All 45 official tools + the 3 progressive-discovery tools (48). |
| clerk | **Fixed** | All 21 official tools incl. the previously missing `list_application_feedback`. |
| microsoft-learn, vybe-solana | **Fixed** | Same lists as before, now labelled Official. |
| mixpanel | **Fixed** | All 64 official tools; 2 more from the Claude connector directory, labelled third-party. |
| kindora-funder-discovery | **Fixed** | All 14 official tools labelled Official; 2 from the Claude directory. |
| jam | **Fixed** | All 30 official tools; 5 more names from Jam's official plugin repository (enabled: Unknown) and 1 from the Claude directory. |
| mintlify | **Fixed** | All 38 official Admin-MCP tools (was 21 outdated names); 4 catalogue-only tools labelled third-party. |
| lilt, metaview | **Fixed** | No official list exists; proxy prefixes `liltmcp_`/`metaviewmcp_` removed; all labelled third-party. |
| vercel | **Mostly fixed** | All 248 official tools (217 + 31) from the 27 category pages (spot check of two categories: 33/33). **Error:** 18 MartechDB names added, among them `buy_credits`, `buy_pro`, `buy_addon`, `create_api_keys`, `exchange_sso_token`, although Vercel states that MCP does not purchase credits/subscriptions/add-ons and does not create API keys or exchange SSO tokens. |
| pendo | **Partial** | 89 of 98 official tools; 9 missing (e.g. `acquisitionTrend`, `cohortRetentionCurve`, `listAllApplications`). Cause: names split as `<code>acquisition</code><br><code>Trend</code>`; `<br>` still produced a line break in `pageN.txt`. |
| hubspot | **Not fixed** | All 32 official names present, but all labelled third-party (HookMCP): the model did not see the official list. Cause: the docs page renders its tool list with JavaScript (compiled MDX inside `<script>`), and `to_text` drops scripts, so `page8.txt` contained no tool names. |

---
### Changes for links_v3 + v9

| Problem (servers)                                                               | Change                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tool list inside JavaScript not visible in `pageN.txt` (hubspot)                | `sources.py`: new `script_text()` extracts text literals from the page's scripts and saves them as `pageN.script.txt` (noted in `INDEX.txt`); tested on the HubSpot page: 32/32 names with descriptions. `prompt_v9`: check `pageN.script.txt` / `pageN.html` before concluding that no official list exists |
| Names split by `<br>` between code spans (pendo)                                | `sources.py`: `</code><br><code>` is joined before converting to text; tested on the Pendo page: 98/98 names intact                                                                                                                                                                                          |
| Catalogue tools added although the vendor says MCP does not offer them (vercel) | `prompt_v9`: officially excluded operations are never added to `actions`; they go to `contradictions` (and `human_can_agent_cannot`) with the vendor's quote                                                                                                                                                 |
| -                                                                               | `config.py`: `PROMPT_FILE = prompt_v9.md`, `SERVERS = hubspot, pendo, vercel`, `EXCEL_DATA_DIRS = [prompt_v7, prompt_v8, prompt_v9]`                                                                                                                                                                         |

---
### Test results links_v3 + v9
Run: 3 servers, GPT-6 Luna, effort high.

| Server | Verdict | Details |
| --- | --- | --- |
| hubspot | **Fixed** | All 32 official tools, labelled Official with the official docs URL. `page8.script.txt` (19,247 chars, all 32 names with descriptions) was created; the model's comment still says the page copy "does not expose" the list and credits HookMCP, i.e. it did not open the new file - the data is right, the comment is not. |
| vercel | **Fixed** | 248 official tools (matches the stated 217 + 31) + 2 catalogue-only names (`status`, `get_deployment_events`). The officially excluded `buy_credits`, `buy_pro`, `buy_addon`, `create_api_keys`, `exchange_sso_token` are no longer in `actions`. Minor: they are not recorded in `contradictions` as the prompt asks. |
| pendo | **Fixed after repair** | 97 of 98 official tools (`productEngagementScore` missing) + the deprecated alias `listCountables`. The answer was valid JSON followed by one extra `}`, so it was saved as `pendo.error.txt`. Fix in `analyse_servers.py`: `extract_json` now ignores trailing characters after a complete JSON object ("Extra data"); the next run repairs the saved answer without a new Codex call. |

---
### Full run links_v3 + v9 and manual corrections (2026-10-27)
Full run of all 186 remaining servers with `prompt_v9` (GPT-6 Luna, effort high), then a re-run of 10 servers (strava, datadog, demandbase, metaview, cloudflare, netlify, firecrawl, postman, magic-patterns, scite). Compared with v7: 7,174 → 7,888 actions, 5,956 → 6,845 confirmed by an official source, servers with 0 actions 10 → 6.

**Re-run of 10 servers:** fixed strava (8 Claude-directory tools), metaview (16 + 39 via Scalekit, prefix removed), magic-patterns and scite (Claude directory no longer labelled Official), firecrawl and postman (tokens counted from code again). Demandbase was correct already: the official docs publish only labels; 6 of the machine names in v7 were not found in any source. Not fixed by re-running: datadog (only the default toolset), cloudflare and netlify (tokens).

**Manual corrections** (recorded in each JSON as `_manual_corrections` and as a `[MANUAL CORRECTION]` prefix in `notes`, with sources):

| Server | Correction | Reason |
| --- | --- | --- |
| canva | 33 → 46 official tools | The official tool reference (46) is written for api.canva.com/connect/v1/mcp; mcp.canva.com/mcp is the entry of the same server for public/CIMD clients (same OAuth scopes). v9 had treated it as a different server. |
| factset | 0 → 23 tools, labelled `[ENDPOINT /content/v1]`, third-party | The host answers 401 on every path, so /mcp has no own evidence; the product is documented only at /content/v1. Prompt rule for that case applied. |
| chargebee | 24 → 35 names (45 stated) | 11 more names found in the page data of the Claude directory listing; v7's 114 belong to the per-site Data Lookup servers. |
| make | repository restored | integromat/make-mcp-server is Make's official legacy local server (npm @makehq/mcp-server, documented by Make); the collector had marked it unofficial because of the former company name. |
| craft | code public: Partially | Separate local npm package @craft-io/mcp-server (MIT); repository stays NOT FOUND (404). |
| datadog | 23 → 68 tools | 45 tools of non-default toolsets from the official tool reference (as read in v7), enabled_by_default = No. Not re-verified live (web access unavailable on 2026-10-27). |
| cloudflare | tokens ≈1,000–1,100 `[VENDOR ESTIMATE]` | Descriptions are generated at runtime; exact count from code impossible. |

Excel rebuilt from `data/prompt_v9/` (186 servers, 8,051 actions). The 4 manual-analysis servers that at that point existed only in v7 (context7, gocardless, launchdarkly, tavily) were then also run with links_v3 + v9; the final workbook contains all 190 servers (8,102 actions, 2,850 capabilities, 1,148 observations, 7 manual corrections).

**Open points for the next prompt version:** (1) one server reachable under several URLs (canva) - compare OAuth scopes before treating URLs as different servers; (2) vendor renamed (Make/Integromat) - a repository is official if the vendor's docs or its npm package point to it; (3) definition of "Non-standard" structure (34 servers changed in v9).

