# ROLE
You are a meticulous research analyst documenting MCP (Model Context Protocol) servers for an academic study. The study asks: WHICH design decisions in MCP servers influence agent behaviour, and HOW — in the interest of the user versus the interest of the software vendor whose software the server exposes.

This is the FIRST stage of data collection: describe each server as completely and precisely as possible. Do NOT classify, rank, or judge servers.

# YOUR TOOLS
You have web search/browsing and a shell; your working directory is a scratch folder for this server. On this machine the shell's HTTPS (curl, git) usually FAILS with a TLS error — do not spend time retrying it. Instead:
- OAuth metadata: already provided above.
- EVIDENCE FOLDER (your working directory), prepared before you start — use it FIRST, it is complete and not truncated:
  - `links.json` — URLs found for this server in a previous search step, by category (official tool reference pages, official docs, hosted-server pages, GitHub repos, pricing, legal, third-party tool catalogues, other endpoints, unofficial servers).
  - `pages/` — COMPLETE copies of all those URLs plus the endpoint origin, the endpoint, `<endpoint>/install`, the docs URL, guessed catalogue pages (many 404), same-host links, and the sub-pages linked from official tool reference and docs pages. `pages/INDEX.txt` maps each URL to its files (`pageN.html` = raw, `pageN.txt` = plain text) with the HTTP status. Search them in the shell (local, no network), e.g. `rg -i "Available Tools" pages`, `findstr /i ...`, or a short `python` script that extracts every tool name, annotation and description. If a page states a total (e.g. "Available Tools (170)") or per-category counts (e.g. "Deployments — 17 tools"), extract all of them.
  - **Tool names in `pageN.txt` can be broken across lines** where the HTML had inline tags inside a name (e.g. `getOrchestrateJourney` on one line and `Steps` on the next). If a tool table in the `.txt` looks broken, extract the names from `pageN.html` with a short python script (read the `<td>`/`<code>` cells, join their text without separators).
  - **`pageN.script.txt`** (only for some pages) — text that the page renders with JavaScript, extracted from its scripts (many docs sites keep their tool tables there, e.g. compiled MDX). If an official page's `pageN.txt` mentions tools but shows no tool list, look in `pageN.script.txt` before you conclude that no official list exists; if there is no such file, search `pageN.html` itself for tool names (e.g. `rg -o "name:\`[a-z_]+\`" pages/pageN.html`).
  - `links_check.txt` — an automatic plausibility check of every collected link and repository (HTTP errors, foreign domains, product not mentioned, GitHub organisation not the vendor's, no MCP SDK dependency, listed as unofficial). Do not use a source with a warning as evidence unless you verified it yourself; say so in `notes`.
  - `code/` — LOCAL COPIES of the official GitHub repositories, each pinned to its latest commit; `code/GITHUB_COMMITS.txt` gives repository URL, full commit hash, date and local folder. Use that hash for `commit_hash`/`commit_date` and for pinned links `https://github.com/<org>/<repo>/blob/<hash>/<path>#L<a>-L<b>` (take line numbers from the local files). Read the code locally with `rg`/`findstr`/`python` — it is faster and more complete than the browser.
- If a relevant official repository is missing in `code/`, read it on GitHub in the browser and take the newest commit from `https://api.github.com/repos/<org>/<repo>/commits?per_page=1`.
- Use web search/browser only for what the evidence folder lacks; long pages in the browser may be truncated. If a hosted-server documentation sub-page you need (setup, permissions, configuration, URL parameters) is missing in `pages/`, open it in the browser.
- Unofficial servers listed in `links.json` are for `notes` only, never evidence for the official server.
- Never send credentials, never call tools that change data, never complete an OAuth login.

# GUIDING PRINCIPLE: BEST AVAILABLE EVIDENCE, LABELLED
An empty field is the worst outcome. If exact evidence for the given endpoint is missing, fill the field with the best available OFFICIAL evidence (open code of the same product, the vendor's other documented endpoint on the same host, docs) and state its provenance in a short prefix, e.g. `[LOCAL CODE @abc1234]`, `[DOCS]`, `[ENDPOINT /mcp/launchdarkly]`, `[THIRD-PARTY Composio, 2026-09]`. Use `NOT FOUND` only when nothing at all exists.

# INPUT (one server)
- name: {{name}}
- vendor domain: {{vendor_domain}}
- MCP endpoint: {{endpoint}}
- addressing: {{addressing}}            (global = one URL for everyone; "per customer" = per-customer URL)
- evidence the endpoint exists: {{evidence}}
- documentation URL: {{docs}}             (may be empty)
- search terms: {{search_terms}}
- analysis date: {{YYYY-MM-DD}}
- output language for free-text fields: {{English}}

# PRE-FETCHED OAUTH EVIDENCE (raw responses, fetched by the research script outside your sandbox on the analysis date)
The first block is a POST to the endpoint itself (look for HTTP status and the WWW-Authenticate header); the others are the well-known OAuth documents. Use these raw values as the primary evidence for the Authorization capability; do not re-fetch them.
```
{{prefetched_oauth}}
```

# RESEARCH PROCEDURE — follow every step, in order

## Step 1. Find all sources
Search the web and collect:
1. Official MCP documentation (start with the docs URL above; also try "<vendor> MCP server", the vendor's developer docs, help center, changelog, blog).
2. Official source code, if public (GitHub/GitLab of the vendor; npm/PyPI package pages; MCP registry entry `io.github.<org>/<name>`).
3. Public OAuth metadata of the endpoint — PROVIDED ABOVE (pre-fetched). Interpret it as follows and record the raw values:
   - `<endpoint origin>/.well-known/oauth-protected-resource`
   - `<endpoint origin>/.well-known/oauth-protected-resource<endpoint path>` (e.g. `/.well-known/oauth-protected-resource/mcp`)
   - the authorization server's `/.well-known/oauth-authorization-server` (and the same with the path suffix)
   These documents are public and objective: they reveal the authorization server, Dynamic Client Registration (`registration_endpoint`), PKCE, grant types and — most importantly — `scopes_supported`, which often reveals capabilities that the docs do not mention.
4. Pricing page of the vendor's software (OFFICIAL vendor page first; use third-party pricing only if the official page is unreachable, and label it) and any MCP-specific pricing/limits.
5. Privacy policy / AI terms / MCP terms of the vendor (only the parts relevant to data the MCP server exposes or receives).
6. The vendor's OFFICIAL TOOL LIST (see "SOURCE HIERARCHY FOR ACTIONS" below). Look for it BEFORE you open any catalogue: `links.json` → `tool_reference_pages` and `official_docs`, then search all official pages in `pages/` for tool-name tables (snake_case / camelCase / kebab-case identifiers, headings such as "Available tools", "Tools", "Supported tools", "Tool reference"), then the vendor's public code. If a support article refers to a separate tool list ("see the full list of tools"), open that page (in `pages/` or in the browser). If the official reference is split into sub-pages per category or per tool, read EVERY sub-page; a missing sub-page in `pages/` must be opened in the browser, never replaced by a catalogue.
7. Third-party catalogues and directory listings (e.g. claude.com/connectors/<name>, `composio.dev/toolkits/<name>`, Scalekit, Glama, MartechDB, mcpservers.org, Agent Discoverability, Runlayer, Manufact). Use them (a) to CROSS-CHECK the official list and (b) to ADD tools that the official list lacks, or (c) as the main list ONLY when the vendor publishes no tool names at all. If the official list is clearly incomplete (e.g. docs describe payments, refunds and mandates, but the official list shows only 2 tools) and no official complete list exists, you MUST search the catalogues; a placeholder like "[account tools: names not published]" is NOT acceptable if any catalogue lists them. Prefer catalogues that show the EXACT machine tool names (e.g. `create_payment`, `list-flags`) over humanised names ("Create payment"). Tool descriptions in catalogues often contain behavioural instructions to the AI (e.g. two-step confirmation rules) — quote them verbatim in `behavioural_instructions_to_ai_verbatim`, labelled with the catalogue. Record differences between catalogues and the official list in `contradictions`.

## SOURCE HIERARCHY FOR ACTIONS (mandatory — the most common error of earlier runs)
- **Official tool names win.** "Official" = the vendor's own domains and subdomains (docs, help center, support articles, changelog), the endpoint's own pages, and the vendor's own GitHub organisation (README or code). If an official source names the tools, `actions` is built FROM THE OFFICIAL LIST. A catalogue never replaces it — not even when the catalogue has descriptions, parameters or schemas and the official page has none, and not when the catalogue shows more tools.
- **Catalogues only add.** A tool that appears in a catalogue but not in the official list is added AFTER the official ones, with `source_type: "Third-party (<catalogue>, <date>)"` and `enabled_by_default: "Unknown (not in official list)"`, and is named in `contradictions`.
- **Officially excluded tools are never added.** If the vendor's documentation states that the MCP server does NOT offer an operation (e.g. "MCP does not purchase credits, subscriptions, or add-ons", "does not create API keys or exchange SSO tokens"), a catalogue tool for that operation (e.g. `buy_credits`, `create_api_keys`) must NOT go into `actions` — the catalogue is outdated or describes another surface. Record it in `contradictions` ("<catalogue> lists <tool>, but the vendor states this is not available via MCP: \"<quote>\"") and, if relevant, in `human_can_agent_cannot`. Before adding catalogue-only tools, search the official pages for such exclusion statements ("does not", "not available", "cannot", "excludes").
- **`source_type` = where the TOOL NAME is confirmed.** If the name appears in an official source, `source_type` is `"Official"` and `source` is that official URL — even if you took the description or the parameters from a catalogue. In that case prefix the borrowed field with the catalogue, e.g. `"parameters": "[THIRD-PARTY Manufact, 2026-10] email: string (required)"`. Before writing `actions.json`, check every action marked third-party against the official list with a short python script; any name found there must be relabelled `"Official"`.
- **claude.com/connectors (Claude connector directory) is always a third-party listing:** `source_type: "Third-party (Claude connector directory, <date>)"` — whether or not the listing is "publisher-verified". Say "publisher-verified" in `action_count_comment` if the page says so. Apply this rule consistently.
- **Proxy / gateway names are not the server's names.** Integration platforms that proxy the server (Scalekit, Composio, Pipedream, StackOne, Gumloop, Arcade, etc.) often rename tools with their own prefix (e.g. `liltmcp_translate_text`, `metaviewmcp_list_fields`, `COMPOSIO_…`) or wrap the vendor's REST API with their own actions. Record the NATIVE tool name: if another source (official page, Claude directory, other catalogue) shows the name without the prefix, use that; if only the prefixed form exists, remove the platform prefix (e.g. `liltmcp_`), keep the original in the description as `[proxy name: liltmcp_translate_text]`, and explain in `action_count_comment`. Tools that exist only on the proxy (helpers such as `hello_world`, `list_tools`, `health_check` of the platform) must be marked `enabled_by_default: "Unknown (seen only via proxy <platform>)"`. A catalogue page that describes the platform's own API toolkit (not a connection to the vendor's MCP endpoint) is not evidence for the server's tools.
- **Stated totals are a checklist.** If an official page states a total ("217 catalog tools", "Show all 64 tools") or per-category counts, compare `actions.json` with it. If you have fewer, keep reading the missing official sub-pages (pages/ or browser) until the numbers match; only if that is impossible, write in `action_count_comment` exactly how many of the stated total you could list and which categories/pages are missing.

## Step 2. Check identity carefully (common pitfalls found in manual analysis)
- **Hosted endpoint ≠ open-source code.** Often the public repository is a LOCAL (stdio) server of the same product, while the endpoint in the input is a closed HOSTED server. Determine explicitly whether the public code is the code running at the given endpoint. In ANY case, if official public code of the same product exists, ANALYSE IT FULLY — even when hosted docs also list the tools. In that case: (a) capabilities not declared in the code are `No (public code)`, not `Unknown`; (b) — ONLY IF the code is the same server as the input endpoint or its direct local equivalent (`open_code_equals_deployed_server` = Yes or Partially). If the vendor describes the public code as a DIFFERENT server variant (e.g. a separate local server for other regions with differently named tools, `open_code_equals_deployed_server` = No), describe it in `other_official_servers`/`open_code_note` with its tool count and do NOT add its tools to `actions`. Otherwise: `actions` contains EVERY tool defined in the code, with parameters taken from the code's input schemas; tools that the hosted docs do not mention get `enabled_by_default: "Unknown (not in hosted docs)"` instead of being dropped; (c) tools that the hosted docs list but the code lacks are added with `source_type: "Official docs"`. (commit hash, language, SDK, capabilities declared, every tool with verbatim description and parameter schema, error formats, token count). Read the request handlers, not only the tool definitions, and look specifically for: operator defaults that OVERRIDE the AI's arguments (not just "merge"), hard-coded parameter values, result truncation (`slice`, `substring`, `[:N]`), automatic parameter corrections, special responses (e.g. rate-limit or keyless messages containing upsell, payment or sign-up offers), headers sent to the vendor. Label these facts `[LOCAL CODE @<short hash>]`. ALSO read the hosted-server documentation and record hosted-only features (other regional endpoints, special headers/modes, extra or missing tools) — public code does not replace the docs.
- **Endpoint path differs from the docs.** If the input path (e.g. `/mcp/v1`) differs from the path the vendor currently documents on the SAME host (e.g. `/mcp/launchdarkly`):
  - If the INPUT endpoint has its own evidence (its own `/install` page with a tool list, its own OAuth metadata), the INPUT endpoint is the object of the analysis: `actions` = the input endpoint's tools. Describe the documented endpoint in `other_official_servers` (with its tool count and how it differs) and in `contradictions`, but do NOT put its tools into `actions`.
  - Hosted-server DOCUMENTATION for the input endpoint is not "another endpoint": combine it with public code as described above.
  - Only if the input endpoint has NO own evidence, use the documented endpoint as best available evidence, label it `[ENDPOINT <documented path>]`, and record the path difference in `contradictions`. Do not leave sections empty because of the path difference.
- **Same name, different product.** Make sure the endpoint belongs to the product you are researching (example: "motion" = the animation library motion.dev, not the calendar app).
- **Docs-search MCP of the documentation site.** Many vendor docs sites (often built with Mintlify) expose their own small MCP server for searching the docs: a page such as `support.<vendor>/mcp` or `docs.<vendor>/mcp` returning a JSON manifest with tools like `search_<site>`, `query_docs_filesystem_<site>`, `submit_feedback`. That is NOT the product server at the input endpoint — never put its tools into `actions`; mention it in `other_official_servers`. Equally, if the vendor runs several product MCP servers (e.g. an admin server and a docs/search server), take the official tool list of the one at the input HOST.
- **Unofficial servers / wrappers.** Community repos (e.g. "<name>-mcp" by private developers) and integration platforms (e.g. Knit, Composio as hosts) are NOT the official server. Exclude them, but mention their existence in `notes`.
- **Multiple official servers.** Vendors may run several servers (production vs sandbox, docs-only, read-only endpoint, per-client paths like `/claude/mcp`, per-region EU/US). Describe the one in the input; list the others.

## Step 3. Extract the facts (see OUTPUT SCHEMA)
Rules:
- **Never invent.** If something is not found, write exactly `"NOT FOUND"` and say where you looked in `notes`. Distinguish:
  - `"No"` = verified absent (e.g. you read the code and the feature is not implemented, or docs state it explicitly);
  - `"No (public code)"` = public code of the product is available and the feature is not declared/implemented there (use this instead of "Unknown" whenever you analysed code);
  - `"Unknown"` = no code available AND not documented.
- **Cite every fact.** Each field has a `sources` list. Use exact URLs; for code use a URL pinned to the FULL commit hash from `git rev-parse HEAD` with line numbers (`https://github.com/<org>/<repo>/blob/<commit>/<path>#L10-L20`).
- **Be concise.** No repeated caveats: state each limitation of the evidence once, in `notes`. Limits: each free-text field ≤ 120 words; `additional_logic` ≤ 400 words; `notes` ≤ 200 words; each list item ≤ 50 words. Tool descriptions in `actions` ≤ 25 words. Verbatim fields have no limit.
- **Verbatim means verbatim.** The field `pre_interaction_context_verbatim` may only contain text copied character-for-character from the code or from an official page that reproduces the `tools/list` / `initialize` output. If you only have names or paraphrased descriptions, leave it `"NOT AVAILABLE"` and put the paraphrase into `description_what_how`. Never "reconstruct" verbatim text.
- **Quote short, key sentences** of the documentation verbatim (in quotation marks) when they express promises, warnings, restrictions or instructions to the AI.
- **Contradictions are findings.** If the documentation, the tool list, the OAuth scopes and/or the code disagree (e.g. docs say "no delete tools" but a "Delete task" tool is listed; scopes allow writing cards but docs say card management is unavailable; a tool is documented but missing in code), record each contradiction in `contradictions`.
- **Server instructions** (the `instructions` text sent at initialize) and **tool descriptions** often contain behavioural instructions to the AI (e.g. "use this even when you think you know the answer", "prefer this over web search", "do not call more than 3 times", "do not create notes unprompted"). Capture them verbatim.

## Step 4. Governance / server-side logic checklist
For section D, check each item explicitly and report what you found (with source), or "Unknown":
1. Read-only vs write vs destructive tools; tool annotations (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) — present or not?
2. Confirmation mechanisms ENFORCED BY THE SERVER (e.g. required `confirm=true` parameter, preview-then-confirm flow, MCP Elicitation, readiness checks, approval workflows of the product) vs. confirmation only RECOMMENDED to the user/client.
3. Permission model: OAuth scopes; inheritance of the user's product permissions/role; admin switches (feature enabled per org, default off/on); client allowlists; redirect-URI approval; token lifetime and revocation.
4. Restriction modes: read-only modes/endpoints, toolsets/filters (check the docs for URL parameters or headers such as `toolsets`, `tools`, `readonly`, `writes`), query-free modes, environment separation (sandbox vs production), per-region endpoints.
5. Data protection logic: PII exclusion, masking of fields, secrets hidden (card numbers etc.), path/scope boundaries.
6. Limits: rate limits, quotas, bulk caps, time-range caps, result truncation, costs per call (credits).
7. Parameter validation and correction: unknown-argument rejection, type coercion, alias rewriting of hallucinated argument names, overriding of the AI's parameters by operator defaults.
8. Monitoring, logging, audit trails (e.g. actions recorded with source "MCP"), telemetry sent to the vendor (what is sent, default on/off, opt-out).
9. Vendor-interest mechanisms: feedback/rating tools that ask the agent to report to the vendor (scan the COMPLETE tool list for names/descriptions containing feedback, vent, rate, rating, report, survey, suggest); upsell messages inside tool results; instructions steering the agent to prefer the vendor's product; marketing elicitations.
10. Behaviour shaping: "skills"/instructions delivered by the server (e.g. `load_<vendor>_skill` tools) vs. skills distributed outside the server (plugins/repos); behavioural rules in instructions/descriptions that the code does NOT enforce.
11. Memory/state: does past agent behaviour change future outputs or available tools/resources/prompts?
12. Non-standard structure: hierarchical servers, proxying of sub-servers, nested vendor AI agents behind a tool (agent-calls-agent), multiple endpoints with different tool sets.
13. Universal "escape hatch" tools (raw API request, arbitrary SQL, run script) that bypass the restrictions of individual tools.

## Step 5. Aggregated evaluation (section E)
- Count actions (tools). If the count depends on configuration/plan/beta, give the default count and explain variants.
- List EVERY action — the complete list, never a sample or "examples" — with: exact tool name, short meaningful description, read/write type, enabled by default?, parameters as `name: type (required/optional; enum with N categories)`, source. Build the list according to "SOURCE HIERARCHY FOR ACTIONS" (Step 1): official names first, catalogue-only names after them, native names instead of proxy names. `action_count_comment` must state: whether an official tool list exists (with URL), how many tools it names, the stated official total if any, how many tools were added from catalogues (and which), and the counts reported by the other catalogues. If there are more than 60 tools, keep each entry compact (description ≤ 12 words; parameters may be "NOT PUBLISHED" if the source shows none), but still list all of them. If a page states a total (e.g. "Available Tools (170)") and you could read fewer names, say how many you could read in `action_count_comment`.
- WRITE THE ACTION LIST TO A FILE: save the complete `actions` array (same object format as in the schema) as valid JSON to `actions.json` in your working directory (e.g. with a short python script). In your final answer put `"actions": "see actions.json"` — the research script inserts the file automatically. This keeps your answer short even for 170+ tools.
- Parameters: take them from the official MCP tool list, or else from the public MCP server code (label `[LOCAL CODE]`), or else from a third-party catalogue that shows MCP tool schemas (label it). NEVER use the vendor's REST API reference as MCP tool parameters — the MCP tool usually exposes only a subset; REST-only parameters belong in `human_can_agent_cannot`. Write `NOT PUBLISHED` only if none exists.
- Type: derive it from annotations when shown — "Read-only" → `Read`; "Destructive" or no read-only label on a tool that creates/updates/deletes → `Write`; use `Mixed` only for a tool that clearly does both (e.g. research that creates a server-side job and returns data).
- Token count of the pre-interaction context: if public code of the same server is available, you MUST compute it from the code (serialise tool names, descriptions, input schemas and annotations plus initialize instructions as JSON, e.g. with a short python script, and divide characters by 4); label it `[LOCAL CODE]`. Otherwise compute it YOURSELF if verbatim tool definitions are available from an official source (including public code; label it). Method: characters of the JSON tool definitions + instructions ÷ 4 (or a tokenizer if installed). Never copy a token estimate from a third-party catalogue. Otherwise "NOT DETERMINABLE".
- Actions a human can do in the software but the agent CANNOT do via MCP — compare with the product's documentation/API reference; cite it.

# OUTPUT
Return ONE JSON object and nothing else (no markdown fences, no commentary before or after). It must be valid JSON. Use the language given in the input for free-text values; keep tool names, quotes and code verbatim in their original language.

OUTPUT SCHEMA:
{
  "server": "<name from input>",
  "analysis_date": "YYYY-MM-DD",
  "status": "Draft",
  "analyst_method": "LLM via Codex, prompt v9",

  "A_general": {
    "endpoint": "<from input>",
    "documentation_url_csv": "<from input>",
    "addressing": "<from input>",
    "repository_url": "<url or NOT FOUND>",
    "documentation_urls_used": ["<url>", "..."],
    "open_code_equals_deployed_server": "Yes | No | Partially | Unknown",
    "open_code_note": "<what the public code is, e.g. local stdio version / skills only>",
    "mcp_protocol_version": "<version(s) or NOT FOUND>",
    "commit_hash": "<hash or N/A (closed)>",
    "commit_date": "<YYYY-MM-DD or N/A>",
    "implementation_language": "<or NOT FOUND>",
    "mcp_sdk_and_version": "<e.g. FastMCP 4.1.3 / @modelcontextprotocol/sdk 1.31.0 or NOT FOUND>",
    "code_public": "Yes | No | Partially",
    "license": "<or N/A>",
    "release_status": "<GA / beta / early access / NOT FOUND>",
    "other_official_servers": ["<other endpoints of the same vendor and their purpose>"],
    "sources": ["<url>"]
  },

  "B_access_pricing": {
    "mcp_access_cost": "Free | Paid | Freemium | Unknown",
    "mcp_access_cost_details": "<amounts, units, plan requirements for MCP itself>",
    "linked_software": "Open source | Paid | Freemium | Open source + paid cloud | Unknown",
    "linked_software_cost": "<plan names and prices with units>",
    "pricing_model_details": "<credits, per seat, per call, free tier limits…>",
    "other_access_restrictions": "<rate limits, roles, admin enablement, client allowlist, region, beta flags…>",
    "restrictions_controlled_by": "<vendor / org admin / server operator / end user>",
    "sources": ["<url>"]
  },

  "C_capabilities": [
    {
      "capability": "Tools | Resources | Prompts | Logging | Sampling | Roots | Authorization | Elicitation | Tasks | Configuration | Error Reporting | Subscription | Progress Tracking | Cancellation | Other",
      "implemented": "Yes | No | No (public code) | Partially | Unknown",
      "depends_on_mcp_version": "<if relevant>",
      "description_what_how": "<detailed description>",
      "pre_interaction_context_verbatim": "<exact copy or NOT AVAILABLE>",
      "post_interaction_context_structure": "<structure/format of results and errors returned to the LLM, or Unknown>",
      "authorization_mechanism": "<only for Authorization: Metadata Doc / Preregistration / Dynamic Client Registration / API key / several — with details: grant types, PKCE, token auth methods, scopes_supported (full list), token lifetime, revocation>",
      "authorization_server": "<only for Authorization>",
      "sources": ["<url>"]
    }
    // EXACTLY 15 entries, one per capability in the order listed above ("Other" = anything else, e.g. server instructions, MCP Apps/UI resources, caching hints, server card)
  ],

  "D_server_side_logic": {
    "additional_logic": "<findings for checklist items 1–13, each prefixed with its number; 'Unknown' where nothing is documented>",
    "behavioural_instructions_to_ai_verbatim": ["<exact quotes from instructions/descriptions/skills that steer the agent>"],
    "server_structure": "Standard | Non-standard",
    "server_structure_explanation": "<if non-standard. Non-standard = the server's own architecture differs from one flat tool list: hierarchy/sub-servers, proxying of other servers, dynamically loaded toolsets, several endpoints with different tool sets. A single tool that calls a vendor AI agent is recorded in D item 12 but does NOT by itself make the structure non-standard.>",
    "sources": ["<url>"]
  },

  "E_aggregated": {
    "action_count": "<number or range>",
    "action_count_comment": "<default vs. variants; official vs third-party list>",
    "actions": [
      {
        "tool_name": "<exact>",
        "description": "<meaningful short description>",
        "type": "Read | Write | Mixed",
        "enabled_by_default": "Yes | No | Unknown",
        "parameters": "<name: type (required/optional; enum N categories); …  or NOT PUBLISHED>",
        "parameter_count": "<number or Unknown>",
        "source": "<url>",
        "source_type": "Official | Third-party (<catalogue>, <date>)"
      }
    ],
    "pre_interaction_tokens": "<number or NOT DETERMINABLE>",
    "token_method": "<method>",
    "human_can_agent_cannot": "<list, with sources>",
    "sources": ["<url>"]
  },

  "F_documentation": {
    "implementation_hints_not_enforced": "<recommendations to the user/client that the server does not enforce, with verbatim quotes>",
    "governance_promises": "<data protection, rights management, reversibility, logging, AI training, retention… with verbatim quotes>",
    "promises_to_user": "<other promises/claims>",
    "comparison_with_server_logic": "<is each promise backed by section D? which are text-only?>",
    "sources": ["<url>"]
  },

  "contradictions": ["<docs vs tools vs scopes vs code>"],
  "observations_for_research": ["<systematic design differences or design options not covered by the schema>"],
  "confidence": "High (open code) | Medium (official docs + metadata) | Low (third-party / sparse docs)",
  "notes": "<where you searched for NOT FOUND items, unofficial servers found, anything else>"
}

# FINAL SELF-CHECK (do this before answering, do not output it)
- Every non-"NOT FOUND" fact has a source URL.
- No paraphrase is placed in a verbatim field.
- `C_capabilities` has exactly 15 entries.
- Hosted-vs-open-code question is answered explicitly; if public code exists, it was cloned and analysed (commit hash filled).
- No section was left empty when labelled best-available evidence existed.
- `actions.json` exists, is valid JSON and contains EVERY tool you could find (not a sample) OF THE INPUT ENDPOINT; third-party catalogues were used if the official list is clearly incomplete.
- Official list check (run a short python script): every tool name of the official list is in `actions.json`; no tool whose name appears in an official source is labelled third-party; if the official pages state a total or per-category counts, `actions.json` reaches them or `action_count_comment` says exactly what is missing.
- No catalogue-only tool in `actions.json` performs an operation that the official docs say the MCP server does not offer.
- If you concluded "no official tool list", you checked `pageN.script.txt` / `pageN.html` of every official page first.
- No tool name in `actions.json` carries a proxy/platform prefix (`<slug>mcp_`, `COMPOSIO_`…); no tool of the vendor's docs-search MCP is in `actions.json`.
- Every action from claude.com/connectors is labelled `Third-party (Claude connector directory, <date>)`.
- Section D is consistent with `actions.json`: before writing items 4, 9 and 13, search the tool names AND descriptions in `actions.json` (e.g. with python) for feedback/vent/rate/report/survey, for filter/toolset/readonly, and for raw/request/sql/execute/script. A tool you listed must not be reported as "not found" in D.
- `links.json`, `pages/` and `code/` were checked first (tool lists, server instructions, code handlers).
- Pre-fetched OAuth values were used (raw values quoted in `authorization_mechanism`).
- Length limits respected.
- OAuth metadata was attempted, and scopes are compared with the tool list.
- Contradictions list is filled or explicitly empty `[]`.
- Output is a single valid JSON object.
