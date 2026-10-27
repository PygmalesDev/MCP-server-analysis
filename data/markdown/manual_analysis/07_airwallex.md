# MCP server: Airwallex (AgentOS MCP)

> **In plain words.** Airwallex is a financial platform for businesses: multi-currency accounts, international transfers, currency exchange, corporate cards, invoicing and subscriptions. Its MCP server **AgentOS** lets an AI agent work with the company's **production account**: view balances and transactions, create payment beneficiaries, issue corporate cards, issue invoices. However, **the agent must not make transfers, currency exchanges or payouts**.
>
> **Analysis date:** 13.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Abbreviations in links:**
- `[agentos]` = [Airwallex AgentOS](https://www.airwallex.com/docs/developer-tools/ai/agentos) (link from the CSV) and its version [agentos.md](https://www.airwallex.com/docs/developer-tools/ai/agentos.md).
- `[devconn]` = [Developer connectors](https://www.airwallex.com/docs/developer-tools/ai/developer-connector.md).
- `[mkt]` = repository [airwallex/airwallex-marketplace](https://github.com/airwallex/airwallex-marketplace/tree/877551077786664d1cbeb32013443291c66e69e6) (plugins and skills), commit `8775510`, 2026-10-14.
- `[bp]` = [skills/awx-best-practices/SKILL.md](https://github.com/airwallex/airwallex-marketplace/blob/877551077786664d1cbeb32013443291c66e69e6/plugins/airwallex-agentos/skills/awx-best-practices/SKILL.md); `[sq]` = [surface-quickstart.md](https://github.com/airwallex/airwallex-marketplace/blob/877551077786664d1cbeb32013443291c66e69e6/plugins/airwallex-agentos/skills/awx-best-practices/references/surface-quickstart.md); `[fb]` = [references/feedback.md](https://github.com/airwallex/airwallex-marketplace/blob/877551077786664d1cbeb32013443291c66e69e6/plugins/airwallex-agentos/references/feedback.md).
- `[prm]` = https://mcp.airwallex.com/.well-known/oauth-protected-resource/mcp; `[asm]` = https://mcp.airwallex.com/.well-known/oauth-authorization-server/mcp.

---

## ⚠️ Important limitation of the analysis

- **The server code is closed.** Only the repository [mkt] with plugins and skills (instructions for AI clients) is open, license Apache 2.0.
- **The AgentOS tool list is not published**, neither in the documentation nor in catalogues. The skills also say: "Discover tool names from your MCP client's tool list. Do not assume names" [sq]. Therefore **the set of capabilities was reconstructed from the list of OAuth scopes** that the server publishes openly [prm]. Scopes show *what* can be accessed, but not the exact tools.
- Airwallex has **three** MCP servers: **AgentOS** (`mcp.airwallex.com/mcp`, production, from the CSV — analysed here), **Developer MCP** (`mcp.sandbox.airwallex.com/developer`, sandbox) and **Docs MCP** (documentation only) [devconn]. The list of 12 tools in the Claude catalogue ([claude.com/marketplace/connectors/airwallex](https://claude.com/marketplace/connectors/airwallex)) belongs to the **Developer MCP**, not to AgentOS.

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Airwallex AgentOS MCP (connector name: `airwallex-agentos`) | [agentos], [mkt] `.mcp.json` |
| Code link | Server — closed. Plugins and skills: [mkt] | [agentos] |
| Documentation | https://www.airwallex.com/docs/developer-tools/ai/agentos (from the CSV) | CSV |
| Endpoint | `https://mcp.airwallex.com/mcp` — **production only** | [agentos], [prm] |
| MCP version | Not published | — |
| Commit / date | Server — not applicable. Skills: `877551077786664d1cbeb32013443291c66e69e6`, 2026-10-14 | `git log` |
| Language / MCP SDK | Not published | — |
| Transport | HTTP (Streamable HTTP) | [agentos] |
| Code open? License | Server — no. Skills/plugins — **Apache 2.0** | [mkt] LICENSE |
| Status | AgentOS skills — **beta**: "The skill set and behavior may change before general availability" | [agentos.md] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | No separate price for MCP is given | [agentos] |
| Linked software | Paid (financial services). Plans (EU): **Explore €0** (with deposits/balance ≥ €10,000/month, otherwise €19/month), **Grow €49/month**, **Accelerate** — custom. FX markup: 0.5% for major currencies, 1% for the others. The Core API is included in Explore, but "fees may apply for additional access" | [pricing](https://www.airwallex.com/de/pricing) |
| Access restrictions | (1) OAuth to the production account; at authorization the user chooses the scopes ("grant only the OAuth scopes your use case needs"). (2) **AgentOS does not initiate outgoing money operations (transfers, currency exchange, payouts).** There are no write scopes for them either (see C). (3) User rights and Airwallex roles ([OAuth permissions and user roles](https://www.airwallex.com/docs/developer-tools/partner-connections/oauth-permissions)) | [agentos.md], [prm] |
| Controlled by | Airwallex (set of scopes, money-out ban), user (choice of scopes at sign-in) | same |
| Rate limits | Not documented | — |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | The exact list is not published. According to the scopes ([prm]) — reading: balances, contacts/beneficiaries, conversions, global accounts, cardholders, cards, card transactions, `pa_view` (probably Payment Acceptance — the meaning is not published), payment links, account details, transfers, billing (customers, discounts, invoices, payment methods, prices, products, subscriptions, transactions, metering), expenses, vendor bills, vendors. Writing: contacts, cardholders, cards, payment links, billing (customers, discounts, invoices, prices, products, subscriptions, metering), **feedback to the developers**. Also search in the Airwallex documentation [agentos] | **Not published.** "The server annotates write tools (create, update, or delete) so clients can prompt for confirmation" [agentos.md] — i.e. the writing tools have annotations | Not documented |
| **Server instructions** | ✅ | "The server declares its environment (sandbox vs production) in its instructions on connect" [sq]; the components are "explicitly instructed not to execute" outgoing money operations [agentos.md] | Text not published | — |
| Resources / Prompts | ❓ | Not documented. Instead of prompts — external skills [mkt] | — | — |
| Logging / Sampling / Roots / Elicitation / Tasks / Subscription / Progress / Cancellation | ❓ | Not documented | — | — |
| **Authorization** | ✅ | OAuth to the production account. **Metadata Doc** — yes ([prm], [asm]); **Dynamic Client Registration** — yes (`registration_endpoint: https://mcp.airwallex.com/mcp/register`); grant types `authorization_code`, `refresh_token`; PKCE `S256`; client authentication methods `client_secret_post`, `client_secret_basic`, `private_key_jwt`, `none`. **35 scopes**: 23 for reading (`r:…`), 12 for writing (`w:…`). **Authorization server** — `https://mcp.airwallex.com/mcp`. Tokens are refreshed automatically; if a 401 persists, the grant has been revoked and re-authorization is needed [bp]. Revocation — on the Airwallex integrations page | [prm], [asm], [agentos] | — |
| Configuration | ✅ partial | Choice of scopes at authorization | [agentos] | — |
| Error Reporting | ❓ | Not documented (the skills advise "Show full error, ask user" [bp]) | — | — |

**Full list of scopes** [prm]:
- Reading (23): `r:awx_action:balances_view`, `contact_management_view`, `conversions_view`, `global_accounts_view`, `issuing_cardholders_view`, `issuing_cards_view`, `issuing_transactions_view`, `pa_view`, `payment_links_view`, `settings.account_details_view`, `transfers_view`; `r:org_action:billing.customer_view`, `billing.discount_view`, `billing.invoice_view`, `billing.payment_source_view`, `billing.price_view`, `billing.product_view`, `billing.subscription_view`, `billing.transaction_view`, `billing.usage_metering_view`, `expense_management.expense:api_view`, `spend.bills:api_view`, `spend.vendors:api_view`.
- Writing (12): `w:awx_action:contact_management_edit`, `devx.feedback_write`, `issuing_cardholders_edit`, `issuing_cards_edit`, `payment_links_edit`; `w:org_action:billing.customer_edit`, `billing.discount_edit`, `billing.invoice_edit`, `billing.price_edit`, `billing.product_edit`, `billing.subscription_edit`, `billing.usage_metering_edit`.

## D. Server logic beyond simply passing commands through

1. **Ban on outgoing money operations at the level of rights.** For transfers and conversions there are only **read** scopes (`transfers_view`, `conversions_view`); there are no write scopes for them. So even with the user's full consent the agent cannot send money. Documentation: "AgentOS components do not initiate money-out actions (transfers, FX conversions, or payouts) on your behalf" [agentos.md].
2. **Annotations of writing tools** so that the client asks for confirmation [agentos.md]. The confirmation itself is shown by the client, not the server.
3. **Declaration of the environment in the server instructions** (production), so that the agent tells the user about it before writing [sq].
4. **Production only.** The sandbox is a separate server (Developer MCP) [devconn].
5. **Rules in skills (outside the server, work when the skill is loaded)** [bp], [sq]:
   - "NEVER fabricate or assume missing information … STOP and ask the user";
   - before irreversible operations (void/finalize an invoice, close a card — "**Permanent**", close a global account) name the environment, explain the consequences, get explicit confirmation;
   - "always show the user the full payload before invoking a write tool; never call a write tool silently";
   - **"Do not provide financial advice"**: refuse requests about exchange rate forecasts, hedging, investments;
   - for the CLI the cycle `--dry-run` → show → confirm → `--confirm` is mandatory.
6. **Feedback collection:** scope `devx.feedback_write`; the skills tell the agent to **offer on its own** to send feedback if it noticed a problem, but only with the user's consent and without sensitive data [fb].

**Server structure:** non-standard at the scale of the ecosystem. Three separate servers by purpose and environment (AgentOS / Developer / Docs) plus a common layer of skills that works the same via MCP and via the CLI [mkt] README.

## E. Overall evaluation

**Number of actions:** the exact number of tools is **not published**. According to the scopes — access to **23 data types for reading** and **12 for writing** (including feedback), plus documentation search.

**List of actions (according to scopes and skills, without exact names):**
- Reading: balances; contacts/beneficiaries; conversions; global accounts; cardholders; cards; card transactions; `pa_view` (probably Payment Acceptance); payment links; account details; transfers; billing (9 objects); expenses; vendor bills; vendors.
- Writing: create/change a beneficiary; create a cardholder; issue, change, block or **close** a card; payment links; billing — customers, discounts, invoices (create, finalize, void, mark as paid), prices, products, subscriptions (including cancel), metering; send feedback.
- Workflow skills: `contract-to-billing`, `beneficiary-creation`, `card-provisioning`, `manage-cashflow`, `awx-best-practices` [mkt].

The skill [bp] separately notes what is **not in MCP**: deleting a draft invoice, finalizing and voiding credit notes ("credit-note tools not exposed — use the CLI or the Airwallex Dashboard").

**Parameters:** not published. The skills mention a mandatory `request_id` (UUIDv4) for some tools [sq].

**Tokens before the first action:** cannot be determined.

**What the agent CANNOT do but a human can:**
- **Transfers, payouts, currency exchange** — only in the dashboard ("FX conversion: Airwallex Dashboard only") [bp], [agentos.md].
- Get the **card number/CVV** [bp].
- Delete a draft invoice, work with credit notes (CLI/dashboard only) [bp].
- Work in the sandbox via AgentOS (this needs the Developer MCP).

## F. Documentation analysis

**Recommendations to the user that the server does not check** [agentos]:
- Turn off auto-approval modes ("Auto-Run", "Dangerously Skip Permissions"); confirm writing actions in the Airwallex web or mobile app.
- Treat untrusted documents and web pages as a **prompt injection** risk and review every tool call.
- Do not paste API tokens into prompts; start a new chat for sensitive tasks.
- Use a **frontier model** for AgentOS sessions.
- Install only trusted MCP servers alongside it.
- **Do not add the agent to shared channels (Slack)**, because any participant could act with your rights.
- Grant only the necessary scopes.

**Promises on governance and data:**
- "AgentOS components do not initiate money-out actions" [agentos.md]. Confirmed by the structure of the scopes.
- Writing tools are annotated for confirmation [agentos.md].
- The MCP documentation has no separate privacy section, only a link to the Terms of Service. "Agent outputs are probabilistic" — review code and recommendations before use [agentos].
- Logging of the agent's actions is not described in the documentation.

**Promises to the user:** AgentOS is a set of tools so that agents can "act on a production Airwallex account"; support for Claude Code, Claude Cowork, Cursor, Codex and others [agentos].

**Comparison with the server logic:** the "no money-out" promise **is confirmed by the public metadata** (no write scopes for transfers and FX). The rest (annotations, instructions) cannot be checked without signing in.

---

## Observations for the research

- **A restriction via OAuth scopes** can be checked from outside without the code. This is a good objective indicator for comparing servers: it is worth collecting `/.well-known/oauth-protected-resource` for all servers in the list.
- **Money operations are excluded by design.** This differs from GoCardless, where they are allowed but with confirmation.
- **The most detailed set of agent security recommendations** (prompt injection, frontier model, shared channels). But these are recommendations, not mechanisms.
- **Behaviour rules and the ban on financial advice are in skills**, outside the server.
- **The agent is asked to initiate product feedback itself** (with the user's consent).
- **Separation by environment at the level of separate servers** (production / sandbox / docs).
