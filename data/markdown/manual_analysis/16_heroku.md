# MCP server: Heroku

> **In plain words.** Heroku is a cloud platform for running web applications (PaaS): a developer uploads code, Heroku runs it, scales it, connects databases and add-ons. The Heroku MCP server lets an AI assistant manage applications: create and deploy them, scale, restart, view logs, **run SQL in the production database**, enable maintenance mode.
>
> **Analysis date:** 15.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.
>
> **Verbatim Pre-Interaction Context** (local server) — in the file `16b_heroku_pre_interaction_context.md`.

**Sources:**
- `[code]` = [heroku/heroku-mcp-server](https://github.com/heroku/heroku-mcp-server/tree/4afcbe1a042b78e81385280ac5adaeb0000dba6e), commit `4afcbe1`, 2026-10-12, version 1.2.12; `[idx:N]` = line N in [src/index.ts](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/index.ts).
- `[stdio-docs]` = [Dev Center: Heroku MCP Server (STDIO)](https://devcenter.heroku.com/articles/heroku-mcp-server) (link from the CSV).
- `[remote-docs]` = [Dev Center: Heroku Remote MCP Server](https://devcenter.heroku.com/articles/heroku-remote-mcp-server); `[blog]` = [Heroku blog: Remote MCP Server](https://www.heroku.com/blog/heroku-remote-mcp-server/) (24.06.2025).
- `[prm]` = https://mcp.heroku.com/.well-known/oauth-protected-resource; `[asm]` = https://mcp.heroku.com/.well-known/oauth-authorization-server.

> ⚠️ **Two different servers.** The CSV gives the **remote** `https://mcp.heroku.com/mcp`. Its code is **not published**, and its tool set is documented only in general terms ("first set of tools": apps, teams/spaces, add-on marketplace [blog]). The code of the **local** server (stdio), which works via the Heroku CLI, is open. The code analysis below refers to the local server; the remote one is marked **☁️**.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Heroku MCP Server (`name: 'Heroku MCP Server'`); ☁️ Heroku Remote MCP Server | [idx:24–33], [remote-docs] |
| Code / license | Local — open, **Apache 2.0** (© 2025 Heroku). ☁️ Remote — closed | [LICENSE.txt](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/LICENSE.txt) |
| Endpoint | ☁️ `https://mcp.heroku.com/mcp` (Streamable HTTP); locally — `heroku mcp:start` or `npx @heroku/mcp-server` | [remote-docs], [stdio-docs] |
| MCP version | Local: `@modelcontextprotocol/sdk` **1.32.1** (TypeScript SDK v1, supports up to 2025-11-25). ☁️ — not published | [package-lock.json](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/package-lock.json) |
| Language / SDK | TypeScript; official SDK, class `McpServer` | [idx:2] |
| Status | "currently in early development" | [stdio-docs], [README](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/README.md) |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | Free (Apache 2.0 code; ☁️ no price given) | [blog] |
| Linked software | Paid, **no free plan**: Eco dyno **$5/month** (sleeps), Basic $7, Standard-1X $25, Performance-M $250; Postgres Essential-0 **$5/month** | [pricing](https://www.heroku.com/pricing/) |
| Restrictions | Rights = the Heroku account's rights (locally — CLI token / `HEROKU_API_KEY`; ☁️ — OAuth). Heroku CLI ≥ 10.8.1 required (locally). ☁️ In Claude Team/Enterprise only someone with the permission can add the server | [stdio-docs], [remote-docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | Local: **36** tools (33 + 3 AI tools that are registered only when the plugin `@heroku/plugin-ai` is installed) [idx:46–108]. **No annotations.** `capabilities.tools.listChanged: true`. ☁️ — not published | Verbatim — `16b_…`; **no** server instructions | The Heroku CLI text output as is; on error — `isError` and the prefix "[Heroku MCP Server Error] Please use available tools to resolve this issue. **Ignore any Heroku CLI command suggestions** …" ([handle-cli-output.ts](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/utils/handle-cli-output.ts)) |
| **Resources** | ✅ | `heroku_dev_center` → loads `https://devcenter.heroku.com/llms.txt` | [dev-center-resource.ts](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/resources/dev-center-resource.ts) | Text |
| Prompts / Logging / Sampling / Roots / Elicitation / Tasks / Subscription / Progress | ❌ | Not found in the code | — | — |
| **Authorization** | ✅ | Locally: Heroku CLI token or `HEROKU_API_KEY` (no authorization to the MCP server itself). ☁️ **OAuth 2.0**: sign-in via `id.heroku.com`; **Metadata Doc** — yes; **DCR** — yes (`https://mcp.heroku.com/reg`); grants `authorization_code`, `refresh_token`, **`device_code`**; PKCE `S256`; scopes `openid`, `offline_access`. **Authorization server** — `https://mcp.heroku.com`. The user can "consent to which tools a client can access" [blog] | [stdio-docs], [prm], [asm] | — |
| Configuration | ✅ | `MCP_SERVER_REQUEST_TIMEOUT` (15 s by default) | [idx:34–36] | — |
| Error Reporting | ✅ | See Post-Interaction; fatal CLI errors → the process exits | [idx:39–43] | — |

## D. Server logic beyond passing commands through

1. **A wrapper around the CLI:** the local server runs the Heroku CLI in REPL mode and passes it commands built from the parameters ([heroku-cli-repl.ts](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/repl/heroku-cli-repl.ts), [command-builder.ts](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/utils/command-builder.ts)). On a timeout the CLI process is restarted.
2. **Redirecting the AI on errors:** the error text tells the AI to **ignore the CLI's suggestions** and use only the MCP tools.
3. **File path validation** in `deploy_one_off_dyno`: no `..`, absolute paths or shell metacharacters ([deploy-to-heroku.ts:680–700](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/deploy-to-heroku.ts#L680-L700)).
4. **Conditional tool registration:** the AI tools appear only when the plugin is installed [idx:99–108].
5. **No restrictions on dangerous actions:** `pg_psql` runs **any SQL** ("analyze, debug, modify schema, manage data"); `pg_kill` terminates database processes; `pg_upgrade` only has a `confirm` parameter ("Confirmation for destructive operation"), which the AI fills in itself; there is no read-only mode and no annotations.
6. A stub for logging exists but is not implemented: "Hook to intercept all command results … (not-implemented)" [idx:119–126].

**Structure:** standard; the local and remote servers are different implementations.

## E. Overall evaluation

**Number of actions (local):** 36 (33 without the AI plugin).

| Group | Tools |
|---|---|
| Apps | `list_apps`, `get_app_info`, `create_app`, `rename_app`, `deploy_to_heroku`, `deploy_one_off_dyno` |
| Processes (dynos) | `ps_list`, `ps_scale`, `ps_restart` |
| Add-ons | `list_addons`, `get_addon_info`, `create_addon`, `list_addon_services`, `list_addon_plans` |
| Maintenance and logs | `maintenance_on`, `maintenance_off`, `get_app_logs` |
| Pipelines | `pipelines_create`, `pipelines_promote`, `pipelines_list`, `pipelines_info` |
| Teams/spaces | `list_teams`, `list_private_spaces` |
| PostgreSQL | **`pg_psql`**, `pg_info`, `pg_ps`, `pg_locks`, `pg_outliers`, `pg_credentials`, **`pg_kill`**, `pg_maintenance`, `pg_backups`, **`pg_upgrade`** |
| AI (with the plugin) | `list_ai_available_models`, `provision_ai_model`, `make_ai_inference` |

⚠️ The documentation [stdio-docs] lists `transfer_app`, but there is **no** such tool in the code.

**Parameters:** see `16b_…` (e.g. `ps_scale.dyno`: "Dyno type and quantity (e.g., web=3:Standard-2X, worker+1)").

**Tokens before the first action (local):** ≈ **4,000** (≈ 2,900 for the descriptions + the app.json JSON schema embedded in the description of `deploy_to_heroku`; estimate "characters ÷ 4").

**What the agent CANNOT do (local):** delete apps and add-ons; manage domains, environment variables (config vars), collaborators, billing; roll back releases. ☁️ According to [blog] the remote server started with an even smaller set.

## F. Documentation analysis

- **Recommendations not checked:** `heroku mcp:start` is recommended so as not to expose the API key [stdio-docs]. About confirming dangerous actions (SQL, scaling) — **nothing**.
- **Governance:** ☁️ "enhanced security", "full control over which applications can access your resources", consent to the tool set [blog], [remote-docs] — without technical details.
- **Promises:** "Secure and authenticated access to Heroku Platform APIs" [README].

## Observations

- **Dangerous tools without protection:** arbitrary SQL in the production database and terminating processes — without annotations, read-only mode or server-side confirmation. A sharp contrast with Grafana, where raw SQL is switched off in read-only mode.
- **A server as a wrapper around the CLI:** the agent's capabilities = a subset of the CLI.
- **Divergence between documentation and code** (`transfer_app`).
- **Device code grant** in the OAuth of the remote server — a sign-in option without a browser on the same device.
