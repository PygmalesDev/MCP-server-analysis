# MCP server analysis with Codex

## Repository structure

```
main.py                 entry point: runs the scripts in src/ via flags
config.py               all settings
requirements.txt        Python dependencies (openpyxl, only for the Excel workbook)
src/
  analyse_servers.py    link collection, download, analysis (steps 1–3)
  sources.py            downloading sources and checking links (step 2)
  build_excel.py        collects all results into one Excel workbook
  fill_manual_excel.py  fills the manual analysis workbook from data/markdown/manual_analysis/json
data/
  mcp_server_screening.csv          input list of MCP servers
  markdown/prompts/                 all prompt versions (prompt_v*.md, links_v*.md), the prompt log
                                    prompt_log.md, reports full_run_review.md and links_validation.md
  markdown/manual_analysis/         manual analysis of the 20 servers chosen for comparison:
                                    01_tavily.md ... 20_similarweb.md (one report per server),
                                    *_pre_interaction_context.md (verbatim tool descriptions for
                                    servers with open code), json/ (the same results prepared for
                                    Excel, one file per server), MCP_manual_analysis_EN.xlsx,
                                    chosen_servers.txt (the list of the 20 servers)
  prompt_v*/                        analysis results, one JSON per server and prompt version
  analysis_result/                  final workbook MCP_analysis_results.xlsx
prompts/, work/                     working files of a run (in .gitignore)
```

## How the analysis works

The script analyses every server from `data/mcp_server_screening.csv` in three steps:

1. **Link collection.** Codex with a reasoning effort `LINKS_EFFORT` only searches for URLs, using the prompt `data/markdown/prompts/links_v2.md`: documentation and its sub-pages, GitHub repositories, pricing, legal pages, third-party tool catalogues. Result: `work/<server>/links.json`. If the file already exists and was made with the same prompt version, the step is skipped.
2. **Download.** The following is saved in `work/<server>/`:
   - `oauth_metadata.txt`: the endpoint's response and its public OAuth metadata (`/.well-known/...`). Skipped if the CSV contains no concrete public endpoint URL (per-customer or unpublished servers);
   - `pages/`: full copies of all collected pages, the endpoint's pages (`/install` etc.) and guessed catalogue pages, as `.html` and `.txt`, with an index `INDEX.txt`;
   - `code/`: the official GitHub repositories at their latest commit (text files only) and `GITHUB_COMMITS.txt` with hashes and dates;
   - `links_check.txt`: an automatic check of every link and repository (page unreachable, foreign domain, product not mentioned, GitHub organisation not the vendor's, no MCP SDK dependency, marked as unofficial). Repositories that the collector itself called unofficial, and unrelated repositories found on pages, are not downloaded.
3. **Analysis.** Codex with a reasoning effort `REASONING_EFFORT` works with these files, using the prompt from `PROMPT_FILE` (currently `data/markdown/prompts/prompt_v7.md`). It writes the complete tool list to `work/<server>/actions.json`, and the script inserts it into the final JSON `data/<prompt version>/<server>.json`.

The script does the downloading itself because HTTPS does not work in the Codex sandbox shell on Windows, and the Codex browser truncates long pages. Codex runs on ChatGPT subscription, therefore no API key is needed. Codex may write files only inside `work/<server>`.

## Setup (once)

1. Install the Codex CLI: `npm install -g @openai/codex`.
2. Log in with your ChatGPT account: `codex login`.
3. Python 3.10+. The analysis needs no third-party libraries; for the Excel workbook: `pip install -r requirements.txt` (openpyxl).

## Running

1. In `config.py`, choose the model (`MODEL`) and the servers (`SERVERS`): a list of names, `"remaining"` (all servers that are not in `data/markdown/manual_analysis/chosen_servers.txt`). `PARALLEL` sets how many servers are processed at the same time.
2. Run `main.py` from the repository root with one or more flags:

```bash
python main.py --analyse        # steps 1-3: links, sources, analysis
python main.py --links-only     # steps 1-2 only: links, sources and link check, no analysis
python main.py --excel          # build data/analysis_result/MCP_analysis_results.xlsx
python main.py --manual-excel   # fill data/markdown/manual_analysis/MCP_manual_analysis_EN.xlsx
python main.py --analyse --excel
```

Without flags, `main.py` prints the help.

## Output

- `prompts/<server>.md` — the final analysis prompt for the server.
- `work/<server>/` — all collected sources (see step 2), `links.json` and `actions.json`. This is a snapshot of the evidence on the analysis date.
- `data/<prompt version>/<server>.json` — the result. The `_run` field records the model, reasoning effort, prompt versions, date and duration in minutes. If the model did not provide a full commit hash, the script adds it (field `commit_note`).
- `data/<prompt version>/<server>.error.txt` — if Codex did not return valid JSON. The raw answer is kept in `<server>.answer.txt`; on the next run the script tries to repair it (e.g. unescaped quotes) before calling Codex again.

The console shows when each server started, when its sources were downloaded and how many minutes the whole analysis took.

Finished servers are skipped when the script is run again. After three failures in a row (usually the usage limit has been reached), the script starts no new servers, waits for the running ones and exits. Once the limit resets, simply run it again.

## Excel workbook

`python main.py --excel` collects all JSON files from `data/<prompt version>/` (the version is taken from `config.py`) into `data/analysis_result/MCP_analysis_results.xlsx` with the sheets Servers, Capabilities, Actions and Observations (contradictions and observations for the research). Close the file in Excel before running.

## Manual analysis workbook

The 20 servers in `chosen_servers.txt` were also analysed manually, using Claude Opus 5.5 for verification and code analysis. The reports are in `data/markdown/manual_analysis/*.md`. The same results are stored as `data/markdown/manual_analysis/json/<server>.json`, one file per server, with one block per sheet: `servers`, `capabilities`, `actions` and `observations`.

`python main.py --manual-excel` clears the workbook `MCP_manual_analysis_EN.xlsx` and fills it again from these JSON files. Formulas and the CSV columns are kept. If an appendix with verbatim tool descriptions fits into one cell, it is inserted into the Capabilities sheet; if it is too long, the cell points to the file. Close the file in Excel before running.
