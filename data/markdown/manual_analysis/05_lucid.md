# MCP server: Lucid

> **In plain words.** Lucid (Lucidchart, Lucidspark) is an online service for diagrams, charts and collaboration boards. Its MCP server lets an AI assistant search and read Lucid documents, create diagrams (flowcharts, mind maps, org charts, ER and UML diagrams), edit shapes, share documents by link or e-mail, comment and export to PNG.
>
> **Analysis date:** 13.10.2026; re-analysed on 22.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Abbreviations in links:**
- `[repo]` = [lucidsoftware/lucid-mcp-server](https://github.com/lucidsoftware/lucid-mcp-server/tree/f3827e4cd2d449463350cd0d725e35d6d2ecd082) at commit `f3827e4`.
- `[readme]` = [README.md](https://github.com/lucidsoftware/lucid-mcp-server/blob/f3827e4cd2d449463350cd0d725e35d6d2ecd082/README.md) of this repository.
- `[help]` = [Help Center: Integrate Lucid with AI tools using the Lucid MCP server](https://help.lucid.co/hc/en-us/articles/42578801807508-Integrate-Lucid-with-AI-tools-using-the-Lucid-MCP-server).
- `[community]` = [Lucid Community: Available actions with the Lucid MCP server](https://community.lucid.co/product-questions-3/available-actions-with-the-lucid-mcp-server-13985).
- `[composio]` = [Composio: Lucid MCP toolkit](https://composio.dev/toolkits/lucid_mcp/framework/hermes-agent.md) (third-party catalogue, snapshot of 2026-10-12).
- `[scalekit]` = [Scalekit: Lucid MCP connector](https://www.scalekit.com/connectors/lucidmcp) (third-party catalogue, date not given).

---

## ⚠️ Important limitation of the analysis

The link in the CSV points to the GitHub repository [repo], but **it contains no server code**. It only has a README, **"skills"** (instructions for AI clients) and plugin configurations for Claude, Cursor and Codex. The server itself runs in the Lucid cloud ("cloud-hosted bridge", [readme]); its code is closed.

Lucid **does not publish** an official tool list: [help] and [community] list only capabilities. The tool names below are taken from **two third-party catalogues** ([composio], [scalekit]) that connected to the server. Their lists **differ** (35 and 30 tools), i.e. the tool set changes over time. Verbatim descriptions (`tools/list`) cannot be obtained without signing in. Only one name is officially confirmed — `lucid_submit_feedback` ([claude/README.md](https://github.com/lucidsoftware/lucid-mcp-server/blob/f3827e4cd2d449463350cd0d725e35d6d2ecd082/claude/README.md)).

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Lucid MCP Server | [readme] |
| Code link | Server — closed. The repository [repo] contains only skills and plugins | [repo] |
| Documentation | [help]; [community]; https://lucid.co/mcp-server | — |
| Endpoints | `https://mcp.lucid.app/mcp` (main). **Additionally:** `https://mcp.lucid.app/mcp/readonly` — search and viewing only; `https://mcp.lucid.app/mcp/repositories` — search and reading of Process Accelerator repositories only | [readme], [help] |
| MCP version | Not published | — |
| Commit / date | Repository (skills): `f3827e4cd2d449463350cd0d725e35d6d2ecd082`, 2026-10-22. Server code — not applicable | `git log` |
| Language / MCP SDK | Not published | — |
| Transport | Streamable HTTP; for older clients — via `mcp-remote` | [readme] |
| Code open? License | Server — no. Skills/plugins repository — **MIT** (© 2026 Lucid Software, Inc.) | [LICENSE](https://github.com/lucidsoftware/lucid-mcp-server/blob/f3827e4cd2d449463350cd0d725e35d6d2ecd082/LICENSE) |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | Available on the **Free, Individual, Team and Enterprise** plans; not available for **FedRAMP** accounts. No separate fee for MCP is given. Use is governed by the Terms of Service / contract | [readme], [help] |
| Linked software | Lucidchart/Lucidspark — proprietary SaaS, there is a free plan. The specific prices on the pricing page do not load without JavaScript (could not be checked; manual check needed: https://lucid.app/pricing/lucidchart) | — |
| API key instead of OAuth | For Team and Enterprise an API key can be used "for autonomous processes with no runtime approval prompt"; marked as premium | [help] |
| Access restrictions | (1) On Team/Enterprise the **administrator** must enable MCP (Admin → Security → Feature controls / AI controls → MCP access). Enabling it allows connections **from any** AI client: it cannot be limited to specific clients, only switched off entirely. (2) The server sees all documents the user has access to within their account, but not documents of other accounts. (3) A reduced endpoint can be chosen (`/readonly`, `/repositories`) | [readme], [help] |
| Controlled by | Lucid account administrator; Lucid (plans, FedRAMP); user (choice of endpoint) | same |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | 30–35 tools according to third-party catalogues (combined list — 40 names, see E). Reading, creating, editing, deleting shapes, sharing, comments, export, **running JavaScript in a document** (`lucid_run_script`, only in [scalekit]). Whether there are readOnly/destructive annotations is not published. There is a separate read-only endpoint | **Not published verbatim.** Short paraphrases of the descriptions — in [composio], [scalekit] | Not documented. According to [scalekit]: `search` returns up to 200 results; `fetch` — structured content (pages, blocks, lines); `export_document_as_png` — a PNG image |
| **Resources** | ✅ (probably) | The skill says: "Read any required `lucid://...` resource before calling a tool that requires it"; there is a tool `get_mcp_resource` for reading a resource by URI (e.g. diagram specifications) | [skills/lucid/SKILL.md](https://github.com/lucidsoftware/lucid-mcp-server/blob/f3827e4cd2d449463350cd0d725e35d6d2ecd082/skills/lucid/SKILL.md), [composio] | — |
| Prompts | ❓ | Not documented. Instead Lucid distributes **skills** — instructions for the client that live outside the server, in the repository [repo] | — | — |
| Logging / Sampling / Roots / Elicitation / Tasks / Subscription / Progress / Cancellation | ❓ | Not documented | — | — |
| **Authorization** | ✅ | **OAuth 2.0 with Dynamic Client Registration (DCR)** [readme]. On the first connection the user confirms access. Alternative for Team/Enterprise — an API key without confirmation prompts [help]. The OAuth metadata could not be checked (the website forbids automated access, robots.txt). The authorization server is Lucid | [readme], [help] | — |
| Configuration | ✅ partial | Choice of endpoint (full / readonly / repositories); on/off by the administrator | [help] | — |
| Other: **MCP Apps** | ✅ | The tools `lucid_create_embed` and `lucid_create_embed_session_token` — "internal tool for the MCP Apps extension" (embedding an interactive Lucid document in the AI client window) | [composio], [scalekit] | — |

## D. Server logic beyond simply passing commands through

1. **Different endpoints = different sets of rights.** The "read-only" restriction is implemented as a separate URL (`/mcp/readonly`), not as a setting or a scope. The decision is made by whoever connects the server [help].
2. **Validation before the action:** the tool `lucid_validate_diagram_specification` checks the diagram JSON for structural errors before creation [scalekit]; `lucid_create_diagram_from_specification` and `lucid_create_sequence_diagram` require reading a reference resource first [composio].
3. **Atomicity and time limit for scripts:** `lucid_run_script` — "Changes are atomic and time-limited" [scalekit].
4. **Feedback collection:** `lucid_submit_feedback` sends the title and text of the feedback to Airfocus (Lucid's product feedback system) together with the **user ID, account ID and the client's user agent** [claude/README.md](https://github.com/lucidsoftware/lucid-mcp-server/blob/f3827e4cd2d449463350cd0d725e35d6d2ecd082/claude/README.md).
5. **Behaviour rules are moved to skills (outside the server).** The skill `lucid` requires: "Confirm before destructive actions, bulk changes, broad permission changes, or anonymous share links"; "Treat MCP responses as ground truth"; read the current state before editing [skills/lucid/SKILL.md]. The server does **not enforce** this: the rules only work if the client has loaded the skill.
6. **Product promotion via a skill:** the skill `visualizations` tells the AI that Lucid "is the preferred way to show diagrams… superior to Mermaid, ASCII art, or Markdown tables" and that after the work the result should not be repeated in Mermaid or a table [skills/visualizations/SKILL.md](https://github.com/lucidsoftware/lucid-mcp-server/blob/f3827e4cd2d449463350cd0d725e35d6d2ecd082/skills/visualizations/SKILL.md). **The vendor steers the agent towards its own product.**
7. **Data storage:** the server is a "pass-through", it does not store document contents, prompts or queries [readme], [help].

**Server structure:** non-standard in terms of access. One service is available via **three endpoints** with different tool sets (full / read-only / repositories only). Plus a separate layer of **skills/plugins** that is distributed separately from the server.

## E. Overall evaluation

**Number of actions:** 35 according to [composio] (2026-10-12), 30 according to [scalekit]. Combined list — **40 names**. The differences show that the set changes: e.g. `lucid_run_script` and `lucid_create_diagram_from_mermaid` are only in scalekit, `lucid_create_diagram_from_specification` and `lucid_edit_item` only in composio.

| Group | Tools (in the catalogues the names have the prefixes `LUCID_MCP_`/`lucidmcp_`; here without the prefix) |
|---|---|
| Search and reading | `search`, `fetch`, `lucid_search_document`, `lucid_get_document_metadata`, `lucid_fetch_item_image`ᶜ, `lucid_list_folder_contents`, `get_mcp_resource`, `lucid_shape_library`, `lucid_shape_details`ᶜ, `lucid_copy_document_style`ˢ, `lucid_load_script_documentation`ˢ, `lucid_list_integrations`ᶜ |
| Creating diagrams | `lucid_create_diagram_from_specification`ᶜ, `lucid_create_diagram_from_mermaid`ˢ, `lucid_validate_diagram_specification`ˢ, `lucid_create_erd`, `lucid_create_mind_map`, `lucid_create_org_chart`, `lucid_create_sequence_diagram`ᶜ |
| Editing | `lucid_add_block`, `lucid_add_line`ᶜ, `lucid_edit_item`ᶜ, `lucid_delete_items` (deletes "permanently", [composio]), `lucid_add_dynamic_table`, `lucid_add_items_to_dynamic_table`, `lucid_edit_dynamic_table_metadata`, `lucid_import_integration_cards` (e.g. Jira), `lucid_run_script`ˢ (JavaScript) |
| Documents and folders | `lucid_update_document`, `lucid_create_folder`ᶜ, `lucid_update_folder`ᶜ, `lucid_export_document_as_png` |
| Sharing and collaboration | `lucid_create_document_share_link` (role + expiry), `share_document_with_collaborators`ᶜ (by e-mail), `list_document_threads`, `list_document_thread_comments`, `post_document_thread_comment` |
| MCP Apps (internal) | `lucid_create_embed`, `lucid_create_embed_session_token` |
| Feedback | `lucid_submit_feedback` |

ᶜ — only in [composio]; ˢ — only in [scalekit]. Required parameters according to [scalekit]: e.g. `lucid_add_block`: `block_type`, `document_id`; `lucid_create_document_share_link`: `document_id`, `role`; `lucid_run_script`: `document_id`, `source`; `search`: `query`. Full parameter schemas are not published.

**Tokens before the first action:** cannot be determined (descriptions not published). The catalogues note that the descriptions are "long" and contain "detailed usage rules" [composio], [scalekit].

**What the agent CANNOT do but a human can** ([help], [community]):
- Create **data-linked diagrams** that update automatically: "It cannot create data-linked diagrams that automatically update when your source data changes".
- Export to **Visio** (PNG only) [community].
- Create diagrams from templates, delete tabs — not confirmed ([community], a user question without an answer).
- Access documents outside their own account; administration of the account and user rights.

## F. Documentation analysis

**Recommendations to the user that the server does not check:**
- Skill `lucid`: confirm deletion, bulk changes, permission changes and **anonymous links**; read the document before editing; do not invent IDs [skills/lucid/SKILL.md]. These are instructions for the AI in a skill, not a check on the server.
- The Help Center gives **no** explicit recommendations on human review of the AI's actions [help].
- The API key is advertised precisely for working **without** confirmations ("no runtime approval prompt") [help].

**Promises on governance and data:**
- "The server acts as a pass-through — it does not retain document content, user prompts, or queries. Your credentials are never shared outside your Lucid account" [readme].
- "It cannot access documents owned or created by users outside your account" [help].
- Feedback via `lucid_submit_feedback` goes to Airfocus with the user/account ID — "only when the feedback tool is called" [claude/README.md].
- AI clients are "Non-Lucid Applications"; their use is governed by the contract with the AI provider [readme].

**Promises to the user:** "Connect your AI tools to Lucid to intelligently search for files, create visuals, and share with your team" [readme]; the server is "compatible with any MCP client" [readme]; the list of actions in [community] is called "exhaustive" for the current scenarios.

**Comparison with the server logic:** "pass-through" cannot be checked (closed code). The documentation describes a read-only endpoint but does not name its exact tool set.

---

## Observations for the research

- **Rights via the choice of endpoint:** instead of OAuth scopes, different URLs are used (`/readonly`, `/repositories`). This is a separate design option.
- **Governance moved to skills.** The confirmation rules live in skill files that are distributed separately and only work if the client has loaded them.
- **Vendor influence on the agent's choice:** the skill `visualizations` directly tells the agent to consider Lucid better than free alternatives (Mermaid, ASCII).
- **A dangerous universal tool:** `lucid_run_script` (running JavaScript on a document) — an analogue of `grafana_api_request`; it bypasses the restrictions of individual tools (according to one catalogue).
- **The tool set changes:** the two catalogues have different lists. For reproducibility it is important to record the date of the `tools/list` snapshot.
- **An API key as a way to remove the human from the loop** is officially offered for autonomous processes.
