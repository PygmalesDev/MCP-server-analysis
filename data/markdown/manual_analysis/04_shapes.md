# MCP server: Shapes

> **In plain words.** Shapes (shapes.co) is an HR platform: employee directory, time off, working time tracking, performance reviews, surveys, knowledge base. Its MCP server lets an AI assistant **read** the company's HR data and compute statistics on it (headcount, distributions, time off, review results). Data cannot be changed through this server.
>
> **Analysis date:** 12.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Abbreviations in links:**
- `[mcp-page]` = the server page https://mcp.shapes.co/ (developer documentation).
- `[landing]` = https://shapes.co/mcp (link from the CSV).
- `[prm]` = OAuth protected resource metadata https://mcp.shapes.co/.well-known/oauth-protected-resource.
- `[asm]` = authorization server metadata https://mcp.shapes.co/.well-known/oauth-authorization-server.

---

## ⚠️ Important limitation of the analysis

**The server code is closed**: the repository is not published, and the Shapes pages contain no links to it [landing], [mcp-page]. The server requires sign-in (HTTP 401), so **the exact tool list with descriptions (`tools/list`) cannot be obtained without a Shapes account**. The analysis is based on the documentation and public OAuth metadata. The tool names are taken from the page [mcp-page]. Their exact descriptions and parameter schemas are **not published**.

Note: the website getknit.dev has a "Shapes MCP Server" with 25 writing actions (terminating an employee, changing a salary etc.). This is a **third-party Knit wrapper**, not the official server, and it is not part of this analysis ([getknit.dev](https://getknit.dev/mcp-servers/shapes)).

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Shapes MCP | [prm] (`resource_name: "Shapes MCP"`) |
| Code link | Not published | [landing], [mcp-page] |
| Documentation | https://shapes.co/mcp (from the CSV); technical page: https://mcp.shapes.co/ | CSV, [claude.com/connectors/shapes](https://claude.com/connectors/shapes) |
| Endpoint | `https://mcp.shapes.co/mcp` (the instructions on [landing] give `http://` without the S — probably a typo) | CSV, [prm], [landing] |
| MCP version | Not published (cannot be found out without signing in) | — |
| Commit / date | Not applicable (code closed). Date of the documentation snapshot: 12.10.2026 | — |
| Language / MCP SDK | Not published | — |
| Transport | Streamable HTTP (URL `/mcp`) | [mcp-page] |
| Code open? License | No, proprietary | — |
| Company | DreamTeam HR Apps Ltd. (d/b/a Shapes); the privacy policy refers to the Israeli Protection of Privacy Law (PPL) | [privacy](https://shapes.co/privacy-policy) |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | Only for Shapes customers: "Existing Shapes customers can connect directly", everyone else is invited to contact sales. No separate price for MCP is given; MCP is not mentioned in the feature lists of the plans | [landing], [pricing](https://shapes.co/pricing) |
| Linked software | Paid (SaaS). **Core: $8 per seat per month**, **Plus: $12 per seat per month** (billed annually), there is a minimum subscription (size not given). Surveys, Performance and Compensation are separate paid modules (prices on request) | [pricing](https://shapes.co/pricing) |
| Access restrictions | (1) Sign-in via OAuth, each employee signs in with **their own** Shapes account. (2) "Your existing Shapes permissions carry through to every Claude conversation" — the user's rights in Shapes carry over to the AI. (3) The connector in Claude is set up by the organisation's administrator | [landing], [mcp-page] |
| Controlled by | Rights — the administrators of the Shapes HR system at the customer. Access to the server — Shapes (subscription) | same |
| Rate limits | Not documented | — |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **35** tools, "All tools are read-only — no data is modified through the MCP server". Groups: employees (8), performance reviews (7), time off (8), surveys (4), attendance (2), working time policies (1), knowledge base (2), helpdesk (3). There are "aggregate_*" tools for computing statistics | **Not published verbatim.** Only the names are known (list in section E) [mcp-page] | Not documented. Judging by the description: lists of records and aggregates ("counts, percentages, and distributions") [mcp-page] |
| Resources | ❓ | Not documented. The only OAuth scope is `mcp:tools` [prm] — an indirect sign that there are only tools | — | — |
| Prompts | ❓ | [mcp-page] mentions "built-in skills". How they are implemented (MCP prompts or otherwise) is not stated | — | — |
| Logging / Sampling / Roots / Elicitation / Tasks / Subscription / Progress / Cancellation | ❓ | Not documented; cannot be checked without signing in | — | — |
| **Authorization** | ✅ | OAuth 2.0 + PKCE [mcp-page]. According to the metadata: **Metadata Doc** — yes (`/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server`); **Dynamic Client Registration** — yes (`registration_endpoint: https://mcp.shapes.co/register`); grant types `authorization_code`, `refresh_token`; PKCE `S256`; the only scope `mcp:tools`. **Authorization server** — `https://mcp.shapes.co` itself (sign-in with a Shapes account) | [prm], [asm] | — |
| Configuration | ❌ | No settings for the user ("No API keys required") | [mcp-page] | — |
| Error Reporting | ❓ | Not documented | — | — |

## D. Server logic beyond simply passing commands through

According to the documentation (cannot be checked against the code):
1. **Read-only at the level of the whole server.** There are no writing tools at all. This is the strongest possible restriction.
2. **The user's rights carry over:** "you can only access data you're authorized to see" [mcp-page]; "No one sees more than they should" [landing]. Filtering happens on the Shapes side according to the rights of the signed-in employee.
3. **Aggregating tools** (`aggregate_employees`, `aggregate_time_away_bookings` etc.): the server computes statistics itself instead of returning raw records. This may reduce the amount of personal data reaching the AI, but the documentation does not claim this.
4. **"My" tools** (`list_my_performance_review_participations`, `list_my_survey_participations`, `get_current_employee`) — separate tools for the user's own data.
5. Human confirmation, confidence scores, logging — not described.

**Server structure:** according to the documentation, standard (a flat set of tools).

## E. Overall evaluation

**Number of actions:** **35** (according to [mcp-page]; the page says "35+ tools"). All are reads.

| Group | Tools |
|---|---|
| Employees (8) | `list_employees`, `aggregate_employees`, `get_current_employee`, `get_reporting_chain`, `list_entities`, `list_employee_field_types`, `list_employee_field_value_changes`, `list_profile_pictures` |
| Performance reviews (7) | `list_performance_review_cycles`, `list_performance_review_participations`, `list_performance_review_reviewers`, `list_my_performance_review_participations`, `list_my_performance_review_reviews`, `aggregate_performance_review_cycles`, `aggregate_performance_review_participations` |
| Time off (8) | `list_time_away_bookings`, `list_time_away_balances`, `list_time_away_reasons`, `list_time_away_reason_policies`, `list_time_away_policy_assignments`, `list_time_away_days_grants`, `list_time_away_holidays`, `aggregate_time_away_bookings` |
| Surveys (4) | `list_surveys`, `list_survey_participations`, `list_my_survey_participations`, `aggregate_survey_participations` |
| Attendance (2) | `list_attendances`, `list_attendance_submissions` |
| Working time (1) | `list_time_management_policies` |
| Knowledge base (2) | `list_knowledge_base_files`, `search_knowledge_base` |
| Helpdesk (3) | `list_helpdesk_collections`, `search_helpdesk`, `read_helpdesk_article` |

**Action parameters:** not published (not available without signing in).

**Tokens before the first action:** cannot be determined (descriptions not published).

**What the agent CANNOT do but a human can:**
- **Any changes**: create or change an employee, book time off, submit a survey answer, carry out a review, upload a document, sign a document (Docs & eSign) [mcp-page] vs [shapes.co](https://shapes.co).
- **Compensation:** [landing] and [claude.com/connectors/shapes](https://claude.com/connectors/shapes) promise analysis of "compensation gaps", but **there is no separate tool for salary data in the list**. The data may be available via employee fields (`list_employee_field_types`), but the documentation does not confirm this. **The contradiction should be checked.**
- Shapes AI functions (Vibe Views, Shapes Agents, Workflows) — not available via MCP.

## F. Documentation analysis

**Recommendations to the user that the server does not check:** none explicit. There are no recommendations on human confirmation of actions (not needed: the server only reads) or on handling personal data in an AI chat.

**Promises on governance and data:**
- "Shapes is SOC2 certified and GDPR compliant so your people data stays protected, always" [landing].
- "Your permissions carry over" / "No one sees more than they should" [mcp-page], [landing].
- Privacy policy: AI features may run via third-party LLM providers (not named); data is stored in Israel, the EEA, the UK, the USA and elsewhere; Shapes may train models on product usage data after removing personal data; processing of customer data is governed by a DPA and the "AI Modules Schedule" [privacy](https://shapes.co/privacy-policy).
- **Important:** the HR data received by the AI client (Claude etc.) goes to a third party — the AI provider. The MCP documentation does not warn about this.

**Promises to the user:** "Connect in minutes. No engineering required."; the AI will be able to answer about "attrition risk, headcount, and compensation gaps" [landing].

**Comparison with the server logic:** the "read-only" promise is confirmed by the tool list: the names contain only `list_`, `get_`, `aggregate_`, `search_`, `read_`. The promise about compensation analysis is not confirmed by the tool list.

---

## Observations for the research

- **The "safest" design:** the server only reads, and rights are inherited from the user. The risks shift towards **confidentiality** rather than actions: the AI sees sensitive HR data (the examples mention "gender breakdown", birthdays, time-off balances).
- **Aggregating tools** are a separate design technique: the server computes statistics itself instead of giving the AI raw records.
- **Third-party wrappers** (Knit) with write rights exist in parallel with the official server. For the research it is important to distinguish the official server from intermediaries.
- **Closed code + OAuth:** without a customer account a researcher cannot obtain even the tool descriptions.
