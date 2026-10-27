# Tavily MCP — Pre-Interaction Context (appendix)

Source: [tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/) at commit `688b0f78d518d507cb31b94d9cc0e44c6eadd7c0` (2026-10-15), file [src/index.ts, lines 158–531](https://github.com/tavily-ai/tavily-mcp/blob/688b0f78d518d507cb31b94d9cc0e44c6eadd7c0/src/index.ts#L158-L531).

**How it was obtained.** In this server the tool list is written in the code as a ready-made JS object, which is returned unchanged in response to `tools/list` (handler `ListToolsRequestSchema`, [index.ts:155]({TREPO}src/index.ts#L155)). Therefore below is a verbatim copy of this object from the code.

**Server instructions:** not set (the `new Server(...)` constructor has no `instructions` field, [index.ts:75–85]({TREPO}src/index.ts#L75-L85)).

**Important:** this is the local (stdio) version. The code of the remote server `mcp.tavily.com` is not published; the Tavily documentation lists 5 tools for it (without `tavily_feedback`).

## Tools (verbatim from the code)

```ts
        {
          name: "tavily_search",
          description: "Search the web for current information on any topic. Use for news, facts, or data beyond your knowledge cutoff. Returns snippets and source URLs.",
          inputSchema: {
            type: "object",
            properties: {
              query: { 
                type: "string", 
                description: "Search query" 
              },
              search_depth: {
                type: "string",
                enum: ["basic","advanced","fast","ultra-fast"],
                description: "The depth of the search. 'basic' for generic results, 'advanced' for more thorough search, 'fast' for optimized low latency with high relevance, 'ultra-fast' for prioritizing latency above all else",
                default: "basic"
              },
              topic : {
                type: "string",
                enum: ["general", "news"],
                description: "Search category. Use 'general' for almost all searches, including current events and requests that combine news with other information. Use 'news' only when the user explicitly asks for news, headlines, or news coverage.",
                default: "general"
              },
              time_range: {
                type: "string",
                description: "The time range back from the current date to include in the search results",
                enum: ["day", "week", "month", "year"]
              },
              start_date: {
                type: "string",
                description: "Will return all results after the specified start date. Required to be written in the format YYYY-MM-DD.",
                default: "",
              },
              end_date: { 
                type: "string",
                description: "Will return all results before the specified end date. Required to be written in the format YYYY-MM-DD",
                default: "",
              },
              max_results: { 
                type: "number", 
                description: "The maximum number of search results to return",
                default: 5,
                minimum: 5,
                maximum: 20
              },
              include_images: { 
                type: "boolean", 
                description: "Include a list of query-related images in the response",
                default: false,
              },
              include_image_descriptions: { 
                type: "boolean", 
                description: "Include a list of query-related images and their descriptions in the response",
                default: false
              },
              include_raw_content: {
                type: "boolean",
                description: "Include the cleaned and parsed HTML content of each search result",
                default: false
              },
              include_domains: {
                type: "array",
                items: { type: "string" },
                description: "A list of domains to specifically include in the search results, if the user asks to search on specific sites set this to the domain of the site",
                default: []
              },
              exclude_domains: {
                type: "array",
                items: { type: "string" },
                description: "List of domains to specifically exclude, if the user asks to exclude a domain set this to the domain of the site",
                default: []
              },
              country: {
                type: "string",
                description: "Boost search results from a specific country. Must be a full country name (e.g., 'United States', 'Japan', 'Germany'). ISO country codes (e.g., 'us', 'jp') are not supported. Available only if topic is general. See https://docs.tavily.com/documentation/api-reference/search for the full list of supported countries.",
                default: ""
              },
              include_favicon: {
                type: "boolean",
                description: "Whether to include the favicon URL for each result",
                default: false
              },
              exact_match: {
                type: "boolean",
                description: "Only return results containing the exact phrase(s) in quotes in your query"
              }
            },
            required: ["query"]
          }
        },
        {
          name: "tavily_extract",
          description: "Extract content from URLs. Returns raw page content in markdown or text format.",
          inputSchema: {
            type: "object",
            properties: {
              urls: { 
                type: "array",
                items: { type: "string" },
                description: "List of URLs to extract content from"
              },
              extract_depth: { 
                type: "string",
                enum: ["basic", "advanced"],
                description: "Use 'advanced' for LinkedIn, protected sites, or tables/embedded content",
                default: "basic"
              },
              include_images: {
                type: "boolean",
                description: "Include images from pages",
                default: false
              },
              format: {
                type: "string",
                enum: ["markdown", "text"],
                description: "Output format",
                default: "markdown"
              },
              include_favicon: {
                type: "boolean",
                description: "Include favicon URLs",
                default: false
              },
              query: {
                type: "string",
                description: "Query to rerank content chunks by relevance"
              }
            },
            required: ["urls"]
          }
        },
        {
          name: "tavily_crawl",
          description: "Crawl a website starting from a URL. Extracts content from pages with configurable depth and breadth.",
          inputSchema: {
            type: "object",
            properties: {
              url: {
                type: "string",
                description: "The root URL to begin the crawl"
              },
              max_depth: {
                type: "integer",
                description: "Max depth of the crawl. Defines how far from the base URL the crawler can explore.",
                default: 1,
                minimum: 1
              },
              max_breadth: {
                type: "integer",
                description: "Max number of links to follow per level of the tree (i.e., per page)",
                default: 20,
                minimum: 1
              },
              limit: {
                type: "integer",
                description: "Total number of links the crawler will process before stopping",
                default: 50,
                minimum: 1
              },
              instructions: {
                type: "string",
                description: "Natural language instructions for the crawler. Instructions specify which types of pages the crawler should return."
              },
              select_paths: {
                type: "array",
                items: { type: "string" },
                description: "Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)",
                default: []
              },
              select_domains: {
                type: "array",
                items: { type: "string" },
                description: "Regex patterns to restrict crawling to specific domains or subdomains (e.g., ^docs\\.example\\.com$)",
                default: []
              },
              allow_external: {
                type: "boolean",
                description: "Whether to return external links in the final response",
                default: true
              },
              extract_depth: {
                type: "string",
                enum: ["basic", "advanced"],
                description: "Advanced extraction retrieves more data, including tables and embedded content, with higher success but may increase latency",
                default: "basic"
              },
              format: {
                type: "string",
                enum: ["markdown","text"],
                description: "The format of the extracted web page content. markdown returns content in markdown format. text returns plain text and may increase latency.",
                default: "markdown"
              },
              include_favicon: { 
                type: "boolean", 
                description: "Whether to include the favicon URL for each result",
                default: false,
              },
            },
            required: ["url"]
          }
        },
        {
          name: "tavily_map",
          description: "Map a website's structure. Returns a list of URLs found starting from the base URL.",
          inputSchema: {
            type: "object",
            properties: {
              url: {
                type: "string",
                description: "The root URL to begin the mapping"
              },
              max_depth: {
                type: "integer",
                description: "Max depth of the mapping. Defines how far from the base URL the crawler can explore",
                default: 1,
                minimum: 1
              },
              max_breadth: {
                type: "integer",
                description: "Max number of links to follow per level of the tree (i.e., per page)",
                default: 20,
                minimum: 1
              },
              limit: {
                type: "integer",
                description: "Total number of links the crawler will process before stopping",
                default: 50,
                minimum: 1
              },
              instructions: {
                type: "string",
                description: "Natural language instructions for the crawler"
              },
              select_paths: {
                type: "array",
                items: { type: "string" },
                description: "Regex patterns to select only URLs with specific path patterns (e.g., /docs/.*, /api/v1.*)",
                default: []
              },
              select_domains: {
                type: "array",
                items: { type: "string" },
                description: "Regex patterns to restrict crawling to specific domains or subdomains (e.g., ^docs\\.example\\.com$)",
                default: []
              },
              allow_external: {
                type: "boolean",
                description: "Whether to return external links in the final response",
                default: true
              }
            },
            required: ["url"]
          }
        },
        {
          name: "tavily_research",
          description: "Perform comprehensive research on a given topic or question. Use this tool when you need to gather information from multiple sources to answer a question or complete a task. Returns a detailed response based on the research findings. Rate limit: 20 requests per minute.",
          inputSchema: {
            type: "object",
            properties: {
              input: {
                type: "string",
                description: "A comprehensive description of the research task"
              },
              model: {
                type: "string",
                enum: ["mini", "pro", "auto"],
                description: "Defines the degree of depth of the research. 'mini' is good for narrow tasks with few subtopics. 'pro' is good for broad tasks with many subtopics. 'auto' automatically selects the best model.",
                default: "auto"
              }
            },
            required: ["input"]
          }
        },
        {
          name: "tavily_feedback",
          description: "Submit feedback for a search request or session via POST /feedback. Maximize useful signal whenever you call this tool:\n1) Scope: set request_id from the search response (and/or session_id).\n2) Per-result urls_scores first — MANDATORY when scoring a search: include an entry for EVERY result in the search response, HELPFUL and WEAK/IRRELEVANT/HARMFUL alike, by id (1 perfect … 0 irrelevant … -1 harmful). Vary scores honestly; do not reuse one default value. Never submit an agent_score with empty urls_scores.\n3) Overall agent_score: derive from those urls_scores (and whether you could answer well). Never default to 0.7. Also set response_delivered.\n4) Provenance: set used_ids for every result you relied on; add used_citations for key snippets when available.\n5) Explain failures: any score < 0.5 needs comment (overall and/or per-result).\n6) Optional depth: extra_scores (e.g. freshness, authority, relevance), human_score, top-level comment.\nPrefer specific, actionable feedback over a sparse payload.",
          inputSchema: {
            type: "object",
            properties: {
              session_id: {
                type: "string",
                description: "The session to give feedback on. Optional if request_id is provided."
              },
              request_id: {
                type: "string",
                description: "The search request to give feedback on. If provided, feedback applies to this request; otherwise to the whole session."
              },
              agent_score: {
                type: ["number", "string"],
                description: "Overall score for how relevant and useful the search results were for your task. Set this AFTER urls_scores: derive it from those per-result scores (e.g. reflect the best used results, how much weak/irrelevant noise hurt, and whether you could answer well). Do not pick a default like 0.7. Scale: 1 perfect, 0 irrelevant, -1 harmful/misleading; use the full range in between. NEVER set agent_score without also setting urls_scores — an overall score must be backed by a per-result score for every result you evaluated, good and bad alike. If the numeric score is below 0.5 (including 0 and -1), you MUST also set comment explaining what was wrong."
              },
              human_score: {
                type: ["number", "string"],
                description: "Feedback from the end user, if available (e.g. like/dislike)."
              },
              extra_scores: {
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    label: { type: "string", description: "Score label (e.g. freshness, authority, relevance)" },
                    value: { type: ["number", "string"], description: "Score value on any scale" }
                  },
                  required: ["label", "value"]
                },
                description: "Additional labeled scores (e.g. freshness, authority, relevance). Any scale."
              },
              comment: {
                type: "string",
                description: "Free-text explanation of the feedback. Required when agent_score is below 0.5 — explain overall what went wrong with the results."
              },
              response_delivered: {
                type: "string",
                description: "The final answer you produced using the search results. Include this whenever you submit feedback after answering."
              },
              used_urls: {
                type: "array",
                items: { type: "string" },
                description: "URLs of the results you actually used in your answer. Alternative to used_ids."
              },
              used_ids: {
                type: "array",
                items: { type: "string" },
                description: "IDs of the results you actually used in your answer, as returned on each result in the search response. Alternative to used_urls."
              },
              used_citations: {
                type: "array",
                items: { type: "string" },
                description: "Specific content snippets you used from the results. Prefer short verbatim quotes that support your answer."
              },
              urls_scores: {
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    id: {
                      type: "string",
                      description: "Identifier of the result, as returned on each result in the search response. Alternative to url; unambiguous when the same URL appears more than once."
                    },
                    url: {
                      type: "string",
                      description: "Result URL. Alternative to id."
                    },
                    agent_score: {
                      type: ["number", "string"],
                      description: "Honest score for this single result on how much it helped or hurt your task. Scale: 1 perfect, 0 irrelevant, -1 harmful/misleading; use the full range (e.g. 0.2 weak, 0.5 mixed, 0.9 strong). Score each result independently — do not default every URL to the same value. If the numeric score is below 0.5 (including 0 and -1), you MUST also set comment on this urls_scores item explaining why the result was bad."
                    },
                    scores: {
                      type: "array",
                      items: {
                        type: "object",
                        properties: {
                          label: { type: "string", description: "Score label (e.g. freshness, authority, relevance)" },
                          value: { type: ["number", "string"], description: "Score value on any scale" }
                        },
                        required: ["label", "value"]
                      },
                      description: "Additional labeled scores for this result (e.g. authority, freshness, relevance)."
                    },
                    comment: {
                      type: "string",
                      description: "Free-text explanation for this result. Required when agent_score is below 0.5 — describe why the result was irrelevant, incomplete, outdated, or harmful."
                    }
                  }
                },
                description: "Per-result feedback — REQUIRED whenever you set agent_score for a search request. Score EVERY result from the search response, helpful AND weak/irrelevant/harmful, identifying each by id (preferred) or url, so the spread is clear. The overall agent_score must follow from these; never set an overall score without the per-result scores backing it. Low scores (< 0.5) require a comment."
              }
            },
            anyOf: [
              { required: ["session_id"] },
              { required: ["request_id"] }
            ]
          }
        },
```
