# MCP server: Grafana

> **In plain words.** Grafana is a popular monitoring program: charts (dashboards), logs, metrics, incident alerts. Its MCP server gives an AI agent a great many "buttons" (more than a hundred): search and change dashboards, run queries against metric and log databases, create alerts and incidents, and also make **any** HTTP request to the Grafana API.
>
> **Analysis date:** 12.10.2026; re-analysed on 23.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.
>
> **Verbatim descriptions of all tools** (Pre-Interaction Context) are in a separate file: `02b_grafana_pre_interaction_context.md`.

**Abbreviations in links:**
- `[code]` = [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana/tree/e97cd4479eb40d25bc8d466db1651c29ce0c783e) at a pinned commit.
- `[readme:N]` = line N of [README.md](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/README.md).
- `[main:N]` = line N of [cmd/mcp-grafana/main.go](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/cmd/mcp-grafana/main.go).
- `[tools:N]` = line N of [tools.go](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools.go).
- `[cloud-mcp]` = [Grafana Cloud MCP server docs](https://grafana.com/docs/grafana-cloud/ai-tools/mcp-servers/cloud-mcp/).

---

## ⚠️ Important limitation of the analysis

The CSV gives the **cloud** server `https://mcp.grafana.com/mcp` (Grafana Cloud MCP). This is a **separate hosted product**. The code of the cloud server is **not published** as a whole. The documentation says it has the same tool categories as the open server, **plus** its own Grafana Assistant tools (`create_investigation`, `describe_infrastructure`, investigation tools and "infrastructure memory"). The published tool list of the cloud server does **not** include `grafana_api_request` [cloud-mcp].

The code analysis below refers to the **open** server `grafana/mcp-grafana`. Information about the cloud server comes from the documentation and is marked **☁️**.

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Grafana MCP server (`mcp-grafana`); cloud variant — Grafana Cloud MCP server | [readme:1], [cloud-mcp] |
| Code link | https://github.com/grafana/mcp-grafana | — |
| Documentation | Open: https://grafana.com/docs/grafana/latest/developer-resources/mcp/ (link from the CSV) · ☁️ Cloud: https://grafana.com/docs/grafana-cloud/ai-tools/mcp-servers/cloud-mcp/ | CSV |
| Endpoint (from CSV) | `https://mcp.grafana.com/mcp`; the stack is selected with the `X-Grafana-URL` header or the path `/mcp/<stack>.grafana.net` | [cloud-mcp] |
| MCP version | go-sdk supports `2026-07-28` (latest, default), `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05` | [go-sdk v1.8.0 shared.go:45–64](https://github.com/modelcontextprotocol/go-sdk/blob/v1.8.0/mcp/shared.go#L45-L64) |
| Commit / date | `e97cd4479eb40d25bc8d466db1651c29ce0c783e`, 2026-10-23. Latest release tag: `v2.1.1` | `git log`, `git tag` |
| Language | Go (module `github.com/grafana/mcp-grafana/v2`, go 1.26.10) | [go.mod](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/go.mod) |
| MCP SDK | Official `github.com/modelcontextprotocol/go-sdk` **v1.8.0** | [go.mod:21](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/go.mod#L21) |
| Transport | `stdio` (default), `sse`, `streamable-http` · ☁️ Streamable HTTP only | [readme:434], [cloud-mcp] |
| Code open? License | Open server — yes, **Apache 2.0**. ☁️ Cloud — no | [LICENSE](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/LICENSE) |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | The open server is free. ☁️ Cloud: a connection **counts as an "active AI user" of Grafana Assistant**, even if no AI tokens are spent. Simple data queries do not consume tokens; calls to Assistant functions do | [cloud-mcp], [Assistant pricing](https://grafana.com/docs/grafana-cloud/platform/pricing-and-usage/assistant/) |
| Assistant prices ☁️ | Free plan: up to **3 active AI users/month** (40 million tokens per user) + 25 million tokens for service accounts; above the limit — blocked until the next period. Pro: **$20 per active AI user** (40 million tokens included), extra tokens **$2 per 1 million** | [grafana.com/pricing](https://grafana.com/pricing/), [Assistant pricing](https://grafana.com/docs/grafana-cloud/platform/pricing-and-usage/assistant/) |
| Linked software | Grafana OSS — free (open source). Grafana Cloud: Free $0; Pro from **$19/month + usage**; Enterprise from **$25,000/year** | [grafana.com/pricing](https://grafana.com/pricing/) |
| Requirements | Grafana ≥ 9.0. ☁️ Grafana Cloud only; Assistant must be available on the stack and the Assistant terms accepted | [readme:36], [cloud-mcp] |
| Access restrictions | (1) **Grafana RBAC**: every action is checked by Grafana itself against the rights of the token/user (controlled by the Grafana administrator). (2) The tool set is defined by the **server operator** with flags (`--enabled-tools`, `--disable-write`, `--disable-query` etc.). (3) ☁️ On the OAuth consent screen the user chooses the access level: **Read / Query / Write**; Write requires the scope `grafana:write`; access requires the role "Assistant Cloud MCP User" (Editor and above by default); Write may require the role "Assistant Admin" | [readme:244–299, 505–542], [cloud-mcp] |
| Rate limits | Not documented. Default timeout for requests to Grafana is 10 s (`--grafana-timeout`) | [readme:490] |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **119** unique tools in the code (34 categories), **79** enabled by default. Some have "read-only" variants (e.g. `grafana_api_request` ×3, `generate_deeplink` ×2, `agento11y_*` ×2). Every tool gets the annotations `title/readOnlyHint/destructiveHint/idempotentHint/openWorldHint` and in `_meta` the key `grafana.com/requiredPermissions` (list of required RBAC permissions) [permissions.go](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/permissions.go) | Verbatim: file `02b_…`. **Server instructions** are assembled dynamically from the enabled categories + a sentence about the UTC time zone [main:532–575]. The operator can append their own text with the flag `--instructions-append` [readme:439]. The `tools/list` response is marked `cacheScope: "private"` [main:595–612] | Structure: the function result is turned into a **JSON string** in one `text` block [tools:480–485]; strings as they are; `get_panel_image` returns PNG (base64). Some tools add hints for the AI: e.g. `query_loki_logs` returns `metadata` (how many lines, whether truncated) and `hints` for an empty result ([tools/loki.go:496–511](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L496-L511)) |
| **Resources** | ✅ | 3 HTML resources of **MCP Apps** (interactive interface inside the client): `ui://mcp-grafana/panel-viewer.html`, `ui://grafana/metrics.html`, `ui://grafana/trace.html`. Linked to tools via `_meta.ui.resourceUri` | [ui_apps.go:11–29](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/ui_apps.go#L11-L29), [ui_metrics.go:11](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/ui_metrics.go#L11), [ui_trace.go:11](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/ui_trace.go#L11) | MIME `text/html;profile=mcp-app` |
| Prompts | ❌ | Not found in the code (no `AddPrompt`) | — | — |
| Logging (MCP) | ❌ | No MCP log notifications are sent. Logs go to stderr (slog) and optionally to OpenTelemetry; there is a slow-request log `--slow-request-threshold` | [readme:1315–1390] | — |
| Sampling | ❌ | Not found | — | — |
| Roots | ❌ | Not found | — | — |
| **Authorization** | ✅ | **Open server.** (1) Access to the MCP server itself over HTTP: optional static Bearer token `--server-auth-token`; without it on a non-loopback address the server starts but logs a security error [readme:453–459]. (2) Access to Grafana: service account token, login/password, Grafana Cloud on-behalf-of tokens, forwarding of cookies/headers from the request (`GRAFANA_FORWARD_HEADERS`) [readme:668–800], [mcpgrafana.go:289–304](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/mcpgrafana.go#L289-L304). No OAuth server of its own. **☁️ Cloud:** OAuth 2.1 in the browser; some clients need manual registration of a client ID/secret ([register-oauth-client](https://grafana.com/docs/grafana-cloud/ai-tools/mcp-servers/register-oauth-client)); consent screen with a choice of rights; the token is valid for 1 hour and is refreshed automatically for 30 days; revocation — Settings → Connectors → MCP clients. The authorization server is Grafana | [cloud-mcp] | — |
| Elicitation | ❌ | Not found. The description of `alerting_rules_write` contains the text instruction "Ask if context conflicts" — this is a request to the AI, not MCP Elicitation | `02b_…` | — |
| Tasks (MCP) | ❌ | Not found. `ask_assistant` blocks the call until the answer arrives (up to 5 min) | [readme:163] | — |
| **Configuration** | ✅ | Very detailed: several dozen flags and environment variables — selection of categories, read-only, query-free, Loki restrictions, TLS, proxy, multi-organisation (`--dynamic-multi-org` adds the parameter `orgId` to every tool), statistics | [readme:429–667], [tools:130–147] | — |
| **Error Reporting** | ✅ | Tool error → `isError: true` + error text [tools:426–443]. Unknown argument → `isError` with a list of allowed names ("self-correcting for LLM callers") [tools_param_validation.go](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools_param_validation.go). Critical errors (`HardError`, no authorization) → JSON-RPC error. Panic → `internal error` [main:624–637] | — | Error text |
| Subscription | ❌ | Not found | — | — |
| Progress Tracking | ❌ | Not found (no `NotifyProgress`) | — | — |
| Cancellation | ⚠️ implicit | No explicit handling; handlers receive a `context.Context` from go-sdk through which the SDK can abort a request (not verified by running it) | [tools:340] | — |
| Other | ✅ | OpenTelemetry tracing, acceptance of W3C trace context from the request `_meta` [tools:344]; Prometheus metrics; anonymous statistics (see F) | [readme:1252–1402] | — |

## D. Server logic beyond simply passing commands through

1. **Restriction modes set by the operator (not the AI):**
   - `--disable-write` — removes all writing tools; `grafana_api_request` becomes "GET only" (or GET + POST on `/api/ds/query`) [readme:544–600], [tools/api.go:208–261](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/api.go#L208-L261).
   - The server **classifies the danger of query languages itself**: `query_sql` and `query_influxdb` count as writing, because SQL can contain `DROP TABLE`; PromQL/LogQL/TraceQL do not [readme:586–600].
   - `--disable-query` — removes all tools that run data queries (only metadata remains) [readme:602–656].
   - Whole categories can be turned on/off; 12 categories are off by default (admin, agento11y, assistant, sql, cloudwatch, cloudlogging, elasticsearch, examples, graphite, influxdb, quickwit, runpanelquery) [readme:505], [main:217].
2. **The server description for the AI changes with the configuration:** the server instructions include only the categories that are actually available; with queries disabled — shortened wording ("Query execution is disabled.") [main:112–122, 532–575].
3. **Argument validation:** unknown parameters are rejected (not ignored) [tools:378–381]; automatic conversion of types that the AI often mixes up (`"42"` → 42, string → array) [tools:177–291].
4. **Cost limiter for Loki queries** (`--loki-guardrail-mode off|shadow|enforce`): requires a selective selector, limits the time range (24 h by default) and the scan volume (100 GiB) based on a prior estimate; in `enforce` mode it rejects the request **with a hint to the AI on how to rewrite it**. Off by default [readme:507–509], [lokiguard/](https://github.com/grafana/mcp-grafana/tree/e97cd4479eb40d25bc8d466db1651c29ce0c783e/lokiguard).
5. **Enforced Loki filters** (`--loki-enforced-matchers`): the operator's filters are added to every log query; the AI's query can only **narrow** the selection; if parsing fails, the request is **rejected** (fail closed). At startup the server warns about bypasses (`grafana_api_request`, `get_panel_image`, `ask_assistant`) [readme:1404–1454].
6. **Response size limits:** `query_loki_logs` — 10 lines by default, maximum 100 (`--max-loki-log-limit`); the server requests 1 line more in order to tell the AI about truncation [readme:506]. Dashboard tools offer the AI economical variants (`get_dashboard_summary`, `get_dashboard_property` with JSONPath) [readme:59–65].
7. **Network security (HTTP mode):** checking of the `Host`/`Origin` headers (protection against DNS rebinding), redirects to another domain are forbidden (so that credentials do not leak), whitelist of Grafana URLs with `X-Grafana-URL` [readme:444–483], [redirect_guard.go](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/redirect_guard.go).
8. **Permissions:** the server **declares** the required RBAC permissions in the `_meta` of each tool, but does **not check** them itself — Grafana checks and returns 403 [permissions.go:9–41](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/permissions.go#L9-L41).
9. **Monitoring:** duration metrics for every call, counters of Loki limiter decisions, tracing; call arguments end up in traces only with `--include-args-in-spans` [readme:492, 1293–1311].
10. **Influence of past actions on future ones:** not found. The tool set is fixed at startup.
11. **Human confirmation:** none in the server. ☁️ The only "manual" point is the OAuth consent screen when connecting.

**Server structure:** flat, but **modular**: 34 categories that are enabled with flags. No hierarchy of sub-servers. ☁️ In the cloud server, the Tempo tools are **proxied** from the MCP servers of Tempo data sources [cloud-mcp].

## E. Overall evaluation

**Number of actions:** 119 tools in the open code, **79 by default**. Some tools are "multi-operation" (e.g. `alerting_rules_write`: create/update/delete; `alerting_manage_routing`: policies, contacts, intervals), so the actual number of operations is larger. In addition, `grafana_api_request` gives access to **any** Grafana API endpoint (GET/POST/PUT/PATCH/DELETE) and is enabled by default. ☁️ Cloud server: the exact list in the documentation is incomplete (grouped by category).

**List of actions and their parameters:** the complete list (name, category, enabled by default or not, readOnly/destructive, verbatim description, all parameters with type, whether required, default values and enum variants) is in the file `02b_grafana_pre_interaction_context.md`. Distribution by category: admin 9, agento11y 8, oncall 8, tempo 7, alerting 6, dashboard 6, incident 6, loki 6, prometheus 6, annotations 5, cloudwatch 5, datasource 5, cloudlogging 4, graphite 4, pyroscope 4, snapshot 4, sql 4, plugin 3, docs 2, provisioning 2, search 2, the rest 1 each.

**Tokens before the first action:** in a standard start ≈ **27,000 tokens** (79 tools ≈ 26,600 + server instructions ≈ 460); with everything enabled ≈ **40,000**. Estimate: length of the reconstructed JSON ÷ 4 characters per token, error ±30 %. The README openly admits the problem: categories can be disabled "if you don't want to take up too much of the context window" [readme:238–239].

**What the agent CANNOT do but a human can:**
- As long as `grafana_api_request` is enabled (default), the agent can technically do almost everything that the Grafana API and the token's rights allow. **The real boundary is the RBAC permissions, not the tool set.**
- Without `grafana_api_request` (or ☁️ in the cloud server, where it is not in the list): there are no tools for **deleting dashboards, folders and data sources**, managing **users, teams, service accounts and roles** (admin tools only read), organisation settings, removing/disabling plugins, changing access rights to resources. Source: comparison of the tool list (`02b_…`) with the [Grafana HTTP API](https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/).
- Browser-only actions: visual editing of panels, the Explore interface (the agent can only get a link via `generate_deeplink` or a picture via `get_panel_image`).

## F. Documentation analysis

**Recommendations to the user that the server does not check:**
- "When creating a service account … ensure it has the necessary permissions"; for simplicity the `Editor` role can be given, but it is "less restrictive" — use it only if convenience matters more than the principle of least privilege [readme:246–248, 672–675].
- Enable `--include-args-in-spans` only outside production or if the arguments contain no personal data [readme:492].
- Do not expose the server without `--server-auth-token` on an external address; use TLS [readme:459].
- For URL overrides: "Deploy behind an authenticating proxy … Restrict the server's outbound network access" [readme:463–468].
- For the Loki restrictions to really work, manually disable the bypasses (`--disable-api`, `--disable-rendering`, `--disable-assistant`) [readme:1441–1454].
- ☁️ For "read-only" mode, untick both Write and **Query**: "clearing only Write access still allows raw SQL" [cloud-mcp].
- There are no explicit recommendations on human confirmation of actions.

**Promises on governance and data:**
- **Anonymous statistics are enabled by default.** Every 4 hours the following is sent: which tools were called, how many errors, the configuration. Not sent: arguments, queries, logs, errors, credentials, instance URL. On Grafana's side a coarse region and network name are added from the IP. Opt-out: `--usage-stats=disabled` or `DO_NOT_TRACK=1` [readme:1252–1273], [usage stats docs](https://grafana.com/docs/grafana/latest/developer-resources/mcp/anonymous-usage-statistics/).
- SQL tools: "credentials are never seen by the MCP server" (authentication via the Grafana data source) [readme:100].
- ☁️ "Grafana doesn't train AI models on your PromQL, LogQL queries, investigation content, or prompt payload data" [cloud-mcp]. Assistant policy: LLM providers (Anthropic, Google Vertex AI, Amazon Bedrock) with zero retention; conversations are stored in the tenant for 30/90/180 days (90 by default); after deletion up to 30 days in the systems; employee access is restricted and audited [Assistant privacy](https://grafana.com/docs/grafana-cloud/platform/grafana-assistant/privacy-and-security/privacy/).
- Reversibility: dashboards have versions (`list_dashboard_versions`, `get_dashboard_by_uid` with `version`), but there is no one-command rollback; `delete_annotation` — "Permanently delete" [readme:46, 218].

**Promises to the user:** the feature list is "for informational purposes only and does not represent a roadmap or commitment" [readme:40]; link generation "instead of relying on LLM URL guessing" [readme:204].

**Comparison with the server logic:** the statements about statistics are consistent with the code (module [usagestats/](https://github.com/grafana/mcp-grafana/tree/e97cd4479eb40d25bc8d466db1651c29ce0c783e/usagestats)), but "enabled by default" means data is transmitted without explicit consent. The Loki restrictions are implemented in the code and honestly documented together with their bypasses.

---

## Observations for the research (as requested by David)

- **The most "governed" server of the three.** Many server-side mechanisms: read-only/query-free modes, classification of query languages by danger, enforced filters, a cost limiter, URL whitelists.
- **A universal tool as a bypass of targeted restrictions.** `grafana_api_request` ("Similar to 'gh api'") makes the other 118 tools in a sense just "convenient shortcuts". Restrictions of individual tools do not work as long as it is enabled.
- **Responsibility is split:** the server declares the permissions (`_meta`), and Grafana checks them. Security depends on how narrowly the administrator has configured the token.
- **The server description for the AI depends on the configuration** (dynamic instructions), so the same model sees a different "world" with different clients.
- **Context size as a design problem:** about 27 thousand tokens by default. The server addresses this with categories and "economical" tools.
- **Commercial model of the cloud version:** every connected user counts as a paid "active AI user".
