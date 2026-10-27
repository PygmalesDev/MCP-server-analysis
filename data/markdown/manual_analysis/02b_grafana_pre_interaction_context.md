# Grafana MCP — Pre-Interaction Context (appendix)

Source: source code of [grafana/mcp-grafana](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/) at commit `e97cd4479eb40d25bc8d466db1651c29ce0c783e` (2026-10-23).

**How it was obtained.** Static parsing of the Go code with a script (without running the server). Tool names and descriptions, as well as parameter descriptions, are copied verbatim from the code (`MustTool(...)` lines and `jsonschema:"description=..."` tags). The exact JSON that the server returns for `tools/list` is generated at runtime by the `invopop/jsonschema` library; the parameter types below are Go types, not JSON types. For a 100% exact copy, the server has to be started and `tools/list` executed.

The column "Default" shows whether the tool is enabled in a standard start (flag `--enabled-tools`, [main.go:217](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/cmd/mcp-grafana/main.go#L217)).

A notation like `datasourceQuery...` in the permissions column is a variable from the code; `datasourceQuery` = `datasources:read`, `datasources:query` ([tools/rbac.go:10](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/rbac.go#L10)).

## 1. Server instructions (sent on `initialize`)

Assembled by the function `buildInstructions()` ([main.go:532](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/cmd/mcp-grafana/main.go#L532)) from the enabled categories. In a standard start the text is as follows (category order as in `toolEntries()`; texts from the dictionary `categoryDescription`):

```text
This server provides access to your Grafana instance and the surrounding ecosystem.

Available Capabilities:
- Search: Find dashboards, folders, and other Grafana resources.
- Datasources: List and fetch details for datasources.
- Incidents: Search, create, update, and resolve incidents in Grafana Incident.
- Prometheus: Run PromQL queries, retrieve metric metadata, and explore label names/values.
- Loki: Run LogQL queries, retrieve log metadata, and explore label names/values.
- Alerting: List and fetch alert rules and notification contact points.
- Dashboards: Search, retrieve, update, and create dashboards. Extract panel queries and datasource information.
- Folders: Manage dashboard folders.
- OnCall: View and manage on-call schedules, shifts, teams, and users.
- Asserts: Query and analyze assertion data.
- Pyroscope: Profile applications and fetch profiling data.
- Navigation: Generate deeplink URLs for Grafana resources like dashboards, panels, and Explore queries, with optional built-in shortening.
- Tempo: Search traces with TraceQL, compute trace-derived metrics, fetch and diff traces, and explore trace attributes.
- Annotations: Create and manage dashboard annotations.
- Rendering: Export dashboard panels or full dashboards as PNG images (requires Grafana Image Renderer plugin).
- Snapshots: List, get, create, and delete dashboard snapshots.
- Plugins: Check whether Grafana plugins are installed and fetch plugin details.
- API: Make authenticated HTTP requests to any Grafana API endpoint with optional jq-style response filtering.
- Config: Generate operator-facing configuration snippets (e.g. Alloy label-enforcement pipelines).
- Provisioning: List provisioning repositories (e.g. git-sync sources) to discover repository slugs for use with rendering tools.
- Docs: Search and retrieve Grafana product documentation (powered by grafana.com/llms-full.txt).
- User: Identify the current user/credential, its capabilities, and the organizations it can access.

Timestamp parameters without a timezone offset are interpreted as UTC. Include an offset like '-05:00' or use relative syntax like 'now-1h' to query in a different timezone.
```

## 2. Tools

| # | Tool | Category | Default | readOnly | destructive | File |
|---|---|---|---|---|---|---|
| 1 | `list_teams` | admin | no | true | false | [tools/admin.go:36](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L36) |
| 2 | `list_users_by_org` | admin | no | true | false | [tools/admin.go:103](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L103) |
| 3 | `list_all_roles` | admin | no | true | false | [tools/admin.go:135](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L135) |
| 4 | `get_role_details` | admin | no | true | false | [tools/admin.go:162](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L162) |
| 5 | `get_role_assignments` | admin | no | true | false | [tools/admin.go:189](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L189) |
| 6 | `list_user_roles` | admin | no | true | false | [tools/admin.go:217](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L217) |
| 7 | `list_team_roles` | admin | no | true | false | [tools/admin.go:245](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L245) |
| 8 | `get_resource_permissions` | admin | no | true | false | [tools/admin.go:273](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L273) |
| 9 | `get_resource_description` | admin | no | true | false | [tools/admin.go:303](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L303) |
| 10 | `agento11y_manage_conversations` | agento11y | no | true | false | [tools/agento11y.go:444](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L444) |
| 11 | `agento11y_manage_generations` | agento11y | no | true | false | [tools/agento11y.go:476](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L476) |
| 12 | `agento11y_manage_evaluators` | agento11y | no | true | false | [tools/agento11y.go:762](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L762) |
| 13 | `agento11y_manage_eval_rules` | agento11y | no | true | false | [tools/agento11y.go:774](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L774) |
| 14 | `agento11y_manage_eval_collections` | agento11y | no | true | false | [tools/agento11y.go:786](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L786) |
| 15 | `agento11y_manage_experiments` | agento11y | no | true | false | [tools/agento11y.go:798](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L798) |
| 16 | `agento11y_manage_test_suites` | agento11y | no | true | false | [tools/agento11y.go:810](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L810) |
| 17 | `agento11y_manage_agents` | agento11y | no | true | false | [tools/agento11y_agents.go:297](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y_agents.go#L297) |
| 18 | `alerting_rules_read` | alerting | yes | true | false | [tools/alerting.go:37](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting.go#L37) |
| 19 | `alerting_rules_write` | alerting | yes | false | true | [tools/alerting.go:51](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting.go#L51) |
| 20 | `alerting_manage_routing` | alerting | yes | true | false | [tools/alerting_routing.go:156](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_routing.go#L156) |
| 21 | `alerting_routing_write` | alerting | yes | false | false | [tools/alerting_routing.go:236](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_routing.go#L236) |
| 22 | `alerting_silences_read` | alerting | yes | true | false | [tools/alerting_silences.go:416](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_silences.go#L416) |
| 23 | `alerting_silences_write` | alerting | yes | false | true | [tools/alerting_silences.go:428](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_silences.go#L428) |
| 24 | `get_annotations` | annotations | yes | true | false | [tools/annotations.go:56](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L56) |
| 25 | `create_annotation` | annotations | yes | false | false | [tools/annotations.go:133](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L133) |
| 26 | `update_annotation` | annotations | yes | false | true | [tools/annotations.go:187](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L187) |
| 27 | `delete_annotation` | annotations | yes | false | true | [tools/annotations.go:228](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L228) |
| 28 | `get_annotation_tags` | annotations | yes | true | false | [tools/annotations.go:269](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L269) |
| 29 | `grafana_api_request` | api | yes | false | true | [tools/api.go:208](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/api.go#L208) |
| 30 | `get_assertions` | asserts | yes | true | false | [tools/asserts.go:143](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/asserts.go#L143) |
| 31 | `ask_assistant` | assistant | no | false | true | [tools/assistant.go:176](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/assistant.go#L176) |
| 32 | `query_cloud_logging` | cloudlogging | no | true | false | [tools/cloudlogging.go:370](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L370) |
| 33 | `list_cloud_logging_projects` | cloudlogging | no | true | false | [tools/cloudlogging.go:411](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L411) |
| 34 | `list_cloud_logging_buckets` | cloudlogging | no | true | false | [tools/cloudlogging.go:443](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L443) |
| 35 | `list_cloud_logging_views` | cloudlogging | no | true | false | [tools/cloudlogging.go:480](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L480) |
| 36 | `query_cloudwatch` | cloudwatch | no | true | false | [tools/cloudwatch.go:303](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L303) |
| 37 | `list_cloudwatch_namespaces` | cloudwatch | no | true | false | [tools/cloudwatch.go:419](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L419) |
| 38 | `list_cloudwatch_metrics` | cloudwatch | no | true | false | [tools/cloudwatch.go:482](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L482) |
| 39 | `list_cloudwatch_dimensions` | cloudwatch | no | true | false | [tools/cloudwatch.go:547](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L547) |
| 40 | `list_cloudwatch_dimension_values` | cloudwatch | no | true | false | [tools/cloudwatch.go:615](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L615) |
| 41 | `suggest_loki_alloy_label_config` | config | yes | true | false | [tools/config.go:115](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/config.go#L115) |
| 42 | `get_dashboard_by_uid` | dashboard | yes | true | false | [tools/dashboard.go:906](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L906) |
| 43 | `update_dashboard` | dashboard | yes | false | true | [tools/dashboard.go:921](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L921) |
| 44 | `get_dashboard_panel_queries` | dashboard | yes | true | false | [tools/dashboard.go:1003](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L1003) |
| 45 | `get_dashboard_property` | dashboard | yes | true | false | [tools/dashboard.go:1056](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L1056) |
| 46 | `get_dashboard_summary` | dashboard | yes | true | false | [tools/dashboard.go:1172](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L1172) |
| 47 | `list_dashboard_versions` | dashboard | yes | true | false | [tools/dashboard_versions.go:77](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard_versions.go#L77) |
| 48 | `list_datasources` | datasource | yes | true | false | [tools/datasources.go:440](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L440) |
| 49 | `create_datasource` | datasource | yes | false | false | [tools/datasources.go:452](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L452) |
| 50 | `update_datasource` | datasource | yes | false | true | [tools/datasources.go:464](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L464) |
| 51 | `get_datasource` | datasource | yes | true | false | [tools/datasources.go:549](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L549) |
| 52 | `check_datasources_health` | datasource | yes | true | false | [tools/datasources.go:909](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L909) |
| 53 | `search_docs` | docs | yes | true | false | [tools/docs.go:162](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/docs.go#L162) |
| 54 | `get_doc` | docs | yes | true | false | [tools/docs.go:232](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/docs.go#L232) |
| 55 | `query_elasticsearch` | elasticsearch | no | true | false | [tools/elasticsearch.go:51](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/elasticsearch.go#L51) |
| 56 | `get_query_examples` | examples | no | true | false | [tools/examples.go:292](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/examples.go#L292) |
| 57 | `create_folder` | folder | yes | false | false | [tools/folder.go:43](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/folder.go#L43) |
| 58 | `query_graphite` | graphite | no | true | false | [tools/graphite.go:243](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L243) |
| 59 | `list_graphite_metrics` | graphite | no | true | false | [tools/graphite.go:321](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L321) |
| 60 | `list_graphite_tags` | graphite | no | true | false | [tools/graphite.go:371](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L371) |
| 61 | `query_graphite_density` | graphite | no | true | false | [tools/graphite.go:513](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L513) |
| 62 | `list_incidents` | incident | yes | true | false | [tools/incident.go:150](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L150) |
| 63 | `create_incident` | incident | yes | false | false | [tools/incident.go:215](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L215) |
| 64 | `add_activity_to_incident` | incident | yes | false | false | [tools/incident.go:247](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L247) |
| 65 | `get_incident` | incident | yes | true | false | [tools/incident.go:287](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L287) |
| 66 | `update_incident` | incident | yes | false | false | [tools/incident.go:379](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L379) |
| 67 | `list_incident_custom_fields` | incident | yes | true | false | [tools/incident_custom_fields.go:92](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident_custom_fields.go#L92) |
| 68 | `query_influxdb` | influxdb | no | false | true | [tools/influxdb.go:208](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/influxdb.go#L208) |
| 69 | `list_loki_label_names` | loki | yes | true | false | [tools/loki.go:249](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L249) |
| 70 | `list_loki_label_values` | loki | yes | true | false | [tools/loki.go:300](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L300) |
| 71 | `query_loki_logs` | loki | yes | true | false | [tools/loki.go:963](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L963) |
| 72 | `query_loki_stats` | loki | yes | true | false | [tools/loki.go:1082](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L1082) |
| 73 | `query_loki_patterns` | loki | yes | true | false | [tools/loki.go:1134](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L1134) |
| 74 | `analyze_loki_labels` | loki | yes | true | false | [tools/loki_label_analyzer.go:1006](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki_label_analyzer.go#L1006) |
| 75 | `generate_deeplink` | navigation | yes | false | false | [tools/navigation.go:314](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/navigation.go#L314) |
| 76 | `list_oncall_schedules` | oncall | yes | true | false | [tools/oncall.go:200](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L200) |
| 77 | `get_oncall_shift` | oncall | yes | true | false | [tools/oncall.go:253](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L253) |
| 78 | `get_current_oncall_users` | oncall | yes | true | false | [tools/oncall.go:324](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L324) |
| 79 | `list_oncall_teams` | oncall | yes | true | false | [tools/oncall.go:380](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L380) |
| 80 | `list_oncall_users` | oncall | yes | true | false | [tools/oncall.go:453](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L453) |
| 81 | `list_alert_groups` | oncall | yes | true | false | [tools/oncall.go:545](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L545) |
| 82 | `get_alert_group` | oncall | yes | true | false | [tools/oncall.go:619](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L619) |
| 83 | `update_alert_group` | oncall | yes | false | true | [tools/oncall.go:727](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L727) |
| 84 | `get_plugin` | plugin | yes | true | false | [tools/plugins.go:124](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/plugins.go#L124) |
| 85 | `install_plugin` | plugin | yes | false | false | [tools/plugins.go:257](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/plugins.go#L257) |
| 86 | `search_plugin_information` | plugin | yes | true | false | [tools/plugins.go:426](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/plugins.go#L426) |
| 87 | `list_prometheus_metric_metadata` | prometheus | yes | true | false | [tools/prometheus.go:58](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L58) |
| 88 | `query_prometheus` | prometheus | yes | true | false | [tools/prometheus.go:290](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L290) |
| 89 | `list_prometheus_metric_names` | prometheus | yes | true | false | [tools/prometheus.go:367](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L367) |
| 90 | `list_prometheus_label_names` | prometheus | yes | true | false | [tools/prometheus.go:517](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L517) |
| 91 | `list_prometheus_label_values` | prometheus | yes | true | false | [tools/prometheus.go:574](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L574) |
| 92 | `query_prometheus_histogram` | prometheus | yes | true | false | [tools/prometheus.go:727](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L727) |
| 93 | `list_provisioning_repositories` | provisioning | yes | true | false | [tools/provisioning.go:159](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/provisioning.go#L159) |
| 94 | `validate_provisioning_file` | provisioning | yes | true | false | [tools/provisioning.go:384](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/provisioning.go#L384) |
| 95 | `list_pyroscope_label_names` | pyroscope | yes | true | false | [tools/pyroscope.go:44](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L44) |
| 96 | `list_pyroscope_label_values` | pyroscope | yes | true | false | [tools/pyroscope.go:106](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L106) |
| 97 | `list_pyroscope_profile_types` | pyroscope | yes | true | false | [tools/pyroscope.go:184](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L184) |
| 98 | `query_pyroscope` | pyroscope | yes | true | false | [tools/pyroscope.go:640](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L640) |
| 99 | `query_quickwit` | quickwit | no | true | false | [tools/quickwit.go:257](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/quickwit.go#L257) |
| 100 | `get_panel_image` | rendering | yes | true | false | [tools/rendering.go:507](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/rendering.go#L507) |
| 101 | `run_panel_query` | runpanelquery | no | true | false | [tools/run_panel_query.go:1197](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/run_panel_query.go#L1197) |
| 102 | `search_dashboards` | search | yes | true | false | [tools/search.go:115](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/search.go#L115) |
| 103 | `search_folders` | search | yes | true | false | [tools/search.go:148](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/search.go#L148) |
| 104 | `list_snapshots` | snapshot | yes | true | false | [tools/snapshot.go:226](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L226) |
| 105 | `get_snapshot` | snapshot | yes | true | false | [tools/snapshot.go:238](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L238) |
| 106 | `create_snapshot` | snapshot | yes | false | false | [tools/snapshot.go:250](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L250) |
| 107 | `delete_snapshot` | snapshot | yes | false | true | [tools/snapshot.go:262](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L262) |
| 108 | `query_sql` | sql | no | false | true | [tools/sql_tools.go:265](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L265) |
| 109 | `list_sql_databases` | sql | no | true | false | [tools/sql_tools.go:283](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L283) |
| 110 | `list_sql_tables` | sql | no | true | false | [tools/sql_tools.go:295](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L295) |
| 111 | `describe_sql_table` | sql | no | true | false | [tools/sql_tools.go:307](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L307) |
| 112 | `search_tempo_traces` | tempo | yes | true | false | [tools/tempo.go:699](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L699) |
| 113 | `query_tempo_metrics` | tempo | yes | true | false | [tools/tempo.go:711](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L711) |
| 114 | `get_tempo_trace` | tempo | yes | true | false | [tools/tempo.go:723](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L723) |
| 115 | `diff_tempo_traces` | tempo | yes | true | false | [tools/tempo.go:736](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L736) |
| 116 | `list_tempo_attribute_names` | tempo | yes | true | false | [tools/tempo.go:748](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L748) |
| 117 | `list_tempo_attribute_values` | tempo | yes | true | false | [tools/tempo.go:760](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L760) |
| 118 | `get_tempo_traceql_docs` | tempo | yes | true | false | [tools/tempo.go:772](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L772) |
| 119 | `user_info` | user | yes | true | false | [tools/user.go:45](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/user.go#L45) |

### Verbatim descriptions and parameters

If a tool has several variants (e.g. a separate variant for "read-only" mode), all of them are given.

#### `list_teams`

Category: `admin` · Code: [tools/admin.go:36](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L36) · Annotations: title="List teams", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `teams:read`

Description (verbatim):

```text
Search for Grafana teams by a query string. Returns a list of matching teams with details like name, ID, and URL.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | no |  |  | The query to search for teams. Can be left empty to fetch all teams |

#### `list_users_by_org`

Category: `admin` · Code: [tools/admin.go:103](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L103) · Annotations: title="List users by org", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `org.users:read`

Description (verbatim):

```text
List users in the Grafana organization, optionally filtered by a search query. Results are paginated; the response includes totalCount, page and perPage alongside organization users with details like userid, email, role etc.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | no |  |  | Optional search string matched against login, email and name |
| `limit` | `int` | no | 100 |  | Maximum number of users to return (max 1000) |
| `page` | `int` | no | 1 |  | Page number for pagination (1-indexed) |

#### `list_all_roles`

Category: `admin` · Code: [tools/admin.go:135](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L135) · Annotations: title="List all roles", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `roles:read`

Description (verbatim):

```text
List all roles in Grafana. Optionally filter to show only roles that can be delegated by the current user. Returns role details including UID, name, permissions, and metadata.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `delegatableOnly` | `bool` | no |  |  | Optional: If set true only return roles that can be delegated by current user |

#### `get_role_details`

Category: `admin` · Code: [tools/admin.go:162](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L162) · Annotations: title="Get role details", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `roles:read`

Description (verbatim):

```text
Get detailed information about a specific Grafana role by its UID, including permissions, metadata, and configuration.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `roleUID` | `string` | yes |  |  | Role UID to retrieve |

#### `get_role_assignments`

Category: `admin` · Code: [tools/admin.go:189](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L189) · Annotations: title="Get role assignments", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `roles:read`, `users.roles:read`, `teams.roles:read`

Description (verbatim):

```text
List all assignments for a specific role, showing which users, teams, and service accounts have been assigned this role.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `roleUID` | `string` | yes |  |  | Role UID to retrieve |

#### `list_user_roles`

Category: `admin` · Code: [tools/admin.go:217](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L217) · Annotations: title="List user roles", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `users.roles:read`

Description (verbatim):

```text
List all roles assigned to one or more users. Returns a map of user IDs to their assigned roles, excluding built-in roles and team-inherited roles.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `userIds` | `[]int64` | yes |  |  | User ID(s) to get roles for. Can be a single user or multiple users. |

#### `list_team_roles`

Category: `admin` · Code: [tools/admin.go:245](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L245) · Annotations: title="List team roles", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `teams.roles:read`

Description (verbatim):

```text
List all roles assigned to one or more teams. Returns a map of team IDs to their assigned roles.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `teamIds` | `[]int64` | yes |  |  | Team ID(s) to get roles for. Can be a single team or multiple teams. |

#### `get_resource_permissions`

Category: `admin` · Code: [tools/admin.go:273](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L273) · Annotations: title="Get resource permissions", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `resourcePermissionsRead...`

Description (verbatim):

```text
List all permissions set on a specific Grafana resource (e.g., dashboard, datasource, folder) by its type and ID.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `resource` | `string` | yes |  |  | Resource type (e.g. 'dashboards' 'datasources' 'folders') |
| `resourceId` | `string` | yes |  |  | Unique identifier of the resource (UID for dashboards/datasources/folders) |

#### `get_resource_description`

Category: `admin` · Code: [tools/admin.go:303](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/admin.go#L303) · Annotations: title="Get resource description", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `resourcePermissionsRead...`

Description (verbatim):

```text
List available permissions and assignment capabilities for a Grafana resource type.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `resourceType` | `string` | yes |  | dashboards, datasources, folders, teams, users, serviceaccounts | Type of Grafana resource to get description for |

#### `agento11y_manage_conversations`

Category: `agento11y` · Code: [tools/agento11y.go:444](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L444) · Annotations: title="Manage Agent Observability conversations", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
List, search, and fetch LLM conversations from Grafana Agent Observability (the grafana-agento11y-app plugin).

Operations:
- 'list': recent conversations (lightweight; id, title, generation count, timestamps), paginated via limit and cursor
- 'search': search conversations by filter expression and time range; results include models, agents, error counts, rating and eval summaries, and trace IDs
- 'get': one conversation by ID with all its generations, including full prompts and outputs (can be large)

Filter syntax for 'search': key operator value, with the value in double quotes; multiple filters are separated by spaces and combined with AND.
Filter keys (trace): model, provider, agent, agent.version, status, error.type, error.category, duration, tool.name, operation, namespace, cluster, service
Filter keys (metadata): generation_count, eval.passed, eval.evaluator_id, eval.score_key, eval.score
Operators: =, !=, >, <, >=, <=, =~ (regex)
Example: status = "error" agent = "claude-code"

Pagination: when a response has next_cursor, fetch the next page by calling the same operation again with cursor set to next_cursor. For 'search', also repeat the same filters, start_time, and end_time as the first call, using absolute RFC3339 times; relative ranges like now-24h shift between calls and the cursor will be rejected.

When to use:
- Debugging an AI application: find failing or low-rated conversations, then inspect their generations
- Reviewing evaluation results and user ratings across conversations

When NOT to use:
- Fetching a single generation or its evaluation scores
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `operation` | `string` | yes |  | list, search, get | The operation to perform: 'list' for recent conversations, 'search' to filter conversations by expression and time range, 'get' to fetch one conversation with all its generations by ID |
| `conversation_id` | `string` | no |  |  | The conversation ID (required for 'get' operation) |
| `filters` | `string` | no |  |  | Filter expression (for 'search' operation). Format: key operator value with the value in double quotes, multiple filters separated by spaces. See the tool description for keys and operators. |
| `start_time` | `string` | no |  |  | Start of the search time range in RFC3339 or relative format (e.g. now-6h). Defaults to now-24h (for 'search' operation) |
| `end_time` | `string` | no |  |  | End of the search time range in RFC3339 or relative format (e.g. now). Defaults to now (for 'search' operation) |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50) (for 'list' and 'search' operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response (for 'list' and 'search' operations). To fetch the next page set this to next_cursor. For 'search' also resend the same filters and start_time/end_time from the first call and use absolute RFC3339 times; relative ranges like now-24h invalidate the cursor. |

#### `agento11y_manage_generations`

Category: `agento11y` · Code: [tools/agento11y.go:476](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L476) · Annotations: title="Manage Agent Observability generations", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
Fetch a single LLM generation and its evaluation scores from Grafana Agent Observability (the grafana-agento11y-app plugin).

Operations:
- 'get': full generation detail by ID, including prompt, output, model, and usage (can be large)
- 'scores': evaluation scores for a generation (evaluator, score key, score type, value, passed, explanation)

When to use:
- Drilling into one generation of a conversation
- Checking why an evaluation passed or failed for a specific generation

When NOT to use:
- Searching or listing conversations
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `operation` | `string` | yes |  | get, scores | The operation to perform: 'get' for the full generation detail, 'scores' for the evaluation scores of the generation |
| `generation_id` | `string` | yes |  |  | The generation ID |
| `limit` | `int` | no |  |  | Maximum number of scores per page (default 50) (for 'scores' operation) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response (for 'scores' operation) |

#### `agento11y_manage_evaluators` (variant 1 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:762](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L762) · Annotations: title="Manage Agent Observability evaluators", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yEvaluatorsDescription(true)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `scope` | `string` | no |  | global, tenant | Template scope filter: 'global' for built-in templates, 'tenant' for templates created in this tenant (for 'list_templates') |
| `provider` | `string` | no |  |  | Judge provider ID to filter models by, e.g. 'openai' (for 'list_judge_models') |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the paginated list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor (for the paginated list operations) |
| `operation` | `string` | yes |  | list_evaluators, get_evaluator, list_templates, get_template, list_template_versions, list_judge_providers, list_judge_models | The operation to perform: 'list_evaluators' for the evaluators in this tenant, 'get_evaluator' for one evaluator's kind/config/output_keys, 'list_templates' for evaluator templates, 'get_template' for one template with its config and versions, 'list_template_versions' for a template's version history, 'list_judge_providers' for configured judge providers, 'list_judge_models' for the judge models of a provider |
| `evaluator_id` | `string` | no |  |  | Evaluator ID (required for 'get_evaluator') |
| `template_id` | `string` | no |  |  | Template ID (required for 'get_template' and 'list_template_versions') |

#### `agento11y_manage_eval_rules` (variant 1 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:774](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L774) · Annotations: title="Manage Agent Observability eval rules and guards", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yEvalRulesDescription(true)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for 'list_rules' and 'list_guards') |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor (for 'list_rules' and 'list_guards') |
| `operation` | `string` | yes |  | list_rules, get_rule, list_guards, get_guard | The operation to perform: 'list_rules' for the asynchronous eval rules in this tenant, 'get_rule' for one eval rule, 'list_guards' for the inline guards (hook rules), 'get_guard' for one guard |
| `rule_id` | `string` | no |  |  | Eval rule ID (for 'get_rule') or guard ID (for 'get_guard'). Required for both. |

#### `agento11y_manage_eval_collections` (variant 1 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:786](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L786) · Annotations: title="Manage Agent Observability saved conversations and collections", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yEvalCollectionsDescription(true)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `source` | `string` | no |  | telemetry, manual | Saved conversation source filter: 'telemetry' for bookmarked production conversations, 'manual' for hand-built ones (for 'list_saved_conversations') |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the paginated list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly and never constructed or incremented. A cursor belongs to the operation and filters that produced it: 'list_saved_conversations' returns an opaque numeric value while 'list_collections' and 'list_collection_members' return the last row ID, so they are not interchangeable. |
| `operation` | `string` | yes |  | list_saved_conversations, get_saved_conversation, list_collections_for_saved_conversation, list_collections, get_collection, list_collection_members | The operation to perform: 'list_saved_conversations' for the bookmarked conversations in this tenant, 'get_saved_conversation' for one bookmark, 'list_collections_for_saved_conversation' for the collections one bookmark belongs to, 'list_collections' for the collections in this tenant, 'get_collection' for one collection, 'list_collection_members' for the saved conversations in a collection |
| `saved_id` | `string` | no |  |  | Saved conversation ID (required for 'get_saved_conversation' and 'list_collections_for_saved_conversation') |
| `collection_id` | `string` | no |  |  | Collection ID (required for 'get_collection' and 'list_collection_members') |

#### `agento11y_manage_experiments` (variant 1 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:798](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L798) · Annotations: title="Manage Agent Observability experiments", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yExperimentsDescription(true)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `suite_id` | `string` | no |  |  | Test suite ID filter (for 'list') |
| `status` | `string` | no |  | running, completed, failed, canceled | Experiment status filter (for 'list'). A finished run is 'completed'; there is no 'succeeded' status. |
| `source` | `string` | no |  | collection, external | Experiment origin filter: 'collection' for runs built from a saved collection, 'external' for runs reported by an SDK runner (for 'list' and 'list_facets') |
| `created_by` | `string` | no |  |  | Owner filter, matched against the values 'list_facets' reports under owners (for 'list') |
| `tag` | `[]string` | no |  |  | Experiment tag filter (for 'list'). Several tags match an experiment carrying any of them, not all of them. |
| `from` | `string` | no |  |  | Start of the created_at window in RFC3339 or relative format (e.g. now-7d), for 'list' and 'list_facets' |
| `to` | `string` | no |  |  | End of the created_at window in RFC3339 or relative format (e.g. now), for 'list' and 'list_facets' |
| `completed_from` | `string` | no |  |  | Start of the completed_at window in RFC3339 or relative format (for 'list'). 'from' and 'to' filter created_at; this pair filters completed_at instead, so it drops runs that have not finished. |
| `completed_to` | `string` | no |  |  | End of the completed_at window in RFC3339 or relative format (for 'list') |
| `order` | `string` | no |  | created_at_desc, completed_at_desc | Sort order for 'list', newest first either way. Defaults to 'created_at_desc'. 'completed_at_desc' returns a single page and cannot be combined with a cursor. |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the paginated list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly and never constructed or incremented. Repeat the same filters as the first call, using absolute RFC3339 times. |
| `row_limit` | `int` | no |  |  | Maximum number of test case rows 'get_report' returns (default 50, max 500). The report route is not paginated, so this trims the returned rows and sets rows_truncated; it does not reduce what the plugin sends. |
| `operation` | `string` | yes |  | list, get, get_report, list_trials, list_scores, get_trial, list_trial_scores, list_trial_artifacts, list_facets | The operation to perform: 'list' for the experiments in this tenant, 'get' for one experiment with its headline result, 'get_report' for the per-test-case breakdown, 'list_trials' for one experiment's trials page by page, 'list_scores' for every score in one experiment, 'get_trial' for one trial in full, 'list_trial_scores' for one trial's scores with their explanations, 'list_trial_artifacts' for one trial's artifact metadata, 'list_facets' for the distinct suites, owners, and tags to filter by |
| `experiment_id` | `string` | no |  |  | Experiment ID from 'list' (required for 'get', 'get_report', 'list_trials', and 'list_scores') |
| `trial_id` | `string` | no |  |  | Trial ID from 'list_trials' or 'get_report' (required for 'get_trial', 'list_trial_scores', and 'list_trial_artifacts') |

#### `agento11y_manage_test_suites` (variant 1 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:810](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L810) · Annotations: title="Manage Agent Observability test suites", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yTestSuitesDescription(true)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly and never constructed or incremented |
| `operation` | `string` | yes |  | list_suites, get_suite, list_test_cases, get_test_case | The operation to perform: 'list_suites' for the test suites in this tenant, 'get_suite' for one suite with its full version history, 'list_test_cases' for the cases of one suite version page by page, 'get_test_case' for one case in full |
| `suite_id` | `string` | no |  |  | Test suite ID from 'list_suites' (required for 'get_suite', 'list_test_cases', and 'get_test_case') |
| `version` | `string` | no |  |  | Suite version such as 'v3', taken from the versions list of 'get_suite' (required for 'list_test_cases' and 'get_test_case'). There is no operation for reading a version on its own. |
| `test_case_id` | `string` | no |  |  | Test case ID from 'list_test_cases' (required for 'get_test_case') |

#### `agento11y_manage_evaluators` (variant 2 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:822](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L822) · Annotations: title="Manage Agent Observability evaluators", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yWrite...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yEvaluatorsDescription(false)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `scope` | `string` | no |  | global, tenant | Template scope filter: 'global' for built-in templates, 'tenant' for templates created in this tenant (for 'list_templates') |
| `provider` | `string` | no |  |  | Judge provider ID to filter models by, e.g. 'openai' (for 'list_judge_models') |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the paginated list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor (for the paginated list operations) |
| `operation` | `string` | yes |  | list_evaluators, get_evaluator, list_templates, get_template, list_template_versions, list_judge_providers, list_judge_models, upsert_evaluator, delete_evaluator, fork_template, test_evaluator | The operation to perform. Reads: 'list_evaluators', 'get_evaluator', 'list_templates', 'get_template', 'list_template_versions', 'list_judge_providers', 'list_judge_models'. Writes: 'upsert_evaluator' (create or update from 'definition'), 'delete_evaluator', 'fork_template' (derive an evaluator from a template), 'test_evaluator' (score one generation with an inline definition without storing it) |
| `evaluator_id` | `string` | no |  |  | Evaluator ID (required for 'get_evaluator' and 'delete_evaluator'). For 'upsert_evaluator' and 'fork_template' the evaluator ID belongs in 'definition' instead, because the API reads it from the request body. |
| `template_id` | `string` | no |  |  | Template ID (required for 'get_template', 'list_template_versions', and 'fork_template') |
| `definition` | `map[string]any` | no |  |  | Request body for 'upsert_evaluator', 'fork_template', and 'test_evaluator'. For 'upsert_evaluator': evaluator_id (string, required, only letters/digits/underscore/dot - hyphens are rejected), version (string, required - re-using an existing version returns HTTP 409, so bump it to change an evaluator), kind (llm_judge\|json_schema\|regex\|heuristic), description (string), config (object, shape depends on kind), output_keys (array of {key, type, description, unit, pass_threshold, enum, min, max, pass_match, pass_value}). The evaluator ID lives in this body, not in a URL or the evaluator_id parameter. For 'fork_template': evaluator_id (required) plus optional version (which template version to fork, defaults to the template's latest), config, and output_keys overrides. For 'test_evaluator': kind, config, and output_keys of the evaluator to try - the API rejects evaluator_id and version here, and nothing is persisted. |
| `generation_id` | `string` | no |  |  | Generation to score (required for 'test_evaluator'). |

#### `agento11y_manage_eval_rules` (variant 2 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:833](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L833) · Annotations: title="Manage Agent Observability eval rules and guards", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yWrite...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yEvalRulesDescription(false)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for 'list_rules' and 'list_guards') |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor (for 'list_rules' and 'list_guards') |
| `operation` | `string` | yes |  | list_rules, get_rule, list_guards, get_guard, create_rule, update_rule, delete_rule, preview_rule, create_guard, update_guard, delete_guard | The operation to perform. Reads: 'list_rules', 'get_rule', 'list_guards', 'get_guard'. Writes: 'create_rule', 'update_rule' (PATCH, partial), 'delete_rule', 'preview_rule' (dry-run a selector and match against recent traffic, stores nothing), 'create_guard', 'update_guard' (PUT, full replace), 'delete_guard' |
| `rule_id` | `string` | no |  |  | Eval rule ID (for the '_rule' operations) or guard ID (for the '_guard' operations). Required for 'get_rule', 'update_rule', 'delete_rule', 'get_guard', 'update_guard', and 'delete_guard'; for 'create_rule', 'create_guard', and 'preview_rule' the ID comes from 'definition'. |
| `definition` | `map[string]any` | no |  |  | Request body for the create/update/preview operations. Eval rules ('create_rule', 'update_rule'): rule_id (string, required on create, only letters/digits/underscore/dot), enabled (bool), selector (user_visible_turn\|all_assistant_generations\|tool_call_steps\|errored_generations\|conversation), match (object of string arrays, e.g. {\"agent_name\": [\"my-agent\"]}), sample_rate (0-1), evaluator_ids (array, the evaluators must already exist), alert_rule_uids (array), min_idle_seconds (int, required when selector is 'conversation': the idle period after which a conversation counts as finished; with that selector sample_rate applies per conversation, not per generation). 'update_rule' is a PATCH: send only the fields to change and do NOT include rule_id, which the API rejects as an unknown field - it is taken from the rule_id parameter. 'preview_rule': selector, match, sample_rate, and optionally rule_id. Guards ('create_guard', 'update_guard'): rule_id (required on create; on update it must match the rule_id parameter), enabled (bool), phase (preflight\|postflight, default preflight), priority (int, lower runs first), selector (as above, plus 'all'), match (as above), action_on_fail (warn\|deny - start with warn, which records the outcome without blocking the request, and promote to deny only after watching the false-positive rate), short_circuit (bool), and exactly ONE decision shape: evaluator_ids (an evaluator decides), redact ({patterns: [{id, regex}]} - each entry is exactly id and regex, a 'replacement' key returns 400, and the placeholder is derived from id) or tool_filter ({blocked_names: [glob]}). 'update_guard' is a PUT full replace: fields you omit reset to server defaults, so send a complete definition (normally a 'get_guard' result with your edits). |

#### `agento11y_manage_eval_collections` (variant 2 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:844](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L844) · Annotations: title="Manage Agent Observability saved conversations and collections", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yWrite...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yEvalCollectionsDescription(false)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `source` | `string` | no |  | telemetry, manual | Saved conversation source filter: 'telemetry' for bookmarked production conversations, 'manual' for hand-built ones (for 'list_saved_conversations') |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the paginated list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly and never constructed or incremented. A cursor belongs to the operation and filters that produced it: 'list_saved_conversations' returns an opaque numeric value while 'list_collections' and 'list_collection_members' return the last row ID, so they are not interchangeable. |
| `operation` | `string` | yes |  | list_saved_conversations, get_saved_conversation, list_collections_for_saved_conversation, list_collections, get_collection, list_collection_members, save_conversation, delete_saved_conversation, create_collection, update_collection, delete_collection, add_collection_members, remove_collection_member | The operation to perform. Reads: 'list_saved_conversations', 'get_saved_conversation', 'list_collections_for_saved_conversation', 'list_collections', 'get_collection', 'list_collection_members'. Writes: 'save_conversation' (bookmark a conversation), 'delete_saved_conversation', 'create_collection', 'update_collection' (PATCH, partial), 'delete_collection', 'add_collection_members', 'remove_collection_member' |
| `saved_id` | `string` | no |  |  | Saved conversation ID. Required for 'get_saved_conversation', 'list_collections_for_saved_conversation', 'delete_saved_conversation', and 'remove_collection_member'. Optional for 'save_conversation', which derives 'saved-<conversation_id>' when it is omitted. Only letters, digits, '_', '.', ':', and '-' are accepted. |
| `collection_id` | `string` | no |  |  | Collection ID. Required for 'get_collection', 'list_collection_members', 'update_collection', 'delete_collection', 'add_collection_members', and 'remove_collection_member'. Rejected by 'create_collection' (the API assigns a UUID) and by 'save_conversation' (bookmarking cannot also add to a collection). |
| `conversation_id` | `string` | no |  |  | Conversation to bookmark (required for 'save_conversation'). |
| `name` | `string` | no |  |  | Human-readable name. Required for 'save_conversation' and 'create_collection'; optional for 'update_collection', where an omitted name is left unchanged and a blank one is rejected. |
| `description` | `*string` | no |  |  | Collection description (for 'create_collection' and 'update_collection'). On 'update_collection' an omitted description is left unchanged and an explicitly empty string clears it. |
| `tags` | `map[string]string` | no |  |  | Optional string tags to store on a bookmark (for 'save_conversation') |
| `saved_ids` | `[]string` | no |  |  | Saved conversation IDs to add to a collection (required, non-empty, for 'add_collection_members'; rejected by 'create_collection', which always creates an empty collection). Every ID must already be a saved conversation; bookmark it with 'save_conversation' first. Re-adding a member is a no-op. |

#### `agento11y_manage_experiments` (variant 2 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:855](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L855) · Annotations: title="Manage Agent Observability experiments", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yWrite...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yExperimentsDescription(false)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `suite_id` | `string` | no |  |  | Test suite ID filter (for 'list') |
| `status` | `string` | no |  | running, completed, failed, canceled | Experiment status filter (for 'list'). A finished run is 'completed'; there is no 'succeeded' status. |
| `source` | `string` | no |  | collection, external | Experiment origin filter: 'collection' for runs built from a saved collection, 'external' for runs reported by an SDK runner (for 'list' and 'list_facets') |
| `created_by` | `string` | no |  |  | Owner filter, matched against the values 'list_facets' reports under owners (for 'list') |
| `tag` | `[]string` | no |  |  | Experiment tag filter (for 'list'). Several tags match an experiment carrying any of them, not all of them. |
| `from` | `string` | no |  |  | Start of the created_at window in RFC3339 or relative format (e.g. now-7d), for 'list' and 'list_facets' |
| `to` | `string` | no |  |  | End of the created_at window in RFC3339 or relative format (e.g. now), for 'list' and 'list_facets' |
| `completed_from` | `string` | no |  |  | Start of the completed_at window in RFC3339 or relative format (for 'list'). 'from' and 'to' filter created_at; this pair filters completed_at instead, so it drops runs that have not finished. |
| `completed_to` | `string` | no |  |  | End of the completed_at window in RFC3339 or relative format (for 'list') |
| `order` | `string` | no |  | created_at_desc, completed_at_desc | Sort order for 'list', newest first either way. Defaults to 'created_at_desc'. 'completed_at_desc' returns a single page and cannot be combined with a cursor. |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the paginated list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly and never constructed or incremented. Repeat the same filters as the first call, using absolute RFC3339 times. |
| `row_limit` | `int` | no |  |  | Maximum number of test case rows 'get_report' returns (default 50, max 500). The report route is not paginated, so this trims the returned rows and sets rows_truncated; it does not reduce what the plugin sends. |
| `operation` | `string` | yes |  | list, get, get_report, list_trials, list_scores, get_trial, list_trial_scores, list_trial_artifacts, list_facets, update, cancel | The operation to perform. Reads: 'list', 'get', 'get_report', 'list_trials', 'list_scores', 'get_trial', 'list_trial_scores', 'list_trial_artifacts', 'list_facets'. Writes: 'update' (PATCH the name, description, tags, or metadata of an experiment), 'cancel' (stop a running experiment) |
| `experiment_id` | `string` | no |  |  | Experiment ID from 'list'. Required for 'get', 'get_report', 'list_trials', 'list_scores', 'update', and 'cancel'. |
| `trial_id` | `string` | no |  |  | Trial ID from 'list_trials' or 'get_report' (required for 'get_trial', 'list_trial_scores', and 'list_trial_artifacts') |
| `name` | `*string` | no |  |  | New experiment name (for 'update'). An omitted field is left unchanged, and a blank name is rejected. A finished experiment accepts only description and tags, so renaming one returns 409. |
| `description` | `*string` | no |  |  | New experiment description (for 'update'). An omitted field is left unchanged and an explicitly empty string clears it. |
| `tags` | `*[]string` | no |  |  | Replacement tag list for 'update'. It overwrites the whole list rather than adding to it, so run 'get' first and send the existing tags plus the new ones; an explicitly empty array clears them. The tag filter for 'list' is the separate 'tag' parameter. |
| `metadata` | `map[string]any` | no |  |  | Replacement metadata object (for 'update'). A finished experiment rejects it with 409. |

#### `agento11y_manage_test_suites` (variant 2 of 2)

Category: `agento11y` · Code: [tools/agento11y.go:866](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y.go#L866) · Annotations: title="Manage Agent Observability test suites", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yWrite...`

Description (verbatim):

```text
⟨generated in code: manageAgento11yTestSuitesDescription(false)⟩
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, max 500) (for the list operations) |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly and never constructed or incremented |
| `operation` | `string` | yes |  | list_suites, get_suite, list_test_cases, get_test_case, create_suite, update_suite, create_draft_version, publish_version, upsert_test_case, delete_test_case | The operation to perform. Reads: 'list_suites', 'get_suite', 'list_test_cases', 'get_test_case'. Writes: 'create_suite', 'update_suite' (PATCH the name, description, or tags), 'create_draft_version' (open an editable version), 'publish_version' (freeze it), 'upsert_test_case' (write a whole case into a draft), 'delete_test_case' |
| `suite_id` | `string` | no |  |  | Test suite ID from 'list_suites'. Required for every operation except 'list_suites', which takes none, and 'create_suite', where it is an optional caller-chosen ID that must not already exist. |
| `version` | `string` | no |  |  | Suite version such as 'v3', taken from the versions list of 'get_suite'. Required for 'publish_version', 'list_test_cases', 'get_test_case', 'upsert_test_case', and 'delete_test_case'. 'create_draft_version' assigns the next version itself, so do not send one. |
| `test_case_id` | `string` | no |  |  | Test case ID. Required for 'get_test_case' and 'delete_test_case'. For 'upsert_test_case' it selects an existing case to replace; omit it to have one created. |
| `name` | `*string` | no |  |  | Suite name. Required and non-blank for 'create_suite'. For 'update_suite' an omitted name is left unchanged and a blank one is rejected. For 'upsert_test_case' it names the case. |
| `description` | `*string` | no |  |  | Suite or test case description. An omitted field is left unchanged by 'update_suite' and an explicitly empty string clears it. |
| `tags` | `*[]string` | no |  |  | Replacement tag list for 'update_suite' and 'upsert_test_case'. It overwrites the whole list rather than adding to it, so read the current tags first; an explicitly empty array clears them. |
| `changelog` | `string` | no |  |  | Note describing what the new version changes (for 'create_draft_version') |
| `empty_draft` | `bool` | no |  |  | Start the new version with no test cases (for 'create_draft_version'). The default copies every case of the latest published version, which is what an edit to an existing suite wants. |
| `category` | `string` | no |  |  | Test case category (for 'upsert_test_case') |
| `input` | `map[string]any` | no |  |  | What the case feeds the agent (required and non-empty for 'upsert_test_case'). The shape is free-form and decided by the runner, so copy an existing case of the suite before inventing one. |
| `expected` | `map[string]any` | no |  |  | What the case expects back (for 'upsert_test_case'). Free-form, and read by the evaluators rather than compared by the API. |
| `metadata` | `map[string]any` | no |  |  | Free-form metadata object (for 'upsert_test_case') |
| `artifact_refs` | `[]Agento11yArtifactRef` | no |  |  | Artifacts the case refers to, each an artifact_id with its name and kind (for 'upsert_test_case') |

#### `agento11y_manage_agents`

Category: `agento11y` · Code: [tools/agento11y_agents.go:297](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/agento11y_agents.go#L297) · Annotations: title="Manage Agent Observability agents", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `agento11yRead...`

Description (verbatim):

```text
Read the agent catalog of Grafana Agent Observability (the grafana-agento11y-app plugin): which agents send telemetry, what their system prompts and tools are, how their prompt versions evolved, and how each version scored.

The catalog is derived from ingested telemetry, not from a registration step: an agent exists here once its generations have been seen. It answers "what is this agent", not "what did it do".

Operations:
- 'list': agents in this tenant, newest activity first. Each row carries the latest effective version, first and latest seen times, generation and version counts, tool count, a system prompt prefix, and token_estimate. Paginated via limit and cursor
- 'get': one agent version in full: the complete system prompt, every tool with its JSON schema, and the models it ran on. Returns the latest version unless 'version' is set
- 'list_versions': the version history of one agent, one row per effective version with its seen window, generation count, tool count, and token_estimate. Paginated
- 'list_version_scores': evaluation score aggregates per version, with per-evaluator score_key, pass and fail counts, and mean_score. Use it to compare how versions scored

Versions: an effective version is always 'sha256:<64 lowercase hex>', and only that form is accepted by 'get'; a declared version such as '1.4.2' is reported in the declared_version fields but cannot be looked up. The plugin derives the effective version from the first of these the telemetry carries: the version the SDK reported, a hash of the declared version, a hash of the system prompt. Adding, removing, or editing a tool never mints a new version. Editing the prompt mints one only for an agent that reports neither its own effective version nor a declared version, so an agent that declares '1.4.2' keeps one effective version across prompt edits.

Response size: 'get' returns the whole system prompt plus every tool schema, which can be tens of thousands of tokens. Check token_estimate.total from 'list' or 'list_versions' before fetching, and prefer the system_prompt_prefix in those rows when a prefix is enough.

Cross-referencing: an agent name from 'list' is the value of the agent = "<name>" filter in conversation search.

Pagination: when a response carries next_cursor, call the same operation again with cursor set to it. For 'list', also repeat the same name_prefix, start_time, and end_time using absolute RFC3339 times; the cursor is bound to those filters and a relative value such as now-7d or 7d re-resolves and is rejected.

Permissions: every operation is a read and needs grafana-agento11y-app.data:read (Agento11y Editor or Admin). This tool performs no writes.

When to use:
- Discovering which agent names exist before filtering conversations or generations by agent
- Reading the system prompt or tool inventory an agent ran with, or how they changed between versions
- Checking whether a new prompt version scores worse than the previous one

When NOT to use:
- Reading individual conversations, generations, or their scores
- Inspecting evaluators or the rules that schedule them
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `operation` | `string` | yes |  | list, get, list_versions, list_version_scores | The operation to perform: 'list' for the agent catalog, 'get' for one agent version in full (system prompt, tools, models), 'list_versions' for the version history of one agent, 'list_version_scores' for evaluation score aggregates per version |
| `agent_name` | `*string` | no |  |  | Agent name from 'list'. Required for 'get', 'list_versions', and 'list_version_scores'. An explicitly empty string selects the unnamed agent (telemetry with no agent name), which 'get' and 'list_versions' accept and 'list_version_scores' rejects. |
| `version` | `string` | no |  |  | Effective version 'sha256:<64 lowercase hex>' from 'list' or 'list_versions', accepted only by 'get'. Omit it for the latest version. Declared versions such as '1.4.2' are not accepted here; they are reported in the declared_version fields. |
| `name_prefix` | `string` | no |  |  | Agent name filter (for 'list'). Despite the parameter name, the API matches it case-insensitively anywhere in the name, so 'agent' also returns 'my-agent'. |
| `start_time` | `string` | no |  |  | Start of the time range in RFC3339 or relative format (e.g. now-7d). For 'list' it keeps agents last seen at or after this time and defaults to no lower bound. For 'list_version_scores' it starts the score window; omitting it does not mean no lower bound, because the API then either scopes to the agent's 50 most recent versions or falls back to a 90-day window. |
| `end_time` | `string` | no |  |  | End of the time range in RFC3339 or relative format (e.g. now). For 'list' it keeps agents last seen at or before this time and defaults to no upper bound. For 'list_version_scores' it ends the score window; passing it without start_time gives a 90-day window ending here. |
| `limit` | `int` | no |  |  | Maximum number of results per page (default 50, capped at 200 by the API) (for 'list' and 'list_versions') |
| `cursor` | `string` | no |  |  | Pagination cursor from a previous response's next_cursor, echoed back exactly (for 'list' and 'list_versions'). For 'list' also resend the same name_prefix, start_time, and end_time as the first call using absolute RFC3339 times; the cursor is bound to those filters and a relative value such as now-7d or 7d drifts between calls and is rejected. |

#### `alerting_rules_read`

Category: `alerting` · Code: [tools/alerting.go:37](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting.go#L37) · Annotations: title="Read alert rules", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `alert.rules:read`, `alert.rules.external:read`, `folders:read`, `datasources:read`

Description (verbatim):

```text
List and inspect Grafana alert rules with filtering capabilities.

When to use:
- Understanding why an alert is or isn't firing
- Auditing alert rule configuration (queries, conditions, labels, notification settings)
- Finding alert rules by state, folder, group, or name
- Comparing rule versions to see what changed

Read-only: does not create, update, or delete rules, and does not show notification routing.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `rule_limit` | `int` | no | 200 |  | Maximum number of rules to return (default 200, max 200). Requires Grafana 12.4+ (for 'list' operation) |
| `label_selectors` | `[]string` | no |  |  | Prometheus-style selectors to filter alert rules by labels. Each string is a selector e.g. '{severity=\"critical\", team=~\"backend.*\"}'. All selectors must match (AND). |
| `limit_alerts` | `int` | no |  |  | Limit alert instances per rule. For list: 0 omits alerts. For get: <=0 defaults to 200. Max 200. |
| `search_folder` | `string` | no |  |  | Search folders by path using partial matching (for 'list' operation). Requires Grafana 12.4+. Mutually exclusive with folder_uid. |
| `search_rule_name` | `string` | no |  |  | Search alert rule names/titles using partial matching. Requires Grafana 12.4+ (for 'list' operation) |
| `states` | `[]string` | no |  |  | Filter by alert state: firing, pending, normal, recovering, nodata, error (for 'list' operation) |
| `rule_type` | `string` | no |  | alerting, recording | Filter by rule type (for 'list' operation) |
| `matchers` | `[]string` | no |  |  | Label matchers to filter alert instances. Each string is a Prometheus-style matcher e.g. 'severity=\"critical\"', 'env!=\"dev\"', 'team=~\"backend.*\"'. Requires Grafana 12.4+. |
| `operation` | `string` | yes |  | list, get, versions | The operation to perform: 'list' to search/filter rules, 'get' to retrieve full rule details (state + configuration) by UID, or 'versions' to get the version history of a rule |
| `rule_uid` | `string` | no |  |  | The UID of the alert rule (required for 'get' and 'versions' operations) |
| `datasource_uid` | `*string` | no |  |  | Optional: UID of a Prometheus or Loki datasource to query for datasource-managed alert rules. If omitted, returns Grafana-managed rules. |
| `folder_uid` | `string` | no |  |  | Filter by exact folder UID (for 'list' operation). Mutually exclusive with search_folder. |
| `rule_group` | `string` | no |  |  | Filter by exact rule group name (for 'list' operation) |

#### `alerting_rules_write`

Category: `alerting` · Code: [tools/alerting.go:51](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting.go#L51) · Annotations: title="Write alert rules", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `alert.rules:read`, `alert.rules:create`, `alert.rules:write`, `alert.rules:delete`, `alert.provisioning.provenance:write`, `folders:read`, `datasources:read`, `alert.rules.external:read`, `alert.rules.external:write`

Description (verbatim):

```text
Create, update, and delete Grafana alert rules.

When to use:
- Creating, updating, or deleting alert rules

Operation 'update' replaces the whole rule: it takes all required fields, not only the changed ones.

Creation defaults to Grafana-managed, even when queries use an external datasource.
Use managed_by='datasource' when requested or when established conversation or environment context clearly identifies a datasource-managed workflow. An external query datasource or an empty Grafana rule list alone is insufficient. Ask if context conflicts.
Datasource-managed creation uses a Mimir/Cortex or Loki ruler with namespace, rule_group, title and expression. datasource_uid is optional if exactly one compatible datasource exists. Ambiguity returns candidates for selection. Never falls back to Grafana-managed creation.

Does not list or inspect rules, and does not manage notification routing.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `rule_limit` | `int` | no | 200 |  | Maximum number of rules to return (default 200, max 200). Requires Grafana 12.4+ (for 'list' operation) |
| `label_selectors` | `[]string` | no |  |  | Prometheus-style selectors to filter alert rules by labels. Each string is a selector e.g. '{severity=\"critical\", team=~\"backend.*\"}'. All selectors must match (AND). |
| `limit_alerts` | `int` | no |  |  | Limit alert instances per rule. For list: 0 omits alerts. For get: <=0 defaults to 200. Max 200. |
| `search_folder` | `string` | no |  |  | Search folders by path using partial matching (for 'list' operation). Requires Grafana 12.4+. Mutually exclusive with folder_uid. |
| `search_rule_name` | `string` | no |  |  | Search alert rule names/titles using partial matching. Requires Grafana 12.4+ (for 'list' operation) |
| `states` | `[]string` | no |  |  | Filter by alert state: firing, pending, normal, recovering, nodata, error (for 'list' operation) |
| `rule_type` | `string` | no |  | alerting, recording | Filter by rule type (for 'list' operation) |
| `matchers` | `[]string` | no |  |  | Label matchers to filter alert instances. Each string is a Prometheus-style matcher e.g. 'severity=\"critical\"', 'env!=\"dev\"', 'team=~\"backend.*\"'. Requires Grafana 12.4+. |
| `managed_by` | `string` | no | grafana | grafana, datasource | Creation target. Omission defaults to Grafana-managed. Select datasource when requested or clearly established by conversation or environment context. Other mutations remain Grafana-only. |
| `namespace` | `string` | no |  |  | Namespace for datasource-managed creation. Required with managed_by=datasource. |
| `expression` | `string` | no |  |  | PromQL or LogQL expression for datasource-managed creation. |
| `evaluation_interval` | `string` | no |  |  | Interval for a new datasource rule group (default 1m). Must match an existing group's interval if supplied. |
| `operation` | `string` | yes |  | list, get, versions, create, update, delete | The operation to perform: 'list', 'get', 'versions', 'create', 'update', or 'delete'. To create a rule, use operation 'create' and provide all required fields in a single call. To update a rule, first use 'get' to retrieve its full configuration, then 'update' with all required fields plus your changes. |
| `rule_uid` | `string` | no |  |  | The UID of the alert rule (required for 'get', 'versions', 'update', 'delete'; optional for 'create') |
| `datasource_uid` | `*string` | no |  |  | Datasource UID for list or explicit managed_by=datasource creation. For creation omit to select the sole compatible datasource. Ambiguity returns candidates for selection. |
| `title` | `string` | no |  |  | The title of the alert rule (required for 'create', 'update') |
| `rule_group` | `string` | no |  |  | The rule group name (required for 'create', 'update') |
| `folder_uid` | `string` | no |  |  | The folder UID. For 'list': filter by exact folder UID (mutually exclusive with search_folder). For Grafana-managed 'create'/'update': required destination folder. |
| `condition` | `string` | no |  |  | Grafana-managed only. The query condition identifier, e.g. 'A', 'B' (required for 'create', 'update') |
| `data` | `[]map[string]any` | no |  |  | Grafana-managed only. Array of alert query objects (required for 'create'/'update'). Each object has: datasourceUid (string, required), model (object with expr for data queries or type/expression/conditions for expressions), refId (string, auto-assigned if omitted), relativeTimeRange ({from, to} in seconds, defaults to {from:600,to:0}). For server-side expressions use datasourceUid '__expr__'. Example: [{datasourceUid: 'prometheus', model: {expr: 'up == 0'}}, {datasourceUid: '__expr__', model: {type: 'threshold', expression: 'A', conditions: [{evaluator: {type: 'gt', params: [0]}}]}}] |
| `no_data_state` | `string` | no |  |  | Grafana-managed only. State when no data: NoData, Alerting, OK (required for 'create', 'update') |
| `exec_err_state` | `string` | no |  |  | Grafana-managed only. State on execution error: NoData, Alerting, OK (required for 'create', 'update') |
| `for` | `string` | no |  |  | Duration before alert fires, e.g. '5m'. Required for Grafana-managed create/update. Optional for datasource-managed rules (default 0s). |
| `keep_firing_for` | `string` | no |  |  | Enables continous firing of alert for specified time even when condition is no longer met. Default is 0 (resolves immediately) |
| `is_paused` | `bool` | no |  |  | If true, the alert rule remains inactive, Default is false |
| `notification_settings` | `map[string]any` | no |  |  | Notification settings object. Fields: receiver (string, required), groupBy ([]string), groupWait/groupInterval/repeatInterval (duration strings), muteTimeIntervals/activeTimeIntervals ([]string). |
| `record` | `map[string]any` | no |  |  | Recording rule config. Fields: from (string, required - ref ID e.g. 'A'), metric (string, required - metric name), targetDatasourceUid (string, optional). |
| `missing_series_evals_to_resolve` | `int64` | no |  |  | Consecutive evaluation intervals with no data required to mark the alert as resolved. Default is 2. |
| `annotations` | `map[string]string` | no |  |  | Optional annotations for the alert rule |
| `labels` | `map[string]string` | no |  |  | Optional labels for the alert rule |
| `org_id` | `int64` | no |  |  | Grafana-managed organization ID (required for 'create', 'update') |
| `disable_provenance` | `*bool` | no |  |  | If true, the alert remains editable in the Grafana UI (sets X-Disable-Provenance header). Defaults to true. |

#### `alerting_manage_routing`

Category: `alerting` · Code: [tools/alerting_routing.go:156](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_routing.go#L156) · Annotations: title="Manage alerting routing", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `alert.notifications:read`, `alert.notifications.receivers:read`, `alert.notifications.time-intervals:read`, `alert.notifications.routes:read`, `notifications.alerting.grafana.app/routingtrees:get`, `alert.notifications.external:read`, `datasourceQuery...`

Description (verbatim):

```text
Manage Grafana alerting routing configuration, including notification policies, contact points and time intervals.

Notification policies define how alerts are grouped, routed, and which contact points receive them.
Time intervals define active/mute periods for alert notifications.

When to use:
- Understanding how alerts are routed to contact points/receivers
- Debugging why an alert went to a specific receiver
- Checking grouping, timing, or mute interval settings

Does not show alert rule configuration or state.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `operation` | `string` | yes |  | get_notification_policies, get_contact_points, get_contact_point, get_time_intervals, get_time_interval | The operation to perform: 'get_notification_policies' to retrieve the notification policy tree, 'get_contact_points' to list all contact points, 'get_contact_point' to get a specific contact point by name, 'get_time_intervals' to list all time intervals, 'get_time_interval' to get a specific time interval by name |
| `datasource_uid` | `*string` | no |  |  | Optional: UID of an Alertmanager-compatible datasource to query for receivers. If omitted, returns Grafana-managed contact points. Only used with get_contact_points. |
| `name` | `*string` | no |  |  | Filter contact points by name (exact match). Only used with get_contact_points. |
| `contact_point_title` | `*string` | no |  |  | Title of the contact point to retrieve (required for get_contact_point operation) |
| `time_interval_name` | `*string` | no |  |  | Name of the time interval to retrieve (required for get_time_interval operation) |
| `limit` | `int` | no |  |  | The maximum number of results to return. Default is 100. Only used with get_contact_points. |

#### `alerting_routing_write`

Category: `alerting` · Code: [tools/alerting_routing.go:236](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_routing.go#L236) · Annotations: title="Write alerting routing", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `alert.notifications.receivers:create`, `alert.provisioning.provenance:write`, `datasources:read`, `alert.notifications.external:read`, `alert.notifications.external:write`

Description (verbatim):

```text
Create Grafana-managed contact points for alert notifications using operation 'create_contact_point'.
Requires name, type and integration-specific settings. Returns uid, name and type without settings or secrets.
Grafana-managed is the default and remains editable in the UI. Use managed_by='datasource' for an external Mimir/Cortex Alertmanager receiver when requested or when established conversation or environment context clearly identifies an external Alertmanager workflow. An external query datasource or an empty Grafana contact point list alone is insufficient. Ask if context conflicts.
Use native Alertmanager settings (email: to, webhook: url). Without datasource_uid select the sole compatible datasource, or return candidates for selection if ambiguous. Does not change notification routes.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `managed_by` | `string` | no | grafana | grafana, datasource | Creation target. Omission defaults to Grafana-managed. Select datasource when requested or clearly established by conversation or environment context. |
| `datasource_uid` | `string` | no |  |  | External Mimir/Cortex Alertmanager UID. Only for managed_by=datasource. Omit to select the sole compatible datasource. Ambiguity returns candidates for selection. |
| `operation` | `string` | yes |  | create_contact_point | The operation to perform: 'create_contact_point' |
| `name` | `string` | yes |  |  | Contact point name. Integrations with the same name are grouped together. |
| `type` | `string` | yes |  |  | Integration type (for example email, slack or webhook). |
| `settings` | `map[string]any` | yes |  |  | Integration-specific settings as a JSON object (for example {\"addresses\":\"team@example.com\"} for email). |
| `uid` | `string` | no |  |  | Optional integration UID. Grafana generates one if omitted. |
| `disable_resolve_message` | `bool` | no |  |  | Disable resolved notifications. Defaults to false. |
| `disable_provenance` | `*bool` | no |  |  | Keep the contact point editable in the Grafana UI. Defaults to true. |

#### `alerting_silences_read`

Category: `alerting` · Code: [tools/alerting_silences.go:416](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_silences.go#L416) · Annotations: title="Read alerting silences", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `alert.silences:read`, `alert.instances:read`

Description (verbatim):

```text
List and inspect Grafana alerting silences. A silence temporarily suppresses notifications for alerts whose labels match a set of matchers.

Operations:
- 'list': list existing silences. Optionally filter by rule_uid (matches the __alert_rule_uid__ label) or by matchers.
- 'get': retrieve a single silence by silence_id.

When to use:
- Inspecting which alerts are currently silenced and why

Read-only: does not create, update, or delete silences, and does not show alert rules or notification routing.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `operation` | `string` | yes |  | list, get | The operation to perform: 'list' to list silences, 'get' to retrieve a silence by id |
| `silence_id` | `*string` | no |  |  | The silence id (required for 'get') |
| `rule_uid` | `*string` | no |  |  | Optional: filter listed silences to those scoped to this alert rule UID (matches the __alert_rule_uid__ label). Only used with 'list'. |
| `matchers` | `[]SilenceMatcherParam` | no |  |  | Optional label matchers used to filter listed silences. Only used with 'list'. |

#### `alerting_silences_write`

Category: `alerting` · Code: [tools/alerting_silences.go:428](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/alerting_silences.go#L428) · Annotations: title="Write alerting silences", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `alert.silences:read`, `alert.silences:create`, `alert.silences:write`, `alert.instances:read`, `alert.instances:create`, `alert.instances:write`

Description (verbatim):

```text
Create, update, and delete Grafana alerting silences. A silence temporarily suppresses notifications for alerts whose labels match a set of matchers, without changing the alert rules themselves.

Operations:
- 'create': create a new silence. Requires matchers, starts_at, ends_at (RFC3339) and comment.
- 'update': modify an existing silence by silence_id. Requires matchers, starts_at, ends_at and comment. The id is only kept when the posted matchers and starts_at match the stored ones, so pass back the stored starts_at of the silence; otherwise Alertmanager expires the old silence and returns a new id.
- 'delete': expire/remove a silence by silence_id.

When to use:
- Muting noisy or expected alerts during maintenance windows

Does not list or inspect silences, change alert rules, or manage notification routing.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `operation` | `string` | yes |  | list, get, create, update, delete | The operation to perform: 'list' to list silences, 'get' to retrieve a silence by id, 'create' to create a new silence, 'update' to modify an existing silence by id, 'delete' to expire a silence by id |
| `silence_id` | `*string` | no |  |  | The silence id (required for 'get', 'update' and 'delete') |
| `rule_uid` | `*string` | no |  |  | Optional: filter listed silences to those scoped to this alert rule UID (matches the __alert_rule_uid__ label). Only used with 'list'. |
| `matchers` | `[]SilenceMatcherParam` | no |  |  | Label matchers. Required (at least one) for 'create' and 'update'. For 'list', used as an optional filter. |
| `starts_at` | `*string` | no |  |  | Silence start time in RFC3339 format, e.g. '2026-07-11T10:00:00Z' (required for 'create' and 'update'). Grafana clamps a start time in the past to the moment of creation, so for 'update' pass back the starts_at returned by 'get' to keep the silence id stable. |
| `ends_at` | `*string` | no |  |  | Silence end time in RFC3339 format, e.g. '2026-07-11T12:00:00Z' (required for 'create' and 'update') |
| `comment` | `*string` | no |  |  | A human-readable comment explaining the silence (required for 'create' and 'update') |
| `created_by` | `*string` | no |  |  | Author of the silence. Defaults to 'grafana-assistant'. |

#### `get_annotations`

Category: `annotations` · Code: [tools/annotations.go:56](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L56) · Annotations: title="Get Annotations", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `annotations:read`

Description (verbatim):

```text
Fetch Grafana annotations using filters such as dashboard UID, time range and tags.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `from` | `*int64` | no |  |  | Epoch ms start time |
| `to` | `*int64` | no |  |  | Epoch ms end time |
| `limit` | `*int64` | no |  |  | Max results default 100 |
| `alertUid` | `*string` | no |  |  | Filter by alert UID |
| `dashboardUid` | `*string` | no |  |  | Filter by dashboard UID |
| `panelId` | `*int64` | no |  |  | Filter by panel ID |
| `userId` | `*int64` | no |  |  | Filter by creator user ID |
| `type` | `*string` | no |  |  | annotation or alert |
| `tags` | `[]string` | no |  |  | Filter by tags. Multiple tags allowed; use matchAny to control AND/OR logic |
| `matchAny` | `*bool` | no |  |  | If true, match any tag (OR). If false, match all tags (AND). Default: false |

#### `create_annotation`

Category: `annotations` · Code: [tools/annotations.go:133](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L133) · Annotations: title="Create Annotation", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `annotations:create`

Description (verbatim):

```text
Create a new annotation on a dashboard or panel. Set format to 'graphite' and provide 'what' for Graphite-format annotations.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `dashboardUid` | `string` | no |  |  | Dashboard UID |
| `panelId` | `int64` | no |  |  | Panel ID |
| `time` | `int64` | no |  |  | Start time epoch ms |
| `timeEnd` | `int64` | no |  |  | End time epoch ms |
| `tags` | `[]string` | no |  |  | Optional list of tags |
| `text` | `string` | no |  |  | Annotation text (required unless format is graphite) |
| `data` | `map[string]any` | no |  |  | Optional JSON payload |
| `format` | `string` | no |  | graphite | Set to 'graphite' to create a Graphite-format annotation |
| `what` | `string` | no |  |  | Annotation text for Graphite format (required when format is graphite) |
| `when` | `int64` | no |  |  | Epoch ms timestamp for Graphite format |
| `graphiteData` | `string` | no |  |  | Optional string payload for Graphite format |

#### `update_annotation`

Category: `annotations` · Code: [tools/annotations.go:187](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L187) · Annotations: title="Update Annotation", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `annotations:read`, `annotations:write`

Description (verbatim):

```text
Updates the provided properties of an annotation by ID. Only fields included in the request are modified; omitted fields are left unchanged.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `id` | `int64` | no |  |  | Annotation ID to update |
| `text` | `*string` | no |  |  | New annotation text |
| `time` | `*int64` | no |  |  | New start time epoch ms |
| `timeEnd` | `*int64` | no |  |  | New end time epoch ms |
| `tags` | `[]string` | no |  |  | Tags to replace existing tags |
| `data` | `map[string]any` | no |  |  | Optional JSON payload |

#### `delete_annotation`

Category: `annotations` · Code: [tools/annotations.go:228](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L228) · Annotations: title="Delete Annotation", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `annotations:delete`

Description (verbatim):

```text
Permanently delete an annotation by ID. The annotation cannot be recovered afterwards.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `id` | `int64` | yes |  |  | Annotation ID to delete |

#### `get_annotation_tags`

Category: `annotations` · Code: [tools/annotations.go:269](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/annotations.go#L269) · Annotations: title="Get Annotation Tags", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `annotations:read`

Description (verbatim):

```text
Returns annotation tags with optional filtering by tag name. Only the provided filters are applied.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `tag` | `*string` | no |  |  | Optional filter by tag name |
| `limit` | `*int64` | no |  |  | Max results, default 100 |

#### `grafana_api_request` (variant 1 of 3)

Category: `api` · Code: [tools/api.go:208](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/api.go#L208) · Annotations: title="Grafana API request", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Make an authenticated HTTP request to the Grafana API. Similar to 'gh api' for GitHub. Supports any Grafana API endpoint with optional jq-style response filtering. Use this for API endpoints that don't have a dedicated tool.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `endpoint` | `string` | yes |  |  | The API path relative to the Grafana base URL (e.g. '/api/org', '/api/dashboards/uid/abc123'). Must start with '/'. |
| `method` | `string` | no |  | GET, POST, PUT, PATCH, DELETE | HTTP method. Defaults to GET |
| `body` | `string` | no |  |  | Request body (JSON string). Used with POST, PUT, and PATCH requests. |
| `headers` | `map[string]string` | no |  |  | Additional HTTP headers to include in the request. |
| `jq` | `string` | no |  |  | A jq expression to filter or transform the JSON response (e.g. '.dashboards[] \| .title'). |

#### `grafana_api_request` (variant 2 of 3)

Category: `api` · Code: [tools/api.go:222](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/api.go#L222) · Annotations: title="Grafana API request", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Make an authenticated HTTP request to the Grafana API. Similar to 'gh api' for GitHub. Supports any Grafana API endpoint with optional jq-style response filtering. Use this for API endpoints that don't have a dedicated tool. Only GET requests are allowed, except POST to read-only query endpoints such as /api/ds/query.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `endpoint` | `string` | yes |  |  | The API path relative to the Grafana base URL (e.g. '/api/org', '/api/dashboards/uid/abc123', '/api/ds/query'). Must start with '/'. |
| `method` | `string` | no |  | GET, POST | HTTP method. Defaults to GET. POST is only allowed for specific read-only query endpoints such as /api/ds/query. |
| `body` | `string` | no |  |  | Request body (JSON string). Used with POST requests to read-only query endpoints such as /api/ds/query. |
| `headers` | `map[string]string` | no |  |  | Additional HTTP headers to include in the request. |
| `jq` | `string` | no |  |  | A jq expression to filter or transform the JSON response (e.g. '.dashboards[] \| .title'). |

#### `grafana_api_request` (variant 3 of 3)

Category: `api` · Code: [tools/api.go:237](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/api.go#L237) · Annotations: title="Grafana API request", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Make an authenticated HTTP request to the Grafana API. Similar to 'gh api' for GitHub. Supports any Grafana API endpoint with optional jq-style response filtering. Use this for API endpoints that don't have a dedicated tool. Only GET requests are allowed.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `endpoint` | `string` | yes |  |  | The API path relative to the Grafana base URL (e.g. '/api/org', '/api/dashboards/uid/abc123'). Must start with '/'. |
| `method` | `string` | no |  | GET | HTTP method. Only GET is allowed in read-only mode |
| `headers` | `map[string]string` | no |  |  | Additional HTTP headers to include in the request. |
| `jq` | `string` | no |  |  | A jq expression to filter or transform the JSON response (e.g. '.dashboards[] \| .title'). |

#### `get_assertions`

Category: `asserts` · Code: [tools/asserts.go:143](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/asserts.go#L143) · Annotations: title="Get assertions summary", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`

Description (verbatim):

```text
Get assertion summary for a given entity with its type, name, env, site, namespace, and a time range
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `startTime` | `string` | yes |  |  | The start time in RFC3339 format (e.g. 2024-01-01T00:00:00Z) or relative format (e.g. now-1h) |
| `endTime` | `string` | yes |  |  | The end time in RFC3339 format (e.g. 2024-01-01T00:00:00Z) or relative format (e.g. now) |
| `entityType` | `string` | no |  |  | The type of the entity to list (e.g. Service, Node, Pod, etc.) |
| `entityName` | `string` | no |  |  | The name of the entity to list |
| `env` | `string` | no |  |  | The env of the entity to list |
| `site` | `string` | no |  |  | The site of the entity to list |
| `namespace` | `string` | no |  |  | The namespace of the entity to list |

#### `ask_assistant`

Category: `assistant` · Code: [tools/assistant.go:176](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/assistant.go#L176) · Annotations: title="Ask Grafana Assistant", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-assistant-app.chats:access`

Description (verbatim):

```text
Send a message to Grafana Assistant and wait for the full text reply. The assistant may use tools, metrics, logs, and other stack context—broader than firing one isolated data-source query.

Use for open-ended questions, triage, or anything that needs assistant reasoning and tool use, in addition to the more targeted MCP tools.

**Multi-turn:** pass contextId from a previous ask_assistant result to continue the same conversation.

**Time:** complex tasks can take several minutes; the call blocks until the reply is done or the request times out. Consider running this tool as a background task if able.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `prompt` | `string` | yes |  |  | The question or instruction to send to Grafana Assistant (natural language). |
| `contextId` | `string` | no |  |  | Optional context ID from a previous ask_assistant response to continue the same conversation. |

#### `query_cloud_logging`

Category: `cloudlogging` · Code: [tools/cloudlogging.go:370](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L370) · Annotations: title="Query Google Cloud Logging", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Query logs from a Google Cloud Logging datasource using the Cloud Logging query language. Returns entries newest-first with timestamp, severity, body, log entry id, trace id, and labels (resource/log labels as JSON).

The time range (start/end, default last hour) is applied automatically, so the filter needs no timestamp clauses. Results are capped at 'limit' (default 100, max 1000); 'truncated' is true when the cap was hit.

Filter examples:
  resource.type="k8s_container" AND resource.labels.namespace_name="payments" AND severity>=ERROR
  logName:"stderr" AND jsonPayload.message:"timeout"
  resource.type="cloud_run_revision" AND httpRequest.status>=500
  labels."k8s-pod/app"="api" AND NOT textPayload:"healthz"

bucketId reads a specific log bucket, optionally narrowed with viewId.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Google Cloud Logging datasource (type googlecloud-logging-datasource). |
| `projectId` | `string` | yes |  |  | GCP project ID to read logs from (e.g. my-prod-project). |
| `filter` | `string` | no |  |  | Cloud Logging query language filter, e.g. resource.type=\"k8s_container\" AND severity>=ERROR. Leave empty to return all logs in the time range. Do NOT add timestamp clauses: the time range is applied automatically from start/end. |
| `bucketId` | `string` | no |  |  | Optional log bucket to scope the query, as '<location>/buckets/<name>' (e.g. global/buckets/_Default). Omit to search the project's default scope. |
| `viewId` | `string` | no |  |  | Optional log view within bucketId (e.g. _AllLogs). Only meaningful when bucketId is set; defaults to _AllLogs. |
| `start` | `string` | no |  |  | Start time. Formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms). Default: now-1h |
| `end` | `string` | no |  |  | End time. Formats: 'now', '2026-02-02T20:00:00Z', '1738522800000' (Unix ms). Default: now |
| `limit` | `int` | no |  |  | Maximum number of log entries to return, newest first. Default: 100, max: 1000. |

#### `list_cloud_logging_projects`

Category: `cloudlogging` · Code: [tools/cloudlogging.go:411](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L411) · Annotations: title="List Cloud Logging projects", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List the GCP project IDs the Google Cloud Logging datasource's credentials can read logs from (at most 100; 'query' narrows the list).
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Google Cloud Logging datasource |
| `query` | `string` | no |  |  | Optional substring to filter project IDs (e.g. prod). |

#### `list_cloud_logging_buckets`

Category: `cloudlogging` · Code: [tools/cloudlogging.go:443](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L443) · Annotations: title="List Cloud Logging buckets", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List the log buckets in a GCP project, as '<location>/buckets/<name>' (e.g. global/buckets/_Default). Each value is a valid bucketId as-is.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Google Cloud Logging datasource |
| `projectId` | `string` | yes |  |  | GCP project ID whose log buckets to list |

#### `list_cloud_logging_views`

Category: `cloudlogging` · Code: [tools/cloudlogging.go:480](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudlogging.go#L480) · Annotations: title="List Cloud Logging views", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List the log views in a log bucket (e.g. _AllLogs, _Default). Each value is a valid viewId for the same bucketId.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Google Cloud Logging datasource |
| `projectId` | `string` | yes |  |  | GCP project ID that owns the bucket |
| `bucketId` | `string` | yes |  |  | Log bucket as '<location>/buckets/<name>' (e.g. global/buckets/_Default) |

#### `query_cloudwatch`

Category: `cloudwatch` · Code: [tools/cloudwatch.go:303](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L303) · Annotations: title="Query CloudWatch", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Query AWS CloudWatch metrics via Grafana. Requires region.

Time formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms)

Common namespaces: AWS/EC2, AWS/ECS, AWS/RDS, AWS/Lambda, ECS/ContainerInsights

Example dimensions: ECS: {ClusterName, ServiceName}, EC2: {InstanceId}

Cross-account monitoring: Use accountId to query metrics from a specific source account (e.g. '123456789012') or 'all' to query all linked accounts. Only applicable when using a CloudWatch monitoring account datasource.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the CloudWatch datasource to query. |
| `namespace` | `string` | yes |  |  | CloudWatch namespace (e.g. AWS/ECS, AWS/EC2, AWS/RDS, AWS/Lambda) |
| `metricName` | `string` | yes |  |  | Metric name (e.g. CPUUtilization, MemoryUtilization, Invocations) |
| `dimensions` | `map[string]string` | no |  |  | Dimensions as key-value pairs (e.g. {\"ClusterName\": \"my-cluster\"}) |
| `statistic` | `string` | no |  |  | Statistic type: Average, Sum, Maximum, Minimum, SampleCount, or a percentile such as p50, p95 or p99.9. Default: Average |
| `period` | `int` | no |  |  | Period in seconds (default: 300) |
| `start` | `string` | no |  |  | Start time. Formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms). Default: now-1h |
| `end` | `string` | no |  |  | End time. Formats: 'now', '2026-02-02T20:00:00Z', '1738522800000' (Unix ms). Default: now |
| `region` | `string` | yes |  |  | AWS region (e.g. us-east-1) |
| `accountId` | `string` | no |  |  | AWS account ID for cross-account monitoring. Specify an account ID to query metrics from a specific source account, or 'all' to query all accounts the monitoring account is permitted to query. Only relevant when using a CloudWatch monitoring account datasource. |

#### `list_cloudwatch_namespaces`

Category: `cloudwatch` · Code: [tools/cloudwatch.go:419](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L419) · Annotations: title="List CloudWatch namespaces", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List available CloudWatch namespaces (AWS/EC2, AWS/ECS, AWS/RDS, etc.). Requires region. Supports cross-account monitoring via optional accountId parameter.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the CloudWatch datasource |
| `region` | `string` | yes |  |  | AWS region (e.g. us-east-1) |
| `accountId` | `string` | no |  |  | AWS account ID for cross-account monitoring. Specify an account ID to filter namespaces from a specific source account, or 'all' for all linked accounts. |

#### `list_cloudwatch_metrics`

Category: `cloudwatch` · Code: [tools/cloudwatch.go:482](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L482) · Annotations: title="List CloudWatch metrics", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List metrics for a CloudWatch namespace. Requires region. Supports cross-account monitoring via optional accountId parameter.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the CloudWatch datasource |
| `namespace` | `string` | yes |  |  | CloudWatch namespace (e.g. AWS/ECS, AWS/EC2) |
| `region` | `string` | yes |  |  | AWS region (e.g. us-east-1) |
| `accountId` | `string` | no |  |  | AWS account ID for cross-account monitoring. Specify an account ID to filter metrics from a specific source account, or 'all' for all linked accounts. |

#### `list_cloudwatch_dimensions`

Category: `cloudwatch` · Code: [tools/cloudwatch.go:547](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L547) · Annotations: title="List CloudWatch dimensions", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List dimension keys for a CloudWatch metric. Requires region. Supports cross-account monitoring via optional accountId parameter.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the CloudWatch datasource |
| `namespace` | `string` | yes |  |  | CloudWatch namespace (e.g. AWS/ECS) |
| `metricName` | `string` | yes |  |  | Metric name (e.g. CPUUtilization) |
| `region` | `string` | yes |  |  | AWS region (e.g. us-east-1) |
| `accountId` | `string` | no |  |  | AWS account ID for cross-account monitoring. Specify an account ID to filter dimensions from a specific source account, or 'all' for all linked accounts. |

#### `list_cloudwatch_dimension_values`

Category: `cloudwatch` · Code: [tools/cloudwatch.go:615](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/cloudwatch.go#L615) · Annotations: title="List CloudWatch dimension values", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List values for a CloudWatch dimension key (e.g. the specific cluster names behind a ClusterName dimension). Requires region. Supports cross-account monitoring via optional accountId parameter.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the CloudWatch datasource |
| `namespace` | `string` | yes |  |  | CloudWatch namespace (e.g. AWS/ECS) |
| `metricName` | `string` | yes |  |  | Metric name (e.g. CPUUtilization) |
| `dimensionKey` | `string` | yes |  |  | Dimension key to list values for (e.g. ClusterName) |
| `region` | `string` | yes |  |  | AWS region (e.g. us-east-1) |
| `accountId` | `string` | no |  |  | AWS account ID for cross-account monitoring. Specify an account ID to filter dimension values from a specific source account, or 'all' for all linked accounts. |

#### `suggest_loki_alloy_label_config`

Category: `config` · Code: [tools/config.go:115](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/config.go#L115) · Annotations: title="Suggest Alloy label enforcement config", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Generates an Alloy loki.process snippet enforcing an approved label set via stage.label_keep, with optional log-level normalisation and soft-enforcement placeholders.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `approvedLabels` | `[]string` | yes |  |  | Labels to keep on the index. |
| `requiredLabels` | `[]string` | no |  |  | Labels that get an 'unknown' placeholder when missing. |
| `normalizeLogLevel` | `bool` | no |  |  |  |
| `componentName` | `string` | no |  |  |  |
| `forwardTo` | `string` | no |  |  |  |

#### `get_dashboard_by_uid`

Category: `dashboard` · Code: [tools/dashboard.go:906](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L906) · Annotations: title="Get dashboard details", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboardRead...`, `dashboards:write`

Description (verbatim):

```text
Retrieves the complete dashboard, including panels, variables, and settings, for a specific dashboard identified by its UID. Pass optional version to load a saved snapshot instead of the current dashboard. Saved snapshots are fetched through Grafana's legacy versions API, so 'apiVersion' is omitted and 'meta' is partial: only version, createdBy, and created are populated. For current (non-versioned) fetches, the response includes 'apiVersion' and 'isV2': when 'isV2' is true the dashboard uses the v2 schema (panels live under 'elements' keyed by name, arranged by 'layout'; variables under 'variables'), otherwise it is classic v1 ('panels[]' with 'templating.list'). The full JSON of a large dashboard can be very large.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | yes |  |  | The UID of the dashboard |
| `version` | `*int64` | no |  |  | Optional saved version. Omit for the current dashboard |

#### `update_dashboard`

Category: `dashboard` · Code: [tools/dashboard.go:921](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L921) · Annotations: title="Create or update dashboard", readOnlyHint=false, destructiveHint=true, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboardRead...`, `dashboards:create`, `dashboards:write`, `folders:read`, `dashboard.grafana.app/dashboards:create`, `dashboard.grafana.app/dashboards:update`

Description (verbatim):

```text
Create or update a dashboard. Returns the saved dashboard UID and dashboard link in the 'url' field, using the instance public URL when available. Two modes: (1) Full JSON — provide 'dashboard' for new dashboards or complete replacements. (2) Patch — provide 'uid' + 'operations' to make targeted changes to an existing dashboard. One of these two modes is required; 'folderUid', 'message', and 'overwrite' are supplementary and do nothing on their own. Dashboard authoring guidance: if a saved query must support one, many, or All values from a multi-select variable inside a regex expression or matcher, save '${var:regex}' rather than plain '$var'. Saved dashboard annotation queries/definitions live in dashboard JSON under 'annotations.list'; annotation events are stored separately and are not part of the dashboard JSON. For stat panels over the current dashboard range, make the query return the range-level result the stat should display; panel-side reduction only reduces returned series and does not compute peak-over-range or ratio-of-peaks semantics for you. Patch operations support JSONPaths like '$.panels[0].targets[0].expr', '$.panels[1].title', '$.panels[2].targets[0].datasource', '$.templating.list/-', and '$.annotations.list/-'. Append to arrays with '/- ' syntax: '$.panels/- '. Remove by index: {"op": "remove", "path": "$.panels[2]"}. Multiple removes on the same array are automatically reordered to avoid index-shifting issues. Note: only numeric array indices are supported in patch paths; filter expressions like [?(@.id==2)] and wildcards like [*] are not supported. Schema: prefer v2 for new dashboards; if this Grafana lacks v2 the save fails saying so, then send v1. Keep an existing dashboard in its stored schema (indicated by 'isV2'/'apiVersion' on the fetched dashboard). A body with top-level 'elements'/'layout' is saved as v2. Minimal v2 body: {"title":"T","timeSettings":{"from":"now-6h","to":"now"},"variables":[],"elements":{"p1":{"kind":"Panel","spec":{"id":1,"title":"Up","vizConfig":{"kind":"VizConfig","group":"timeseries","spec":{}},"data":{"kind":"QueryGroup","spec":{"queries":[{"kind":"PanelQuery","spec":{"refId":"A","query":{"kind":"DataQuery","group":"prometheus","datasource":{"name":"<ds uid>"},"spec":{"expr":"up"}}}}]}}}}},"layout":{"kind":"GridLayout","spec":{"items":[{"kind":"GridLayoutItem","spec":{"x":0,"y":0,"width":24,"height":8,"element":{"kind":"ElementReference","name":"p1"}}}]}}}. For tabs, layout is {"kind":"TabsLayout","spec":{"tabs":[{"kind":"TabsLayoutTab","spec":{"title":"A","layout":<GridLayout>}}]}}.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `dashboard` | `map[string]interface{}` | no |  |  | The full dashboard JSON: classic v1 (panels[]) or v2 (elements/layout; skeleton in the tool description). Use for creating new dashboards or complete updates. Saved dashboard annotation queries/definitions live in 'annotations.list' inside this JSON; they are different from annotation events, which are stored separately. Large dashboards consume significant context - consider using patches for small changes. |
| `uid` | `string` | no |  |  | UID of existing dashboard to update. Must be used together with 'operations'. Providing 'uid' without 'operations' will fail. |
| `operations` | `[]PatchOperation` | no |  |  | Array of patch operations for targeted updates. More efficient than full dashboard JSON for small changes. Common paths: '$.templating.list/-' to add a variable, '$.annotations.list/-' to add a saved dashboard annotation query/definition, '$.panels[0].targets[0].expr' to replace a panel query. v2 paths: '$.elements.<name>.spec.title', '$.variables/-', '$.layout.spec.items/-'. |
| `folderUid` | `string` | no |  |  | The UID of the dashboard's folder |
| `message` | `string` | no |  |  | Set a commit message for the version history |
| `overwrite` | `bool` | no |  |  | Overwrite the dashboard if it exists. Otherwise create one |
| `userId` | `int64` | no |  |  | ID of the user making the change |

#### `get_dashboard_panel_queries`

Category: `dashboard` · Code: [tools/dashboard.go:1003](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L1003) · Annotations: title="Get dashboard panel queries", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboardRead...`

Description (verbatim):

```text
Retrieve panel queries from a Grafana dashboard. Supports all datasource types (Prometheus, Loki, CloudWatch, SQL, etc.) and row-nested panels. Optionally filter to a specific panel by ID with `panelId`. Provide `variables` (an empty object uses saved selections) or `start`/`end` to populate `processedQuery` and `requiredVariables`. Referenced All selections return `warnings` requesting explicit values. Returns an array of objects with fields: title, query (raw expression), datasource (object with uid and type), and optionally processedQuery, refId, requiredVariables, and target. Targets built in a visual editor (CloudWatch metric search, InfluxDB query builder) have no string expression: those return an empty query plus `target`, the panel's raw query JSON. They can be executed as panel queries but not as standalone expressions.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | yes |  |  | The UID of the dashboard |
| `panelId` | `*int` | no |  |  | Optional panel ID to filter to a specific panel |
| `variables` | `map[string]string` | no |  |  | Optional variable substitutions (e.g., {\"job\": \"api-server\"}) |
| `start` | `string` | no |  |  | Query start time for macros (default now-1h). |
| `end` | `string` | no |  |  | Query end time for macros (default now). |

#### `get_dashboard_property`

Category: `dashboard` · Code: [tools/dashboard.go:1056](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L1056) · Annotations: title="Get dashboard property", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboardRead...`

Description (verbatim):

```text
Get specific parts of a dashboard using JSONPath expressions to minimize context window usage. JSONPath targets the dashboard's native schema. Classic v1 paths: '$.title' (title), '$.panels[*].title' (all panel titles), '$.panels[0]' (first panel), '$.templating.list' (variables), '$.annotations.list' (saved dashboard annotation queries/definitions), '$.tags' (tags), '$.panels[*].targets[*].expr' (all queries). v2 dashboards (isV2 true) use different paths: '$.title', '$.elements' (panels, keyed by name), '$.variables' (variables), '$.annotations'.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | yes |  |  | The UID of the dashboard |
| `jsonPath` | `string` | yes |  |  | JSONPath expression to extract specific data (e.g., '$.panels[0].title' for first panel title, '$.panels[*].title' for all panel titles, '$.templating.list' for variables, '$.annotations.list' for saved dashboard annotation queries/definitions) |

#### `get_dashboard_summary`

Category: `dashboard` · Code: [tools/dashboard.go:1172](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard.go#L1172) · Annotations: title="Get dashboard summary", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboardRead...`

Description (verbatim):

```text
Get a compact summary of a dashboard including title, panel count, panel types, variables, and other metadata without the full JSON. Use this for dashboard overview and planning modifications without consuming large context windows.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | yes |  |  | The UID of the dashboard |

#### `list_dashboard_versions`

Category: `dashboard` · Code: [tools/dashboard_versions.go:77](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/dashboard_versions.go#L77) · Annotations: title="List dashboard versions", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboards:read`, `dashboards:write`

Description (verbatim):

```text
List saved versions of a Grafana dashboard. Returns compact metadata: version number, author, timestamp, and save message. A version number can be passed to the dashboard fetch to load that snapshot.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | yes |  |  | The UID of the dashboard |
| `limit` | `int` | no |  |  | Maximum number of versions to return |
| `start` | `int` | no |  |  | Version to start from. Only versions at or below this number are returned |

#### `list_datasources`

Category: `datasource` · Code: [tools/datasources.go:440](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L440) · Annotations: title="List datasources", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasources:read`

Description (verbatim):

```text
List all configured datasources in Grafana. Use this to discover available datasources and their UIDs. Supports filtering by type and/or name (case-insensitive substring match) and pagination.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `type` | `string` | no |  |  | The type of datasources to search for. For example, 'prometheus', 'loki', 'tempo', etc... |
| `name` | `string` | no |  |  | Case-insensitive substring match on the datasource name. For example, 'prod' matches datasources named 'prometheus-prod-eu' and 'loki-prod-us'. Useful on instances with many datasources where filtering by type alone returns too many results. |
| `limit` | `int` | no | 50 |  | Maximum number of datasources to return (max 100) |
| `offset` | `int` | no | 0 |  | Number of datasources to skip for pagination |

#### `create_datasource`

Category: `datasource` · Code: [tools/datasources.go:452](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L452) · Annotations: title="Create datasource", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasources:read`, `datasources:create`

Description (verbatim):

```text
Create a datasource in two steps. Called with only the type, it returns the plugin's field schema and creates nothing. Called with the type, the display name in the top-level name argument, schemaReviewed=true, and field values in the fields map, it creates the datasource. The plugin for the type must already be installed. Secrets (passwords, tokens) are not accepted. Returns UID, health check, and a config page link.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `name` | `string` | yes |  |  | Datasource display name |
| `type` | `string` | yes |  |  | Grafana datasource plugin type, for example prometheus |
| `url` | `string` | no |  |  | Datasource base URL when required by the plugin |
| `access` | `string` | no |  |  | How Grafana should access the datasource (proxy or direct) |
| `database` | `string` | no |  |  | Optional database name |
| `basicAuth` | `bool` | no |  |  | Whether Grafana should use basic auth |
| `withCredentials` | `bool` | no |  |  | Whether Grafana should forward credentials such as cookies |
| `isDefault` | `bool` | no |  |  | Whether this should become the default datasource |
| `fields` | `map[string]any` | no |  |  | Datasource field values to provision, keyed by field key from the schema returned on the first call. The server uses each field's target (root or jsonData) to place values correctly in the YAML. Example: {\"url\": \"http://prometheus:9090\", \"httpMethod\": \"POST\"}. |
| `schemaReviewed` | `bool` | no |  |  | True once the field schema has been retrieved; required to create a schema-backed datasource. |

#### `update_datasource`

Category: `datasource` · Code: [tools/datasources.go:464](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L464) · Annotations: title="Update datasource", readOnlyHint=false, destructiveHint=true, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasources:read`, `datasources:write`

Description (verbatim):

```text
Update non-secret datasource fields by UID in two steps. Called with only the uid, it returns the datasource's field schema and changes nothing. Called with the uid, schemaReviewed=true, and the changed values in the fields map, it applies the update. Omitted fields are preserved. Secrets (passwords, tokens) cannot be changed. Returns an update message and a health check.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | yes |  |  | UID of the datasource to update |
| `name` | `*string` | no |  |  | Display name |
| `url` | `*string` | no |  |  | Base URL |
| `access` | `*string` | no |  |  | proxy or direct |
| `database` | `*string` | no |  |  | Database name |
| `basicAuth` | `*bool` | no |  |  | Enable basic auth |
| `isDefault` | `*bool` | no |  |  | Make this the default datasource |
| `jsonData` | `map[string]interface{}` | no |  |  | Non-secret plugin settings; replaces existing jsonData when set |
| `fields` | `map[string]any` | no |  |  | Datasource field values to change, keyed by field key from the schema returned on the first call. The server uses each field's target (root or jsonData) to place values correctly, merging jsonData changes into the existing settings. Only include the fields you want to change. Example: {\"httpMethod\": \"POST\"}. |
| `schemaReviewed` | `bool` | no |  |  | True once the field schema has been retrieved; required to apply the update. |

#### `get_datasource`

Category: `datasource` · Code: [tools/datasources.go:549](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L549) · Annotations: title="Get datasource", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasources:read`

Description (verbatim):

```text
Retrieves detailed information about a specific datasource by UID or name. Returns the full datasource model, including name, type, URL, access settings, JSON data, and secure JSON field status. Provide either uid or name; uid takes priority if both are given.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `uid` | `string` | no |  |  | The UID of the datasource. If provided, takes priority over name. |
| `name` | `string` | no |  |  | The name of the datasource. Used if UID is not provided. |

#### `check_datasources_health`

Category: `datasource` · Code: [tools/datasources.go:909](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/datasources.go#L909) · Annotations: title="Check datasources health", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Check datasource health. Filter by type or UIDs; omit both to check all.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `type` | `string` | no |  |  | Plugin type filter; omit to check all |
| `uids` | `[]string` | no |  |  | UIDs to check |
| `offset` | `int` | no | 0 |  | Number to skip for pagination |

#### `search_docs`

Category: `docs` · Code: [tools/docs.go:162](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/docs.go#L162) · Annotations: title="Search Docs", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=true · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Search Grafana documentation. Returns matching pages with title, URL, description, and product. Call with no query to list available product groups.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | no |  |  | Search query for Grafana documentation. Omit to list all available product groups. |
| `product` | `string` | no |  |  | Filter results to a specific product (e.g. 'Grafana Tempo', 'Grafana Loki') |
| `limit` | `int` | no |  |  | Maximum results to return (default 5) |

#### `get_doc`

Category: `docs` · Code: [tools/docs.go:232](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/docs.go#L232) · Annotations: title="Get Doc", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=true · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Fetch a Grafana documentation page. Set outline_only=true to get the heading structure first, then call again with a section name for bounded retrieval.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `url` | `string` | yes |  |  | The grafana.com/docs/ URL to fetch |
| `outline_only` | `bool` | no |  |  | Return only the heading outline (use to discover section names before fetching content) |
| `section` | `string` | no |  |  | Heading text to extract (returns only that section) |
| `offset` | `int` | no |  |  | Line offset for paging (0-indexed) |
| `limit` | `int` | no |  |  | Max lines to return (default ~80) |

#### `query_elasticsearch`

Category: `elasticsearch` · Code: [tools/elasticsearch.go:51](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/elasticsearch.go#L51) · Annotations: title="Query Elasticsearch", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Executes a search query against an Elasticsearch or OpenSearch datasource and retrieves matching documents. Supports Lucene query syntax (e.g., 'status:200 AND host:server1') for both Elasticsearch and OpenSearch. Elasticsearch Query DSL JSON is also supported for Elasticsearch datasources only (not OpenSearch). Returns a list of documents with their index, ID, source fields, and optional score. Use this to search logs, metrics, or any indexed data stored in Elasticsearch or OpenSearch. Defaults to 10 results and sorts by @timestamp in descending order (newest first).
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Elasticsearch or OpenSearch datasource to query |
| `index` | `string` | yes |  |  | The index pattern to search (e.g., 'logs-*', 'filebeat-*', or a specific index name) |
| `query` | `string` | yes |  |  | The search query. For Elasticsearch datasources, this can be either Lucene query syntax (e.g., 'status:200 AND host:server1') or Elasticsearch Query DSL JSON (for advanced queries with aggregations). For OpenSearch datasources, only Lucene query syntax is supported. |
| `startTime` | `string` | no |  |  | Optionally, the start time. Filters results to documents with the configured time field (default @timestamp) >= this value. Supports RFC3339 (e.g. '2024-01-01T00:00:00Z'), relative to now (e.g. 'now', 'now-1h', 'now-30m'), or Unix timestamps |
| `endTime` | `string` | no |  |  | Optionally, the end time. Filters results to documents with the configured time field (default @timestamp) <= this value. Supports RFC3339 (e.g. '2024-01-01T23:59:59Z'), relative to now (e.g. 'now', 'now-1h'), or Unix timestamps |
| `limit` | `int` | no | 10 |  | Optionally, the maximum number of documents to return (max: 100, default: 10) |

#### `get_query_examples`

Category: `examples` · Code: [tools/examples.go:292](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/examples.go#L292) · Annotations: title="Get query examples", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Get example queries for a specific datasource type. Provides sample queries with descriptions for Prometheus (PromQL), Loki (LogQL), ClickHouse (SQL with Grafana macros), CloudWatch (metric configurations), and InfluxDB (Flux and InfluxQL). Use this to understand query syntax and common patterns for each datasource.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceType` | `string` | yes |  |  | The datasource type to get examples for (e.g. 'prometheus', 'loki', 'clickhouse', 'cloudwatch', 'influxdb') |

#### `create_folder`

Category: `folder` · Code: [tools/folder.go:43](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/folder.go#L43) · Annotations: title="Create folder", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `folders:read`, `folders:create`, `folders:write`

Description (verbatim):

```text
Create a Grafana folder. Provide a title and optional UID. Returns the created folder.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `title` | `string` | yes |  |  | The title of the folder. |
| `uid` | `string` | no |  |  | Optional folder UID. If omitted, Grafana will generate one. |
| `parentUid` | `string` | no |  |  | Optional parent folder UID. If set, the folder will be created under this parent. |

#### `query_graphite`

Category: `graphite` · Code: [tools/graphite.go:243](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L243) · Annotations: title="Query Graphite metrics", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Executes a Graphite render API query against a Graphite datasource and returns matching metric series with their datapoints. Supports the full Graphite target expression language including wildcard patterns (e.g. 'servers.web*.cpu.load5'), aggregation functions (e.g. 'sumSeries(app.*.requests)'), and tag-based queries (e.g. 'seriesByTag(\'name=cpu.load\')'). Datapoints with no recorded value are returned with a null value field. Time range defaults to the last hour if not specified.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Graphite datasource to query |
| `target` | `string` | yes |  |  | The Graphite target expression to evaluate (e.g. 'servers.web*.cpu.load5', 'sumSeries(app.*.requests)', 'seriesByTag(\\'name=cpu.load\\')') |
| `from` | `string` | no |  |  | Start of the time range. Accepts RFC3339 (e.g. '2024-01-01T00:00:00Z') or Graphite relative times (e.g. '-1h', '-24h'). Defaults to '-1h'. |
| `until` | `string` | no |  |  | End of the time range. Accepts RFC3339 or Graphite relative times (e.g. 'now'). Defaults to 'now'. |
| `maxDataPoints` | `int` | no |  |  | Optional maximum number of data points per series. Graphite consolidates data when the requested range exceeds this value. |

#### `list_graphite_metrics`

Category: `graphite` · Code: [tools/graphite.go:321](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L321) · Annotations: title="List Graphite metrics", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Discover available metric paths in a Graphite datasource by browsing the metric tree. Returns nodes matching the query pattern, each indicating whether it is a leaf metric (has data) or an expandable branch (has children). Use '*' as a wildcard at any level to enumerate the tree (e.g. '*' → top-level nodes, 'servers.*' → all second-level nodes under 'servers').
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Graphite datasource to query |
| `query` | `string` | yes |  |  | Metric path pattern to search. Use '*' as a wildcard at any level (e.g. '*' lists top-level nodes, 'servers.*' lists all servers, 'servers.web01.*' lists all metrics under web01). |

#### `list_graphite_tags`

Category: `graphite` · Code: [tools/graphite.go:371](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L371) · Annotations: title="List Graphite tags", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List available tag names in a Graphite datasource that uses tag-based metrics. Returns a list of tag name strings (e.g. ["name", "env", "region"]). These tags can be used to build tag-based target expressions (e.g. seriesByTag('name=cpu.load,env=prod')). Optionally filter by a prefix. Requires Graphite to be configured with tag support.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Graphite datasource to query |
| `prefix` | `string` | no |  |  | Optional prefix to filter tag names (e.g. 'env' returns tags whose name starts with 'env'). |

#### `query_graphite_density`

Category: `graphite` · Code: [tools/graphite.go:513](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/graphite.go#L513) · Annotations: title="Query Graphite metric density", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Analyses metric data density for one or more Graphite series over a time window. Returns per-series statistics: fillRatio (fraction of non-null datapoints, 0.0–1.0), totalPoints, nonNullPoints, lastSeen (Unix timestamp of most recent non-null value, or null if none), longestGap (longest consecutive null run in seconds), and estimatedInterval (inferred write interval in seconds). Supports wildcard targets (e.g. 'obox-cl*.sys.sessions') to diagnose stale, sparse, or dead metrics across a cluster. A fillRatio of 0 with lastSeen null means the series reported no data in the requested window.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Graphite datasource to query |
| `target` | `string` | yes |  |  | Graphite target expression; supports wildcards (e.g. 'obox-cl*.sys.sessions') |
| `from` | `string` | no |  |  | Start of the time range. Accepts RFC3339 or Graphite relative times (e.g. '-1h'). Defaults to '-1h'. |
| `until` | `string` | no |  |  | End of the time range. Accepts RFC3339 or Graphite relative times (e.g. 'now'). Defaults to 'now'. |

#### `list_incidents`

Category: `incident` · Code: [tools/incident.go:150](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L150) · Annotations: title="List incidents", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `incidentAccess...`

Description (verbatim):

```text
List Grafana incidents. Allows filtering by status ('active', 'resolved') and optionally including drill incidents. Returns a preview list with basic details, and custom field values if requested.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `limit` | `int` | no | 10 |  | The maximum number of incidents to return |
| `drill` | `bool` | no |  |  | Whether to include drill incidents |
| `status` | `string` | no |  |  | The status of the incidents to include. Valid values: 'active', 'resolved' |
| `includeCustomFields` | `bool` | no |  |  | Whether to include each incident's custom field values. Off by default because it costs an extra request and makes the response considerably larger |

#### `create_incident`

Category: `incident` · Code: [tools/incident.go:215](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L215) · Annotations: title="Create incident", readOnlyHint=false, destructiveHint=false, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `incidentAccess...`

Description (verbatim):

```text
Create a new Grafana incident. Requires title, severity, and room prefix. Allows setting status, labels and custom fields. Creating an incident may notify or page many people.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `title` | `string` | yes |  |  | The title of the incident |
| `severity` | `string` | yes |  |  | The severity of the incident |
| `roomPrefix` | `string` | yes |  |  | The prefix of the room to create the incident in |
| `isDrill` | `bool` | no |  |  | Whether the incident is a drill incident |
| `status` | `string` | no |  |  | The status of the incident |
| `attachCaption` | `string` | no |  |  | The caption of the attachment |
| `attachUrl` | `string` | no |  |  | The URL of the attachment |
| `labels` | `[]incident.IncidentLabel` | no |  |  | The labels to add to the incident |
| `customFields` | `[]IncidentCustomFieldInput` | no |  |  | Custom field values to set on the new incident |

#### `add_activity_to_incident`

Category: `incident` · Code: [tools/incident.go:247](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L247) · Annotations: title="Add activity to incident", readOnlyHint=false, destructiveHint=false, idempotentHint=—, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `incidentAccess...`

Description (verbatim):

```text
Add a note (userNote activity) to an existing incident's timeline using its ID. The note body can include URLs which will be attached as context. Use this to add context to an incident.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `incidentId` | `string` | yes |  |  | The ID of the incident to add the activity to |
| `body` | `string` | yes |  |  | The body of the activity. URLs will be parsed and attached as context |
| `eventTime` | `string` | no |  |  | The time that the activity occurred. If not provided, the current time will be used |

#### `get_incident`

Category: `incident` · Code: [tools/incident.go:287](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L287) · Annotations: title="Get incident details", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `incidentAccess...`

Description (verbatim):

```text
Get a single incident by ID. Returns the full incident details including title, status, severity, labels, custom fields, timestamps, and other metadata.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `id` | `string` | yes |  |  | The ID of the incident to retrieve |

#### `update_incident`

Category: `incident` · Code: [tools/incident.go:379](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident.go#L379) · Annotations: title="Update incident", readOnlyHint=false, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `incidentAccess...`

Description (verbatim):

```text
Update an existing Grafana incident by ID. Allows changing the status ('active' or 'resolved'), the severity, the title, and custom field values. Only the provided fields are changed. Use this to resolve an incident, to correct its severity or title, or to fill in custom fields as part of an on-call workflow.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `incidentId` | `string` | yes |  |  | The ID of the incident to update |
| `status` | `string` | no |  |  | The new status of the incident. Valid values: 'active', 'resolved' |
| `severity` | `string` | no |  |  | The new severity of the incident, e.g. 'minor', 'major', 'critical' |
| `title` | `string` | no |  |  | The new title of the incident |
| `customFields` | `[]IncidentCustomFieldInput` | no |  |  | Custom field values to set. Only the listed fields are changed |

#### `list_incident_custom_fields`

Category: `incident` · Code: [tools/incident_custom_fields.go:92](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/incident_custom_fields.go#L92) · Annotations: title="List incident custom fields", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `incidentAccess...`

Description (verbatim):

```text
List the custom fields configured for Grafana incidents, including their type and, for select fields, the options that may be chosen.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `includeArchived` | `bool` | no |  |  | Whether to include archived custom fields. Archived fields cannot be set on new incidents but may still hold values on older ones |

#### `query_influxdb`

Category: `influxdb` · Code: [tools/influxdb.go:208](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/influxdb.go#L208) · Annotations: title="Query InfluxDB", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Query an InfluxDB datasource via Grafana. Supports both InfluxQL (v1.x) and Flux (v2.x). The 'dialect' parameter selects the query language; if omitted it's inferred from the datasource configuration.

Time formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms)

InfluxQL example: SELECT mean("value") FROM "cpu" WHERE time > now() - 1h GROUP BY time(1m)
Flux example:    from(bucket: "metrics") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "cpu")
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the InfluxDB datasource to query. |
| `query` | `string` | yes |  |  | Raw query string. InfluxQL for v1.x datasources (e.g. SELECT * FROM cpu WHERE time > now() - 1h), or Flux for v2.x datasources (e.g. from(bucket: \"mybucket\") \|> range(start: -1h)). |
| `dialect` | `string` | no |  |  | Query dialect: 'influxql' or 'flux'. If omitted, inferred from the datasource's configured query language (v1 -> influxql, v2 -> flux). |
| `start` | `string` | no |  |  | Start time for the query. Time formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms). Defaults to 1 hour ago. |
| `end` | `string` | no |  |  | End time for the query. Time formats: 'now', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms). Defaults to now. |
| `maxDataPoints` | `int` | no |  |  | Maximum number of data points to return. Default: 1000. |

#### `list_loki_label_names`

Category: `loki` · Code: [tools/loki.go:249](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L249) · Annotations: title="List Loki label names", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Lists all available label/field names (keys) found in logs within a specified Loki or VictoriaLogs datasource and time range. Returns a list of unique label strings (e.g., `["app", "env", "pod"]`). If the time range is not provided, it defaults to the last hour. Optionally narrow the search to a subset of streams with `matcher` (e.g. `{namespace="prod"}`).
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `matcher` | `string` | no |  |  | Optionally, a stream selector to narrow the search to matching streams (Loki: LogQL, e.g. '{namespace=\"prod\"}'; VictoriaLogs: LogsQL). Defaults to searching across all streams. |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') (defaults to now) |

#### `list_loki_label_values`

Category: `loki` · Code: [tools/loki.go:300](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L300) · Annotations: title="List Loki label values", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Retrieves all unique values associated with a specific `labelName` within a Loki or VictoriaLogs datasource and time range. Returns a list of string values (e.g., for `labelName="env"`, might return `["prod", "staging", "dev"]`). Useful for discovering filter options. Defaults to the last hour if the time range is omitted. Optionally narrow the search to a subset of streams with `matcher` (e.g. `{namespace="prod"}`) — for example, to list `service` values seen only within a specific namespace.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `labelName` | `string` | yes |  |  | The name of the label to retrieve values for (e.g. 'app', 'env', 'pod') |
| `matcher` | `string` | no |  |  | Optionally, a stream selector to narrow the search to matching streams (Loki: LogQL, e.g. '{namespace=\"prod\"}'; VictoriaLogs: LogsQL). Defaults to searching across all streams. |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') (defaults to now) |

#### `query_loki_logs`

Category: `loki` · Code: [tools/loki.go:963](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L963) · Annotations: title="Query Loki logs", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Executes a log query against a Loki or VictoriaLogs datasource and returns matching log entries (or metric samples on Loki). Defaults to the last hour, a limit of 10 entries, and 'backward' direction (newest first). The `logql` parameter takes LogQL on Loki and LogsQL on VictoriaLogs (e.g., Loki: `{app="foo"} |= "error"`; VictoriaLogs: `{app="foo"} "error"`). To count matching log lines precisely, use a `count_over_time()` metric query with queryType='instant'. For broad queries that match many lines, set `format` to 'compact' to group results by stream and avoid repeating label metadata on every line. Query cost is the bytes scanned, which the index statistics for the stream selector over the same time range estimate before a broad selector or long time range is run. If this server enables the Loki cost guardrail, expensive queries are rejected before execution: query cost is bytes SCANNED, determined only by the stream selector and time range — line filters (|=) and parsers (| json) reduce what is returned, not what is scanned. Use a stream selector with at least one selective positive label matcher (never `{}`, `=~".*"`/`=~".+"`, or negative-only matchers), keep time ranges narrow; rejected queries return rewrite guidance.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `logql` | `string` | yes |  |  | The LogQL query to execute against Loki. This can be a simple label matcher or a complex query with filters, parsers, and expressions. Supports full LogQL syntax including label matchers, filter operators, pattern expressions, and pipeline operations. |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') |
| `limit` | `int` | no | 10 |  | Optionally, the maximum number of log lines to return (default max: 100, configurable by MCP server). |
| `direction` | `string` | no |  |  | Optionally, the direction of the query: 'forward' (oldest first) or 'backward' (newest first, default) |
| `queryType` | `string` | no |  |  | Query type: 'range' (default) or 'instant'. Instant queries return a single value at one point in time. Range queries return values over a time window. Use 'instant' for metric queries when you want the current value. |
| `stepSeconds` | `int` | no |  |  | Resolution step in seconds for range metric queries. When running metric queries with queryType='range', this controls the time resolution of the returned data points. |
| `format` | `string` | no |  | full, compact | Output format for log (streams) queries: 'full' (default) returns every entry with its own label metadata; 'compact' groups lines by stream so each label set is emitted only once, substantially reducing response size for broad queries. Structured metadata keys that are constant within a stream appear once on the stream header; keys that vary across lines appear per-line. Ignored for metric queries. |

#### `query_loki_stats`

Category: `loki` · Code: [tools/loki.go:1082](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L1082) · Annotations: title="Get Loki log statistics", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Retrieves index-level statistics about log streams matching a given selector within a Loki or VictoriaLogs datasource and time range. Returns an object containing the count of streams, chunks, entries, and total bytes (e.g., `{"streams": 5, "chunks": 50, "entries": 10000, "bytes": 512000}`). **Important**: the `entries` count reflects storage-level index entries (chunk metadata), NOT the number of individual log lines matching the selector. Counting actual matching log lines requires a `count_over_time()` LogQL metric query. On VictoriaLogs only `entries` is populated; the other fields remain zero. The `logql` parameter **must** be a simple label selector (e.g., `{app="nginx", env="prod"}`) and does not support line filters, parsers, or aggregations. The `bytes` field estimates how much data a log query over the same selector and time range would scan, which is useful to know before running a broad selector or long time range. Defaults to the last hour if the time range is omitted.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `logql` | `string` | yes |  |  | The LogQL matcher expression to execute. This parameter only accepts label matcher expressions and does not support full LogQL queries. Line filters, pattern operations, and metric aggregations are not supported by the stats API endpoint. Only simple label selectors can be used here. |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') |

#### `query_loki_patterns`

Category: `loki` · Code: [tools/loki.go:1134](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki.go#L1134) · Annotations: title="Query Loki patterns", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Retrieves detected log patterns from a Loki datasource for a given stream selector and time range. Returns a list of patterns, each containing a pattern string and a total count of occurrences. Patterns help identify common log structures and anomalies. The `logql` parameter must be a stream selector (e.g., `{job="nginx"}`) and does not support line filters or aggregations. Defaults to the last hour if the time range is omitted. **Not supported on VictoriaLogs** datasources - use a `| stats` pipeline instead.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `logql` | `string` | yes |  |  | A LogQL stream selector to identify the logs to analyze for patterns (e.g. {job=\"foo\", namespace=\"bar\"}) |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') (defaults to now) |
| `step` | `string` | no |  |  | Optionally, the query resolution step (e.g. '5m') |

#### `analyze_loki_labels`

Category: `loki` · Code: [tools/loki_label_analyzer.go:1006](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/loki_label_analyzer.go#L1006) · Annotations: title="Analyze Loki label strategy", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Audits a Loki label strategy and optionally diagnoses query performance. Returns per-label verdicts, missing base labels, normalisation issues, and a recommended set. Pass datasourceUid for live cardinality or labels for static scoring; both may be combined.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | no |  |  | Datasource UID (live mode). |
| `labels` | `[]LabelDescriptor` | no |  |  | Caller-supplied labels (static mode). |
| `selector` | `string` | no |  |  | Optional LogQL selector for stats / perf diagnosis. |
| `maxLabels` | `int` | no |  |  |  |
| `startRfc3339` | `string` | no |  |  |  |
| `endRfc3339` | `string` | no |  |  |  |
| `expectedBaseLabels` | `[]string` | no |  |  |  |
| `perfMetrics` | `*QueryPerfMetrics` | no |  |  | Runtime metrics; presence triggers perf diagnosis. |

#### `generate_deeplink` (variant 1 of 2)

Category: `navigation` · Code: [tools/navigation.go:314](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/navigation.go#L314) · Annotations: title="Generate navigation deeplink", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Generate deeplink URLs for Grafana resources. Supports dashboards (requires dashboardUid or provisioningPreview), panels (requires dashboardUid or provisioningPreview, plus panelId), and Explore queries (requires datasourceUid and optionally queries). For dashboard and panel links, provisioningPreview points at a dashboard staged on a provisioning repository branch (e.g. a git-sync PR preview). For explore links, the time range and queries are embedded inside the Grafana explore state. Set shorten=true to return a /goto/<uid> short URL instead; if shortening fails, an error containing the full deeplink is returned.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `resourceType` | `string` | yes |  |  | Type of resource: dashboard, panel, or explore |
| `dashboardUid` | `*string` | no |  |  | Dashboard UID (for stored dashboards). Mutually exclusive with provisioningPreview for dashboard and panel types. |
| `provisioningPreview` | `*DeeplinkProvisioningPreview` | no |  |  | Identifies a dashboard staged on a provisioning repository branch (e.g. a git-sync PR preview). Mutually exclusive with dashboardUid for dashboard and panel types. |
| `datasourceUid` | `*string` | no |  |  | Datasource UID (required for explore type) |
| `panelId` | `*int` | no |  |  | Panel ID (required for panel type) |
| `queries` | `[]map[string]interface{}` | no |  |  | List of query objects for explore links (e.g. [{\"refId\":\"A\",\"expr\":\"up\"}]) |
| `queryParams` | `map[string]string` | no |  |  | Additional URL query parameters (for dashboard/panel types) |
| `timeRange` | `*TimeRange` | no |  |  | Time range for the link |
| `shorten` | `bool` | no |  |  | If true, try to shorten the generated URL to /goto/<uid>. If shortening fails, an error containing the full deeplink is returned. |

#### `generate_deeplink` (variant 2 of 2)

Category: `navigation` · Code: [tools/navigation.go:326](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/navigation.go#L326) · Annotations: title="Generate navigation deeplink", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Generate deeplink URLs for Grafana resources. Supports dashboards (requires dashboardUid or provisioningPreview), panels (requires dashboardUid or provisioningPreview, plus panelId), and Explore queries (requires datasourceUid and optionally queries). For dashboard and panel links, provisioningPreview points at a dashboard staged on a provisioning repository branch (e.g. a git-sync PR preview). In read-only mode, shorten=true is accepted but ignored and the full deeplink is returned.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `resourceType` | `string` | yes |  |  | Type of resource: dashboard, panel, or explore |
| `dashboardUid` | `*string` | no |  |  | Dashboard UID (for stored dashboards). Mutually exclusive with provisioningPreview for dashboard and panel types. |
| `provisioningPreview` | `*DeeplinkProvisioningPreview` | no |  |  | Identifies a dashboard staged on a provisioning repository branch (e.g. a git-sync PR preview). Mutually exclusive with dashboardUid for dashboard and panel types. |
| `datasourceUid` | `*string` | no |  |  | Datasource UID (required for explore type) |
| `panelId` | `*int` | no |  |  | Panel ID (required for panel type) |
| `queries` | `[]map[string]interface{}` | no |  |  | List of query objects for explore links (e.g. [{\"refId\":\"A\",\"expr\":\"up\"}]) |
| `queryParams` | `map[string]string` | no |  |  | Additional URL query parameters (for dashboard/panel types) |
| `timeRange` | `*TimeRange` | no |  |  | Time range for the link |
| `shorten` | `bool` | no |  |  | If true, try to shorten the generated URL to /goto/<uid>. If shortening fails, an error containing the full deeplink is returned. |

#### `list_oncall_schedules`

Category: `oncall` · Code: [tools/oncall.go:200](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L200) · Annotations: title="List OnCall schedules", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.schedules:read`

Description (verbatim):

```text
List Grafana OnCall schedules, optionally filtering by team ID. If a specific schedule ID is provided, retrieves details for only that schedule. Returns a list of schedule summaries including ID, name, team ID, timezone, and shift IDs. Supports pagination.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `teamId` | `string` | no |  |  | The ID of the team to list schedules for |
| `scheduleId` | `string` | no |  |  | The ID of the schedule to get details for. If provided, returns only that schedule's details |
| `page` | `int` | no |  |  | The page number to return (1-based) |

#### `get_oncall_shift`

Category: `oncall` · Code: [tools/oncall.go:253](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L253) · Annotations: title="Get OnCall shift", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.schedules:read`

Description (verbatim):

```text
Get detailed information for a specific Grafana OnCall shift using its ID. A shift represents a designated time period within a schedule when users are actively on-call. Returns the full shift details.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `shiftId` | `string` | yes |  |  | The ID of the shift to get details for |

#### `get_current_oncall_users`

Category: `oncall` · Code: [tools/oncall.go:324](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L324) · Annotations: title="Get current on-call users", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.schedules:read`, `grafana-irm-app.user-settings:read`

Description (verbatim):

```text
Get the list of users currently on-call for a specific Grafana OnCall schedule ID. Returns the schedule ID, name, and a list of detailed user objects for those currently on call.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `scheduleId` | `string` | yes |  |  | The ID of the schedule to get current on-call users for |

#### `list_oncall_teams`

Category: `oncall` · Code: [tools/oncall.go:380](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L380) · Annotations: title="List OnCall teams", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.user-settings:read`

Description (verbatim):

```text
List teams configured in Grafana OnCall. Returns a list of team objects with their details. Supports pagination.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `page` | `int` | no |  |  | The page number to return |

#### `list_oncall_users`

Category: `oncall` · Code: [tools/oncall.go:453](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L453) · Annotations: title="List OnCall users", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.user-settings:read`

Description (verbatim):

```text
List users from Grafana OnCall. These are OnCall users (separate from Grafana users). Can retrieve all users in the OnCall directory, a specific user by ID, or filter by username. Returns a list of user objects with their details. Supports pagination.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `userId` | `string` | no |  |  | The ID of the user to get details for. If provided, returns only that user's details |
| `username` | `string` | no |  |  | The username to filter users by. If provided, returns only the user matching this username |
| `page` | `int` | no |  |  | The page number to return |

#### `list_alert_groups`

Category: `oncall` · Code: [tools/oncall.go:545](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L545) · Annotations: title="List IRM alert groups", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.alert-groups:read`

Description (verbatim):

```text
List alert groups from Grafana OnCall with filtering options. Supports filtering by alert group ID, route ID, integration ID, state (new, acknowledged, resolved, silenced), team ID, time range, labels, and name. For time ranges, use format '{start}_{end}' ISO 8601 timestamp range (e.g., '2025-01-19T00:00:00_2025-01-19T23:59:59' for a specific day). For labels, use format 'key:value' (e.g., ['env:prod', 'severity:high']). Returns a list of alert group objects with their details. Supports pagination.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `page` | `int` | no |  |  | The page number to return |
| `id` | `string` | no |  |  | Filter by specific alert group ID |
| `routeId` | `string` | no |  |  | Filter by route ID |
| `integrationId` | `string` | no |  |  | Filter by integration ID |
| `state` | `string` | no |  |  | Filter by alert group state (one of: new, acknowledged, resolved, silenced) |
| `teamId` | `string` | no |  |  | Filter by team ID |
| `startedAt` | `string` | no |  |  | Filter by time range in format '{start}_{end}' ISO 8601 timestamp range (UTC assumed, no timezone indicator needed) (e.g., '2025-01-19T00:00:00_2025-01-19T23:59:59') |
| `labels` | `[]string` | no |  |  | Filter by labels in format key:value (e.g., ['env:prod', 'severity:high']) |
| `name` | `string` | no |  |  | Filter by alert group name |

#### `get_alert_group`

Category: `oncall` · Code: [tools/oncall.go:619](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L619) · Annotations: title="Get IRM alert group", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.alert-groups:read`

Description (verbatim):

```text
Get a specific alert group from Grafana OnCall by its ID. Returns the full alert group details, including the most recent alert and its raw payload when the OnCall API provides them. Alert payloads carry integration-specific fingerprints (for example Sentry's payload.data.event.hashes or Alertmanager's payload.alerts[].fingerprint) that identify recurring alerts across different alert groups.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `alertGroupId` | `string` | yes |  |  | The ID of the alert group to retrieve |

#### `update_alert_group`

Category: `oncall` · Code: [tools/oncall.go:727](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/oncall.go#L727) · Annotations: title="Update IRM alert group", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`, `grafana-irm-app.alert-groups:read`, `grafana-irm-app.alert-groups:write`

Description (verbatim):

```text
Update the state of a Grafana OnCall alert group: acknowledge, unacknowledge, resolve, or unresolve it by ID. Returns the alert group's resulting OnCall state (one of new, acknowledged, resolved, silenced), or a stateWarning explaining why that state could not be read back after a successful update.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `alertGroupId` | `string` | yes |  |  | The ID of the alert group to update |
| `state` | `string` | yes |  |  | New state for the alert group. One of: acknowledged, unacknowledged, resolved, unresolved |

#### `get_plugin`

Category: `plugin` · Code: [tools/plugins.go:124](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/plugins.go#L124) · Annotations: title="Get plugin", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `plugins.app:access`

Description (verbatim):

```text
Check whether a Grafana plugin is installed and retrieve its details (name, version, type, enabled status). Returns installed=false when the plugin is not found.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `pluginId` | `string` | yes |  |  | The plugin ID to check (e.g. 'prometheus', 'grafana-piechart-panel', 'grafana-oncall-app') |

#### `install_plugin`

Category: `plugin` · Code: [tools/plugins.go:257](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/plugins.go#L257) · Annotations: title="Install plugin", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=true · `_meta.grafana.com/requiredPermissions`: `plugins:install`

Description (verbatim):

```text
Install a Grafana plugin by its plugin ID. When version is omitted, the tool looks up the latest version and returns it without installing; supplying a version installs that version.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `pluginId` | `string` | yes |  |  | The plugin ID to install (e.g. 'grafana-image-renderer', 'grafana-piechart-panel') |
| `version` | `string` | no |  |  | The exact version to install. When omitted, the tool returns the latest available version without installing. |

#### `search_plugin_information`

Category: `plugin` · Code: [tools/plugins.go:426](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/plugins.go#L426) · Annotations: title="Search plugins", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=true · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Search the Grafana plugin catalog by keyword, purpose, or partial name (e.g. 'azure monitoring', 'loki', 'database'). Returns results sorted by trust: official Grafana Labs plugins first, then commercial partner plugins, then community plugins, each with its exact pluginId. Results include warnings for enterprise-only or Angular-based plugins.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | yes |  |  | Keyword to search for plugins (e.g. 'azure', 'prometheus', 'loki', 'database'). Matches against plugin name, slug, description, and keywords. |

#### `list_prometheus_metric_metadata`

Category: `prometheus` · Code: [tools/prometheus.go:58](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L58) · Annotations: title="List Prometheus metric metadata", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List Prometheus metric metadata. Returns metadata about metrics currently scraped from targets. Note: This endpoint is experimental.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `limit` | `int` | no | 10 |  | The maximum number of metrics to return |
| `limitPerMetric` | `int` | no |  |  | The maximum number of metrics to return per metric |
| `metric` | `string` | no |  |  | The metric to query |
| `projectName` | `string` | no |  |  | GCP project name to query (Cloud Monitoring datasources only). Overrides or substitutes the defaultProject configured on the datasource. |

#### `query_prometheus`

Category: `prometheus` · Code: [tools/prometheus.go:290](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L290) · Annotations: title="Query Prometheus metrics", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Query a PromQL-compatible datasource (Prometheus, Thanos, Mimir, Cloud Monitoring, etc.) using a PromQL expression. Supports instant queries (single point) and range queries (time range). Time: RFC3339 or relative expressions like 'now', 'now-1h'.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `expr` | `string` | yes |  |  | The PromQL expression to query |
| `startTime` | `string` | no |  |  | The start time. Required if queryType is 'range', ignored if queryType is 'instant' Supported formats are RFC3339 or relative to now (e.g. 'now', 'now-1.5h', 'now-2h45m'). Valid time units are 'ns', 'us' (or 'µs'), 'ms', 's', 'm', 'h', 'd'. |
| `endTime` | `string` | yes |  |  | The end time. Supported formats are RFC3339 or relative to now (e.g. 'now', 'now-1.5h', 'now-2h45m'). Valid time units are 'ns', 'us' (or 'µs'), 'ms', 's', 'm', 'h', 'd'. |
| `stepSeconds` | `int` | no |  |  | The time series step size in seconds. Required if queryType is 'range', ignored if queryType is 'instant' |
| `queryType` | `string` | no |  |  | The type of query to use. Either 'range' or 'instant' |
| `projectName` | `string` | no |  |  | GCP project name to query (Cloud Monitoring datasources only). Overrides or substitutes the defaultProject configured on the datasource. |

#### `list_prometheus_metric_names`

Category: `prometheus` · Code: [tools/prometheus.go:367](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L367) · Annotations: title="List Prometheus metric names", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Lists metric names in a PromQL-compatible datasource (Prometheus, Thanos, Mimir, Cloud Monitoring, etc.). Filters metric names using the provided regex. Supports pagination (page * limit must not exceed 10000) and an optional time range to restrict results to metrics active within that window. Cloud Monitoring ignores the time range.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `regex` | `string` | no |  |  | The regex to match against the metric names |
| `limit` | `int` | no | 10 |  | The maximum number of results to return |
| `page` | `int` | no | 1 |  | The page number to return |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the time range to filter the results by. Supports RFC3339 or relative time (e.g. 'now-1h') |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the time range to filter the results by. Supports RFC3339 or relative time (e.g. 'now') |
| `projectName` | `string` | no |  |  | GCP project name to query (Cloud Monitoring datasources only). Overrides or substitutes the defaultProject configured on the datasource. |

#### `list_prometheus_label_names`

Category: `prometheus` · Code: [tools/prometheus.go:517](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L517) · Annotations: title="List Prometheus label names", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List label names in a PromQL-compatible datasource (Prometheus, Thanos, Mimir, Cloud Monitoring, etc.). Allows filtering by series selectors and time range.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `matches` | `[]Selector` | no |  |  | Optionally, a list of label matchers to filter the results by |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the time range to filter the results by. Supports RFC3339 or relative time (e.g. 'now-1h') |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the time range to filter the results by. Supports RFC3339 or relative time (e.g. 'now') |
| `limit` | `int` | no | 100 |  | Optionally, the maximum number of results to return |
| `projectName` | `string` | no |  |  | GCP project name to query (Cloud Monitoring datasources only). Overrides or substitutes the defaultProject configured on the datasource. |

#### `list_prometheus_label_values`

Category: `prometheus` · Code: [tools/prometheus.go:574](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L574) · Annotations: title="List Prometheus label values", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Gets the values for a specific label name in a PromQL-compatible datasource (Prometheus, Thanos, Mimir, Cloud Monitoring, etc.). Allows filtering by series selectors and time range.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the datasource to query |
| `labelName` | `string` | yes |  |  | The name of the label to query |
| `matches` | `[]Selector` | no |  |  | Optionally, a list of selectors to filter the results by |
| `startRfc3339` | `string` | no |  |  | Optionally, the start time of the query. Supports RFC3339 or relative time (e.g. 'now-1h') |
| `endRfc3339` | `string` | no |  |  | Optionally, the end time of the query. Supports RFC3339 or relative time (e.g. 'now') |
| `limit` | `int` | no | 100 |  | Optionally, the maximum number of results to return |
| `projectName` | `string` | no |  |  | GCP project name to query (Cloud Monitoring datasources only). Overrides or substitutes the defaultProject configured on the datasource. |

#### `query_prometheus_histogram`

Category: `prometheus` · Code: [tools/prometheus.go:727](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/prometheus.go#L727) · Annotations: title="Query Prometheus histogram percentile", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Query Prometheus histogram percentiles from classic histogram '_bucket' series.

Generates histogram_quantile PromQL. Example: metric='http_duration', percentile=95, labels='job="api"'

Time formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms)
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Prometheus datasource |
| `metric` | `string` | yes |  |  | Base histogram metric name (without _bucket suffix) |
| `percentile` | `float64` | yes |  |  | Percentile to calculate (e.g. 50, 90, 95, 99) |
| `labels` | `string` | no |  |  | Label selector (e.g. job=\"api\", service=\"gateway\") |
| `rateInterval` | `string` | no |  |  | Rate interval for the query (default: 5m) |
| `startTime` | `string` | no |  |  | Start time (default: now-1h). Supports RFC3339, relative (now-1h), or Unix ms. |
| `endTime` | `string` | no |  |  | End time (default: now). Supports RFC3339, relative, or Unix ms. |
| `stepSeconds` | `int` | no |  |  | Step size in seconds for range query (default: 60) |
| `projectName` | `string` | no |  |  | GCP project name to query (Cloud Monitoring datasources only). Overrides or substitutes the defaultProject configured on the datasource. |

#### `list_provisioning_repositories`

Category: `provisioning` · Code: [tools/provisioning.go:159](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/provisioning.go#L159) · Annotations: title="List provisioning repositories", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `provisioning.repositories:read`, `provisioning.grafana.app/repositories:list`

Description (verbatim):

```text
List provisioning repositories (e.g. git-sync sources) configured for this Grafana instance. Returns each repository's slug along with its source URL, branch, path, sync state, and health. The `name` is the slug used to render not-yet-applied dashboard previews.
```

_No parameters._

#### `validate_provisioning_file`

Category: `provisioning` · Code: [tools/provisioning.go:384](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/provisioning.go#L384) · Annotations: title="Validate provisioning file", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `provisioning.repositories:read`, `provisioning.grafana.app/repositories:get`, `dashboards:read`, `dashboard.grafana.app/dashboards:get`, `folders:read`, `folder.grafana.app/folders:get`

Description (verbatim):

```text
Validate a file in a provisioning repository at a given branch or commit by dry-run applying it. Returns whether the file would be accepted (valid), what resource action would result (create/update), the target resource type, and any structured validation errors. Use to confirm a draft dashboard or other resource will be accepted before merging or applying a PR — this is the same validation surface that Grafana's PR commenter reports.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `repo` | `string` | yes |  |  | Provisioning repository slug (the repository name). |
| `path` | `string` | yes |  |  | File path within the repository (e.g. 'folder/dashboard.json'). |
| `ref` | `string` | no |  |  | Branch or commit SHA. Defaults to the repository's main branch. |

#### `list_pyroscope_label_names`

Category: `pyroscope` · Code: [tools/pyroscope.go:44](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L44) · Annotations: title="List Pyroscope label names", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text

Lists all available label names (keys) found in profiles within a specified Pyroscope datasource, time range, and
optional label matchers. Label matchers are typically used to qualify a service name ({service_name="foo"}). Returns a
list of unique label strings (e.g., ["app", "env", "pod"]). Label names with double underscores (e.g. __name__) are
internal and rarely useful to users. If the time range is not provided, it defaults to the last hour.

```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `data_source_uid` | `string` | yes |  |  | The UID of the datasource to query |
| `matchers` | `string` | no |  |  |  |
| `start_rfc_3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `end_rfc_3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') (defaults to now) |

#### `list_pyroscope_label_values`

Category: `pyroscope` · Code: [tools/pyroscope.go:106](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L106) · Annotations: title="List Pyroscope label values", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text

Lists all available label values for a particular label name found in profiles within a specified Pyroscope datasource,
time range, and optional label matchers. Label matchers are typically used to qualify a service name ({service_name="foo"}).
Returns a list of unique label strings (e.g. for label name "env": ["dev", "staging", "prod"]). If the time range
is not provided, it defaults to the last hour.

```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `data_source_uid` | `string` | yes |  |  | The UID of the datasource to query |
| `name` | `string` | yes |  |  | A label name |
| `matchers` | `string` | no |  |  | Optionally, Prometheus style matchers used to filter the result set (defaults to: {}) |
| `start_rfc_3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `end_rfc_3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') (defaults to now) |

#### `list_pyroscope_profile_types`

Category: `pyroscope` · Code: [tools/pyroscope.go:184](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L184) · Annotations: title="List Pyroscope profile types", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text

Lists all available profile types available in a specified Pyroscope datasource and time range. Returns a list of all
available profile types (example profile type: "process_cpu:cpu:nanoseconds:cpu:nanoseconds"). A profile type has the
following structure: <name>:<sample type>:<sample unit>:<period type>:<period unit>. Not all profile types are available
for every service. If the time range is not provided, it defaults to the last hour.

```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `data_source_uid` | `string` | yes |  |  | The UID of the datasource to query |
| `start_rfc_3339` | `string` | no |  |  | Optionally, the start time of the query in RFC3339 format or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `end_rfc_3339` | `string` | no |  |  | Optionally, the end time of the query in RFC3339 format or relative time (e.g. 'now') (defaults to now) |

#### `query_pyroscope`

Category: `pyroscope` · Code: [tools/pyroscope.go:640](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/pyroscope.go#L640) · Annotations: title="Query Pyroscope", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text

Unified Pyroscope query tool for fetching profiles or metrics from Pyroscope. Profile data shows WHICH functions consume resources; metrics data
shows WHEN consumption spiked. Use query_type="both" for complete analysis in one call.

query_type options (extends Grafana's PyroscopeQueryType):
- "profile": returns profile data (shape controlled by format)
- "metrics": returns time-series data points
- "both" (default): returns both profile and metrics in one response

format options (shape of the profile data):
- "table" (default): per-function table with flat (self) and cumulative values, ranked by flat
- "dot": call graph in Graphviz DOT format; nodes are per source line, so one function may span several nodes

```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `data_source_uid` | `string` | yes |  |  | The UID of the datasource to query |
| `profile_type` | `string` | yes |  |  | The profile type (e.g. process_cpu:cpu:nanoseconds:cpu:nanoseconds) |
| `query_type` | `string` | no |  |  | Query type: \"profile\" (flamegraph), \"metrics\" (time-series), or \"both\" (default). Use \"both\" for complete analysis |
| `format` | `string` | no |  |  | Profile output format: \"table\" (default) for a per-function flat/cum table, or \"dot\" for a call graph in Graphviz DOT format |
| `matchers` | `string` | no |  |  | Prometheus style matchers (defaults to: {}) |
| `group_by` | `[]string` | no |  |  | Labels to group metrics series by |
| `step` | `float64` | no |  |  | Seconds between metrics data points (default: auto) |
| `max_node_depth` | `int` | no |  |  | Max functions in the profile table or nodes in the call graph; it is a count, not a depth (default: 100) |
| `start_rfc_3339` | `string` | no |  |  | Start time in RFC3339 or relative time (e.g. 'now-1h') (defaults to 1 hour ago) |
| `end_rfc_3339` | `string` | no |  |  | End time in RFC3339 or relative time (e.g. 'now') (defaults to now) |

#### `query_quickwit`

Category: `quickwit` · Code: [tools/quickwit.go:257](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/quickwit.go#L257) · Annotations: title="Query Quickwit", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Executes a search query against a Quickwit datasource and retrieves matching documents. Supports Lucene query syntax (e.g., 'severity_text:ERROR AND service_name:api') and partial Elasticsearch-compatible Query DSL JSON. The timestamp field is resolved from Quickwit index metadata (not jsonData.timeField). Returns a list of documents with their index, ID, source fields, and optional score. Use this to search logs or other indexed data stored in Quickwit. Defaults to 10 results and sorts by the index timestamp field in descending order (newest first).
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | The UID of the Quickwit datasource to query |
| `index` | `string` | no |  |  | Optionally, the index or index pattern to search. Defaults to the index configured on the datasource (jsonData.index) |
| `query` | `string` | yes |  |  | The search query in Lucene syntax (e.g., 'severity_text:ERROR AND service_name:api') or partial Elasticsearch-compatible Query DSL JSON |
| `startTime` | `string` | no |  |  | Optionally, the start time. Filters results to documents with timestamp >= this value. Supports RFC3339 (e.g. '2024-01-01T00:00:00Z'), relative to now (e.g. 'now', 'now-1h', 'now-30m'), or Unix timestamps |
| `endTime` | `string` | no |  |  | Optionally, the end time. Filters results to documents with timestamp <= this value. Supports RFC3339 (e.g. '2024-01-01T23:59:59Z'), relative to now (e.g. 'now', 'now-1h'), or Unix timestamps |
| `limit` | `int` | no | 10 |  | Optionally, the maximum number of documents to return (max: 100, default: 10) |

#### `get_panel_image`

Category: `rendering` · Code: [tools/rendering.go:507](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/rendering.go#L507) · Annotations: title="Get panel or dashboard image", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboards:read`, `datasourceQuery...`, `datasources:explore`, `provisioning.repositories:read`

Description (verbatim):

```text
Render a Grafana dashboard panel, full dashboard or Explore view as a PNG image. Returns the image as base64 encoded data. Requires the Grafana Image Renderer service to be installed. Exactly one of dashboardUid (for stored dashboards), provisioningPreview (for dashboards staged on a provisioning repository branch, e.g. a git-sync PR) or explore (an ad-hoc datasource query rendered in Explore, no saved dashboard needed) must be supplied. Defaults in CSS pixels: panel 1000x750, dashboard 1200x900, Explore 1000x1000. Scale defaults to 1 for all views and is clamped to 1-3. Use this for generating visual snapshots of dashboards for reports, alerts, or presentations.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `dashboardUid` | `string` | no |  |  | The UID of a stored dashboard containing the panel. Required unless provisioningPreview is provided. |
| `panelId` | `*int` | no |  |  | The ID of the panel to render. If omitted, the entire dashboard is rendered |
| `width` | `*int` | no |  |  | Positive viewport width in CSS pixels. See tool description for per-view defaults. Capped so width times scale is at most 3000. The renderer may raise values below its configured minimum (1000 by default). |
| `height` | `*int` | no |  |  | Positive viewport height in CSS pixels, or -1 for full-page rendering. See tool description for per-view defaults. Positive heights are capped so height times scale is at most 3000. The renderer may raise values below its configured minimum (500 by default). |
| `timeRange` | `*RenderTimeRange` | no |  |  | Time range for the rendered image |
| `variables` | `map[string]StringOrSlice` | no |  |  | Dashboard variables to apply. Values can be a single string or an array of strings for multi-value variables (e.g., {\"var-datasource\": \"prometheus\", \"var-instance\": [\"server1\", \"server2\"]}) |
| `theme` | `*string` | no |  |  | Theme for the rendered image: light or dark. Defaults to dark |
| `scale` | `*int` | no |  |  | Image scale factor. See tool description for default and limits. Higher scales reduce the maximum allowed viewport dimensions. |
| `timeout` | `*int` | no |  |  | Rendering timeout in seconds. Defaults to 60, capped at 120 |
| `provisioningPreview` | `*ProvisioningPreview` | no |  |  | Render a dashboard from a provisioning repository branch (e.g. a git-sync PR preview). Mutually exclusive with dashboardUid. |
| `explore` | `*RenderExplore` | no |  |  | Render an ad-hoc Explore view for a datasource and queries instead of a stored dashboard. Mutually exclusive with dashboardUid and provisioningPreview. Requires Grafana 10.2 or later. |

#### `run_panel_query`

Category: `runpanelquery` · Code: [tools/run_panel_query.go:1197](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/run_panel_query.go#L1197) · Annotations: title="Run panel query", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboardRead...`, `datasourceQuery...`

Description (verbatim):

```text
Executes one or more dashboard panel queries with optional time range and variable overrides. Accepts an array of panel IDs to query in a single call. Fetches the dashboard, extracts queries from the specified panels, substitutes template variables and Grafana macros ($__range, $__rate_interval, $__interval), and routes to the appropriate datasource (Prometheus, Loki, ClickHouse, CloudWatch, InfluxDB, BigQuery, MSSQL, PostgreSQL, or Infinity with a backend parser). Returns results keyed by panel ID - partial failures are allowed (some panels can succeed while others fail). If a panel uses a template variable datasource you cannot access, provide datasourceUid and datasourceType to override.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `dashboardUid` | `string` | yes |  |  | Dashboard UID |
| `panelIds` | `[]int` | yes |  |  | Panel IDs to execute (one or more) |
| `queryIndex` | `*int` | no |  |  | Index of the query to execute per panel (0-based, defaults to 0). |
| `start` | `string` | no |  |  | Override start time (e.g. 'now-1h', RFC3339, Unix ms) |
| `end` | `string` | no |  |  | Override end time (e.g. 'now', RFC3339, Unix ms) |
| `variables` | `map[string]string` | no |  |  | Override dashboard variables (e.g. {\"job\": \"api-server\"}) |
| `datasourceUid` | `string` | no |  |  | Override datasource UID |
| `datasourceType` | `string` | no |  |  | Fallback datasource type used only when the datasource cannot be read (prometheus, loki, grafana-clickhouse-datasource, cloudwatch, influxdb, grafana-bigquery-datasource, mssql, grafana-postgresql-datasource, postgres). When the datasource is readable its real type is used and this is ignored. |

#### `search_dashboards`

Category: `search` · Code: [tools/search.go:115](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/search.go#L115) · Annotations: title="Search dashboards", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `dashboards:read`, `folders:read`

Description (verbatim):

```text
Search Grafana dashboards by query and/or folderUid, tag, and starred. Returns matching dashboards with title, UID, folder, tags, and URL.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | no |  |  | Optional query. Omit to filter by folderUid, tag, or starred |
| `folderUid` | `string` | no |  |  | Optional immediate folder UID (not nested) |
| `tag` | `[]string` | no |  |  | Optional tags to match (AND) |
| `starred` | `bool` | no |  |  | If true, only starred dashboards |
| `limit` | `int` | no | 50 |  | Maximum number of results to return (max 100) |
| `page` | `int` | no | 1 |  | Page number for pagination (1-indexed) |

#### `search_folders`

Category: `search` · Code: [tools/search.go:148](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/search.go#L148) · Annotations: title="Search folders", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `folders:read`

Description (verbatim):

```text
Search for Grafana folders by a query string. Returns matching folders with details like title, UID, and URL.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | no |  |  | The query to search for |

#### `list_snapshots`

Category: `snapshot` · Code: [tools/snapshot.go:226](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L226) · Annotations: title="List snapshots", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `snapshots:read`

Description (verbatim):

```text
List Grafana dashboard snapshots with optional query and result limit filters.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `query` | `string` | no |  |  | Optional search query for snapshot name |
| `limit` | `*int` | no |  |  | Maximum number of snapshots to return (Grafana defaults to 1000 when omitted) |

#### `get_snapshot`

Category: `snapshot` · Code: [tools/snapshot.go:238](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L238) · Annotations: title="Get snapshot", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Get a Grafana snapshot by key, including snapshot metadata and dashboard payload.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `key` | `string` | yes |  |  | Snapshot key to retrieve |

#### `create_snapshot`

Category: `snapshot` · Code: [tools/snapshot.go:250](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L250) · Annotations: title="Create snapshot", readOnlyHint=false, destructiveHint=false, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `snapshots:create`, `dashboards:read`

Description (verbatim):

```text
Create a Grafana snapshot from a full dashboard payload. Supports optional expiration and external snapshot fields.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `dashboard` | `map[string]any` | yes |  |  | Complete dashboard model to snapshot (as returned by Grafana dashboard APIs) |
| `name` | `string` | no |  |  | Optional snapshot name |
| `expires` | `*int64` | no |  |  | Snapshot expiration in seconds (e.g. 3600 for 1 hour) |
| `external` | `*bool` | no |  |  | Store snapshot on external server. Requires key and deleteKey when true |
| `key` | `string` | no |  |  | Custom snapshot key. Required when external is true |
| `deleteKey` | `string` | no |  |  | Secret key for deleting external snapshots. Required when external is true |

#### `delete_snapshot`

Category: `snapshot` · Code: [tools/snapshot.go:262](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/snapshot.go#L262) · Annotations: title="Delete snapshot", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `snapshots:delete`, `dashboards:write`

Description (verbatim):

```text
Delete a Grafana snapshot by snapshot key.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `key` | `string` | yes |  |  | Snapshot key to delete |

#### `query_sql`

Category: `sql` · Code: [tools/sql_tools.go:265](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L265) · Annotations: title="Query SQL", readOnlyHint=false, destructiveHint=true, idempotentHint=false, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Query a supported SQL datasource (ClickHouse, Snowflake, Athena, MySQL, PostgreSQL, MSSQL) via Grafana.

Supports datasource-specific macros: $__timeFilter(column), $__from/$__to, $__interval, ${varname}

Time formats: 'now-1h', '2026-02-02T19:00:00Z', '1738519200000' (Unix ms)

Example: SELECT timestamp, message FROM logs WHERE $__timeFilter(timestamp) LIMIT 100
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| _(embedded struct `QuerySQLParams`, not parsed)_ | | | | | |

#### `list_sql_databases`

Category: `sql` · Code: [tools/sql_tools.go:283](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L283) · Annotations: title="List SQL databases", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List databases, schemas, or catalogs from a supported SQL datasource. Returns the organizational units (databases, schemas, or catalogs) that contain tables. For Athena: omit catalog to list catalogs, or pass catalog to list databases in it.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| _(embedded struct `ListSQLDatabasesParams`, not parsed)_ | | | | | |

#### `list_sql_tables`

Category: `sql` · Code: [tools/sql_tools.go:295](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L295) · Annotations: title="List SQL tables", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List tables from a supported SQL datasource (ClickHouse, Snowflake, Athena, MySQL, PostgreSQL, MSSQL). Returns table names, schemas, and metadata.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| _(embedded struct `ListSQLTablesParams`, not parsed)_ | | | | | |

#### `describe_sql_table`

Category: `sql` · Code: [tools/sql_tools.go:307](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/sql_tools.go#L307) · Annotations: title="Describe SQL table", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Get column schema for a table in a supported SQL datasource (ClickHouse, Snowflake, Athena, MySQL, PostgreSQL, MSSQL). Returns column names and types.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| _(embedded struct `DescribeSQLTableParams`, not parsed)_ | | | | | |

#### `search_tempo_traces`

Category: `tempo` · Code: [tools/tempo.go:699](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L699) · Annotations: title="Search Tempo traces", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Search for traces using TraceQL queries
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | UID of the tempo datasource to query |
| `query` | `string` | yes |  |  | TraceQL query string |
| `start` | `string` | no |  |  | Start time for the search (RFC3339 format). If not provided will search the past 1 hour. If provided, must be before end. |
| `end` | `string` | no |  |  | End time for the search (RFC3339 format). If not provided will search the past 1 hour. If provided, must be after start. |

#### `query_tempo_metrics`

Category: `tempo` · Code: [tools/tempo.go:711](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L711) · Annotations: title="Query Tempo metrics", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Compute trace-derived metrics using a TraceQL metrics query. The syntax is unlike PromQL. Use type 'instant' for a single value or 'range' for a time series (default). Instant queries over large time ranges may timeout — keep the window under 15 minutes for instant, or use range instead.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | UID of the tempo datasource to query |
| `query` | `string` | yes |  |  | TraceQL metrics query of the form '{ <selector> } \| <aggregation> [by (<attribute>)]'. Example: '{ } \| quantile_over_time(span:duration, .99) by (span.name)'. |
| `type` | `string` | no | range | instant, range | Query type: 'instant' returns a single value at the end of the time range; 'range' returns a time series. Default is 'range'. |
| `start` | `string` | no |  |  | Start time (RFC3339 format). If not provided will search the past 1 hour. |
| `end` | `string` | no |  |  | End time (RFC3339 format). If not provided will search the past 1 hour. |

#### `get_tempo_trace`

Category: `tempo` · Code: [tools/tempo.go:723](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L723) · Annotations: title="Get Tempo trace", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Retrieve a specific trace by ID
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `focus_span_id` | `*string` | no |  |  | Optional 16-character hexadecimal span ID to select initially. The full trace remains available. |
| `datasourceUid` | `string` | yes |  |  | UID of the tempo datasource to query |
| `trace_id` | `string` | yes |  |  | Trace ID to retrieve |

#### `diff_tempo_traces`

Category: `tempo` · Code: [tools/tempo.go:736](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L736) · Annotations: title="Diff Tempo traces", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
Compare two complete traces. Returns a compact summary and includes the full span-level patch when it is at most 64 KiB. Request trace-patch-v0 only when full details are required; full patches are not size-bounded.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | UID of the tempo datasource to query |
| `base_trace_id` | `string` | yes |  |  | Trace ID for the baseline trace |
| `compare_trace_id` | `string` | yes |  |  | Trace ID for the comparison trace |
| `base_start` | `string` | no |  |  | Optional start of the baseline trace search range in RFC3339 format. Must be provided with base_end. |
| `base_end` | `string` | no |  |  | Optional end of the baseline trace search range in RFC3339 format. Must be provided with base_start. |
| `compare_start` | `string` | no |  |  | Optional start of the comparison trace search range in RFC3339 format. Must be provided with compare_end. |
| `compare_end` | `string` | no |  |  | Optional end of the comparison trace search range in RFC3339 format. Must be provided with compare_start. |
| `format` | `string` | no | trace-summary-v0-composed | trace-summary-v0-composed, trace-summary-v0-native, trace-patch-v0 | Output format. The composed format returns a compact summary and attaches the full patch only when it is at most 64 KiB. trace-patch-v0 has no output-size guarantee. |

#### `list_tempo_attribute_names`

Category: `tempo` · Code: [tools/tempo.go:748](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L748) · Annotations: title="List Tempo attribute names", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List available attribute names for TraceQL queries. Without a scope (resource, span, etc.) the response can be very large.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | UID of the tempo datasource to query |
| `scope` | `string` | no |  |  | Scope to filter attributes by (span, resource, event, link, instrumentation). Strongly recommended — omitting scope returns all attributes across all scopes which can be very large (100K+ chars). |

#### `list_tempo_attribute_values`

Category: `tempo` · Code: [tools/tempo.go:760](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L760) · Annotations: title="List Tempo attribute values", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: `datasourceQuery...`

Description (verbatim):

```text
List values for a fully scoped attribute name (e.g. resource.service.name). Useful for discovering what values exist for a specific attribute.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `datasourceUid` | `string` | yes |  |  | UID of the tempo datasource to query |
| `name` | `string` | yes |  |  | The attribute name to get values for (e.g. 'span.http.method', 'resource.service.name') |
| `filter-query` | `string` | no |  |  | Filter query to apply to the attribute values. It can only have one spanset and only &&'ed conditions like { <cond> && <cond> && ... }. This is useful for filtering the values to a specific set of values. |

#### `get_tempo_traceql_docs`

Category: `tempo` · Code: [tools/tempo.go:772](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/tempo.go#L772) · Annotations: title="Get TraceQL documentation", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Retrieve TraceQL reference documentation with examples, covering attribute filters, aggregates, structural operators, and metrics queries. Consult this before writing a non-trivial TraceQL query, or after one returns an error or no results.
```

| Parameter | Type (Go) | Req. | Default | Enum | Description (verbatim) |
|---|---|---|---|---|---|
| `topic` | `string` | yes |  | basic, aggregates, structural, metrics | Which section of the TraceQL reference to retrieve: 'basic' for attribute and duration filters, 'aggregates' for count/avg/sum and by() grouping, 'structural' for parent/child and descendant operators, 'metrics' for rate/quantile_over_time metrics queries |

#### `user_info`

Category: `user` · Code: [tools/user.go:45](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/tools/user.go#L45) · Annotations: title="Get current user info", readOnlyHint=true, destructiveHint=false, idempotentHint=true, openWorldHint=false · `_meta.grafana.com/requiredPermissions`: —

Description (verbatim):

```text
Get information about the current Grafana identity: login, email, name, whether it is a Grafana (server) admin, the current organization, and the organizations it can access (with roles). Call this to discover which orgId values are valid before targeting a specific organization, and to understand the identity's capabilities.
```

_No parameters._

## 3. Resources (MCP Apps UI)

- `ui://mcp-grafana/panel-viewer.html` — [ui_apps.go:11](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/ui_apps.go#L11)
- `ui://grafana/metrics.html` — [ui_metrics.go:11](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/ui_metrics.go#L11)
- `ui://grafana/trace.html` — [ui_trace.go:11](https://github.com/grafana/mcp-grafana/blob/e97cd4479eb40d25bc8d466db1651c29ce0c783e/ui_trace.go#L11)
