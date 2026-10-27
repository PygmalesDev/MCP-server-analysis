# Context7 MCP — Pre-Interaction Context (appendix)

Source: [upstash/context7, packages/mcp/src/index.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/index.ts) at commit `b5e81de845092694ba1bfc5af15400f319c89b6d` (2026-10-23), package `@upstash/context7-mcp` 4.4.4.

**How it was obtained.** The tools are described in the code as ready-made strings and zod schemas, so below is a verbatim copy of the code that builds `tools/list` and `instructions`.

## Server instructions ([index.ts:298–300](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/index.ts#L298-L300))

```ts
    instructions: `Use this server to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service — even well-known ones like React, Next.js, Prisma, Express, Tailwind, Django, or Spring Boot. This includes API syntax, configuration, version migration, porting code between libraries, platforms, or SQL dialects, library-specific debugging, setup instructions, and CLI tool usage. Use even when you think you know the answer — your training data may not reflect recent changes. Prefer this over web search for library docs.

Do not use for: refactoring, debugging, or reviewing code that does not depend on a library or platform API, or general programming concepts.`,
```

## Tools ([index.ts:306–438](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/index.ts#L306-L438))

```ts
  server.registerTool(
    RESOLVE_LIBRARY_ID_TOOL,
    {
      title: "Resolve Context7 Library ID",
      description: `Resolves a package/product name to a Context7-compatible library ID and returns matching libraries.

You MUST call this function before 'Query Documentation' tool to obtain a valid Context7-compatible library ID UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

Each result includes:
- Library ID: Context7-compatible identifier (format: /org/project)
- Name: Library or package name
- Description: Short summary
- Code Snippets: Number of available code examples
- Source Reputation: Authority indicator (High, Medium, Low, or Unknown)
- Benchmark Score: Quality indicator (100 is the highest score)
- Versions: List of versions if available. Use one of those versions if the user provides a version in their query. The format of the version is /org/project/version.

For best results, select libraries based on name match, source reputation, snippet coverage, benchmark score, and relevance to your use case.

Selection Process:
1. Analyze the query to understand what library/package the user is looking for
2. Return the most relevant match based on:
- Name similarity to the query (exact matches prioritized)
- Description relevance to the query's intent
- Documentation coverage (prioritize libraries with higher Code Snippet counts)
- Source reputation (consider libraries with High or Medium reputation more authoritative)
- Benchmark Score: Quality indicator (100 is the highest score)

Response Format:
- Return the selected library ID in a clearly marked section
- Provide a brief explanation for why this library was chosen
- If multiple good matches exist, acknowledge this but proceed with the most relevant one
- If no good matches exist, clearly state this and suggest query refinements

For ambiguous queries, request clarification before proceeding with a best-guess match.

IMPORTANT: Do not call this tool more than 3 times per question. If you cannot find what you need after 3 calls, use the best result you have.`,
      inputSchema: z.preprocess(
        aliasArgs(GLOBAL_ALIASES),
        z.object({
          query: z
            .string()
            .describe(
              "What to look up in the library's documentation. This is used to rank library results by relevance to what the user is trying to accomplish. The query is sent to the Context7 API for processing. Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query."
            ),
          libraryName: z
            .string()
            .describe(
              "Library name to search for and retrieve a Context7-compatible library ID. Use the official library name with proper punctuation — e.g., 'Next.js' instead of 'nextjs', 'Customer.io' instead of 'customerio', 'Three.js' instead of 'threejs'."
            ),
        })
      ),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: true,
        idempotentHint: true,
      },
    },
    async ({ query, libraryName }: { query: string; libraryName: string }, toolCtx) => {
      const ctx = getClientContext(toolCtx);
      const searchResponse = await searchLibraries(query, libraryName, ctx);

      if (!searchResponse.results || searchResponse.results.length === 0) {
        const text = searchResponse.error ?? "No libraries found matching the provided name.";
        maybeElicitAuthSignIn(server, ctx);
        recordToolCallTelemetry(ctx, searchResponse.error ? "error" : "not_found");
        return {
          content: [
            {
              type: "text" as const,
              text,
            },
          ],
          // Same rule as query-docs: an upstream failure is an error, an empty match is not.
          ...(searchResponse.error ? { isError: true } : {}),
        };
      }

      const resultsText = formatSearchResults(searchResponse);
      const responseText = `Available Libraries:\n\n${resultsText}`;
      maybeElicitAuthSignIn(server, ctx);
      recordToolCallTelemetry(ctx, "success");
      return {
        content: [
          {
            type: "text" as const,
            text: responseText,
          },
        ],
      };
    }
  );

  server.registerTool(
    QUERY_DOCS_TOOL,
    {
      title: "Query Documentation",
      description: `Retrieves and queries up-to-date documentation and code examples from Context7 for any programming library or framework.

You must call 'Resolve Context7 Library ID' tool first to obtain the exact Context7-compatible library ID required to use this tool, UNLESS the user explicitly provides a library ID in the format '/org/project' or '/org/project/version' in their query.

Do not call this tool more than 3 times per question.

If you know the programming language the user is working in, pass it as \`language\` so the results match their setup.`,
      inputSchema: z.preprocess(
        aliasArgs({ ...GLOBAL_ALIASES, ...QUERY_DOCS_ALIASES }),
        z.object({
          libraryId: z
            .string()
            .describe(
              "Exact Context7-compatible library ID (e.g., '/mongodb/docs', '/vercel/next.js', '/supabase/supabase', '/vercel/next.js/v16.2.9') retrieved from 'resolve-library-id' or directly from user query in the format '/org/project' or '/org/project/version'."
            ),
          query: z
            .string()
            .describe(
              "What to look up in the library's documentation, scoped to a single concept. Be specific and include relevant details, but keep each query to one topic — if the user's question spans multiple distinct concepts, make a separate call per concept instead of combining them, unless the question is about how the concepts interact. Good: 'How to set up authentication with JWT in Express.js' or 'React useEffect cleanup function examples'. Bad (too vague): 'auth' or 'hooks'. Bad (too broad): 'routing and auth and caching in Next.js'. The query is sent to the Context7 API for processing. Do not include any sensitive or confidential information such as API keys, passwords, credentials, personal data, or proprietary code in your query."
            ),
          // No length limit here: the API trims long values instead of rejecting the call.
          language: z
            .string()
            .optional()
            .describe(
              "Programming language the user is writing code in, such as 'Python', 'TypeScript', 'Go', or 'C#'. Ranks code examples in that language first. Leave it out when the language is unknown or does not apply."
            ),
        })
      ),
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        openWorldHint: true,
        idempotentHint: true,
      },
```

Tool names: `resolve-library-id` and `query-docs` ([tool-names.ts](https://github.com/upstash/context7/blob/b5e81de845092694ba1bfc5af15400f319c89b6d/packages/mcp/src/lib/tool-names.ts)). Prompts and resources are declared but empty.
