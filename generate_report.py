#!/usr/bin/env python
"""Generate ART Risk Assessment Report

Fourth step in the demo flow:
  1. red-team-prompt-generation.ipynb
  2. garak-to-sdg.ipynb
  3. run_garak.py
  4. generate_report.py (this script) — generates HTML risk assessment report

Usage:
  python generate_report.py                    # uses most recent report
  python generate_report.py path/to/run.jsonl  # uses specified report
"""

import sys
import os
from pathlib import Path

from llama_stack_provider_trustyai_garak.utils import _ensure_xdg_vars
from llama_stack_provider_trustyai_garak.result_utils import generate_art_report

_ensure_xdg_vars()

if len(sys.argv) > 1:
    report_path = Path(sys.argv[1])
else:
    garak_runs = Path(os.environ["XDG_DATA_HOME"]) / "garak" / "garak_runs"
    reports = sorted(garak_runs.glob("*.report.jsonl"))
    if not reports:
        raise FileNotFoundError(f"No .report.jsonl files found in {garak_runs}")
    report_path = reports[-1]

if not report_path.exists():
    raise FileNotFoundError(f"Report not found: {report_path}")

print(f"JSONL report: {report_path.resolve()}")

report_content = report_path.read_text()
html = generate_art_report(report_content)

# handles garak.<UUID>.report.jsonl -> garak.<UUID>.report.html
html_path = report_path.with_name(report_path.name.replace(".jsonl", ".html"))
html_path.write_text(html)

print(f"HTML report:  {html_path.resolve()}")
