# MCP server: Motion (motion.dev)

> **In plain words.** Motion (formerly Framer Motion) is a popular library for animations in web interfaces (React, JavaScript, Vue). This is **not** the Motion calendar (usemotion.com). Its free MCP server gives a code-writing AI assistant one "button": **search in the Motion documentation**. The paid version (Motion+) adds an animation performance audit, example source code and a transition editor.
>
> **Analysis date:** 14.10.2026; re-analysed on 23.10.2026, when a new commit appeared in the repository. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [motion.dev/docs/ai-kit](https://motion.dev/docs/ai-kit) (link from the CSV).
- `[srv]` = the server page [mcp.motion.dev/mcp](https://mcp.motion.dev/mcp) (answers a GET with a description of the server).
- `[kit]` = [motiondivision/ai-kit](https://github.com/motiondivision/ai-kit/tree/0ebeb5313a069986376430f665415252e223d1d4), commit `0ebeb53`, 2026-10-23 (skills, plugin, installer).
- `[plus]` = [motion.dev/plus](https://motion.dev/plus).

> ⚠️ **The MCP server code is closed.** Only the repository [kit] is open: skills, a Cursor plugin, the installer `npx motion-ai` (MIT license according to [srv]). The description of the only free tool is not published verbatim. The CSV records HTTP 200 without sign-in: the server is open to everyone, but direct requests to it from our environment are blocked by the network policy.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Motion MCP ("Motion's free MCP server") | [srv] |
| Code | Server closed; skills/installer — [kit], MIT | [srv], [kit] |
| Endpoints | **Free:** `https://mcp.motion.dev` (in the CSV — `/mcp`). **Paid:** `https://mcp.motion.dev/plus` | [kit] `plugins/motion/mcp.json` |
| **MCP version** | **2025-06-18** (stated by the server itself) | [srv] |
| Transport | Streamable HTTP, POST JSON-RPC 2.0 | [srv] |
| Language / SDK | Not published | — |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Free server | "Documentation search is free. No token, account or configuration is required." | [docs] |
| Motion+ | **One-time purchase** ("Pay once for each developer", "Yours forever"; the amount did not load on the page). Gives: search in examples, CSS spring generation, the MotionScore audit, a transition editor. Separately — an annual Pro add-on (AI agent Ultramotion) | [plus], [docs] |
| Linked software | The Motion library is open source (MIT) | [motion.dev](https://motion.dev) |
| Restrictions | The performance audit only profiles a "running local site" | [docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | Free server: **1** tool `search-motion-docs` [srv]. "Examples", "compatibility" etc. also go through it: "there is no separate tool" [kit] SKILL.md. Paid server: MotionScore audit, source code of 450–510+ examples and Motion UI, spring generation, saved transitions (tool names not published) | Not published verbatim | Not documented. The audit methodology is "served live to your agent from the Motion+ MCP server" [kit] README |
| **Authorization** | ✅ (Plus only) | Free — no authorization. Plus — sign-in from the editor ("Sign in from your editor"; "Ask Cursor to sign you in and it hands you a link. Nothing gets pasted into chat") | [docs], [kit] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic beyond passing commands through

1. **Monetisation via tool responses:** "the rest is tiered, and the tools say so when you reach them" [kit] SKILL.md. The free tool **tells the agent about paid features** when it reaches them.
2. **Two servers by access level:** free and paid are different endpoints.
3. **The performance evaluation methodology is defined by the server** and changes on its side ("every audit follows the current MotionScore scoring engine"): the agent receives the rules at the time of the call [kit] README.
4. The agent's behaviour rules (best practices, "If the Motion MCP server is unavailable…") are in skills [kit].

**Structure:** non-standard — two servers (free/plus) plus skills and a reviewer agent (`plugins/motion/agents/motion-reviewer.md`) in a separate repository.

## E. Overall evaluation

- **Number of actions (free server):** 1 — `search-motion-docs` [srv]. Paid — not published (at least 4 groups: audit, example source code, springs, transition editor) [docs].
- **Parameters:** not published.
- **Tokens:** cannot be determined; with a single tool the context is minimal.
- **What the agent CANNOT do:** without Motion+ — generate springs, run an audit, get the source code of examples and Motion UI; the agent cannot buy a license [docs], [plus].

## F. Documentation analysis

- **Recommendations not checked:** none.
- **Governance/data:** the documentation does not describe data processing or telemetry [docs]. The Motion+ audit analyses **the source code of the user's project** — what is sent to the server is not described.
- **Promises:** "Hand-written advice by the creator of Motion"; "Nothing gets pasted into chat" (about sign-in) [kit].

## Observations

- **Freemium inside MCP:** the free server itself tells the agent about paid features — a sales channel through the agent.
- **A minimal server** (1 tool), the main logic is in skills on the client side.
- **A methodology loaded from the server** can change without updating the client.
