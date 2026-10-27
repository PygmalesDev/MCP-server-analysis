# MCP server: Tripadvisor

> **In plain words.** Tripadvisor is a travel review website (hotels, restaurants, attractions). Its MCP server gives an AI assistant data about **hotels**: search in an area, details, photos, reviews and ratings, availability and prices, places nearby. The server only reads.
>
> **Analysis date:** 14.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[claude]` = [claude.com/connectors/tripadvisor](https://claude.com/connectors/tripadvisor) (official connector card).
- `[dir]` = [mcpservers.org — Tripadvisor](https://mcpservers.org/remote-mcp-servers/tripadvisor) (third-party catalogue).

> ⚠️ **Very little official information.** The CSV contains no documentation link. The code is closed. The endpoint `https://mcp.tripadvisor.ai/mcp` returns HTTP 403 (CSV), and its pages and OAuth metadata are not available for automated reading. The catalogue [dir] gives **a different address** — `https://production.ai-mcp-extensibility-prd.tamg.cloud/.../mcp` (tamg = TripAdvisor Media Group); this is probably the real hosting behind `mcp.tripadvisor.ai`. GitHub has **unofficial** "tripadvisor-mcp" servers (pab1it0, hhw67865) — not part of the analysis.

## A. General

| Field | Value | Source |
|---|---|---|
| Name | Tripadvisor (Claude connector, "Made by Tripadvisor") | [claude] |
| Code / license | Closed | — |
| Documentation | No official documentation; the "Documentation" link in [claude] leads to tripadvisor.com | [claude] |
| Endpoint | `https://mcp.tripadvisor.ai/mcp` (CSV); in [dir] — `https://production.ai-mcp-extensibility-prd.tamg.cloud/ogMvjY4De1G7CiHanMOAgddl/mcp` | CSV, [dir] |
| MCP version / language / SDK | Not published | — |
| Support | TripadvisorDataSupport@tripadvisor.com | [claude] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access | No price given; the connector is available in Claude (web, desktop, mobile, Code, API) | [claude] |
| Linked software | Tripadvisor — free for travellers | — |
| Restrictions | 403 response when checked without sign-in (CSV) — the authorization method is not documented | CSV |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | Read only ("Read (listed as read-only)", "Interactive"). Functions: search for hotels in an area; details, photos, reviews, ratings, availability, prices, places nearby. The tools work with location/hotel IDs; follow-up requests use these IDs | Not published | Not documented |
| Authorization | ❓ | Not documented; OAuth metadata not available | — | — |
| **Interactive (MCP Apps?)** | ✅ (according to the card) | The label "Interactive" in [claude] — probably an interactive interface in the client window | [claude] | — |
| Elicitation-like | ✅ (according to the description) | For an ambiguous place name ("Springfield") the connector **asks for clarification** before searching. The mechanism (MCP Elicitation or response text) is not stated | [claude] | — |
| Others | ❓ | — | — | — |

## D. Server logic

- Clarification of ambiguous places before searching [claude].
- Read only, no booking.
- Everything else is not documented.

**Structure:** standard (according to the available information); hosted on a separate platform ("ai-mcp-extensibility").

## E. Overall evaluation

- **Number of actions:** not published exactly; according to the description — **4 functions**: hotel search, hotel details (photos, reviews, ratings), prices and availability, places nearby [claude], [dir].
- **Parameters:** not published.
- **Tokens:** cannot be determined.
- **What the agent CANNOT do:** book; work with restaurants and attractions (hotels only); write reviews; manage "Trips".

## F. Documentation analysis

- There is practically no documentation. The privacy policy in the card is the **2019 version** [claude].
- **Promises:** "Find your perfect hotel based on Tripadvisor reviews", "ground accommodation planning in real-time data and other travelers' opinions" [claude].

## Observations

- **Minimal transparency:** an official server without documentation; the address from the CSV is a facade over hosting on another domain.
- **A server in the vendor's interest:** the results rely on Tripadvisor ratings and reviews; how hotels are ranked (including possible paid placements) is not described.
