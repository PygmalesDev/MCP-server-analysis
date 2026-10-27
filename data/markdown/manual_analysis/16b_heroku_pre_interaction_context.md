# Heroku MCP — Pre-Interaction Context (appendix)

Source: the open **local** server [heroku/heroku-mcp-server](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/) at commit `4afcbe1a042b78e81385280ac5adaeb0000dba6e` (2026-10-12), package version 1.2.12.

**How it was obtained.** Static parsing of the TypeScript code (without running it). Tool names and descriptions (`server.tool(name, description, schema)`) and parameter descriptions (`.describe(...)` in zod schemas) are copied verbatim from the code. The exact `tools/list` JSON is built by the SDK at startup (zod → JSON Schema).

**Important:** this is the code of the **local** server (stdio). The code of the remote server `mcp.heroku.com/mcp` from the CSV is not published. Its tool set may differ.

**Server instructions:** not set (`new McpServer(...)` has no `instructions`) — [src/index.ts:24–33](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/index.ts#L24-L33).

**Tool annotations (readOnlyHint etc.):** not set for any tool.

**Resources:** `heroku_dev_center` — URI `https://devcenter.heroku.com/llms.txt`, description: "This resource provides a summary of Heroku Dev Center articles, and how to use Heroku." ([src/resources/dev-center-resource.ts](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/resources/dev-center-resource.ts)).

## Tools

| # | Tool | File | Description (verbatim) |
|---|---|---|---|
| 1 | `list_addons` | [addons.ts:36](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/addons.ts#L36) | List add-ons: all apps or specific app, detailed metadata |
| 2 | `get_addon_info` | [addons.ts:77](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/addons.ts#L77) | Get add-on details: plan, state, billing |
| 3 | `create_addon` | [addons.ts:115](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/addons.ts#L115) | Create add-on: specify service, plan, custom names |
| 4 | `list_addon_services` | [addons.ts:157](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/addons.ts#L157) | List available add-on services and features |
| 5 | `list_addon_plans` | [addons.ts:194](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/addons.ts#L194) | List service plans: features, pricing, availability |
| 6 | `list_ai_available_models` | [ai.ts:19](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/ai.ts#L19) | List available AI inference models _(registered only if the `@heroku/plugin-ai` plugin is installed)_ |
| 7 | `provision_ai_model` | [ai.ts:60](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/ai.ts#L60) | Provision AI model access for app _(registered only if the `@heroku/plugin-ai` plugin is installed)_ |
| 8 | `make_ai_inference` | [ai.ts:164](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/ai.ts#L164) | Make inference request to Heroku AI API _(registered only if the `@heroku/plugin-ai` plugin is installed)_ |
| 9 | `list_apps` | [apps.ts:32](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/apps.ts#L32) | List Heroku apps: owned, collaborator access, team/space filtering |
| 10 | `get_app_info` | [apps.ts:72](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/apps.ts#L72) | Get app details: config, dynos, addons, access, domains |
| 11 | `create_app` | [apps.ts:112](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/apps.ts#L112) | Create app: custom name, region (US/EU), team, private space |
| 12 | `rename_app` | [apps.ts:152](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/apps.ts#L152) | Rename app: validate and update app name |
| 13 | `pg_psql` | [data.ts:157](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L157) | Execute SQL queries: analyze, debug, modify schema, manage data |
| 14 | `pg_info` | [data.ts:185](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L185) | View database status: config, metrics, resources, health |
| 15 | `pg_ps` | [data.ts:210](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L210) | Monitor active queries: progress, resources, performance |
| 16 | `pg_locks` | [data.ts:236](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L236) | Analyze locks: blocked queries, deadlocks, concurrency |
| 17 | `pg_outliers` | [data.ts:262](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L262) | Find resource-heavy queries: performance, patterns, optimization |
| 18 | `pg_credentials` | [data.ts:290](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L290) | Manage access: credentials, permissions, security, monitoring |
| 19 | `pg_kill` | [data.ts:315](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L315) | Stop processes: stuck queries, blocking transactions, runaway operations |
| 20 | `pg_maintenance` | [data.ts:344](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L344) | Track maintenance: windows, schedules, progress, planning |
| 21 | `pg_backups` | [data.ts:369](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L369) | Manage backups: schedules, status, verification, recovery |
| 22 | `pg_upgrade` | [data.ts:393](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/data.ts#L393) | Upgrade PostgreSQL: version migration, compatibility, safety |
| 23 | `deploy_to_heroku` | [deploy-to-heroku.ts:642](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/deploy-to-heroku.ts#L642) | Use for all deployments. Deploys new/existing apps, with or without teams/spaces, and env vars to Heroku. Ask for app name if missing. Requires valid app.json via appJson param. |
| 24 | `get_app_logs` | [logs.ts:32](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/logs.ts#L32) | App logs: monitor/debug/filter by dyno/process/source |
| 25 | `maintenance_on` | [maintenance.ts:32](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/maintenance.ts#L32) | Enable maintenance mode and redirect traffic for a Heroku app |
| 26 | `maintenance_off` | [maintenance.ts:57](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/maintenance.ts#L57) | Disable maintenance mode and restore normal app operations |
| 27 | `pipelines_create` | [pipelines.ts:67](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/pipelines.ts#L67) | Creates new Heroku deployment pipeline with configurable stages, apps, and team settings |
| 28 | `pipelines_promote` | [pipelines.ts:94](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/pipelines.ts#L94) | Promotes apps between pipeline stages with configurable target applications |
| 29 | `pipelines_list` | [pipelines.ts:119](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/pipelines.ts#L119) | Lists accessible Heroku pipelines with ownership and configuration details |
| 30 | `pipelines_info` | [pipelines.ts:143](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/pipelines.ts#L143) | Displays detailed pipeline configuration, stages, and connected applications |
| 31 | `ps_list` | [ps.ts:54](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/ps.ts#L54) | List and monitor Heroku app dynos. View running dynos, check status/health, monitor process states, verify configurations. |
| 32 | `ps_scale` | [ps.ts:79](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/ps.ts#L79) | Scale Heroku app dynos. Adjust quantities, change sizes, view formation details, manage resources. |
| 33 | `ps_restart` | [ps.ts:104](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/ps.ts#L104) | Restart Heroku app processes. Restart specific dynos, process types, or all dynos. Reset dyno states selectively. |
| 34 | `list_private_spaces` | [spaces.ts:33](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/spaces.ts#L33) | Lists Heroku Private Spaces with CIDR blocks, regions, compliance and capacity details. JSON output supported. |
| 35 | `list_teams` | [teams.ts:39](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/teams.ts#L39) | Lists accessible Heroku Teams. Use for: viewing teams, checking membership, getting team metadata, and verifying access. JSON output available. |
| 36 | `deploy_one_off_dyno` | [deploy-to-heroku.ts:749](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/deploy-to-heroku.ts#L749) | see below (the description is the variable `execToolSchemaDescription`) |

### Parameters (verbatim)

#### `list_addons`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `all` | `boolean` | no | List all add-ons across accessible apps. Overrides app param, shows full status |
| `app` | `string` | no | Filter by app name. Shows add-ons and attachments. Uses Git remote default if omitted |

#### `get_addon_info`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `addon` | `string` | yes | Add-on identifier: UUID, name (postgresql-curved-12345), or attachment name (DATABASE) |
| `app` | `string` | no | App context for add-on lookup. Required for attachment names. Uses Git remote default |

#### `create_addon`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app for add-on. Must have write access. Region/space affects availability |
| `as` | `string` | no | Custom attachment name. Used for config vars prefix. Must be unique in app |
| `name` | `string` | no | Global add-on identifier. Must be unique across all Heroku add-ons |
| `serviceAndPlan` | `string` | yes | Format: service_slug:plan_slug (e.g., heroku-postgresql:essential-0) |

#### `list_addon_services`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `json` | `boolean` | no | JSON output with sharing options and app generation support. Default: basic text |

#### `list_addon_plans`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `service` | `string` | yes | Service slug (e.g., heroku-postgresql). Get from list_addon_services |
| `json` | `boolean` | no | JSON output with pricing, features, space compatibility. Default: text format |

#### `list_ai_available_models`

_No parameters._

#### `provision_ai_model`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name for AI model access provisioning |
| `modelName` | `string` | yes | Name of the AI model to provision access for. Valid model names can be found with tool "list_ai_available_models" |
| `as` | `string` | no | Alias for the model resource when attaching to the app. Randomly generated if not provided. |

#### `make_ai_inference`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | App name/ID (required for alias) |
| `modelResource` | `string` | yes | Model resource ID/alias (requires --app for alias) |
| `json` | `boolean` | no | Output as JSON |
| `output` | `string` | no | Output file path |

#### `list_apps`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `all` | `boolean` | no | Show owned apps and collaborator access. Default: owned only |
| `personal` | `boolean` | no | List personal account apps only, ignoring default team |
| `space` | `string` | no | Filter by private space name. Excludes team param |
| `team` | `string` | no | Filter by team name. Excludes space param |

#### `get_app_info`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name. Requires access permissions |
| `json` | `boolean` | no | JSON output with full metadata. Default: text format |

#### `create_app`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | no | App name. Auto-generated if omitted |
| `region` | `enum[us, eu]` | no | Region: us/eu. Default: us. Excludes space param |
| `space` | `string` | no | Private space name. Inherits region. Excludes region param |
| `team` | `string` | no | Team name for ownership |

#### `rename_app`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Current app name. Requires access |
| `newName` | `string` | yes | New unique app name |

#### `pg_psql`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `command` | `string` | no | SQL command. Single line. Ignored if file provided |
| `file` | `string` | no | SQL file path. Ignored if command provided |
| `credential` | `string` | no | credential to use |
| `app` | `string` | yes | app to run command against |
| `database` | `string` | no | Database identifier: config var, name, ID, alias. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_info`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: all databases |

#### `pg_ps`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `verbose` | `boolean` | no | Show query plan and memory usage |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_locks`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `truncate` | `boolean` | no | Truncate queries to 40 chars |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_outliers`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `num` | `number` | no | Number of queries to show. Default: 10 |
| `reset` | `boolean` | no | Reset pg_stat_statements stats |
| `truncate` | `boolean` | no | Truncate queries to 40 chars |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_credentials`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_kill`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `pid` | `number` | yes | Process ID to terminate |
| `force` | `boolean` | no | Force immediate termination |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_maintenance`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `pg_backups`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |

#### `pg_upgrade`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target app name |
| `version` | `string` | no | PostgreSQL version target |
| `confirm` | `string` | no | Confirmation for destructive operation |
| `database` | `string` | no | Database identifier. Format: APP_NAME::DB for other apps. Default: DATABASE_URL |

#### `deploy_to_heroku`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `name` | `string` | yes | App name for deployment. Creates new app if not exists. |
| `rootUri` | `string` | yes | Workspace root directory path. |
| `tarballUri` | `string` | no | URL of deployment tarball. Creates from rootUri if not provided. |
| `teamId` | `string` | no | Team ID for team deployments. |
| `spaceId` | `string` | no | Private space ID for space deployments. |
| `internalRouting` | `boolean` | no | Enable internal routing in private spaces. |
| `env` | `record` | no | Environment variables overriding app.json values |
| `appJson` | `string` | yes | App.json config for deployment. Must follow schema: ${JSON.stringify(appJsonSchema, null, 0)} |

#### `get_app_logs`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Heroku app name. Requires: permissions, Cedar-gen |
| `dynoName` | `string` | no | Format: web.1/worker.2. Excludes processType |
| `source` | `string` | no | app=application, heroku=platform. Default: all |
| `processType` | `string` | no | web\|worker. All instances. Excludes dynoName |

#### `maintenance_on`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target Heroku app name |

#### `maintenance_off`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Target Heroku app name |

#### `pipelines_create`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `name` | `string` | yes | Pipeline name |
| `stage` | `enum[development, staging, production]` | yes | Initial pipeline stage |
| `app` | `string` | no | App to add to pipeline |
| `team` | `string` | no | Team owning the pipeline |

#### `pipelines_promote`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | Source app for promotion |
| `to` | `string` | no | Target apps for promotion (comma-separated) |

#### `pipelines_list`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `json` | `boolean` | no | Enable JSON output |

#### `pipelines_info`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `pipeline` | `string` | yes | Target pipeline name |
| `json` | `boolean` | no | Enable JSON output |

#### `ps_list`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | App name to list processes for |
| `json` | `boolean` | no | Output process info in JSON format |

#### `ps_scale`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | yes | App name to scale |
| `dyno` | `string` | no | Dyno type and quantity (e.g., web=3:Standard-2X, worker+1). Omit to show current formation |

#### `ps_restart`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `app` | `string` | no | App name to restart processes for |

#### `list_private_spaces`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `json` | `boolean` | no | JSON output for detailed space metadata, text output if false/omitted |

#### `list_teams`

| Parameter | Type (zod) | Req. | Description |
|---|---|---|---|
| `json` | `boolean` | no | Output format control - true for detailed JSON with team metadata, false/omitted for simplified text |

#### `deploy_one_off_dyno` — description (verbatim, src/tools/deploy-to-heroku.ts:708)

```text
const execToolSchemaDescription = `
Run code/commands in Heroku one-off dyno with network and filesystem access.

Requirements:
- Show command output
- Use app_info for buildpack detection
- Support shell setup commands
- Use stdout/stderr

Features:
- Network/filesystem access
- Environment variables
- File operations
- Temp directory handling

Usage:
1. Use Heroku runtime
2. Proper syntax/imports
3. Organized code structure
4. Package management:
   - Define dependencies
   - Minimize external deps
   - Prefer native modules

Example package.json:
\`\`\`json
{
  "type": "module",
  "dependencies": {
    "axios": "^1.6.0"
  }
}
\`\`\`
`;
```

Parameters: `name` (string, 5–30 chars, "Target Heroku app name."), `command` (string, "Command to run in dyno."), `sources` (array of {`relativePath`, `contents`}, optional; the path is checked for safe characters, no `..` and no shell metacharacters), for the rest see the [code](https://github.com/heroku/heroku-mcp-server/blob/4afcbe1a042b78e81385280ac5adaeb0000dba6e/src/tools/deploy-to-heroku.ts#L680).
