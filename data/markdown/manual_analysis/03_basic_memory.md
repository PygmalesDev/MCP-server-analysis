# MCP server: Basic Memory

> **In plain words.** Basic Memory is a "long-term memory" for AI. It is a database of notes in Markdown format (ordinary text files) that both a human and an AI assistant can read and write. This way the AI "remembers" past conversations. There is a free local version (files on the user's computer) and a paid cloud version (Basic Memory Cloud). The MCP server gives the AI "buttons": find, read, write, edit, move and delete notes, and manage projects (folders of notes).
>
> **Analysis date:** 12.10.2026; re-analysed on 23.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.
>
> **Verbatim descriptions of all tools, resources and prompts** (Pre-Interaction Context) are in a separate file: `03b_basic_memory_pre_interaction_context.md`.

**Abbreviations in links:**
- `[code]` = [basicmachines-co/basic-memory](https://github.com/basicmachines-co/basic-memory/tree/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587) at a pinned commit.
- `[srv:N]` = line N of [src/basic_memory/mcp/server.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/server.py).
- `[cfg:N]` = line N of [src/basic_memory/config_models.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/config_models.py).
- `[readme:N]` = line N of [README.md](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/README.md).
- `[tools-ref]` = [MCP Tools Reference](https://docs.basicmemory.com/reference/mcp-tools-reference).
- `[cloud-guide]` = [Cloud guide](https://docs.basicmemory.com/cloud/cloud-guide).

---

## ⚠️ Important limitation of the analysis

The CSV gives the **cloud** endpoint `https://cloud.basicmemory.com/mcp`. According to the developers, the cloud uses the same engine and the "same MCP tools" [readme:127–131]. However, the documentation lists cloud tools that are **not** in the open code: `review_note` (comments and suggested edits) and `open_basic_memory` (the Pocketbook interface), as well as cloud parameters (`review_mode`, `workspace`) [tools-ref]. So the cloud server contains closed parts. The code analysis below refers to the open server. Cloud specifics are marked **☁️**.

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Basic Memory (`basic-memory`), the server is called `"Basic Memory"` | [srv:277–281] |
| Code link | https://github.com/basicmachines-co/basic-memory | — |
| Documentation | https://docs.basicmemory.com/cloud/cloud-guide (from the CSV); tool reference: https://docs.basicmemory.com/reference/mcp-tools-reference | CSV |
| Endpoint (from CSV) | `https://cloud.basicmemory.com/mcp` | [cloud-guide] |
| MCP version | Python SDK `mcp` 2.3.0 supports `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25` (via the `initialize` handshake) and `2026-07-28` (new stateless format). Latest: `2026-07-28` | [python-sdk v2.3.0 version.py](https://github.com/modelcontextprotocol/python-sdk/blob/v2.3.0/src/mcp-types/mcp_types/version.py), [uv.lock](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/uv.lock) |
| Commit / date | `9b47a7cd4784ca3a4df5d85437bdbd2db2dee587`, 2026-10-23; package version **0.24.1** | `git log`, [__init__.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/__init__.py) |
| Language | Python ≥ 3.12 | [pyproject.toml](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/pyproject.toml) |
| MCP SDK | **FastMCP 4.1.3** (on top of the official `mcp` 2.3.0) | [pyproject.toml:18, 32](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/pyproject.toml#L18) |
| Code open? License | Yes, **AGPL-3.0** (the cloud part is partly closed, see above) | [LICENSE](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/LICENSE), [readme:162–175] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | Local — **free** ("Free to run locally"). ☁️ Cloud — requires an **active subscription** (without it the sign-in returns "Active subscription required") | [pricing](https://basicmemory.com/pricing), [cloud-guide] |
| Prices ☁️ | **Team: $15 per seat/month** ($13 from 10 seats, $12 from 20); **Business: $30 per seat/month** (SSO/SAML, audit logs, HIPAA, priority support); **Agent Infrastructure** — custom (credits, metered usage). 7-day trial. ⚠️ The README in the repository describes the old scheme: "$15.00/mo … One plan, no tiers", discount for OSS users with the code `BMFOSS` | [pricing](https://basicmemory.com/pricing), [readme:149–160] |
| Linked software | The program itself is open (AGPL-3.0). The cloud is built on WorkOS AuthKit (sign-in), Neon Postgres, Tigris S3 (storage), Polar.sh (payments) | [readme:147], [privacy](https://basicmemory.com/privacy) |
| Access restrictions | (1) ☁️ Subscription (controlled by Basic Machines). (2) **User settings** in `~/.basic-memory/config.json`: project deletion is **off by default** (`enable_project_delete=false`); POSIX tools can be hidden; overwriting notes is forbidden by default [cfg:591–618]. (3) ☁️ ZIP upload up to 100 MB; `.env` and similar files are not uploaded [cloud-guide] | |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | The code has **41** tool functions. Of these, 2 are not registered (`search_notes_ui`, `read_note_ui`: import commented out, "TODO: re-enable") [tools/__init__.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/tools/__init__.py), 2 are hidden by default (`delete_project`, `bm_project_delete`). **Visible by default: 37.** A transition to a "1.0" set `bm_*` is under way: the new tools are registered **next to the old ones** they will replace, so the AI sees almost every action twice (`bm_write`/`write_note`, `bm_read`/`read_note`, `bm_edit`/`edit_note` etc.). All tools have readOnly/destructive/idempotent/openWorld annotations | Verbatim: file `03b_…`. **Server instructions** (≈ 520 tokens) [srv:243–275] — see section D | By default **text** (Markdown), on request `output_format="json"` — structured JSON [readme:566–568]. After creating a note, `bm_write` adds a **"similar notes"** section (up to 3, similarity ≥ 0.70) — "advisory and does not block the write" [similar_notes.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/similar_notes.py). `bm_read` returns a `checksum` for a safe subsequent write. Empty list → block `"[]"` (middleware) [empty_results.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/empty_results.py) |
| **Resources** | ✅ | 5: `memory://ai_assistant_guide` (guide for the AI), `memory://man` (table of contents of the "manual"), `memory://man/{ref*}` (manual page for a tool), `memory://{project}/{path*}` (any note as a resource), `memory://{workspace}/{project}/info` (project statistics) | Verbatim in `03b_…`, section 3 | Markdown (`text/markdown`) |
| **Prompts** | ✅ | 4: `continue_conversation`, `getting_started`, `recent_activity`, `search_knowledge_base` | Verbatim in `03b_…`, section 4 | A hint text for the AI |
| Logging (MCP) | ✅ partial | Only in the project management tools: `context.info("Listing all available projects")`, `"Creating project: …"`, `"Deleting project: …"` — sent to the client as MCP log notifications [project_management.py:389, 616, 848](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/tools/project_management.py#L389) | — | — |
| Sampling | ❌ | Not found | — | — |
| Roots | ❌ | Not found | — | — |
| **Authorization** | ✅ ☁️ | **Local (stdio):** no authorization; access = access to the computer's files. **☁️ Cloud:** OAuth (browser sign-in, provider WorkOS AuthKit; the subscription is checked at sign-in). The local server can call the cloud with an API key or an OAuth token (the key takes precedence) [cloud-guide], [readme:147], [mcp/tools/utils.py:229](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/tools/utils.py#L229). Details (Dynamic Client Registration, metadata) are not documented | — | — |
| Elicitation | ❌ | Not found. Instead the instructions say: "offer … — then wait for them to agree before writing anything" (a request to the AI to ask the human) | [srv:243–275] | — |
| Tasks (MCP) | ❌ | Not found. ☁️ Deleting a project in the cloud runs asynchronously in the background, but not via MCP Tasks [cloud-guide] | — | — |
| **Configuration** | ✅ | `~/.basic-memory/config.json` and environment variables: `default_project`, `enable_posix_tools` (on), `enable_project_delete` (off), `write_note_overwrite_default` (off) etc. The visibility of tool groups is switched with FastMCP tags (`Visibility`) at startup [srv:36–52, 125–129], [cfg:196, 591–618] | — | — |
| **Error Reporting** | ✅ | A **"refusal"** system: `isError: true` and a code `NOT_FOUND`, `AMBIGUOUS`, `ALREADY_EXISTS`, `REVISION_CONFLICT`, `INVALID_ARGUMENTS`, `OUTSIDE_PROJECT`, `LOCKED`, `UNSUPPORTED`, `PARTIAL_FAILURE`, `OUTCOME_UNKNOWN`, `UNAVAILABLE` + a hint "Try instead: …" [refusals.py:1–80](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/refusals.py#L1-L80) | — | Text: `CODE: message\nTry instead: …` or JSON `{"error","message","try_instead"}` |
| Subscription | ❌ | Not found | — | — |
| Progress Tracking | ❌ | Not found | — | — |
| Cancellation | ❌ (explicit) | Not found | — | — |
| Other | ✅ | **Client dependency:** a middleware remembers the client name; the tools `search`/`fetch` (for ChatGPT) work **only for the OpenAI client**, all others get the error "Use search_notes instead" [client_info.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/client_info.py), [chatgpt_tools.py:28–38, 172–174](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/tools/chatgpt_tools.py#L28-L38) | — | — |

## D. Server logic beyond simply passing commands through

1. **Behaviour rules in the server instructions (not enforced by the code):** "check them (`recent_activity` is a good first look) before answering from memory", "offer to save something … — then wait for them to agree before writing anything. **Do not create notes unprompted.**" [srv:243–275]. Developers' comment: the "offer-not-act" approach was chosen deliberately so that the AI is not intrusive [srv:237–242]. The code does **not prevent** the AI from creating a note without asking. For example, `edit_note` with `append`/`prepend` creates the note if it does not exist (tool description in `03b_…`).
2. **Protection against accidental overwriting:** writing over an existing note is an `ALREADY_EXISTS` error unless `overwrite=true` is passed [cfg:591–599].
3. **Optimistic locking:** the parameter `expected_checksum` — change or delete only if the note has not changed since it was read; otherwise `REVISION_CONFLICT` (descriptions of `bm_write`, `bm_edit`, `bm_delete` in `03b_…`).
4. **Explicit confirmation of dangerous operations via parameters:** deleting a folder requires `recursive=true` (`bm_delete`); project deletion is hidden altogether until the user enables `enable_project_delete` ("so an assistant cannot remove a project unless you turn this on") [cfg:610–618].
5. **Project boundaries:** the path is checked; leaving the project folder (including via symlinks) is forbidden — refusal `OUTSIDE_PROJECT` [utils.py:971–988](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/utils.py#L971-L988), [note_targets.py:110–118](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/mcp/note_targets.py#L110-L118).
6. **Influence of the past on the future (agent memory):** this is the essence of the product. Everything the agent wrote earlier comes back to it in future sessions via `recent_activity`, `build_context`, search. The server actively pushes for reuse: after a note is created it shows **similar existing notes** to avoid duplicates [similar_notes.py:1–5].
7. **Self-documentation for the AI:** a built-in "manual" (`memory://man/<tool>(3)`) with verified examples; the instructions advise the AI to read it after an error [srv:243–275].
8. **Different behaviour for different clients:** `search`/`fetch` only for OpenAI (see C).
9. **Auto-update:** CLI installations check for and **silently** install updates once every 24 hours. This means the tool set and its descriptions can change without any action by the user. Disabled with `auto_update: false` [readme:601–614].
10. None of: permission checks (locally), human confirmation at the protocol level, confidence scores, rate limits.

**Server structure:** flat, one server. Special features: tool groups are switched on by tags; a transition period in which the old and new sets are visible at the same time; "local ↔ cloud" routing by project/workspace ([routing](https://docs.basicmemory.com/cloud/routing)).

## E. Overall evaluation

**Number of actions:** **37** tools are visible by default (39 registered, of which the 2 project deletion tools are hidden). If the "old/new" duplicates and the 2 OpenAI-only wrappers are removed, there are **about 15 actions that differ in meaning**: write, read, edit, move, delete a note/folder; search; list folders; find files; recent activity; building context from the link graph; projects (list/create/delete); workspaces; schemas (validate/infer/diff); diagnostics; displaying a note (`view_note`); POSIX navigation (`ls/cat/grep/find/tail/man`). Many tools contain several operations (e.g. `bm_edit`: `append/prepend/find_replace/replace_section/insert_before_section/insert_after_section/set_metadata`; `bm_project`: `list/create/recent`).

**List of actions and parameters:** the complete list with verbatim descriptions, types, whether required and default values is in the file `03b_basic_memory_pre_interaction_context.md`. Examples of parameters with categories:
- `bm_search.mode` — **5** variants (hybrid, text, semantic, title, permalink);
- `bm_edit.command` — **7** variants (see above);
- `output_format` in all tools — **2** (text, json).

**Tokens before the first action:** ≈ **11,400 tokens** (tools + resources + prompts ≈ 10,900, instructions ≈ 520). Estimate: length of the reconstructed description ÷ 4 characters per token, error ±30 %. About half of the volume is taken up by the duplicate "old" tools.

**What the agent CANNOT do but a human can** (compared with the CLI commands in [cli/commands/](https://github.com/basicmachines-co/basic-memory/tree/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/cli/commands) and [cloud-guide]):
- **Import** from ChatGPT, Claude (conversations, projects), documents, memory.json — CLI only (`import_*`).
- **☁️ Snapshots and restore**, push/pull synchronisation (bisync), ZIP upload, **sharing** (`shares`), subscription management, teams and workspaces (except viewing via `list_workspaces`).
- Database maintenance: reindexing, `prune`, `orphans`, `doctor`, `update`.
- Deleting a project — only if the user has enabled `enable_project_delete` themselves.
- ☁️ Web app: comments and suggested edits (partly available in the cloud MCP via `review_note`).

## F. Documentation analysis

**Recommendations to the user that the server does not check:**
- "Deletion is irreversible for active project storage" and "Back up any local files you need before running the destructive command" [cloud-guide].
- Agents should not write CriticMarkup directly (cloud reviews) [tools-ref].
- For a "clean" deletion of cloud data from a local session, `workspace` must be passed, otherwise the wrong data is deleted [tools-ref].
- The documentation does not describe a separate confirmation step before destructive actions [tools-ref].

**Promises on governance and data:**
- Open version: "Notes and content never leave your device" [privacy](https://basicmemory.com/privacy).
- ☁️ "We don't train AI models", "Your data is encrypted at rest and in transit", servers in the **USA**; after the subscription is cancelled, data is kept for 30 days, in backups up to 90 days; "We don't sell your data" [privacy](https://basicmemory.com/privacy).
- **CLI telemetry (on by default):** anonymous events of the "CLI → cloud" funnel (promo impressions, cloud sign-in attempts) are sent to Umami Cloud; file contents, note titles, IP and individual tool calls are not collected. Opt-out: `BASIC_MEMORY_NO_PROMOS=1` [readme:616–635], [cli/analytics.py](https://github.com/basicmachines-co/basic-memory/blob/9b47a7cd4784ca3a4df5d85437bdbd2db2dee587/src/basic_memory/cli/analytics.py). Logfire telemetry is off by default [cfg:204–211].
- Reversibility: "No lock-in … Export to local Markdown any time"; ☁️ snapshots and "Point-in-time restore" [readme:133–145]. There are no versions for local notes (apart from your own Git etc.).
- `basic_memory_diagnostics` — read-only, secrets and credentials in URLs are masked [tools-ref].

**Promises to the user:** "Your AI never forgets again" [readme:32]; "Every tool is annotated with MCP behavior hints … so agents can pick the right one without trial-and-error" [readme:553–556]; "Cancel anytime, your data stays yours" [readme:143–145, 157].

**Comparison with the server logic:** the promise about annotations is kept (all tools are annotated). The rule "do not create notes unprompted" exists **only as text** in the instructions; the code does not enforce it. The promise "Notes … never leave your device" (local) is consistent with the code when the cloud is disabled; the CLI telemetry does not send note contents (according to the code of `analytics.py` — events only).

---

## Observations for the research (as requested by David)

- **A "memory" server changes the agent's future behaviour by its very nature.** This is a direct example of the item "Does past agent behaviour change future outputs?". The server also pushes in this direction: "similar notes" hints, the advice to start with `recent_activity`.
- **Governance through texts, not through code:** "Do not create notes unprompted" is only in the instructions. At the same time, overwriting, folder deletion, project deletion and project boundaries are implemented in code. The result is a mixed model.
- **The transition period doubles the context:** about 37 visible tools for about 15 different actions, i.e. almost half of the tokens are spent on duplicates.
- **Behaviour depends on the client:** the tools for OpenAI silently work differently for other clients.
- **Open code ≠ cloud:** the cloud has additional closed tools (review, Pocketbook UI).
- **Auto-update without user involvement** can change the tool surface between sessions.
