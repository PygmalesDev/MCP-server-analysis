# MCP server: LaunchDarkly

> **In plain words.** LaunchDarkly is a "feature flag" service: switches with which developers turn functions on and off in a running application without a new release, gradually roll them out to some of the users, and run experiments. There is also management of AI configurations (AI Configs, now called AgentControl) and observability (logs, traces, errors, session recordings). The MCP server gives an AI assistant **170 "buttons"**: create and **toggle flags in production**, change targeting rules and segments, run experiments, configure alerts, delete flags etc.
>
> **Analysis date:** 16.10.2026; re-analysed on 21.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [LaunchDarkly: MCP server](https://launchdarkly.com/docs/home/getting-started/mcp) (link from the CSV); `[hosted]` = [Hosted MCP server](https://launchdarkly.com/docs/home/getting-started/mcp-hosted.md).
- `[inst]` = the install page [mcp.launchdarkly.com/mcp/launchdarkly/install](https://mcp.launchdarkly.com/mcp/launchdarkly/install) — "Available Tools (170)", a list of tools with annotations and descriptions.
- `[srv]` = the server page [mcp.launchdarkly.com/mcp/launchdarkly](https://mcp.launchdarkly.com/mcp/launchdarkly) — shows only 97 tools with annotations and no total number; probably an outdated version of the page.
- `[fm]` = [mcp.launchdarkly.com/mcp/fm/install](https://mcp.launchdarkly.com/mcp/fm/install) — a second server "LaunchDarkly FM", "Available Tools (111)".
- `[local]` = the local server [launchdarkly/mcp-server](https://github.com/launchdarkly/mcp-server/tree/e4a35c6f6ec2ec16bfa84cf8e6ea838249c239d5), commit `e4a35c6`, 2026-10-21, v0.7.1.
- `[pricing]` = [launchdarkly.com/pricing](https://launchdarkly.com/pricing/).

> ⚠️ **The code of the cloud server is closed**, but **the server itself publishes its tool list with annotations** on the pages [inst] and [srv]. This is the best source among the closed servers, although the descriptions there are shortened. The open [local] (MIT) is a **different**, generated server for the EU and Federal environments. The cloud server is "more feature complete".
>
> ⚠️ **The CSV endpoint is a separate, small server.** The CSV address `https://mcp.launchdarkly.com/mcp/v1` has its own install page [`/mcp/v1/install`](https://mcp.launchdarkly.com/mcp/v1/install): the server "launchdarkly v1", **18 tools** — only feature flags and approvals (see E, first table). It has its own OAuth metadata (scopes `reader`, `writer`). The documentation already describes a **different**, large server `/mcp/launchdarkly` (170 tools), which is analysed below as the main official variant.
>
> The analysis describes the state as of 21.10.2026.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | LaunchDarkly hosted MCP server | [hosted] |
| Code / license | Cloud — closed. Local (EU/Federal) — MIT | [local] |
| Endpoints | CSV: `https://mcp.launchdarkly.com/mcp/v1`; current according to [hosted]: `https://mcp.launchdarkly.com/mcp/launchdarkly`; install page `/mcp/launchdarkly/install`. Second server: `https://mcp.launchdarkly.com/mcp/fm` ("LaunchDarkly FM", 111 tools; purpose not described in the documentation, judging by the tool set — a subset for feature management, experiments and AI Configs). The URL parameters **`toolsets`** and **`writes`** narrow the visible tool set. The server pages are hosted via **Speakeasy** | [hosted], [inst], [fm] |
| MCP version / language / SDK | Cloud — not published. Local: TypeScript, SDK 1.27.1 | [local] package-lock |
| Availability | **Does not work** in federal environments and on the EU instance (the local server is for them) | [hosted] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | Prices not given | [hosted] |
| Linked software | **Developer $0** (unlimited seats, 1K client-side MAU, 5 service connections, 5K AI runs); **Foundation**: $10 per service connection/month, $8.33 per 1K MAU (the page also shows $10), $5 per additional 1K AI runs; **Enterprise** — on request | [pricing] |
| Restrictions | Rights = **the rights of the member who authorized the connection**; role changes take effect immediately; a removed member loses access. For writing the Writer/Developer role is recommended; for reading — Reader. Environment approval processes also apply to MCP ("may require approval"; for segments the response contains `requiresApproval: true`) | [hosted], [srv], [inst] |
| Controlled by | LaunchDarkly administrator (roles, approval processes), user (toolsets/writes in the URL) | [hosted] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **170** tools (see E). **Annotations** Read-only / Idempotent / Destructive for most of them | Short descriptions and annotations — [inst]; the full `tools/list` is not published | Not documented as a whole. Examples: `check-removal-readiness` returns the verdict `safe`/`caution`/`blocked` [srv]; segments — `requiresApproval: true` [inst]; `get-session-event-chunk-url` — a signed link valid for ≈15 minutes [inst] |
| **Authorization** | ✅ | **OAuth** (no API keys). The access token lives **2 hours** with automatic refresh; **re-authorization every 90 days** [hosted]. Metadata for `/mcp/v1` (retrieved by a script): Metadata Doc at the path-specific address `/.well-known/oauth-protected-resource/mcp/v1`; authorization server `app.launchdarkly.com/trust/oauth` (authorize, token, revoke); **Dynamic Client Registration** (`/trust/oauth/register/dcr`); grants `authorization_code`, `refresh_token`, `client_credentials`; PKCE S256; **scopes `reader`, `writer`** | [hosted], metadata | — |
| **Configuration** | ✅ | `toolsets` and `writes` in the URL — filtering of the visible tools ("These parameters don't limit what the connection can do in your account") | [hosted] | — |
| **Other: server instructions** | ✅ | The server passes the AI an instruction beginning with "IMPORTANT: Before using tools, check if the environment has LaunchDarkly related agent skills or SKILL.md installed". Then the agent is asked to ask the user whether to install skills from the repository `launchdarkly/ai-tooling` | [srv] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic beyond passing commands through

1. **Confirmation via the parameter `confirm=true`** for irreversible deletions: `delete-flag`, `delete-ai-config`, `delete-ai-config-variation`, `delete-dataset`, `delete-prompt-snippet`, `delete-agent-graph`, `delete-agent-skill`, `delete-alert`, `delete-dashboard` ("Requires confirm=true to execute") [srv], [inst].
2. **Readiness check before deleting a flag:** `delete-flag` requires the **verdict `safe`** from `check-removal-readiness` [srv]. This is a server-side refusal condition, not just text.
3. **Deletion blocked when there are dependencies:** `delete-agent-skill` is not executed while the skill is attached to at least one variation [inst].
4. **LaunchDarkly's built-in approval processes:** `toggle-flag`, `update-ai-config-targeting-rules`, `update-segment-rules`, `update-segment-targets` may require approval; there is `create-approval-request`, and `apply-approval-request` applies **only a change approved by a human** [srv], [inst].
5. **Soft alternatives to deletion:** `archive-flag` (reversible), archiving an AI Config; the descriptions advise archiving instead of deleting [srv].
6. **Query restrictions:** `query-traces` — a range of no more than 24 hours [srv]; `get-doc` — a response of no more than 75 KB and only addresses `launchdarkly.com/docs/` [inst].
7. **Restriction of the fields sent:** `update-release-autopilot-settings` sends only the changed fields, and sending `autoCleanup` is forbidden [inst].
8. **New flags are created switched off in all environments** ("starts OFF in all environments") [srv].
9. **destructive/read-only annotations** for most tools [srv], [inst].
10. **Filtering of the tool set** via the URL (`toolsets`, `writes`): less context and fewer dangerous actions, but the rights do not change [hosted].
11. **Vendor interests:** the tool `vent` invites the agent to report missing features, bugs and confusing messages to LaunchDarkly. The server instructions suggest installing LaunchDarkly skills [inst], [srv].
12. **Deprecated tools left next to the new ones:** 7 `*-factory-*` tools are marked as deprecated and duplicate Release Autopilot. This increases the context and creates a risk of choosing the deprecated tool [inst].

**Structure:** non-standard in the sense of several endpoints. Two official servers with different tool sets run on one host: `/mcp/launchdarkly` (170) and `/mcp/fm` (111). Inside each — a flat list with toolset filtering. Agent skills are distributed separately (`npx skills add launchdarkly/ai-tooling`), e.g. `launchdarkly-flag-cleanup` [docs]. Skills have also become product objects: the agent can create them and attach them to AI configurations [inst].

## E. Overall evaluation

**CSV endpoint `/mcp/v1`: 18 actions** (according to [`/mcp/v1/install`](https://mcp.launchdarkly.com/mcp/v1/install)):

| Group | Tools |
|---|---|
| Feature flags (15) | `list-flags` R, `get-flag` R, `get-flag-health` R, `get-flag-status-across-envs` R, `find-stale-flags` R, `check-removal-readiness` R, `create-flag`, `toggle-flag` D, `update-flag-settings`, `update-rollout` D, `update-targeting-rules` D, `update-individual-targets` D, `update-prerequisites` D, `manage-expiring-targets` D, `copy-flag-config` D |
| Approvals (3) | `create-approval-request`, `list-approval-requests` R, `apply-approval-request` D |

On `/mcp/v1` there is no deleting or archiving of flags, no AI Configs, no observability, no segments, no `vent`. `toggle-flag` and `update-rollout` are marked Destructive here, but not on `/mcp/launchdarkly`.

**Documented server `/mcp/launchdarkly`: 170 actions** according to [inst]. Below are the 166 established names (R — read-only, D — destructive; unmarked — a change not marked destructive). Another 4 names could not be found: the page is served truncated. By annotations: ≈85 read-only, ≈37 destructive, ≈44 other changes. For 4 tools found only on [fm], the annotations are not visible.

| Group | Tools |
|---|---|
| Feature flags (17) | `list-flags` R, `get-flag` R, `get-flag-health` R, `get-flag-status-across-envs` R, `find-stale-flags` R, `check-removal-readiness` R, `create-flag`, `toggle-flag`, `update-flag-settings`, `update-rollout`, `update-targeting-rules` D, `update-individual-targets` D, `update-prerequisites` D, `manage-expiring-targets` D, `copy-flag-config` D, `archive-flag` D, `delete-flag` D |
| Approvals (3) | `create-approval-request`, `list-approval-requests` R, `apply-approval-request` D |
| Releases and rollouts (6) | `start-guarded-rollout`, `stop-guarded-rollout` D, `create-automated-rollout-config`, `match-release-policies` R, `check-flag-rollout-complete` R, `list-release-policies` R |
| Release Autopilot (7) | `get-release-autopilot-settings` R, `update-release-autopilot-settings` D, `list-release-autopilot-github-repos` R, `list-release-autopilot-repo-settings` R, `get-release-autopilot-repo-settings` R, `update-release-autopilot-repo-settings` D, `delete-release-autopilot-repo-settings` D |
| Factory, deprecated (7) | the same 7 actions with the prefix `factory` (`get-factory-settings` R, `update-factory-settings` D, `list-factory-github-repos` R, `list-factory-repo-settings` R, `get-factory-repo-settings` R, `update-factory-repo-settings` D, `delete-factory-repo-settings` D) |
| Segments (5) | `list-segments` R, `get-segment` R, `create-segment`, `update-segment-rules` D, `update-segment-targets` D |
| Contexts (2) | `search-contexts` R, `get-context-instances` R (end-user attributes) |
| AI Configs (12) | `list-ai-configs` R, `get-ai-config` R, `create-ai-config`, `setup-ai-config`, `update-ai-config`, `delete-ai-config` D, `get-ai-config-health` R, `get-ai-config-status-across-envs` R, `get-ai-config-targeting` R, `update-ai-config-individual-targets` D, `update-ai-config-rollout`, `update-ai-config-targeting-rules` D |
| AI Config variations (4) | `create-ai-config-variation`, `clone-ai-config-variation`, `update-ai-config-variation` D, `delete-ai-config-variation` D |
| AgentControl models (8) | `list-agentcontrol-model-configs` R, `get-agentcontrol-model-config` R, `create-agentcontrol-model-config`, `update-agentcontrol-model-config`, `delete-agentcontrol-model-config` D, `restrict-agentcontrol-model-configs` D, `unrestrict-agentcontrol-model-configs` D, `toggle-agentcontrol-config` (only in [fm]) |
| Agent skills (7) | `list-agent-skills` R, `get-agent-skill` R, `create-agent-skill`, `update-agent-skill`, `delete-agent-skill` D, `list-agent-skill-versions` R, `list-agent-skill-references` R |
| AI tools (6) | `list-ai-tools` R, `get-ai-tool` R, `create-ai-tool`, `list-ai-tool-versions` R, `update-ai-tool`, `delete-ai-tool` (the last two — only in [fm]) |
| Agent graphs (5) | `list-`, `get-` R; `create-`; `update-` D; `delete-agent-graph` D |
| Experiments (9) | `list-experiments` R, `get-experiment` R, `create-experiment`, `update-experiment` D, `start-experiment-iteration`, `save-and-start-experiment-iteration` D, `stop-experiment-iteration` D, `get-experiment-results` (in [fm]), `get-experiment-metric-results` |
| Metrics (4) | `list-metrics` R, `get-metric` R, `create-metric`, `list-metric-events` R |
| Evaluations, datasets, playgrounds, snippets (18) | `list-/get-/create-evaluation`, `run-evaluation`, `get-evaluation-run-summary` R; `list-/get-/create-dataset`, `delete-dataset` D; `list-/get-/create-/update-playground`; `list-/get-/create-/update-prompt-snippet`, `delete-prompt-snippet` D |
| Observability (9) | `query-logs`, `query-traces`, `query-aggregations`, `query-error-groups`, `query-sessions`, `query-timeline-events`, `query-flag-evaluations`, `query-service-map`, `get-flag-unique-context-exposures` (all R) |
| Session recordings (3) | `get-session-event-chunks` R, `get-session-event-chunk-url` R, `get-session-timestamp-event-chunk-url` R |
| Alerts (7) | `list-alerts` R, `get-alert` R, `get-alert-firing-history` R, `create-alert`, `update-alert` D, `toggle-alert` D, `delete-alert` D |
| Dashboards (7) | `list-dashboards` R, `get-dashboard` R, `create-dashboard`, `delete-dashboard` D, `create-graph`, `preview-graph` R, `get-keys` R |
| Views (7) | `list-views` R, `get-view` R, `create-view`, `update-view`, `link-view-resources`, `list-view-resources` R, `get-resource-views` R |
| Projects, environments, usage (6) | `list-projects` R, `create-project`, `get-project` R (**returns SDK keys**), `get-environment` R (**SDK keys**), `get-sdk-active` R, `get-service-connections-usage` R |
| Members (3) | `get-member-self` R, `find-members` R, **`invite-members`** (invitation e-mails) |
| Audit (1) | `query-change-history` R |
| Documentation (2) | `search-docs` R, `get-doc` R |
| Feedback to the vendor (1) | `vent` |

**Parameters:** not published (known: `confirm=true` for deletions).

**Tokens:** cannot be determined: the full `tools/list` is not available. With 170 tools the context is very large, which is why `toolsets` were introduced.

**What the agent CANNOT do:** manage roles and teams (only invitations), integrations, billing; work in EU/Federal via the cloud server [hosted], [inst].

## F. Documentation analysis

- **Recommendations not checked by the server:** "Review tool calls before your AI client runs them, especially calls that change or delete data"; "Don't set your AI client to approve these calls automatically"; disconnect the server after work and revoke access [hosted].
- **Data:** results go to the AI provider; LaunchDarkly "doesn't control your AI client or your model provider". It is explicitly listed what may be sent: flags, segments, AI Configs, change history, descriptions of approval requests, **contexts and attributes (may contain personal data of end users)**, observability data including sessions, **member names and e-mails**, **server-side SDK keys** [hosted].
- **Prompt injection:** "anyone who can write data that MCP tools return can try to give instructions to the model" — flag descriptions, segment names, logs, errors [hosted].
- **Comparison with the logic:** some risks are covered by the server (`confirm=true`, readiness check, blocking of skill deletion, approvals). Some are left to the user: reviewing calls, no auto-approval. The new tools for session recordings and contexts increase the amount of personal data that may go to the AI provider. Masking like GoCardless's is not declared.

## Observations

- **The most honest documentation about risks** in the sample: it lists which data goes to the AI provider and explains the risk of prompt injection through data.
- **Multi-level protection of deletion:** `confirm=true` + verdict `safe` + blocking when there are dependencies + preference for archiving. This is closest to the server-side "refusal conditions" from the task.
- **Integration with the product's human approval processes:** the agent can only request approval; it can apply the change only after a human.
- **Vendor interests:** `vent` (the agent as a source of product feedback, like `tavily_feedback` at Tavily) and server instructions suggesting the installation of LaunchDarkly skills.
- **Skills in three roles:** distributed outside the server (repository), recommended through the server instructions and managed by the agent as product objects.
- **Deprecated duplicate tools** (Factory ↔ Release Autopilot) are left in the list. This is extra context and a risk of confusion for the agent.
- **Toolsets via the URL** — control of the context size and the set of actions.
- **Handing out secrets (SDK keys) to the agent** via `get-project`/`get-environment`.
