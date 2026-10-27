"""Fill data/markdown/manual_analysis/MCP_manual_analysis_EN.xlsx with the manual analysis of the 20 servers.

Input:  data/markdown/manual_analysis/json/<server>.json - one file per server; the keys are mapped to the
        Excel columns in SERVERS_COLS, CAP_COLS, ACTION_COLS and OBS_COLS below
        data/markdown/manual_analysis/*_pre_interaction_context.md - inserted verbatim into the Capabilities
        sheet if the text fits into one cell
Output: the same workbook; all old values are cleared first, formulas are kept.

    python main.py --manual-excel
"""

import json

import openpyxl
from openpyxl.styles import Alignment
from openpyxl.worksheet.datavalidation import DataValidation

import config

HERE = config.MANUAL_DIR
WORKBOOK = HERE / "MCP_manual_analysis_EN.xlsx"
CELL_LIMIT = 32000          # Excel allows 32,767 characters per cell

# JSON key -> column header on the sheet "Servers" (row 2)
SERVERS_COLS = {
    "status": "Status",
    "analyst": "Analyst / method",
    "date": "Analysis date",
    "code_repo": "Code repository link",
    "docs_used": "Documentation used (link)",
    "open_eq_deployed": "Open code = deployed server?",
    "mcp_version": "MCP version (protocol)",
    "commit_hash": "Commit hash",
    "commit_date": "Commit date",
    "language": "Implementation language",
    "sdk": "MCP SDK and version",
    "code_public": "Code public?",
    "license": "License",
    "access": "MCP server access: free / paid",
    "server_cost": "MCP server cost (how much)",
    "linked_sw": "Linked software: open source / paid",
    "linked_cost": "Linked software cost",
    "pricing": "Pricing model (details)",
    "restrictions": "Other access restrictions (which)",
    "restricted_by": "Restrictions controlled by",
    "governance_logic": "Additional logic between LLM and software (governance)",
    "structure": "Server structure",
    "structure_note": "Structure: explanation",
    "actions_comment": "Number of actions (manual / comment)",
    "tokens": "Tokens before first action",
    "token_method": "Token counting method",
    "agent_cannot": "Actions a human can do but the agent cannot",
    "docs_recs": "Recommendations in docs not enforced by the server",
    "gov_promises": "Governance promises (data, rights, reversibility, logging)",
    "user_promises": "Promises to the user",
    "promises_vs_logic": "Promises vs. server logic",
    "sources": "Sources (links)",
    "notes": "Notes / questions",
}
CAP_COLS = {
    "impl": "Implemented?",
    "version": "Depends on MCP version (which)",
    "desc": "Detailed description (WHAT / HOW)",
    "pre": "Pre-Interaction Context (verbatim copy)",
    "post": "Post-Interaction Context (result structure)",
    "auth_mech": "Authorization: mechanism",
    "auth_server": "Authorization: authorization server",
    "src": "Sources",
}
ACTION_COLS = {
    "tool": "Tool (name in MCP)",
    "desc": "Meaningful action description",
    "type": "Action type",
    "default": "Enabled by default?",
    "params": "Parameters (name: type; number of categories if enum)",
    "n_params": "Number of parameters",
    "src": "Source",
}
OBS_COLS = {"type": "Observation type", "text": "Observation", "src": "Source / example"}

ALLOWED = {
    ("servers", "status"): {"Not started", "In progress", "Done", "Verified"},
    ("servers", "open_eq_deployed"): {"Yes", "No", "Partially", "Unknown"},
    ("servers", "code_public"): {"Yes", "No", "Partially", "Unknown"},
    ("servers", "access"): {"Free", "Paid", "Freemium", "Unknown"},
    ("servers", "linked_sw"): {"Open source", "Paid", "Freemium", "Open source + paid cloud", "Unknown"},
    ("servers", "structure"): {"Standard", "Non-standard"},
    ("cap", "impl"): {"Yes", "No", "Partially", "Unknown"},
    ("cap", "auth_mech"): {"—", "Metadata Doc", "Preregistration", "Dynamic Client Registration", "API key", "Several methods"},
    ("action", "type"): {"Read", "Write", "Mixed"},
    ("action", "default"): {"Yes", "No", "Unknown"},
    ("obs", "type"): {"Systematic difference", "New design option", "Question for David", "Other"},
}
WRAP = Alignment(wrap_text=True, vertical="top")


def check(kind, key, value, where):
    allowed = ALLOWED.get((kind, key))
    if allowed and value not in allowed:
        raise ValueError(f"{where}: {key}={value!r} is not one of {sorted(allowed)}")


def header_map(ws, row):
    return {ws.cell(row, c).value: c for c in range(1, ws.max_column + 1) if ws.cell(row, c).value}


def resolve(value):
    """'@file:<name>' -> the file's text if it fits into one cell, otherwise a pointer to the file.
    '@section:<name>|<heading>' -> one section of the file (from the heading to the next heading of the same level)."""
    if isinstance(value, str) and value.startswith("@file:"):
        name = value[len("@file:"):]
        text = (HERE / name).read_text(encoding="utf-8")
        if len(text) <= CELL_LIMIT:
            return text
        note = (f"The full verbatim copy is too long for one cell ({len(text):,} characters): "
                f"data/markdown/manual_analysis/{name}")
        if "## 1. Server instructions" in text:
            return note + "\n\n" + resolve(f"@section:{name}|## 1. Server instructions")
        return note
    if isinstance(value, str) and value.startswith("@section:"):
        name, heading = value[len("@section:"):].split("|", 1)
        text = (HERE / name).read_text(encoding="utf-8")
        start = text.index(heading)
        level = heading.split(" ")[0] + " "
        end = text.find("\n" + level, start + len(heading))
        part = text[start:end if end > 0 else None].strip()
        return part if len(part) <= CELL_LIMIT else part[:CELL_LIMIT - 200] + f"\n... (truncated, full text: {name})"
    if isinstance(value, str) and len(value) > CELL_LIMIT:
        raise ValueError(f"cell text too long ({len(value)} characters)")
    return value


def put(ws, row, col, value):
    cell = ws.cell(row, col, resolve(value))
    cell.alignment = WRAP


def extend_validation(ws, col_letter, last_row):
    for dv in ws.data_validations.dataValidation:
        ref = str(dv.sqref)
        if ref.startswith(col_letter + "2:"):
            dv.sqref = openpyxl.worksheet.cell_range.MultiCellRange(f"{col_letter}2:{col_letter}{last_row}")


def clear(s, cap, act, obs):
    """Remove old values so that the workbook can be filled again; formulas and labels stay."""
    for row in s.iter_rows(min_row=3, min_col=2):
        for c in row:
            if not (isinstance(c.value, str) and c.value.startswith("=")):
                if c.column not in (6, 7, 8):          # F-H: endpoint, docs and addressing from the CSV
                    c.value = None
    for row in cap.iter_rows(min_row=2, min_col=3):
        for c in row:
            c.value = None
    for ws in (act, obs):
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.value = None


def main():
    wb = openpyxl.load_workbook(WORKBOOK)
    s, cap, act, obs = wb["Servers"], wb["Capabilities"], wb["Actions"], wb["Observations"]
    clear(s, cap, act, obs)
    s_cols, c_cols = header_map(s, 2), header_map(cap, 1)
    a_cols, o_cols = header_map(act, 1), header_map(obs, 1)

    server_rows = {s.cell(r, 1).value: r for r in range(3, s.max_row + 1) if s.cell(r, 1).value}
    cap_rows = {(cap.cell(r, 1).value, cap.cell(r, 2).value): r for r in range(2, cap.max_row + 1)}

    data = []
    for name in server_rows:
        path = HERE / "json" / f"{name}.json"
        if not path.exists():
            print(f"missing: {path.name}")
            continue
        data.append(json.loads(path.read_text(encoding="utf-8")))

    a_row, o_row = 2, 2
    for d in data:
        name = d["server"]
        row = server_rows[name]
        fields = dict(d["servers"], status=d["status"], analyst=d["analyst"], date=d["date"])
        for key, value in fields.items():
            check("servers", key, value, name)
            put(s, row, s_cols[SERVERS_COLS[key]], value)

        for capability, values in d["capabilities"].items():
            r = cap_rows[(name, capability)]
            for key, value in values.items():
                check("cap", key, value, f"{name}/{capability}")
                put(cap, r, c_cols[CAP_COLS[key]], value)

        for i, action in enumerate(d["actions"], 1):
            put(act, a_row, a_cols["Server"], name)
            put(act, a_row, a_cols["#"], i)
            for key, value in action.items():
                check("action", key, value, f"{name}/{action.get('tool')}")
                put(act, a_row, a_cols[ACTION_COLS[key]], value)
            a_row += 1

        for item in d["observations"]:
            check("obs", "type", item["type"], name)
            put(obs, o_row, o_cols['Server (or "General")'], item.get("server", name))
            for key, value in item.items():
                if key != "server":
                    put(obs, o_row, o_cols[OBS_COLS[key]], value)
            o_row += 1

    # more actions/observations than prepared rows: stretch the drop-down lists
    if a_row - 1 > 601:
        for col in ("A", "E", "F"):
            extend_validation(act, col, a_row - 1)
    if o_row - 1 > 151:
        for col in ("A", "B"):
            extend_validation(obs, col, o_row - 1)

    wb.save(WORKBOOK)
    print(f"{len(data)} servers, {a_row - 2} actions, {o_row - 2} observations -> {WORKBOOK}")
