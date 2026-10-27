# MCP server: GoCardless

> **In plain words.** GoCardless is a payment service for collecting payments by Direct Debit and bank payments: one-off payments, subscriptions, refunds. Its MCP server lets an AI assistant (1) help a developer with the integration (code examples, API explanations) and (2) after signing in, work with the **company's real account**: search payments and customers, and also **create payments, issue refunds, cancel mandates**. This is a server that **moves money**.
>
> **Analysis date:** 13.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Abbreviations in links:**
- `[docs]` = [GoCardless Developer Docs: MCP](https://docs.gocardless.com/docs/developer-resources/mcp) (the CSV link redirects here).
- `[support]` = [Support: Use AI to manage your account](https://support.gocardless.com/hc/en-gb/articles/26830050176028-Use-AI-to-manage-your-account).
- `[terms]` = [MCP Terms (Live)](https://docs.gocardless.com/docs/developer-resources/mcp/terms); `[terms-sb]` = [Terms (Sandbox)](https://docs.gocardless.com/docs/developer-resources/mcp/terms-sandbox).
- `[prm]` = https://mcp.gocardless.com/.well-known/oauth-protected-resource; `[asm]` = https://mcp.gocardless.com/.well-known/oauth-authorization-server.
- `[composio]` = [Composio: GoCardless MCP toolkit](https://composio.dev/toolkits/gocardless_mcp/framework/claude-cowork) (third-party catalogue, date not given).

---

## ⚠️ Important limitation of the analysis

**The server code is closed.** There is no repository, and the documentation contains no links to code [docs]. GoCardless does not publish an official tool list: [docs] and [support] describe only capabilities. The list of 24 tools below is taken from a **third-party catalogue** [composio]. The names there are given in a "human-readable" form (e.g. "Create payment"); the real names in `tools/list` may differ. Verbatim descriptions cannot be obtained without signing in.

glama.ai lists an open-source "gocardless-mcp" by a private developer (jmceleney). This is **not** the official server and is not part of the analysis.

---

## A. General

| Field | Value | Source |
|---|---|---|
| Name | GoCardless MCP | [docs] |
| Code link | Not published | [docs] |
| Documentation | https://developer.gocardless.com/developer-tools/mcp/ (from the CSV) → redirects to [docs]; [support] | — |
| Endpoint | `https://mcp.gocardless.com/mcp` (CSV); [docs] gives `https://mcp.gocardless.com`. OAuth resource: `https://mcp.gocardless.com` | CSV, [docs], [prm] |
| Environments | **Live** (real money) and **Sandbox** (test). Chosen at sign-in; to switch — disconnect and connect again | [docs], [support] |
| MCP version | Not published | [docs] (checked: the .md version of the page contains no version) |
| Commit / date | Not applicable (code closed). Documentation snapshot: 13.10.2026 | — |
| Language / MCP SDK | Not published | — |
| Transport | HTTP (Streamable HTTP) | [docs] |
| Code open? License | No | — |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to the MCP server | **Free**: "The CLI, MCP and MCP Data are provided free of charge", but "GoCardless reserves the right to charge in the future" (clause 2.3) | [terms] |
| Linked software | Paid, fee per transaction: **Standard 1% + 20p (max £4)**, international 2% + 20p; **Advanced 1.25% + 20p (max £5)**; **Pro 1.4% + 20p (max £5.60)**; Custom — by agreement; no subscription fee (except add-ons at £50 and £150/month) | [pricing](https://gocardless.com/pricing/) |
| Requirements for the AI client | Claude requires a "Pro, Max, Team, or Enterprise" plan; free AI plans "typically don't support MCPs". On Team/Enterprise the connector is first added by the Owner/Primary Owner | [docs], [support] |
| Access restrictions | (1) **The user chooses the rights at sign-in**: everything, read-only or specific actions (e.g. "refunds only"); to change them — reconnect. (2) Plus the restrictions of the **user's role** in the dashboard (a read-only user cannot create a payment). (3) **Bulk operation limits**, e.g. no more than 25 payments at a time. (4) Access expires periodically — a new sign-in is needed | [support] |
| Controlled by | User (choice of rights at sign-in), dashboard administrator (roles), GoCardless (limits, masking) | [support] |
| Rate limits | Not documented | — |

## C. Implemented capabilities

| Capability | Present? | Details (what/how) | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | 24 tools according to [composio]: 16 reading, 7 writing, 1 feedback. For each writing tool the required scope is given (`payments:write`, `refunds:write`, `mandates:write`, `subscriptions:write`, `payment_links:write`) | **Not published verbatim** | Not documented. Known: sensitive fields are **masked before the AI sees them** (e-mail, phone, postcode, identification numbers); bank details are not passed at all [support] |
| Resources | ❓ | Not documented. There is a tool "Read gocardless resource" that returns documentation, guides and code examples (not account data) [composio] — the resource function is implemented via a tool | — | — |
| Prompts | ❓ | Not documented. The tool "Integrate with gocardless" gives an overview of integration options [composio] | — | — |
| **Elicitation / confirmation** | ✅ (mechanism not specified) | "Higher-risk write actions, such as creating a payment, show a preview and wait for explicit confirmation before proceeding" [support]; "read the confirmation preview before approving" [docs]. **By which mechanism this is done (MCP Elicitation, a two-step tool or client confirmation) is not stated** | — | A preview of the action (content not documented) |
| Logging (MCP) | ❓ | Not documented. On the product side there is a log: see D | — | — |
| Sampling / Roots / Tasks / Subscription / Progress / Cancellation | ❓ | Not documented | — | — |
| **Authorization** | ✅ | Sign-in in the browser ("sign in"). According to the metadata — OAuth: **Metadata Doc** — yes ([prm], [asm]); **Dynamic Client Registration** — yes (`registration_endpoint: https://mcp.gocardless.com/register`); `grant_types_supported: authorization_code`; PKCE `S256`; `token_endpoint_auth_methods_supported: none` (public clients); `scopes_supported` is not given in the metadata. **Authorization server** — `https://mcp.gocardless.com` itself. Revoking access: Settings → Connected apps → Revoke access | [prm], [asm], [support] | — |
| Configuration | ✅ partial | Choice of environment (Live/Sandbox) and set of rights at sign-in | [docs], [support] | — |
| Error Reporting | ❓ | Not documented | — | — |
| Other | ✅ | The tool "Get environment" reports whether it is Sandbox or Live and how to switch [composio]; "Submit feedback" — a session rating from 1 to 5 [composio] | — | — |

## D. Server logic beyond simply passing commands through

According to the documentation (code closed):
1. **Confirmation of money operations:** "money-moving actions need your confirmation before they execute" [docs]; preview and explicit confirmation for risky actions [support]. This is the only one of the analysed servers that **promises mandatory server-side confirmation** (mechanism not disclosed).
2. **Masking of personal data** before passing it to the AI (e-mail, phone, postcode, ID numbers); bank details are never passed [support].
3. **Granular rights at sign-in** (down to "refunds only") plus the intersection with the user's role [support].
4. **Bulk operation limits** (e.g. ≤ 25 payments per call) [support].
5. **Action log:** all actions via MCP are recorded in the event history with the source "App (GoCardless MCP)" (Developers → Events) [support].
6. **Separation of environments:** Sandbox and Live are separate connections with separate terms ([terms], [terms-sb]).
7. **Access expiry:** access expires periodically. The user is explicitly discouraged from using API tokens because they do not expire and give permanent access if leaked [support].

**Server structure:** standard, but **two purposes in one server**: integration help (without account access) and account management (after sign-in).

## E. Overall evaluation

**Number of actions:** **24** (according to [composio]; not officially confirmed).

| # | Action (as in the catalogue) | Type | Right (scope) / note |
|---|---|---|---|
| 1 | Create payment | change (money) | `payments:write`; preview + confirmation |
| 2 | Cancel payment | change | `payments:write` |
| 3 | Create refund | change (money) | `refunds:write` |
| 4 | Create subscription | change (money, recurring) | `subscriptions:write` |
| 5 | Cancel mandate | change | `mandates:write` |
| 6 | Create payment link | change | `payment_links:write` |
| 7 | Create payment template link | change | `payment_links:write` |
| 8–14 | Get customer / mandate / payment / payout / refund / subscription; Get environment | read | — |
| 15–21 | List customers / events (change log) / mandates / payments (filters, counting) / payouts / refunds / subscriptions | read | — |
| 22 | Integrate with gocardless | help | without account access |
| 23 | Read gocardless resource | help | documentation, code |
| 24 | Submit feedback | sending a rating 1–5 | — |

[support] also mentions **"retry" of payments**, but the catalogue has no separate tool for this. Possibly the catalogue is outdated or the retry is part of another tool.

**Parameters:** not published. From the descriptions in [composio]: filters by status, customer, mandate, subscription, currency, date.

**Tokens before the first action:** cannot be determined.

**What the agent CANNOT do but a human can** (comparison of [support] and [composio] with the capabilities of the dashboard/API):
- Create customers and mandates directly (the API has this, the MCP tool list does not; the agent can only create a payment link) ([API reference](https://developer.gocardless.com/api-reference)); manage account settings, users, webhooks; run Sandbox scenario simulators ([Scenario Simulators](https://docs.gocardless.com/docs/developer-resources/scenario-simulators) — a separate dashboard/API tool, not MCP). Source of the MCP list: [composio].
- See **unmasked** personal data and bank details.
- Act outside the rights chosen at sign-in.

## F. Documentation analysis

**Recommendations to the user that the server does not check:**
- "Never share your API keys with your LLM"; use the sandbox during development; **review generated code** before running it; give the AI only the necessary rights; **test writing actions in Sandbox first**; in writing requests, specify the exact resource and amount and read the preview [docs].
- Check the AI provider's policy: on free/personal plans "conversations may be used for AI training" [docs].
- Add to the prompt "For any prompt that mentions GoCardless, use the GoCardless MCP", because some AIs search the internet instead of using MCP [docs].
- Agents without human review carry "extra risk", and **the responsibility for their actions lies with the user** [support].

**Promises on governance and data:**
- Masking of sensitive data, bank details are not passed [support], [docs].
- Log of all actions in Events [support].
- Terms [terms]: GoCardless's liability is limited to **£50** (clause 9.5); **using MCP to process personal data is prohibited** (clause 4.1.5) — even though the server returns customer data (masked); the AI provider must use the data only for the answer and **delete it immediately** (clauses 4.2.1, 4.2.4), and **the user is liable** for breaches by the provider (clause 4.3); GoCardless does not guarantee the absence of "bias or hallucinations" (clause 7.3); continuous availability is not guaranteed (clause 2.4).

**Promises to the user:** two functions — "integration guidance and account management" [docs]; the possibility to submit a request for a missing feature [support].

**Comparison with the server logic:** the declared measures (confirmation, masking, limits, log) cannot be checked against the code. There is an **internal contradiction**: the terms prohibit processing personal data via MCP, while the server returns customer data (albeit masked). The requirement that the AI provider "delete the data immediately" cannot be ensured by the user: it depends on the provider's policy.

---

## Observations for the research

- **The most developed protection model for financial actions:** server-side confirmation, granular rights at sign-in, masking, limits, a log with the source marked, a separate sandbox.
- **Legal shift of responsibility to the user:** liability cap of £50, the user is liable for the AI provider and for the agents' actions.
- **Data masking** is a design technique that the other analysed servers do not have: the server decides what the AI sees.
- **The user chooses the rights at sign-in** (not the administrator and not a fixed set), but they can be changed only by reconnecting.
- **Collection of ratings** ("Submit feedback" 1–5), like Tavily and Lucid.
