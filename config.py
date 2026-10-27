from pathlib import Path

MODEL = "gpt-6-luna" # or "gpt-6.1-sol"
LINKS_EFFORT = "medium" # low / medium / high / xhigh
REASONING_EFFORT = "high"

# Which servers to analyse: a list of names from the CSV column "name",
# or "remaining" = every server in the CSV that is not in chosen_servers.txt, or "chosen" = the 20 manual ones.
SERVERS = "remaining"
# Language of free-text fields in the result
LANGUAGE = "English"
# Re-analyse servers that already have a file in data/<prompt version>/ (True overwrites the manual corrections!)
OVERWRITE = False
# How many Codex runs at the same time
PARALLEL = 20
# Max time for one server, minutes
TIMEOUT_MIN = 40
# Step 1 (link collection): max time, minutes
LINKS_TIMEOUT_MIN = 15

# Files - everything lives inside this repository
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
CSV_FILE = DATA / "mcp_server_screening.csv"                   # input: list of MCP servers
PROMPT_DIR = DATA / "markdown" / "prompts"                     # prompt versions, prompt log, reports
MANUAL_DIR = DATA / "markdown" / "manual_analysis"             # manual analysis of 20 servers
CHOSEN_FILE = MANUAL_DIR / "chosen_servers.txt"                # the 20 manually analysed servers
LINKS_PROMPT_FILE = PROMPT_DIR / "links_v3.md"                 # step 1: link collection
PROMPT_FILE = PROMPT_DIR / "prompt_v9.md"                      # step 3: analysis
RESULT_DIR = DATA / "analysis_result"                          # final Excel workbook
DATA_DIR = DATA / "results" / PROMPT_FILE.stem.replace("prompt_", "")   # JSON results: data/results/v9 for prompt_v9.md
# Excel: result folders merged in this order; a server found in a later folder replaces the earlier result
EXCEL_DATA_DIRS = [DATA / "results" / "v9"]
PROMPTS_DIR = DATA / "prompts"                                 # generated prompt per server (not uploaded to GitHub)
WORK_DIR = ROOT / "work"                                       # per server: links.json, oauth_metadata.txt, pages/, code/, actions.json
