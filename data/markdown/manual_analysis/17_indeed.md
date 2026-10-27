# MCP server: Indeed

> **In plain words.** Indeed is the largest job search website. Its MCP server helps a **job seeker**: the AI assistant searches for jobs, shows job details, reads **the user's resume** from the Indeed profile (to find suitable matches) and tells about employer companies (reviews, salaries, culture). Applying for jobs through the server is not possible.
>
> **Analysis date:** 16.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [docs.indeed.com/mcp](https://docs.indeed.com/mcp/) (link from the CSV).
- `[prm]` = https://mcp.indeed.com/.well-known/oauth-protected-resource/claude/mcp.

> ⚠️ **The code is closed.** The tool names in [docs] are "human-readable" (Job Search, Job Detail etc.). The exact names and descriptions in `tools/list` are not published.

## A. General

| Field | Value | Source |
|---|---|---|
| Code / license | Closed | — |
| Endpoint | `https://mcp.indeed.com/claude/mcp` — **a separate path for Claude** | CSV, [prm] |
| Status | **Beta** | [docs] |
| MCP version / language / SDK | Not published | — |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access | Free for the job seeker (no prices given); an Indeed account is required | [docs] |
| Clients | **Claude Connector only** (Claude.ai, Claude Desktop), although the protocol is standard | [docs] |
| Countries | Not specified | [docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **4**: Job Search (title, keywords, location, employment type → titles, companies, locations, **salaries, application links**); Job Detail (by job ID); **Get Resume** (experience from the user's profile); Get Company Data (satisfaction, compensation, culture, management, reviews) | Not published | Not documented |
| **Authorization** | ✅ | Sign-in to the Indeed account. **Metadata Doc** — yes. **Authorization server** — `https://secure.indeed.com`. **Scopes:** `job_seeker.jobs.search`, `job_seeker.company.details.read`, `job_seeker.profile.read`, `offline_access` | [prm] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic

- **The scopes mirror the tool set exactly**: read only, a separate scope for the profile (resume) [prm].
- **A separate endpoint for one AI client** (`/claude/mcp`) — the server is tied to a specific platform.
- Everything else is not documented.

## E. Overall evaluation

| # | Action | Parameters (according to [docs]) |
|---|---|---|
| 1 | Search for jobs | title/keywords, location, employment type |
| 2 | Job details | job ID |
| 3 | Get one's own resume | — |
| 4 | Company data | company |

**Tokens:** cannot be determined.

**What the agent CANNOT do:** apply for jobs (it only returns links); edit the resume; correspond with employers; save jobs, subscribe to alerts; employer functions [docs].

## F. Documentation analysis

- **Recommendations not checked:** none.
- **Governance:** Indeed's Terms of Service and Privacy Policy apply "plus any third-party terms that apply to the AI or LLM model used" [docs]. It is not stated separately that **the user's resume is passed to the AI provider**.
- **Promises:** "Real-time access to Indeed's job marketplace" [docs].

## Observations

- **A server "for one client"** (Claude only, its own URL path) — the vendor chooses which AIs to work with.
- **The user's personal data (resume)** has a separate scope `job_seeker.profile.read`; a good example of granular rights.
- **Strictly read-only and a minimal set** — the agent has no actions with consequences.
