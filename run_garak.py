#!/usr/bin/env python
"""
Run Garak Red-Team Evaluation

Third step in the demo flow:

  1. red-team-prompt-generation.ipynb — generates adversarial prompts → $XDG_DATA_HOME
  2. garak-to-sdg.ipynb              — converts JSON to garak format under
                                       $XDG_DATA_HOME/garak/data/cas/
  3. run_garak.py (this script)      — runs garak with data/garak.yaml and
                                       prints the resulting report paths
"""

import json
import os
from pathlib import Path

from llama_stack_provider_trustyai_garak.utils import _ensure_xdg_vars

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

_ensure_xdg_vars()

if "OPENAICOMPATIBLE_API_KEY" not in os.environ:
    raise EnvironmentError(
        "Set OPENAICOMPATIBLE_API_KEY before running. "
        "Export it in your shell: export OPENAICOMPATIBLE_API_KEY=..."
    )

repo_root = Path(__file__).resolve().parent
config_path = repo_root / "data" / "garak.yaml"
if not config_path.exists():
    raise FileNotFoundError(f"Cannot find garak config: {config_path}")

print(f"Config:    {config_path}")

# ---------------------------------------------------------------------------
# Verify Garak data
# ---------------------------------------------------------------------------

xdg_data = os.environ["XDG_DATA_HOME"]
typology_path = Path(xdg_data) / "garak" / "data" / "cas" / "trait_typology.json"

with open(typology_path) as f:
    typology = json.load(f)

print(f"Typology: {typology_path}")
print(f"Intents:  {list(typology.keys())}")

# ---------------------------------------------------------------------------
# Run Garak
# ---------------------------------------------------------------------------

import garak.cli

garak.cli.main(["--config", str(config_path)])

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

garak_runs = Path(xdg_data) / "garak" / "garak_runs"
report_files = sorted(garak_runs.glob("*.report.jsonl"))
html_files = sorted(garak_runs.glob("*.report.html"))

if report_files:
    print(f"JSONL report: {report_files[-1].resolve()}")
if html_files:
    print(f"HTML report:  {html_files[-1].resolve()}")
