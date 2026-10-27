# MCP server: Braze

> **In plain words.** Braze is a platform for marketing communication with customers: mailings (e-mail, push, SMS), campaigns, multi-step journeys (Canvas), audience segments, product catalogues, analytics. Its MCP server lets an AI assistant view the analytics of campaigns and segments and also **create and change** campaigns, e-mail templates, content blocks and catalogues, including **launching and stopping campaigns**. The server does not return data of individual users (personal data).
>
> **Analysis date:** 13.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Abbreviations in links:**
- `[overview]` = [Braze MCP server (user guide)](https://www.braze.com/docs/user_guide/brazeai/mcp_server) (link from the CSV); `[dev]` = [Developer guide: MCP server](https://www.braze.com/docs/developer_guide/mcp_server/).
- `[setup]` = [Setup](https://www.braze.com/docs/user_guide/brazeai/mcp_server/setup/); `[usage]` = [Usage](https://www.braze.com/docs/user_guide/brazeai/mcp_server/usage/).
- `[functions]` = [Available API functions](https://braze.com/docs/developer_guide/mcp_server/available_api_functions/) (the same page in the user guide: [link](https://www.braze.com/docs/user_guide/brazeai/mcp_server/available_api_functions/)).
- `[prm]` = https://mcp.braze.com/.well-known/oauth-protected-resource.
- `[pypi]` = [PyPI: braze-mcp-server](https://pypi.org/project/braze-mcp-server/) (deprecated local server).

---

## ⚠️ Important limitation of the analysis

- **The code of the remote server is closed.** There used to be a **local** server (package `braze-mcp-server` on PyPI, version 1.2.0 of 14.05.2026, MIT license, Python ≥ 3.12). It has been **declared deprecated** ("deprecated and doesn't receive additional updates") and has **fewer** tools than the remote one [overview], [setup], [pypi]. No public repository with the code could be found.
- **The tool list is taken from the official documentation** [functions]: names and short descriptions. These are descriptions *from the documentation*; whether they match `tools/list` verbatim cannot be checked without signing in.

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Braze MCP server | [overview] |
| Code link | Remote — closed. Deprecated local one: PyPI package only | [pypi] |
| Documentation | [overview] (from the CSV), [dev], [setup], [usage], [functions] | — |
| Endpoints | US: `https://mcp.braze.com/mcp`; EU: `https://mcp.braze.eu/mcp`. Either one works with any Braze cluster | [overview] |
| MCP version | Not published | — |
| Commit / date | Not applicable (closed). Documentation snapshot: 13.10.2026 | — |
| Language / MCP SDK | Remote — not published. Local (deprecated) — Python | [pypi] |
| Transport | Remote HTTP (Streamable HTTP) | [overview] |
| Code open? License | Remote — no. Local package — MIT | [pypi] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | No price given. The server is available to Braze customers | [overview] |
| Linked software | Braze is a proprietary enterprise platform; no public prices (by contract) | — |
| Access restrictions | (1) The permission **"Use MCP Server" is off by default** and is granted explicitly, per workspace. (2) The **company administrator** must enable MCP OAuth and approve the client's redirect URI. (3) Only AI clients from Braze's **allowlist** work (verified: Claude, ChatGPT, Cursor, OpenAI Codex, Claude Code, VS Code). (4) The agent's rights = the user's rights in the dashboard; changes to rights take effect from the next request. (5) Does not work for customers with **IP Allowlisting**. (6) Tools marked with an asterisk require participation in the **campaigns API beta program** | [setup], [overview], [functions] |
| Controlled by | The company administrator in Braze (enabling OAuth, rights, mass token revocation); Braze (client allowlist, beta program) | [setup] |
| Rate limits | Not documented | [usage] |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **71** tools in 16 groups: 37 reading, 34 writing (create, change, delete, launch and stop). Tools that reveal data of individual users (PII) are excluded: "Tools that expose user-level PII are not available" | Descriptions from the documentation — in section E. Example (`get_workspaces`): "Discover which Braze workspaces the current OAuth access token can reach." + an instruction to call it first, because the workspace ID (`app_group_id`) is needed by all other tools [functions]. The exact `tools/list` is not published | Not documented in detail. Restrictions in the descriptions: catalogues ≤ 50 items per request, events — 50/250 at a time, CDI — 10 per call; send analytics is kept for 14 days [functions] |
| **Resources** | ✅ (by scope) | The OAuth metadata contains the scope `mcp:resources` [prm]. Which resources — not documented | — | — |
| Prompts | ❓ | Not documented | — | — |
| **Tasks (background tasks)** | ✅ (own implementation) | Group **Operator** (beta): `send_operator_prompt` sends a prompt to the AI agent BrazeAI Operator and returns a `job_id`; `get_operator_result` polls for the result; `cancel_operator_job` cancels. This is an asynchronous task, but **implemented with tools**, not with the MCP Tasks mechanism. Separate scope `mcp:operator` [prm] | [functions] | `job_id`, then the result |
| Cancellation | ✅ (Operator only) | `cancel_operator_job` | [functions] | — |
| Logging / Sampling / Roots / Elicitation / Subscription / Progress | ❓ | Not documented | — | — |
| **Authorization** | ✅ | OAuth with sign-in via the Braze account (including SSO), without API keys. **Metadata Doc** — yes ([prm]); scopes: `mcp:tools`, `mcp:resources`, `mcp:operator`; token only in the header. **Authorization server** — `https://dashboard.braze.com`. **Preregistration**: the administrator must **approve the client's redirect URI** ("Registration alone doesn't approve it"), plus an allowlist of client domains. Whether there is Dynamic Client Registration could not be checked (the authorization server metadata is closed to automated access). Consent: a screen confirming access and a mandatory tick for the Braze Privacy Policy. Short-lived tokens with automatic refresh; **the administrator can revoke all MCP tokens of the company at once** | [setup], [prm] | — |
| Configuration | ✅ partial | The workspace is chosen **in every request** (not in a config); the company is chosen at the first authorization | [setup], [usage] | — |
| Error Reporting | ❓ | Not documented; beta tools without beta access "may return an error" [functions] | — | — |
| Other: log | ✅ partial | Campaign edits via MCP appear in the **campaign change history** under the signed-in user's name [overview] | — | — |

## D. Server logic beyond simply passing commands through

1. **Exclusion of PII by design:** tools with data of individual users are not implemented; only aggregated data and configuration are available [overview].
2. **Inheritance of dashboard rights** with a check on every request; deactivated users lose access immediately [overview], [setup].
3. **Multi-level access:** a separate permission "Use MCP Server" (off by default) + OAuth enabled by the administrator + approval of the redirect URI + client allowlist [setup].
4. **Batch limits** in the catalogue tools (≤ 50 items) and pagination [functions].
5. **Attribution and log:** campaign edits are recorded under the user's name [overview].
6. **An agent inside an agent:** via `send_operator_prompt` the external AI hands a task over to **Braze's internal AI agent** (BrazeAI Operator) in the background [functions]. What exactly Operator can do and with which restrictions is not described in the MCP documentation.
7. **Beta gating:** 15 campaign-changing tools and 3 segment tools only work for participants of the beta program [functions].
8. There is **no** server-side confirmation of actions: "Braze receives and executes the tool call as the AI model sends it" and cannot check whether the call matches the user's intent [functions], [usage].

**Server structure:** standard, but with a **nested agent** (Operator). Two regional endpoints.

## E. Overall evaluation

**Number of actions:** **71** (according to [functions]); 37 reading, 34 changing. ⭑ — requires the campaigns API beta program.

| Group | Tools (type) |
|---|---|
| Workspaces (1) | `get_workspaces` (R) |
| Campaigns (19) | `get_campaign_list`, `get_campaign_details`, `get_campaign_dataseries` (R); `duplicate_campaign` (C); `create_campaign`⭑ (C); `edit_campaign`⭑, `launch_campaign`⭑, `stop_campaign`⭑, `archive_campaign`⭑, `unarchive_campaign`⭑ (U); `get_campaign_draft`⭑, `get_campaign_live_details`⭑ (R); `create_campaign_message`⭑ (C), `update_campaign_message`⭑ (U), `delete_campaign_message`⭑ (D); `create_campaign_message_variation`⭑ (C), `update_campaign_message_variation`⭑ (U), `delete_campaign_message_variation`⭑ (D); `update_campaign_distribution`⭑ (U) |
| Canvases (4) | `get_canvas_list`, `get_canvas_details`, `get_canvas_data_series`, `get_canvas_data_summary` (all R) |
| Catalogs (13) | `get_catalogs`, `get_catalog_items`, `get_catalog_item` (R); `create_catalog`, `create_catalog_fields`, `create_catalog_items`, `create_catalog_selection` (C); `edit_catalog_items`, `replace_catalog_items` (U); `delete_catalog`, `delete_catalog_field`, `delete_catalog_items`, `delete_catalog_selection` (D) |
| Custom attributes (1) | `get_custom_attributes` (R) |
| Custom events (3) | `get_events`, `get_events_list`, `get_events_data_series` (R) |
| CDI integrations (3) | `list_integrations`, `get_integration_job_sync_status` (R); `trigger_integration_sync` (W) |
| KPI (4) | `get_dau_data_series`, `get_mau_data_series`, `get_new_users_data_series`, `get_uninstalls_data_series` (R) |
| Media library (1) | `create_media_library_asset` (C) — by URL or base64, exactly one of the two |
| Purchases (3) | `get_product_list`, `get_quantity_series`, `get_revenue_series` (R) |
| Segments (6) | `get_segment_list`, `get_segment_details`, `get_segment_data_series` (R); `get_segment_filters`⭑ (R); `create_segment`⭑ (C); `edit_segment`⭑ (U) |
| Sends (1) | `get_send_data_series` (R) |
| Sessions (1) | `get_session_data_series` (R) |
| Templates (4) | `get_email_templates`, `get_email_template_info` (R, without drag-and-drop templates); `create_email_template` (C); `update_email_template` (U) |
| Content blocks (4) | `get_content_blocks`, `get_content_block_info` (R); `create_content_block` (C); `update_content_block` (U) |
| Operator, beta (3) | `send_operator_prompt` (U), `get_operator_result` (R), `cancel_operator_job` (U) |

R — read, C — create, U — update, D — delete, W — write (as in the documentation).

**Parameters:** full schemas are not published. Known: almost all tools need `app_group_id` (from `get_workspaces`); `get_campaign_details` — `campaign_id`; `get_segment_details` — `segment_id`; `get_send_data_series` — `send_id`; Operator — `job_id` [functions].

**Tokens before the first action:** cannot be determined (exact descriptions and schemas not published). With 71 tools, the volume is probably considerable.

**What the agent CANNOT do but a human can:**
- **User data (PII)**: profiles, user export, user deletion [overview].
- **Canvas — read only**: journeys cannot be created or changed [overview].
- Send messages directly (Messaging API) — no tools; launching only via a campaign [functions].
- Drag-and-drop templates [functions], [usage].
- Delete templates and content blocks (only create/change) [functions].
- Administration: users, rights, API keys, company settings.
- Without the beta program: creating and editing campaigns and segments.

## F. Documentation analysis

**Recommendations to the user that the server does not check** [usage], [functions]:
- **Do not use auto-mode** in the AI client; "review any AI-proposed action before implementing it".
- Check AI summaries against the data in the Braze dashboard ("Compare high-impact recommendations against source data").
- **Name the workspace explicitly in every request**, especially so as not to mix up production and staging. Otherwise the agent may ask or "choose an unexpected workspace".
- Specify dates and metrics; ask the agent which tools it used.

**Promises on governance and data:**
- "non-PII Braze data" / "Tools that expose user-level PII are not available" [overview].
- "An agent can never exceed your own access" [usage].
- Campaign edits are visible in the change history [overview].
- Braze **does not see the original prompt** ("Braze does not see your original natural-language prompt") [usage].
- **Disclaimer:** Braze is "not liable for instructions generated by, or responses conveyed through, third-party MCP clients"; it does not control how the AI retells the data [functions], [usage].
- Privacy policy: for customer data Braze is a processor; "We maintain human oversight and do not make decisions based solely on automated processing" (about Braze's own AI processes) [privacy](https://www.braze.com/company/legal/privacy).
- A log of MCP activity as a whole is not described [usage].

**Promises to the user:** "a secure remote connection that lets AI tools like Claude and Cursor access non-PII Braze data" [dev]; one connector works with all accessible workspaces [usage].

**Comparison with the server logic:** "non-PII" is consistent with the tool list: it has no user export, only aggregates and configuration. However, **catalogues, media and content blocks can contain any data** the customer has uploaded there; the documentation does not discuss this.

---

## Observations for the research

- **The most "writing" server among the cloud ones:** 34 changing tools, including **launching and stopping campaigns** — real mailings to customers. At the same time there is no server-side confirmation, only the recommendation not to enable auto-mode.
- **Strong administrative access control** (permission off by default, redirect URI approval, client allowlist, mass token revocation) combined with **weak control of individual actions**.
- **A nested vendor agent** (BrazeAI Operator): the external agent delegates a task to Braze's internal AI. A new design option not covered by the task items.
- **Beta gating of tools:** the set of capabilities depends on participation in the beta program.
- **Explicit shift of responsibility** to the user and the AI client (legal disclaimer right on the tools page).
- **Exclusion of PII as a design principle** — comparable to GoCardless's masking, but implemented at the level of the tool set.
