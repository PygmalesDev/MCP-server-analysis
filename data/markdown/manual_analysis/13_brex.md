# MCP server: Brex

> **In plain words.** Brex is a financial platform for companies: corporate cards, expense management, paying vendor bills, business travel, bank accounts. Its MCP server lets an AI assistant view expenses, cards, limits, accounts and transactions, and also make small edits: add a description (memo) to an expense, attach a receipt, specify attendees. **There are no payments or card management via MCP.**
>
> **Analysis date:** 15.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [developer.brex.com/docs/mcp](https://developer.brex.com/docs/mcp) (link from the CSV).
- `[prm]` = https://api.brex.com/.well-known/oauth-protected-resource/mcp.
- `[pricing]` = [brex.com/pricing](https://www.brex.com/pricing).

> ⚠️ **The code is closed.** The tool list with exact names and required rights is taken from the official documentation [docs]. Verbatim descriptions (`tools/list`) are not published.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Brex MCP Server | [prm] |
| Code / license | Closed | — |
| Endpoint | `https://api.brex.com/mcp` (HTTP) | [docs] |
| Status | **Beta**: the tools "may change" | [docs] |
| MCP version / language / SDK | Not published | — |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | No separate price. Required: (1) the account or card admin accepts the Developer API agreement; (2) the beta "Brex in AI assistants" is enabled; after that every user can connect | [docs] |
| Linked software | Essentials **$0**/user/month; Premium **$12**; Enterprise and Smart Card — on request | [pricing] |
| Restrictions | Access = the user's **capabilities** in Brex; some tools require separate rights (viewing expenses, bills, accounting etc.); `brex-analytics` — admins only | [docs] |
| Controlled by | Brex administrator (agreement, beta, roles), Brex | [docs] |
| Rate limits | Not documented | [docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **44** tools (+1 deprecated, see E), mostly reading. Writing: expense memos (in bulk), receipts by URL, expense attendees, assigning expenses to a limit, feedback | Not published | **Card number, CVV and expiry date are not returned**; only metadata (name, status, limits). Exports — asynchronously: `start_expense_download` → `get_expense_download_result` (URL) |
| **Authorization** | ✅ | (1) **OAuth (recommended)**: authorization server `https://accounts-api.brex.com/oauth2/default` (in [prm] also `https://api.brex.com`); **Metadata Doc** — yes; **DCR (RFC 7591)** — yes; sessions can be viewed and revoked (Settings → Personal settings → Connected integrations). (2) **API token** (for admins) as Bearer — "restricted tokens" are recommended. **Scopes** in [prm]: `openid`, `offline_access`, `email`, `users.readonly`, `departments.readonly`, `locations.readonly`, `titles.readonly`, `legal_entities.readonly`, `cards.readonly`, **`cards`**, `companies.readonly`, `budgets.readonly`, `travel.trips.readonly`, `expenses.card.readonly`, `expenses.card`, **`expenses.bill`**, `accounts.cash.readonly`, `vendors.readonly`, `accounting.integration.read`, `accounting.record.read`, `fields.read`, `field_values.read` | [docs], [prm] | — |
| Tasks-like | ✅ (own) | Asynchronous expense export with two tools (not MCP Tasks) | [docs] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic beyond passing commands through

1. **Rights by capabilities:** every tool requires its own right; for a user without the right the tool does not work [docs].
2. **Hiding of sensitive card data** (PAN, CVV, expiry) at the server level [docs].
3. **Exclusion of money operations:** "approvals and card management are not yet available via MCP" [docs]. ⚠️ At the same time the scopes include the writing `cards` and `expenses.bill` — possibly groundwork for the future.
4. **Deprecation of tools:** `query_expense_analytics` is marked deprecated in favour of `brex-analytics` [docs].
5. Server-side confirmation is **not declared**; it is recommended to configure it in the client [docs].

**Structure:** standard; the tool `brex-analytics` is an analytical "super-tool" for admins (free-form questions about expenses, banking, accounting).

## E. Overall evaluation

**Number of actions:** **44** active + 1 deprecated (`query_expense_analytics`) (according to [docs]).

| Right | Tools |
|---|---|
| All users (22) | `get_user_myself`, `get_user_by_id`, `list_users_by_name_or_email`, `list_users`, `list_cost_centers`, `list_departments`, `list_locations`, `list_legal_entities`, `list_titles`, `list_roles`, **`update_expense_memo`** (W), **`upload_card_expense_receipt_from_urls`** (W), **`replace_attendees_for_card_expense`** (W), **`assign_limit_for_card_expenses`** (W), `get_reimbursement_payout_date`, `get_expense_download_result`, `list_merchants`, `list_merchant_categories`, `list_expense_categories`, `list_cards`, `list_my_limits`, **`submit_feedback`** (W) |
| View expenses | `list_expenses`, `get_expense_by_id`, `start_expense_download` |
| Rewards | `get_reward_points` |
| Cards and limits | `get_card_by_id` |
| Policy | `get_expense_policy` |
| Accounts and balances | `list_business_accounts`, `get_business_account`, `list_banking_transactions`, `get_banking_transaction` |
| Vendor bills | `list_bills`, `get_bill_by_id`, `get_vendor_by_id`; all vendors: `list_vendors` |
| Accounting | `get_active_integration`, `list_accounting_records`, `list_gl_accounts` |
| Travel | `list_trips`, `list_bookings`, `list_group_events` |
| Admins only | `brex-analytics` (`query_expense_analytics` — deprecated) |

**Parameters:** not published. **Tokens:** cannot be determined.

**What the agent CANNOT do:** approve expenses; issue or block cards and change limits; pay bills and make transfers; see card details [docs].

## F. Documentation analysis

- **Recommendations not checked by the server:** configure **confirmation before actions** in the assistant; prefer OAuth; use restricted tokens; keep tokens in environment variables; **review the API logs** in the dashboard [docs].
- **Governance promises:** PAN/CVV/expiry are not disclosed; rights = the user's capabilities [docs]. Nothing about data storage or use by the AI provider.
- **Comparison with the logic:** the promise "card management not available" does not match the scope `cards` (write) — either the scope is requested in advance or the documentation is behind.

## Observations

- **A financial server "with spare rights":** the scopes are broader than the documented tools.
- **Hiding of sensitive fields** — like GoCardless's masking.
- **A separate analytical "agent tool"** for admins (`brex-analytics`) — free-form questions instead of fixed queries.
- **Two access mechanisms** (OAuth and API token) with different recommendations.
