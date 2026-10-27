# MCP server: Calendly

> **In plain words.** Calendly is a meeting scheduling service: a person picks a free time slot via a link and the meeting appears in the calendar. Its MCP server lets an AI assistant view meeting types and free slots, **book and cancel meetings**, change availability schedules, create single-use links and invite people to the organisation.
>
> **Analysis date:** 15.10.2026. **Analyst:** Manual analysis using Claude Opus 5.5 for verification and code analysis.

**Sources:**
- `[docs]` = [developer.calendly.com/calendly-mcp-server](https://developer.calendly.com/calendly-mcp-server) (link from the CSV).
- `[tools]` = [Supported tools](https://developer.calendly.com/docs/mcp/supported-tools).
- `[pricing]` = [calendly.com/pricing](https://calendly.com/pricing).

> ⚠️ **The code is closed.** The exact tool names are taken from the official documentation [tools]; the descriptions there are paraphrased. Verbatim descriptions and `tools/list` schemas are not published.

## A. General

| Field | Value | Source |
|---|---|---|
| Code / license | Closed; "Self-hosting or local deployment is not supported" | [docs] |
| Endpoint | `https://mcp.calendly.com` (CSV: `https://mcp.calendly.com/`) | [docs] |
| MCP version / language / SDK | Not published | — |
| Annotations | Present: title, readOnlyHint, destructiveHint, idempotentHint | [docs] |

## B. Access and pricing

| Field | Value | Source |
|---|---|---|
| Access to MCP | No price given | [docs] |
| Linked software | Free; Standard **$10**; Teams **$16** per seat/month; Enterprise from **$15,000/year** (50+ seats) | [pricing] |
| Plan restrictions on tools | `meetings-create_invitee` (booking) — "paid plan required"; routing forms — Teams and above | [tools] |
| Other restrictions | OAuth via DCR only (personal tokens and pre-registered apps are not accepted); limits not given, DCR is "heavily validated and rate-limited" | [docs] |

## C. Capabilities

| Capability | Present? | Details | Pre-Interaction Context | Post-Interaction Context |
|---|---|---|---|---|
| **Tools** | ✅ | **36** tools (see E): 34 correspond to the REST API v2, 2 "skills" tools | Not published verbatim; annotations present | Not documented |
| **"Skills" via tools** | ✅ | `list_calendly_skills`, `load_calendly_skill` — **the server itself delivers skill instructions to the agent** ("No REST equivalent") | [tools] | Skill text |
| **Authorization** | ✅ | **OAuth 2.1** Authorization Code + **PKCE S256**. **Metadata Doc** — yes (`https://mcp.calendly.com/.well-known/oauth-protected-resource`, `https://calendly.com/.well-known/oauth-authorization-server`). **DCR** — yes (`https://calendly.com/oauth/register`), `token_endpoint_auth_method: none`, **Preregistration is not supported**. Scopes: `mcp:scheduling:read`, `mcp:scheduling:write` (assigned by the server, the client cannot request them). Redirect URIs — exact HTTPS only. **Authorization server** — calendly.com. Consent: a "Connect to Calendly" button | [docs] | — |
| Others | ❓ | Not documented | — | — |

## D. Server logic beyond passing commands through

1. **Separate read and write scopes** (`read`/`write`); the scopes are assigned by the server [docs].
2. **Strict client policy:** DCR only, no secrets, exact redirect URIs [docs].
3. **Server-side skills** — the server controls the agent's behaviour with its own instructions that are loaded on demand [tools].
4. **Plan restrictions at the tool level** (booking, routing forms) [tools].
5. Confirmation of individual actions — **none**; the only consent is at sign-in [docs].

## E. Overall evaluation

**Number of actions:** **36** [tools]. The HTTP method indicates the type: GET — read (23), POST/PATCH/PUT/DELETE — change (11), skills (2).

| Group | Tools |
|---|---|
| Event types | `event_types-create_event_type` (POST), `event_types-update_event_type` (PATCH), `event_types-list_event_types`, `event_types-get_event_type`, `event_types-list_event_type_available_times`, `event_types-list_event_type_availability_schedule`, `event_types-update_event_type_availability_schedule` (PUT) |
| Locations | `locations-list_user_meeting_locations` |
| Meetings | `meetings-list_events`, `meetings-get_event`, **`meetings-cancel_event`** (POST), **`meetings-create_invitee`** (POST, booking, paid plan), `meetings-list_event_invitees`, `meetings-get_event_invitee`, `meetings-create_invitee_no_show` (POST), `meetings-get_invitee_no_show`, `meetings-delete_invitee_no_show` (DELETE) |
| Links | `scheduling_links-create_single_use_scheduling_link` (POST), `shares-create_share` (POST) |
| Availability | `availability-list_user_availability_schedules`, `availability-get_user_availability_schedule`, `availability-list_user_busy_times` |
| Routing forms (Teams+) | `routing_forms-list_routing_forms`, `routing_forms-get_routing_form`, `routing_forms-list_routing_form_submissions`, `routing_forms-get_routing_form_submission` |
| Users and organisation | `users-get_current_user`, `users-get_user`, `organizations-get_organization`, `organizations-list_organization_memberships`, `organizations-get_organization_membership`, `organizations-list_organization_invitations`, **`organizations-create_organization_invitation`** (POST), **`organizations-revoke_organization_invitation`** (DELETE) |
| Skills | `list_calendly_skills`, `load_calendly_skill` |

**Parameters:** not published. **Tokens:** cannot be determined.

**What the agent CANNOT do:** delete event types; remove organisation members (only invitations); work with webhooks, calendar integrations, payments, workflows; the Data Deletion API (Enterprise) [tools], [pricing].

## F. Documentation analysis

- **Recommendations not checked:** there are no recommendations on confirming actions [docs].
- **Governance:** nothing about data, only a link to the privacy notice [docs]. The agent sees the data of **invitees** (third parties) and routing form answers.
- **Promises:** works with any client that supports DCR [docs].

## Observations

- **Server-side skills** (`load_calendly_skill`) are a new design option: the vendor delivers instructions to the agent via MCP rather than via external files (compare Lucid and Airwallex, where the skills are outside the server).
- **Actions with consequences for third parties** (booking, cancelling meetings, invitations to the organisation) without server-side confirmation.
- **Strict and standard authorization** (DCR only, PKCE, no secrets).
