# TASK
You are collecting source URLs for a later, separate analysis of one MCP (Model Context Protocol) server. Do NOT analyse the server. Only search the web and return URLs. Speed matters: about 10 searches are usually enough.

# INPUT
- name: {{name}}
- vendor domain: {{vendor_domain}}
- MCP endpoint: {{endpoint}}
- documentation URL: {{docs}}
- search terms: {{search_terms}}

# WHAT TO FIND (only official vendor sources, except where noted)
1. official_docs: the vendor's MCP server documentation pages — overview, setup/installation, authentication/permissions, configuration (URL parameters, headers, toolsets, read-only modes), tool reference, security/privacy pages about the MCP server, changelog/blog announcements of the MCP server. Include SUB-PAGES, not only the landing page.
2. hosted_server_pages: pages on the endpoint's own host that list tools or install instructions (e.g. `<endpoint>/install`, other paths on the same host mentioned in the docs and their `/install` pages).
3. github_repos: the vendor's OFFICIAL GitHub repositories of this MCP server (local/stdio version, SDK of the server, agent skills or plugins for it) — only repositories in the vendor's own GitHub organisation or explicitly linked from the vendor's own docs. Repository root URLs only, e.g. `https://github.com/<org>/<repo>`. Repositories of private persons or other companies go to `unofficial_servers`, never here.
4. package_pages: official npm/PyPI/MCP-registry pages of the server package.
5. pricing: the vendor's official pricing page(s) of the product and any MCP-specific pricing/limits page.
6. legal: privacy policy, terms, AI terms, MCP terms, data processing pages relevant to the product.
7. tool_catalogues: THIRD-PARTY catalogue pages that list this server's tools (e.g. composio.dev/toolkits/…, agentdiscoverability.com, getprecision.ai, scalekit, glama.ai, mcpservers.org, martechdb.com, pulsemcp, smithery). Include them even if an official list exists.
8. other_official_endpoints: other official MCP endpoints of the same vendor (regional, sandbox, docs-only, per-client paths).
9. unofficial_servers: community/unofficial MCP servers or wrappers for this product (for reference only).

# OUTPUT
Return ONE JSON object and nothing else (no markdown fences, no commentary). Only real URLs you actually saw in search results or pages; never guess URLs. Empty lists are allowed.
{
  "server": "{{name}}",
  "official_docs": ["<url>"],
  "hosted_server_pages": ["<url>"],
  "github_repos": ["https://github.com/<org>/<repo>"],
  "package_pages": ["<url>"],
  "pricing": ["<url>"],
  "legal": ["<url>"],
  "tool_catalogues": ["<url>"],
  "other_official_endpoints": ["<url>"],
  "unofficial_servers": ["<url>"],
  "notes": "<max 50 words: anything the analyst should know, e.g. name collisions with other products>"
}
