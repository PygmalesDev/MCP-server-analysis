"""
Entry point of the MCP server analysis. Settings are in config.py; the flags choose what to run.

    python main.py --analyse       collect links, download sources and analyse the servers (steps 1-3)
    python main.py --links-only    only collect links, download sources and check links (steps 1-2)
    python main.py --excel         collect all JSON results into data/analysis_result/MCP_analysis_results.xlsx
    python main.py --manual-excel  fill data/markdown/manual_analysis/MCP_manual_analysis_EN.xlsx from the manual analysis

Flags can be combined, e.g. python main.py --analyse --excel
"""

import argparse

import config


def main():
    parser = argparse.ArgumentParser(description="MCP server analysis (settings: config.py)")
    parser.add_argument("--analyse", action="store_true", help="steps 1-3: links, sources, analysis with Codex")
    parser.add_argument("--links-only", action="store_true", help="steps 1-2 only: links and sources, no analysis")
    parser.add_argument("--excel", action="store_true", help="build the Excel workbook from the JSON results")
    parser.add_argument("--manual-excel", action="store_true",
                        help="fill the manual analysis workbook from data/markdown/manual_analysis/json")
    args = parser.parse_args()

    if not (args.analyse or args.links_only or args.excel or args.manual_excel):
        parser.print_help()
        return
    if args.analyse and args.links_only:
        parser.error("use either --analyse or --links-only")

    if args.analyse or args.links_only:
        config.LINKS_ONLY = args.links_only
        from src import analyse_servers
        analyse_servers.main()
    if args.excel:
        from src import build_excel
        build_excel.main()
    if args.manual_excel:
        from src import fill_manual_excel
        fill_manual_excel.main()


if __name__ == "__main__":
    main()
