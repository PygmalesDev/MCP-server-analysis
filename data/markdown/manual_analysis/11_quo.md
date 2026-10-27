# MCP server: Quo

> **In plain words.** Quo (formerly OpenPhone, see ["OpenPhone is now Quo"](https://quo.com/blog/next-chapter/)) is cloud business telephony: numbers, calls, SMS, shared team "inboxes", contacts, call transcripts. Its MCP server lets an AI assistant read conversations and call history, get transcripts, manage contacts and **send SMS on behalf of the company**, including bulk sends.
>
> **Analysis date:** 14.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [support.quo.com — MCP](https://support.quo.com/core-concepts/integrations/mcp) (link from the CSV).
- `[claude]` = [claude.com/connectors/quo](https://claude.com/connectors/quo).
- `[prm]` = https://mcp.quo.com/.well-known/oauth-protected-resource; `[asm]` = https://mcp.quo.com/.well-known/oauth-authorization-server.
- `[pricing]` = [quo.com/pricing](https://www.quo.com/pricing).

> ⚠️ **The code is closed, the tool list is not published.** The documentation describes only capabilities. The description below is based on the documentation and the **public list of OAuth scopes**.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Quo (official connector for Claude, ChatGPT, Grok) | [docs] |
| Code / license | Closed | — |
| Endpoint | `https://mcp.quo.com/mcp` (OAuth resource: `https://mcp.quo.com`) | CSV, [prm] |
| MCP version / language / SDK | Not published | — |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | "ChatGPT / Claude MCP" is included **in all plans** at no extra charge. For clients: Claude — all users; ChatGPT — Plus and Pro; Grok — Grok users | [pricing], [docs] |
| **Sending SMS** | "Pre-paid credits are needed to send texts through your AI assistant" | [docs] |
| Linked software | Starter **$19/$15**, Business **$33/$23**, Scale **$47/$35** per user per month (monthly/annual). Plus automation credits (1,000 free = 10 calls of the AI agent Sona; packages $25–$199/month); automated SMS via the API — $0.01 per segment | [pricing] |
| Restrictions | Transcripts only on numbers where they are enabled | [docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | According to [docs]: conversation summaries; **sending SMS to one or several** people; message history and inboxes (filters by contact, date, topic); call history and voicemail transcripts; searching, adding, changing contacts; missed calls. The exact names are not published | Not published | Not documented |
| **Authorization** | ✅ | OAuth. **Metadata Doc** — yes; **DCR** — yes (`https://mcp.quo.com/register`); grants `authorization_code`, `refresh_token`; PKCE `S256`; client methods `client_secret_basic`, `client_secret_post`, `none`. **8 scopes:** `read:conversations`, `write:conversations`, `read:calls`, **`write:calls`**, `write:contacts`, `read:account`, `read:agents`, **`write:agents`**. **Authorization server** — `https://mcp.quo.com` | [prm], [asm] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic beyond passing commands through

1. **Pre-paid credits as a limiter** on the agent sending SMS [docs].
2. **Scopes broader than the documentation:** `write:calls` and `read:agents`/`write:agents` point to capabilities that are not in [docs]: managing calls and Quo's AI agents (e.g. Sona). ⚠️ Needs checking.
3. Confirmation before sending messages, bulk-send limits, a log — **not described**.

**Structure:** standard (according to the available information).

## E. Overall evaluation

- **Number of actions:** not published exactly; according to [docs] — **6 groups** (summaries, sending SMS, messages/inboxes, calls/transcripts, contacts, missed calls). The scopes additionally point to calls (writing) and AI agents.
- **Parameters:** not published.
- **Tokens:** cannot be determined.
- **What the agent CANNOT do:** make calls — not stated in the documentation (although there is a `write:calls` scope); manage numbers, users, billing; send SMS without credits [docs].

## F. Documentation analysis

- **Recommendations not checked:** none; nothing is said about confirming messages before sending.
- **Governance/data:** not described in [docs]; there is a link to the [privacy](https://quo.com/privacy) policy. The agent has access to **conversations with customers and call transcripts**, i.e. personal data of third parties.
- **Promises to the user:** "Surface call insights and missed opportunities" [claude].

## Observations

- **The agent communicates with external people on behalf of the company** (SMS, bulk sends) without a described confirmation step. In this set, this is one of the riskiest "real-world actions".
- **Divergence between scopes and documentation** — the OAuth metadata reveals more capabilities than described.
- **Paying for the agent's actions with credits** — an economic limiter.
