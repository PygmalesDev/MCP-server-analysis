# TASK
You are collecting source URLs for a later, separate analysis of one MCP (Model Context Protocol) server. Do NOT analyse the server. Only search the web and return URLs. About 10–15 searches are usually enough; spend the extra searches on finding the OFFICIAL TOOL LIST (item 1 below), because it is the most important source of the later analysis.

# INPUT
- name: {{name}}
- vendor domain: {{vendor_domain}}
- MCP endpoint: {{endpoint}}
- documentation URL: {{docs}}
- search terms: {{search_terms}}

# IDENTITY RULES (read before searching)
- The object is the server at the INPUT ENDPOINT HOST. Search for the endpoint host itself (e.g. `"mcp.example.com"`) and collect the vendor page that documents exactly this host.
- **Docs-search MCP trap.** Many documentation sites (e.g. those built with Mintlify) run their OWN small MCP server that only searches the docs (tools such as `search_<site>`, `query_docs_filesystem_<site>`, `submit_feedback`; pages such as `support.<vendor>/mcp` or `docs.<vendor>/mcp` returning a JSON manifest). That is NOT the product server. Do not put such a page into `official_docs` as the server's documentation; mention it in `notes`. Likewise, the vendor may run several product MCP servers (admin vs search vs index); pick the pages of the one at the input host.
- **Official = the vendor's own domains and subdomains, and the vendor's own GitHub organisation.** Copies of the vendor's docs on other hosts (mirrors, preview deployments such as `*.vercel.app`, `*.manicule.dev`) are NOT official; if the only copy you find is a mirror, search again for the same page on the vendor's own domain (usually the same path) and list that URL instead.

# WHAT TO FIND (only official vendor sources, except where noted)
1. tool_reference_pages: the vendor's OFFICIAL page(s) that list the server's tools (names like `create_issue`, `listJams`). If the reference is split into SUB-PAGES (one page per category or per tool, e.g. `/tools/deployments`, `/tools/domains`), list EVERY sub-page URL, not only the overview. If the docs site offers plain versions (`<page>.md`, `llms.txt`, `llms-full.txt`), add those too — they are easier to read. A support article that says "see the full list of tools" points to such a page: follow the link and list it.
2. official_docs: the vendor's MCP server documentation pages — overview, setup/installation, authentication/permissions, configuration (URL parameters, headers, toolsets, read-only modes), security/privacy pages about the MCP server, changelog/blog announcements of the MCP server. Include SUB-PAGES, not only the landing page.
3. hosted_server_pages: pages on the endpoint's own host that list tools or install instructions (e.g. `<endpoint>/install`, other paths on the same host mentioned in the docs and their `/install` pages).
4. github_repos: the vendor's OFFICIAL GitHub repositories of this MCP server (local/stdio version, SDK of the server, agent skills or plugins for it) — only repositories in the vendor's own GitHub organisation or explicitly linked from the vendor's own docs. Repository root URLs only, e.g. `https://github.com/<org>/<repo>`. Repositories of private persons or other companies go to `unofficial_servers`, never here.
5. package_pages: official npm/PyPI/MCP-registry pages of the server package.
6. pricing: the vendor's official pricing page(s) of the product and any MCP-specific pricing/limits page.
7. legal: privacy policy, terms, AI terms, MCP terms, data processing pages relevant to the product.
8. tool_catalogues: THIRD-PARTY catalogue pages that list this server's tools (e.g. composio.dev/toolkits/…, agentdiscoverability.com, getprecision.ai, scalekit, glama.ai, mcpservers.org, martechdb.com, pulsemcp, smithery, claude.com/connectors/…). Include them even if an official list exists — they are used for cross-checking only.
9. other_official_endpoints: other official MCP endpoints of the same vendor (regional, sandbox, docs-only, per-client paths).
10. unofficial_servers: community/unofficial MCP servers or wrappers for this product (for reference only).

# OUTPUT
Return ONE JSON object and nothing else (no markdown fences, no commentary). Only real URLs you actually saw in search results or pages; never guess URLs. Empty lists are allowed.
{
  "server": "{{name}}",
  "tool_reference_pages": ["<url>"],
  "official_docs": ["<url>"],
  "hosted_server_pages": ["<url>"],
  "github_repos": ["https://github.com/<org>/<repo>"],
  "package_pages": ["<url>"],
  "pricing": ["<url>"],
  "legal": ["<url>"],
  "tool_catalogues": ["<url>"],
  "other_official_endpoints": ["<url>"],
  "unofficial_servers": ["<url>"],
  "notes": "<max 60 words: anything the analyst should know, e.g. name collisions, docs-search MCP of the vendor, whether an official tool list exists and where; if none was found, say so explicitly>"
}
