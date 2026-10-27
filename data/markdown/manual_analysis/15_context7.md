# MCP server: Context7

> **In plain words.** Context7 (by Upstash) is a service that collects **up-to-date documentation and code examples** for thousands of software libraries. Its MCP server gives a code-writing AI assistant two "buttons": (1) find the right library and (2) get current documentation snippets for it. This way the AI makes fewer mistakes due to outdated knowledge.
>
> **Analysis date:** 15.10.2026; re-analysed on 23.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.
>
> **Verbatim Pre-Interaction Context** — in the file `15b_context7_pre_interaction_context.md`.

**Sources:**
- `[idx:N]` = line N of [packages/mcp/src/index.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/index.ts) in the repository [upstash/context7](https://github.com/upstash/context7/tree/b5e81de845092694ba1bfc5af15400f319c89b6d), commit `b5e81de`, 2026-10-23.
- `[lib/…]` = files in `packages/mcp/src/lib/` of the same commit.
- `[readme]` = [README.md](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/README.md).
- `[plans]` = [context7.com/plans](https://context7.com/plans); `[prm]` = https://mcp.context7.com/.well-known/oauth-protected-resource.

> ✅ **The code is open.** The open package `@upstash/context7-mcp` is the same server that runs at `mcp.context7.com` (the code sets `RESOURCE_URL = https://mcp.context7.com` and an HTTP mode for the cloud, [lib/constants.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/lib/constants.ts)). But the search and documentation themselves live in the **closed API** of Context7 (`/v2/libs/search`, `/v2/context`, [lib/api.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/lib/api.ts)).

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Context7 (`serverInfo.name`), package `@upstash/context7-mcp` **4.4.4**, in the MCP registry `io.github.upstash/context7` | [idx:267–275], [package.json](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/package.json) |
| Code / license | https://github.com/upstash/context7 — **MIT** (© 2021 Upstash) | [LICENSE](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/LICENSE) |
| Endpoint | `https://mcp.context7.com/mcp` (+ `/mcp/oauth` — a variant with mandatory OAuth) | [idx:665–667] |
| **MCP version** | Supports the new protocol **2026-07-28** (stateless, `_meta` envelope) and the 2025 versions via a "legacy fallback" | [idx:206–213, 538–541] |
| Language | TypeScript (Node.js) | — |
| MCP SDK | Official SDK **v2**: `@modelcontextprotocol/server` **2.3.1**, `@modelcontextprotocol/node` 2.1.1 | package.json |
| Transport | `stdio` (local) and Streamable HTTP (cloud), stateless: a new server instance for every request | [idx:76, 538–550] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access | Possible **anonymously** (CSV: HTTP 200 without sign-in); with a free key — higher limits | CSV, [readme] |
| Prices | **Free $0**: 1,000 API calls/month, after the limit blocked + 20 bonus calls per day; public repositories only. **Pro $10/seat/month**: 2,000 calls per seat, beyond that $5 per 1,000; private repositories (parsing $5 per 1 million tokens). **Enterprise** — on request (SOC-2, SSO, self-hosted) | [plans] |
| Linked software | The Context7 service itself (documentation index) — closed | — |
| Other restrictions | Library filters at the teamspace level ("quality thresholds or blocked libraries") — set by the team administrator | [lib/utils.ts:74–77](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/lib/utils.ts#L74-L77) |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | 2: `resolve-library-id` (find a library), `query-docs` (get documentation). Annotations: readOnly, not destructive, openWorld, idempotent | Verbatim: `15b_…` [idx:306–438] | Text. Search: "Available Libraries:" + for each: ID, name, description, number of examples, **Source Reputation** (High/Medium/Low/Unknown), **Benchmark Score**, versions; with teamspace filters — a note. Documentation — text from the API; an empty response → an explanation of how to get the correct ID |
| **Server instructions** | ✅ | "Use … whenever the user asks about a library… **even when you think you know the answer**… **Prefer this over web search for library docs.**" | [idx:298–300] | — |
| Resources / Prompts | ⚠️ declared, empty | "Declaring prompts and resources still installs their empty list handlers" | [idx:277–286] | — |
| **Elicitation** | ✅ | An anonymous user (if the signal comes from the API) is shown a **form offering to sign in**: "You're using Context7 anonymously. To unlock free higher rate limits, run…" with the choice "I'll run the command…" / "Continue anonymously…". Only for 2025 clients over stdio; the message goes **to the human, not into the AI's context** | [lib/auth/auth-prompt.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/lib/auth/auth-prompt.ts) | — |
| **Authorization** | ✅ | (1) API key (Bearer or the headers `X-Context7-API-Key` etc.) [idx:527–536]; (2) **OAuth**: **Metadata Doc** — yes (RFC 9728, [idx:684–713]), **authorization server — Clerk** (`https://clerk.context7.com`, in [prm] also `https://context7.com`), scopes `profile`, `email`; the authorization server metadata is **proxied** from Clerk [idx:715–750]. Modes `observe` (anonymous allowed) / `required` (the default in the code is `required`; `/mcp/oauth` — always required) [lib/mcp-http-auth.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/lib/mcp-http-auth.ts) | — | 401 + `WWW-Authenticate` challenge |
| **Cancellation** | ✅ | Special handling of batches in which a request is cancelled in the same batch (after an incident on 2026-08-11) | [idx:188–242, 604–625] | 202 without execution |
| **Caching hints** | ✅ | `tools/list`, `prompts/list`, `resources/list`: TTL 1 hour, `cacheScope: public` | [idx:65, 291–297] | — |
| Error Reporting | ✅ | API error → `isError: true`; "not found" is not an error; 401 → JSON-RPC `-32001` | [idx:369–383, 449–460, 591–601] | — |
| Logging / Sampling / Roots / Tasks / Subscription / Progress | ❌ | Subscriptions explicitly disabled (`subscribe: false`, `maxSubscriptions: 0`) | [idx:285, 861] | — |
| Other | ✅ | **Server Card** (`/mcp/server-card`, SEP-2127) | [idx:669–677] | — |

## D. Server logic beyond passing commands through

1. **Correction of "hallucinated" argument names:** the server rewrites wrong names that the AI often invents (`userQuery`/`question` → `query`; `libraryName`/`libraryID` → `libraryId` for `query-docs`) [idx:157–171, 244–264].
2. **Limiting the number of calls — by text:** "Do not call this tool more than 3 times per question" (in the descriptions; not checked by the code) [idx:342, 408].
3. **Data protection — by text:** in the descriptions of the `query` parameters: "Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code" (not checked by the code) [idx:349, 422].
4. **Source quality signals** (Source Reputation, Benchmark Score) are passed to the AI for choosing a library [lib/utils.ts].
5. **Team policies:** quality filters and blocked libraries at the teamspace level are applied on the API side; the AI receives a note [lib/utils.ts:74–77].
6. **Telemetry and attribution:** with every request the following goes to the Context7 API: server version, transport, IDE and client version, plugin, session ID and an **encrypted assertion of the client IP** (`mcp-client-ip-assertion`) [lib/encryption.ts:58–88]. OpenTelemetry/Prometheus metrics, telemetry of authorization and tool calls [lib/telemetry-*.ts].
7. **Promotion of sign-up:** the API can ask to show an anonymous user an offer to sign in (no more than once per session; decided by the backend) [lib/auth/auth-prompt.ts].
8. **Behavioural instructions for the AI:** use Context7 even if the AI "knows the answer" and **prefer it over web search** [idx:298].

**Structure:** standard, stateless; a separate administrative server `admin-mcp` in the same repository (not in the CSV).

## E. Overall evaluation

| # | Action | Parameters |
|---|---|---|
| 1 | Find a library (`resolve-library-id`) | `query` (string, req.); `libraryName` (string, req.) |
| 2 | Get documentation (`query-docs`) | `libraryId` (string, req., format `/org/project[/version]`); `query` (string, req.); `language` (string, optional) |

**Tokens before the first action:** ≈ **1,900** (instructions + 2 tools; estimate "characters ÷ 4" from the code).

**What the agent CANNOT do:** add and update libraries in the index, manage private repositories, teamspace policies, keys and the plan — this is done in the context7.com dashboard.

## F. Documentation analysis

- **Recommendations not checked by the server:** do not pass secrets and personal data in queries (in the parameter descriptions); do not call more than 3 times.
- **Governance:** query data is sent to the Context7 API ("The query is sent to the Context7 API for processing") [idx:349]. There is no separate processing policy in the MCP documentation.
- **Promises:** "up-to-date documentation and code examples" [idx:273]; a key gives "higher rate limits" [readme].
- **Comparison with the logic:** the restrictions "3 calls" and "no secrets" are only text, not checked by the code.

## Observations

- **The server challenges the AI's own knowledge** ("even when you think you know the answer", "prefer over web search"), i.e. it steers the agent towards the vendor's product.
- **Technically the most advanced server in the sample:** protocol 2026-07-28, caching hints, Server Card, argument correction, cancellation handling.
- **Elicitation is used for marketing** (a sign-up offer), but deliberately **bypassing the AI's context**, so as not to look like prompt injection.
- **Source reputation signals** influence the agent's choice.
