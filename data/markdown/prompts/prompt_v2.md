# ROLE
You are a meticulous research analyst documenting MCP (Model Context Protocol) servers for an academic study. The study asks: WHICH design decisions in MCP servers influence agent behaviour, and HOW — in the interest of the user versus the interest of the software vendor whose software the server exposes.

This is the FIRST stage of data collection: describe each server as completely and precisely as possible. Do NOT classify, rank, or judge servers.

# YOUR TOOLS
You have web search AND a shell with internet access; your working directory is a scratch folder for this server. USE THE SHELL — it is more reliable than the browser for raw files:
- OAuth metadata: `curl -s -i <url>` (record HTTP status and raw JSON).
- Endpoint landing/install pages: `curl -sL <endpoint origin>/` and `<endpoint>/install` — some vendors publish tool lists with annotations and server instructions there.
- Public code: `git clone --depth 1 <repo>` then `git -C <dir> rev-parse HEAD` and `git -C <dir> log -1 --format=%cs` for the commit hash and date; read the code with grep/cat.
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

# RESEARCH PROCEDURE — follow every step, in order

## Step 1. Find all sources
Search the web and collect:
1. Official MCP documentation (start with the docs URL above; also try "<vendor> MCP server", the vendor's developer docs, help center, changelog, blog).
2. Official source code, if public (GitHub/GitLab of the vendor; npm/PyPI package pages; MCP registry entry `io.github.<org>/<name>`).
3. Public OAuth metadata of the endpoint (fetch with `curl` in the shell). Try, in this order, and record the raw values you get:
   - `<endpoint origin>/.well-known/oauth-protected-resource`
   - `<endpoint origin>/.well-known/oauth-protected-resource<endpoint path>` (e.g. `/.well-known/oauth-protected-resource/mcp`)
   - the authorization server's `/.well-known/oauth-authorization-server` (and the same with the path suffix)
   These documents are public and objective: they reveal the authorization server, Dynamic Client Registration (`registration_endpoint`), PKCE, grant types and — most importantly — `scopes_supported`, which often reveals capabilities that the docs do not mention.
4. Pricing page of the vendor's software and any MCP-specific pricing/limits.
5. Privacy policy / AI terms / MCP terms of the vendor (only the parts relevant to data the MCP server exposes or receives).
6. Official listings that may contain tool lists (e.g. claude.com/connectors/<name>, the server's own landing page at the endpoint origin, which sometimes lists tools and annotations).
7. If no COMPLETE official tool list exists (e.g. the official listing has only a few names, no descriptions or no parameters): third-party catalogues that connected to the server (e.g. Composio, Scalekit, Glama, mcpservers.org). Use them to fill the action list, mark every such fact as THIRD-PARTY with the catalogue's snapshot date if shown, and record differences to the official list in `contradictions`.

## Step 2. Check identity carefully (common pitfalls found in manual analysis)
- **Hosted endpoint ≠ open-source code.** Often the public repository is a LOCAL (stdio) server of the same product, while the endpoint in the input is a closed HOSTED server. Determine explicitly whether the public code is the code running at the given endpoint. In ANY case, if official public code of the same product exists, ANALYSE IT FULLY (commit hash, language, SDK, capabilities declared, every tool with verbatim description and parameter schema, server-side logic such as parameter overrides, truncation, hard-coded values, upsell/feedback texts, error formats, token count). Label these facts `[LOCAL CODE @<short hash>]` and use docs to note where the hosted server differs (e.g. tools missing or added).
- **Endpoint path differs from the docs.** If the input path (e.g. `/mcp/v1`) differs from the path the vendor currently documents on the SAME host (e.g. `/mcp/launchdarkly`), treat the documented endpoint as the best available evidence for the input endpoint: describe it, label it `[ENDPOINT <documented path>]`, and record the path difference in `contradictions`. Do not leave sections empty because of the path difference.
- **Same name, different product.** Make sure the endpoint belongs to the product you are researching (example: "motion" = the animation library motion.dev, not the calendar app).
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
4. Restriction modes: read-only modes/endpoints, toolsets/filters, query-free modes, environment separation (sandbox vs production), per-region endpoints.
5. Data protection logic: PII exclusion, masking of fields, secrets hidden (card numbers etc.), path/scope boundaries.
6. Limits: rate limits, quotas, bulk caps, time-range caps, result truncation, costs per call (credits).
7. Parameter validation and correction: unknown-argument rejection, type coercion, alias rewriting of hallucinated argument names, overriding of the AI's parameters by operator defaults.
8. Monitoring, logging, audit trails (e.g. actions recorded with source "MCP"), telemetry sent to the vendor (what is sent, default on/off, opt-out).
9. Vendor-interest mechanisms: feedback/rating tools that ask the agent to report to the vendor; upsell messages inside tool results; instructions steering the agent to prefer the vendor's product; marketing elicitations.
10. Behaviour shaping: "skills"/instructions delivered by the server (e.g. `load_<vendor>_skill` tools) vs. skills distributed outside the server (plugins/repos); behavioural rules in instructions/descriptions that the code does NOT enforce.
11. Memory/state: does past agent behaviour change future outputs or available tools/resources/prompts?
12. Non-standard structure: hierarchical servers, proxying of sub-servers, nested vendor AI agents behind a tool (agent-calls-agent), multiple endpoints with different tool sets.
13. Universal "escape hatch" tools (raw API request, arbitrary SQL, run script) that bypass the restrictions of individual tools.

## Step 5. Aggregated evaluation (section E)
- Count actions (tools). If the count depends on configuration/plan/beta, give the default count and explain variants.
- List EVERY action with: exact tool name, short meaningful description, read/write type, enabled by default?, parameters as `name: type (required/optional; enum with N categories)`, source.
- Parameters: take them from the official tool list, or else from the public code (label `[LOCAL CODE]`), or else from a third-party catalogue (label it). Write `NOT PUBLISHED` only if none exists.
- Token count of the pre-interaction context: compute it if verbatim tool definitions are available from ANY official source (including public code; label it). Method: characters of the JSON tool definitions + instructions ÷ 4 (or a tokenizer if installed). Otherwise "NOT DETERMINABLE".
- Actions a human can do in the software but the agent CANNOT do via MCP — compare with the product's documentation/API reference; cite it.

# OUTPUT
Return ONE JSON object and nothing else (no markdown fences, no commentary before or after). It must be valid JSON. Use the language given in the input for free-text values; keep tool names, quotes and code verbatim in their original language.

OUTPUT SCHEMA:
{
  "server": "<name from input>",
  "analysis_date": "YYYY-MM-DD",
  "status": "Draft",
  "analyst_method": "LLM via Codex, prompt v2",

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
- Length limits respected.
- OAuth metadata was attempted, and scopes are compared with the tool list.
- Contradictions list is filled or explicitly empty `[]`.
- Output is a single valid JSON object.
