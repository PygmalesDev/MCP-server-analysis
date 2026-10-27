# MCP server: Similarweb

> **In plain words.** Similarweb is a "digital market" analytics service: it estimates website traffic, traffic sources, keywords, mobile app data (downloads, users, revenue), audiences. Its MCP server gives an AI assistant more than 40 tools to **get these estimates for any website or app**, e.g. for competitors. The server only reads, but **every request consumes paid data credits**.
>
> **Analysis date:** 16.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[landing]` = [similarweb.com/corp/ai/mcp](https://www.similarweb.com/corp/ai/mcp/) (link from the CSV).
- `[setup]` = [Similarweb MCP: Getting Started](https://docs.similarweb.com/api-v5/mcp-integration/mcp-setup).
- `[prm]` = https://mcp.similarweb.com/.well-known/oauth-protected-resource.
- `[pricing]` = [similarweb.com/corp/pricing](https://www.similarweb.com/corp/pricing/).

> ⚠️ **The code is closed.** The tool names in [setup] are "human-readable" (e.g. "Traffic and Engagement"), the descriptions are paraphrased. The exact `tools/list` is not published.

## A. General

| Field | Value | Source |
|---|---|---|
| Code / license | Closed | — |
| Endpoint | `https://mcp.similarweb.com` (CSV: `/mcp`) | [setup], [prm] |
| MCP version / language / SDK | Not published | — |
| Clients | Claude, ChatGPT, Cursor, Copilot, Manus, Perplexity, Zapier, n8n and others; custom connections — via support | [setup], [landing] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Requirements | "Similarweb subscription with API/MCP access" — API-only, Business or Enterprise plans | [setup] |
| **Cost of actions** | "MCP uses **data credits** the same way standard API responses do"; consumption depends on the prompt and the amount of data ("Queries that pull more data points use more credits"); no figures per call | [setup] |
| Linked software | Web Intelligence from **$125/month** (for small companies); Business/Enterprise and API — on request; MCP is a feature of AI Studio / Data as a Service without a separate price | [pricing] |
| Limits | Not given | [setup] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **43** tools (see E): web and traffic (19), search (4), apps and ASO (20). All are reads | Not published | Not documented |
| **Authorization** | ✅ | Sign-in to the Similarweb account. **Metadata Doc** — yes; **authorization server** — `https://mcp-auth.similarweb.com`; scope **`read`** (read only) | [setup], [prm] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic

- **Every call is charged** in data credits, like the API. The agent spends the user's money, and the consumption depends on how it formulates its requests [setup].
- **Read only** (the only scope is `read`) [prm].
- Restrictions: Audience Overlap — 2–5 websites; ASO Keyword Rank History — up to 50 keywords [setup].
- Spending limits and cost warnings on the server side are **not described**.

## E. Overall evaluation

**Number of actions:** **43** [setup] (19 + 4 + 20).

| Group | Tools |
|---|---|
| Web and traffic (19) | Traffic and Engagement; Traffic Sources; Website Rank; Subdomains; Similar Sites; Referrals; Audience Interests; Audience Overlap (2–5 websites); Deduplicated Audience; Leading Folders; Popular Pages; PPC Spend; Segment Traffic and Engagement; Segment Traffic Sources; Ad Networks; Geography; Technologies; Demographics; Traffic by Demographics |
| Search (4) | SERP Players; SERP Clicks; Keywords Overview; Website Keywords |
| Apps and ASO (20) | App Install Penetration; App Store Rank; App Search; App Details; App Changelog; App IAB Categories; App SDKs; App Active Users; App Downloads; App Sessions; App Retention; App Revenue; App Ratings; App Ranks; App Top Charts; App Audience Demographics; App Audience Interests; ASO Keyword Rank History (up to 50 keywords); ASO Top Ranked Keywords; ASO Search Results |

**Parameters:** not published (domains, keywords, app IDs, countries, periods).

**Tokens:** cannot be determined; with 40+ tools the context is noticeable.

**What the agent CANNOT do:** Amazon data and lead enrichment (announced on [landing], but there are no tools for them in the list in [setup]); management of the account, credits, reports and platform dashboards; checking the credit balance (a separate API page) [setup].

## F. Documentation analysis

- **Recommendations/disclaimers:** AI answers "may be incomplete, inaccurate, or subject to AI interpretation"; use is "at the user's sole risk"; Similarweb disclaims warranties for data and conclusions [setup].
- **Governance/data:** there is no privacy section; only "Secure and scalable" [landing].
- **Comparison with the logic:** the Amazon data and lead enrichment promised on [landing] were not found in the tool list.

## Observations

- **Every action of the agent costs money** (credits), and the consumption depends on the agent's behaviour. There are no limits or warnings on the server.
- **Shift of responsibility** for the quality of AI conclusions to the user ("sole risk").
- **A broad read-only server** — 40+ tools, one scope `read`.
- **Divergence between marketing and the tool set** (Amazon, lead enrichment).
