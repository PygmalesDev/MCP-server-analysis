# MCP server: Tavily

> **In plain words.** Tavily is a paid internet search service built specifically for AI. Its MCP server gives an AI agent "buttons": search the internet, download the text of a page, crawl a website, build a site map, research a topic and (new) send Tavily a rating of the quality of the results.
>
> **Analysis date:** 12.10.2026; re-analysed on 15.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.
>
> **Verbatim tool descriptions** (Pre-Interaction Context) are in a separate file: `01b_tavily_pre_interaction_context.md`.

**Abbreviations in links:**
- `[code]` = repository [tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp/tree/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0) at a pinned commit.
- `[idx:N]` = line N of [src/index.ts](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/src/index.ts).
- `[readme]` = [README.md](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/README.md).
- `[docs-mcp]` = [docs.tavily.com/documentation/mcp](https://docs.tavily.com/documentation/mcp).

---

## ⚠️ Important limitation of the analysis

The list (`mcp_server_screening.csv`) gives the **remote** server `https://mcp.tavily.com/mcp`. Its code is **not published**. Only the code of the **local** version is open (it runs on the user's computer via `npx tavily-mcp`). The code analysis below refers to the local version. What is known about the remote version is taken from the documentation. Visible differences:
- the documentation lists **5** tools for the remote server, while the open code has **6** (`tavily_feedback` was added) [docs-mcp];
- the remote server supports sign-in via OAuth and HTTP headers (`DEFAULT_PARAMETERS`, `X-Human-Id`), the local one only environment variables [readme], [docs-mcp].

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Tavily MCP Server (`tavily-mcp`, in the MCP registry: `io.github.tavily-ai/tavily-mcp`) | [package.json](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/package.json) |
| Code link | https://github.com/tavily-ai/tavily-mcp | — |
| Documentation link | https://docs.tavily.com/documentation/mcp (the CSV gives https://docs.tavily.com/mcp — this address now serves the documentation MCP server, not a page) | [docs-mcp] |
| Endpoint (from CSV) | `https://mcp.tavily.com/mcp` (remote, code closed) | CSV, [readme] |
| MCP version | The SDK supports protocol versions `2025-11-25` (latest), `2025-06-18`, `2025-03-26`, `2024-11-05`, `2024-10-07`. This SDK does **not** support the newest version `2026-07-28` | [typescript-sdk 1.31.0, types.ts:4–6](https://github.com/modelcontextprotocol/typescript-sdk/blob/1.31.0/src/types.ts#L4-L6) |
| Commit / date | `688b0f78d518d507cb31b94d9cc0e44c6eadd7c0`, 2026-10-15 (last change to the server code: `08dfecd`, 2026-10-15) | `git log` |
| Package version | `0.2.23` in package.json, but the server reports itself as `0.2.22` (inconsistency in the code) | [package.json], [idx:78] |
| Language | TypeScript (Node.js ≥ 20) | [package.json], [readme] |
| MCP SDK | Official `@modelcontextprotocol/sdk` **1.31.0**, low-level `Server` class (no FastMCP/McpServer) | [package.json], [idx:3] |
| Transport | Local: only `stdio` [idx:697]. Remote: Streamable HTTP [docs-mcp] | |
| Code open? License | Yes, **MIT** (Copyright 2024 Alpha AI Technologies Inc.) — only for the local version | [LICENCE](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/LICENCE) |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | The MCP server itself is free (MIT code). You pay for the Tavily API calls it makes | [LICENCE], [api-credits](https://docs.tavily.com/documentation/api-credits) |
| Linked software | Tavily API — a closed commercial service (company Alpha AI Technologies Inc.) | [privacy](https://www.tavily.com/privacy) |
| Pricing model | Credits. **Free: 1,000 credits per month** without a card. Pay-as-you-go: **$0.008 per credit**. Subscriptions: Project 4,000 cr./$30; Bootstrap 15,000/$100; Startup 38,000/$220; Growth 100,000/$500; Enterprise — custom | [api-credits](https://docs.tavily.com/documentation/api-credits) |
| Cost of actions | Search: basic/fast/ultra-fast = 1 credit, advanced = 2. Extract: 1 credit per 5 successful URLs (advanced — 2). Map: 1 credit per 10 pages (with instructions — 2). Crawl = Map + Extract. Research: mini 4–110, pro 15–250 credits per request | [api-credits](https://docs.tavily.com/documentation/api-credits), [search API](https://docs.tavily.com/documentation/api-reference/endpoint/search) |
| Keyless mode | If no key is set, the server works in "keyless" mode: free, rate-limited, only Search and Extract. Crawl/Map/Research require a key | [idx:17, 91–101], [keyless](https://docs.tavily.com/documentation/keyless) |
| Rate limits | Development key: 100 requests/min; Production key: 1,000/min. Crawl: 100/min; Research: 20/min. Production key only with a paid plan or PAYGO enabled | [rate-limits](https://docs.tavily.com/documentation/rate-limits) |
| Who controls the restrictions | Tavily (on the API side). The MCP server itself introduces no restrictions except the research timeouts (see section D) | same |
| Key selection with OAuth | The key named `mcp_auth_default` is used (personal takes precedence over team), otherwise `default`, otherwise the first available one | [readme], [docs-mcp] |

## C. Implemented capabilities

The server declares only `capabilities: { tools: {} }` [idx:81–83].

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | 6 tools: `tavily_search`, `tavily_extract`, `tavily_crawl`, `tavily_map`, `tavily_research`, `tavily_feedback`. Each is a wrapper around one REST endpoint of `api.tavily.com` [idx:56–63] | Verbatim: file `01b_…`. Server instructions are **not set** [idx:75–85]. There are **no** annotations (readOnlyHint etc.) | Always one block `type: "text"`. Search/Extract: lines `Request ID: …`, `Answer: …`, `Detailed Results:`, then for each result `Title/ID/URL/Content/Raw Content/Favicon`, then `Images:` [format-results.ts](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/src/format-results.ts). Crawl: `Crawl Results:`, `Base URL`, for each page the URL and the **first 200 characters** of text [idx:1052–1074]. Map: list of URLs [idx:1076–1088]. Research: the finished report text [idx:1090–1096]. Feedback: `Feedback submitted (feedback_id: …)` [idx:1098–1107] |
| Resources | ❌ | — | — | — |
| Prompts | ❌ | — | — | — |
| Logging (MCP) | ❌ | Logs are written only to stderr (`console.error`), no MCP log notifications are sent [idx:100, 109, 699] | — | — |
| Sampling | ❌ | — | — | — |
| Roots | ❌ | — | — | — |
| **Authorization** | ✅ (remote) / partial (local) | **Local:** the API key from the `TAVILY_API_KEY` variable is sent in the `Authorization: Bearer` header and in the request body as `api_key` [idx:93, 724]. **Remote:** (1) key in the URL `?tavilyApiKey=…`; (2) key in the `Authorization: Bearer` header; (3) OAuth. The README describes the flow via MCP Inspector: Metadata discovery → Client registration → Authorization → Token request (i.e. metadata discovery and dynamic client registration are supported). The authorization server is Tavily; details (address, token lifetime) are not documented | [readme] lines 18–39, 106–147; [docs-mcp] | — |
| Elicitation | ❌ | — | — | — |
| Tasks (MCP) | ❌ | The long-running `tavily_research` is executed **within a single call**: the server polls the API itself (every 2→10 s, up to 5 min for `mini` and 15 min for `pro/auto`) [idx:779–854]. The MCP Tasks mechanism is not used | — | — |
| **Configuration** | ✅ | `TAVILY_API_KEY`; `DEFAULT_PARAMETERS` (JSON with default values for search); `TAVILY_HUMAN_ID` (end-user ID → header `X-Human-Id`). Flag `--list-tools` [idx:16–18, 118–148, 1153–1165]. Remote — the same via headers | [readme] | — |
| **Error Reporting** | ✅ | API error → result with `isError: true` and the text `Tavily API error: <detail>\nDocumentation: <link>` [idx:674–688]. Unknown tool → JSON-RPC error `MethodNotFound` [idx:652–655]. **Special case:** keyless-mode errors (limit reached, key required) are returned **as ordinary successful text, without `isError`** [idx:666–673] | — | The keyless error text contains a message, `Retry after: Ns` and "Continuation options": payment by the agent via the **x402** protocol, a sign-up link, **bonus credits for answering questions** [idx:1026–1050] |
| Subscription | ❌ | — | — | — |
| Progress Tracking | ❌ | Even for research lasting up to 15 minutes no progress notifications are sent | — | — |
| Cancellation | ❌ (explicit) | The handlers do not handle a cancellation signal; HTTP requests to Tavily continue | [idx:536–692] | — |
| Other | — | Every request is tagged with the headers `X-Session-Id` (random UUID per process), `X-Client-Source: MCP` and, if present, `X-Human-Id` [idx:19, 87–97] | — | — |

## D. Server logic beyond simply passing commands through

What the server does **between** the AI's request and the Tavily API:

1. **The operator's default values override the AI's choice.** If `DEFAULT_PARAMETERS` is set, its values **replace** the parameters sent by the AI rather than only supplementing them (loop `for key in searchParams … searchParams[key] = defaults[key]`) [idx:727–732]. Applies only to `tavily_search`. *Example:* if the operator set `max_results: 5`, the agent cannot request 20.
2. **Parameter correction:** if `country` is given, `topic` is forced to `general` [idx:543–546]; if dates are given, `time_range` is removed [idx:737–739]; empty values are cleaned out before sending [idx:1005–1016].
3. **Hard-coded parameter:** for crawl always `chunks_per_source: 3`, the AI cannot change it [idx:591].
4. **Result truncation:** in crawl the AI sees only the first 200 characters of each page [idx:1063–1066].
5. **Timeouts and retries for research:** polling with a growing interval (2 s × 1.5, maximum 10 s), limit 5/15 min. If the API requires streaming mode, the server switches to it itself (response wait timeout 30 s, idle 5 min). An incomplete report is not returned — an error is returned instead [idx:779–986].
6. **User attribution:** `X-Session-Id` and optionally `X-Human-Id` on every request — for Tavily's analytics [idx:94–95]; Tavily promises to hash the human ID (SHA-256) [readme] line 230.
7. **Feedback tool `tavily_feedback`** (governance-relevant). Its description **instructs the agent** to rate *every* search result (from −1 to 1), explain ratings below 0.5 and send Tavily **its final answer to the user** (`response_delivered`) and the citations used [idx:431–531]. The server does not check whether the user wanted this.
8. **Keyless responses as "hints" to the agent:** when the free limit is exhausted, the agent receives ordinary text with options to continue — payment by the agent (x402), sign-up, bonus credits for answering questions [idx:1026–1050].
9. None of: permission checks, human confirmation, domain restrictions (other than the AI's own parameters), confidence assessment.

**Server structure:** standard, flat. One process → 6 tools. No hierarchy and no sub-servers.

## E. Overall evaluation

**Number of actions:** 6 (local code); 5 according to the remote server documentation.

| # | Action | Parameters (type; categories) |
|---|---|---|
| 1 | Search the internet (`tavily_search`) | `query` (string, req.); `search_depth` (enum, **4**: basic/advanced/fast/ultra-fast); `topic` (enum, **2**: general/news); `time_range` (enum, **4**: day/week/month/year); `start_date`, `end_date` (string YYYY-MM-DD); `max_results` (number 5–20); `include_images`, `include_image_descriptions`, `include_raw_content`, `include_favicon`, `exact_match` (boolean); `include_domains`, `exclude_domains` (array of string); `country` (string). Total **15** parameters |
| 2 | Extract page content (`tavily_extract`) | `urls` (array, req.); `extract_depth` (enum, **2**); `include_images`, `include_favicon` (boolean); `format` (enum, **2**: markdown/text); `query` (string). Total **6** |
| 3 | Crawl a website (`tavily_crawl`) | `url` (req.); `max_depth`, `max_breadth`, `limit` (integer ≥1); `instructions` (string); `select_paths`, `select_domains` (array regex); `allow_external` (boolean); `extract_depth` (enum, **2**); `format` (enum, **2**); `include_favicon` (boolean). Total **11** |
| 4 | Build a site map (`tavily_map`) | `url` (req.); `max_depth`, `max_breadth`, `limit` (integer); `instructions` (string); `select_paths`, `select_domains` (array); `allow_external` (boolean). Total **8** |
| 5 | Research a topic (`tavily_research`) | `input` (string, req.); `model` (enum, **3**: mini/pro/auto). Total **2** |
| 6 | Send a rating of the results to Tavily (`tavily_feedback`) | `session_id`/`request_id` (string, at least one required); `agent_score`, `human_score` (number\|string); `extra_scores` (array of {label, value}); `comment`, `response_delivered` (string); `used_urls`, `used_ids`, `used_citations` (array of string); `urls_scores` (array of {id, url, agent_score, scores, comment}). Total **11** |

Source: [idx:158–531].

**Tokens before the first action:** ≈ **3,300 tokens** (estimate: length of the JSON tool descriptions ÷ 4 characters per token; error ±30 %, depends on the model). No server instructions.

**What the agent CANNOT do but a human can** (compared with the [REST API](https://docs.tavily.com/documentation/api-reference/endpoint/search) and [credits](https://docs.tavily.com/documentation/api-credits)):
- Search parameters that exist in the API but are not exposed to the agent: `include_answer` (a ready answer from Tavily's LLM), `auto_parameters`, `chunks_per_source`, `include_domains_mode`, `language`, `filter_by_language`, `include_published_date`, `filter_by_published_date`, `include_usage`, `safe_search`.
- In crawl, `chunks_per_source` cannot be changed (hard-coded = 3).
- View credit usage (Usage endpoint), manage keys, plan, team — only in the web dashboard app.tavily.com.
- Get the full text of pages in crawl (the agent sees only the first 200 characters).

## F. Documentation analysis

**Recommendations to the user that the server does not check:**
- Use an opaque ID as the user identifier, not an e-mail ("prefer opaque identifiers … over raw PII") [readme] line 230.
- The OpenAI integration example in the documentation sets `"require_approval": "never"` — i.e. human confirmation is **turned off** in the official example [docs-mcp].
- The API key is suggested to be passed directly in the URL (`?tavilyApiKey=…`); the documentation does not warn about the risks of this [readme], [docs-mcp].
- There are no explicit recommendations on human confirmation of actions.

**Promises on governance and data:**
- The human ID is hashed with SHA-256 before storage, the raw ID is not stored [readme] line 230, [docs-mcp].
- Privacy policy: Tavily **may use parts of request data to improve future responses** (legitimate interest; EU users can object by e-mail); requests may be passed to **third-party search indexes (e.g. Google)**; data is stored as long as the account exists; deletion on request [privacy](https://www.tavily.com/privacy).
- There is no information on logging of the agent's actions or reversibility (all actions only read the internet, except feedback).

**Promises to the user:** "real-time web search", "seamless experience without requiring local installation" [readme]; identifiers help Tavily "better understand multi-step interactions and improve response quality" [docs-mcp].

**Comparison with the server logic:** the promise to hash the human ID cannot be verified from the code (it happens on the API side). The server indeed forwards `X-Human-Id` only if it is set [idx:95].

---

## Observations for the research (as requested by David)

- **Vendor interests are built into the tool descriptions.** `tavily_feedback` asks the agent to send Tavily ratings and its final answer to the user, i.e. the agent works as a free data labeller for the vendor.
- **Commercial offers inside tool responses.** In keyless mode the agent is offered payment (x402) and bonus credits for answering questions. These texts arrive as an ordinary result, not as an error, so the agent may take them as an instruction.
- **The operator can override the agent.** `DEFAULT_PARAMETERS` overrides the parameters chosen by the AI, and the AI is not told about it.
- **Open code ≠ deployed service.** The tool set of the local version and of the remote endpoint differ.
- **Behavioural hints in the descriptions:** "Use for news, facts, or data beyond your knowledge cutoff", "Use 'news' only when the user explicitly asks for news".
