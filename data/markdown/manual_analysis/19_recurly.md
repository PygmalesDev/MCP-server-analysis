# MCP server: Recurly (Compass)

> **In plain words.** Recurly is a platform for managing subscriptions and recurring payments (subscription billing, invoices, revenue). Its MCP server **Compass** is currently a **reference assistant**: it answers questions about the Recurly documentation and helps write code for the API. According to the documentation it does **not work** with account data (subscribers, payments).
>
> **Analysis date:** 16.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [Recurly Compass public MCP server](https://docs.recurly.com/docs/compass-public-mcp-server) (link from the CSV).
- `[prm]` = https://mcp.recurly.com/.well-known/oauth-protected-resource.
- `[pricing]` = [recurly.com/pricing](https://recurly.com/pricing/).

> ⚠️ **The code is closed.** The descriptions of the two tools are quoted in the documentation; the full `tools/list` is not published.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Compass MCP (Recurly's "public MCP server") | [docs] |
| Code / license | Closed | — |
| Endpoint | `https://mcp.recurly.com/mcp` (Streamable HTTP) | [docs], [prm] |
| Status | **Early access only**; "available on all Recurly subscription plans at general release" | [docs] |
| MCP version / language / SDK | Not published | — |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | No separate price; currently a Recurly site with the **MCP feature flag** enabled and rights on this site are required | [docs] |
| Linked software | Starter **$249/month + 0.9%** of billing volume (the first $40K per month free); All-Access — from <1% (minimum $1 million volume); Engage from $1,600/month; RevRec from $850/month | [pricing] |
| Restrictions | Tokens expire after **30 days** | [docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **2** tools, each an interface to a Recurly "agent": `docs_search` (Knowledge Agent): "Searches Recurly's documentation knowledge base to answer questions and surface relevant content"; `api_reference_search` (Coding Agent): "Provides code examples, parameter references, library guidance, and explanations to help you get code running faster" | Quoted descriptions — [docs] (whether they match `tools/list` cannot be checked) | Not documented |
| **Authorization** | ✅ | OAuth (sign-in to Recurly). **Metadata Doc** — yes; **authorization server** — `https://oauth.recurly.com`; scope `mcp:tools` | [docs], [prm] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic

- **The server as a facade for the vendor's own AI agents:** the tools do not call the API but pass the question to Recurly's internal agents (Knowledge Agent, Coding Agent) — "exposes Recurly's agents to compatible AI tools" [docs].
- **Feature flag at the site level** — the vendor controls who gets early access.
- In the configuration example for Cursor both tools are listed in **`autoApprove`** — calls without confirmation [docs]. For tools that only read this is safe.

## E. Overall evaluation

| # | Action | Parameters |
|---|---|---|
| 1 | Search the documentation (`docs_search`) | not published (probably the question text) |
| 2 | API reference and code examples (`api_reference_search`) | not published |

**Tokens:** cannot be determined; with 2 tools the context is small.

**What the agent CANNOT do:** **any operations with account data** — subscribers, subscriptions, invoices, payments, plans, reports (neither reading nor writing is documented) [docs].

## F. Documentation analysis

- **Recommendations not checked:** none. The `autoApprove` example effectively recommends **turning off confirmation**.
- **Governance/data:** not described [docs]. At the same time sign-in is via the Recurly account with rights on the site, although the tools only work with documentation.
- **Promises:** brings "Recurly knowledge" into developer tools [docs].

## Observations

- **"An agent behind the tool":** MCP is a thin wrapper around the vendor's internal AI agents (like Braze's Operator). The external AI talks to the internal one.
- **Authorization broader than necessary:** reading public documentation requires sign-in to an account with rights on the site. Possibly groundwork for future tools with data.
- **Early access via a feature flag** — the vendor opens the feature gradually.
