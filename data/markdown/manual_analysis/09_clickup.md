# MCP server: ClickUp

> **In plain words.** ClickUp is a service for managing tasks and projects: tasks, lists, folders, documents, chats, time tracking. Its MCP server gives an AI assistant almost 50 "buttons": search and create tasks, change their status and assignees, comment, track time, write in chat and in documents.
>
> **Analysis date:** 14.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [Connect an AI assistant to ClickUp's MCP server](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) (link from the CSV).
- `[tools]` = [Supported Tools](https://developer.clickup.com/docs/mcp-tools).
- `[prm]` = https://mcp.clickup.com/.well-known/oauth-protected-resource; `[asm]` = https://mcp.clickup.com/.well-known/oauth-authorization-server.
- `[pricing]` = [clickup.com/pricing](https://clickup.com/pricing).

> ⚠️ **The server code is closed.** The tool list is taken from the official documentation [tools]. It gives "human-readable" names (e.g. "Create Task") and paraphrased descriptions. The exact names and descriptions in `tools/list` cannot be obtained without signing in.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | ClickUp MCP Server (`resource_name` in the OAuth metadata) | [prm] |
| Code / license | Closed, proprietary | — |
| Documentation | [docs], [tools]; for AI agents — `https://developer.clickup.com/llms.txt` | [docs] |
| Endpoint | `https://mcp.clickup.com/mcp`; data comes from `https://api.clickup.com` (`resource_server_origin`) | [docs], [prm] |
| MCP version / language / SDK | Not published | — |
| Commit / date | Not applicable; documentation snapshot 14.10.2026 | — |
| Transport | JSON-RPC 2.0 over HTTP (Streamable HTTP) | [docs] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | **On all plans**, no separate fee; MCP **does not consume AI credits** | [docs] |
| Linked software | Free Forever $0; Unlimited $7 (annual) / $10 (monthly) per user; Business $12/$19; Enterprise — on request. The same page has a second set of prices (Core $9, Business $17, Max $100) — the page is contradictory. Add-on **Everything AI: $28** per user per month | [pricing] |
| **Rate limits** | Without the Everything AI add-on — **calls per rolling 24 h**: Free 100, Core/Unlimited 300, Business 1,000, Business Plus 2,500, Enterprise 5,000, Enterprise Plus 25,000. The limit is counted **per workspace and per AI client separately** (300 for Claude + 300 for Cursor). `initialize` and `tools/list` are not counted. With the add-on — the public API limits. When exceeded — `RATE_LIMIT_EXCEEDED` with `retryAfter`; the limit cannot be reset | [docs] |
| Other restrictions | OAuth only (personal API keys are not accepted); rights = the user's rights in ClickUp; "AI fair use policy" | [docs], [tools] |
| Controlled by | ClickUp (plans, limits, fair use), workspace administrator (user rights) | same |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **48** tools (see E): search, tasks (including bulk), attachments, comments, tags, links and dependencies, moving, time tracking, hierarchy, members, **chat (sending messages)**, documents, time-in-status reports | Not published verbatim | Not documented; when the limit is reached — error `RATE_LIMIT_EXCEEDED` + `retryAfter` |
| Resources / Prompts | ❓ | Not documented | — | — |
| **Authorization** | ✅ | **OAuth 2.1 + PKCE**, OAuth only. **Metadata Doc** — yes ([prm], [asm]). **Dynamic Client Registration** — yes (`https://mcp.clickup.com/oauth/register`). Grant `authorization_code`; PKCE `S256`; `token_endpoint_auth_methods: none`; scopes `read`, `write`; support for resource indicators. **Authorization server** — `https://mcp.clickup.com` | [docs], [prm], [asm] | — |
| Error Reporting | ✅ partial | `RATE_LIMIT_EXCEEDED` with `retryAfter` | [docs] | — |
| Others (Logging, Sampling, Roots, Elicitation, Tasks, Subscription, Progress, Cancellation) | ❓ | Not documented | — | — |

## D. Server logic beyond passing commands through

1. **Daily limits per client and workspace** — a plan-dependent restriction of the volume of the agent's actions [docs].
2. **Restriction of deletion:** the main page says deletion is not offered "as a safety measure for now"; at the same time [tools] contains **"Delete task"**, and the assistant "may confirm" the task before deleting it. ⚠️ **Contradiction in the documentation.**
3. **Inheritance of the ClickUp user's rights** [tools].
4. Server-side confirmations and a log of the agent's actions are not described.
5. Connected Search (search across connected apps) is not available via MCP [docs].

**Structure:** standard.

## E. Overall evaluation

**Number of actions:** **48** (according to [tools]).

| Group | Actions |
|---|---|
| Search (3) | Search Workspace; Search tasks by task type; Search tasks by tag |
| Tasks (5) | Create Task; Get Task; Update Task; Set Custom Fields; **Delete task** |
| Bulk (2) | Create Bulk Tasks; Update Bulk Tasks |
| Attachments (1) | Attach File to Task |
| Comments (3) | Get Task Comments; Get Threaded Replies; Create Task Comment (with @mentions) |
| Tags (2) | Add Tag to Task; Remove Tag from Task |
| Links (4) | Add/Remove task link; Add/Remove dependency |
| Moving (2) | Move task to a new List; Add task to another List |
| Time tracking (6) | Get Task Time Entries; Get time entries for multiple tasks; Start Time Tracking; Stop Time Tracking; Add Time Entry; Get Current Time Entry |
| Hierarchy (8) | Get Workspace Hierarchy; Create List; Create List in Folder; Get List; Update List; Get Folder; Create Folder; Update Folder |
| Members (3) | Get Workspace Members; Find Member by Name; Resolve Assignees |
| Chat (2) | Get Chat Channels; **Send Chat Message** |
| Documents (5) | Create Document; List Document Pages; Get Document Pages; Create Document Page; Update Document Page |
| Reports (2) | Get Time in Status for a task / for tasks in a List |

**Parameters:** schemas not published; from the descriptions — name, description, assignees, due date, priority, status, custom fields.

**Tokens before the first action:** cannot be determined.

**What the agent CANNOT do but a human can:** delete lists, folders, spaces, documents, comments (only tasks can be deleted); manage members and rights; automations; goals, dashboards, whiteboards; Connected Search across external apps [docs], [tools].

## F. Documentation analysis

- **Recommendations not checked by the server:** there are no explicit recommendations on human confirmation (except "may confirm" for deleting a task) [tools].
- **Governance promises:** only links to the security, privacy and AI fair use policies; no specific promises about the data passed to the AI [docs].
- **Promises to the user:** "available on all plans"; the limits "may change", "future restrictions" are possible [docs].
- **Comparison with the logic:** the promise "no deletion" contradicts the tool "Delete task".

## Observations

- **A limit per AI client** (not only per user) is a separate design technique that limits the volume of the agent's work.
- **The contradiction "no deletion" / "Delete task"** shows that the documentation and the actual tool set diverge.
- **The agent can write to people on behalf of the user** (chat, comments with @mentions).
