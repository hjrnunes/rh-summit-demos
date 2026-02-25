# Red Hat Summit Demos — LLM Automated Red-Teaming

Jupyter notebook demos for Red Hat Summit showcasing LLM automated red-teaming on OpenShift AI using [NVIDIA Garak](https://github.com/NVIDIA/garak) and [sdg_hub](https://github.com/Red-Hat-AI-Innovation-Team/sdg_hub).

The workflow starts from a policy document, generates a red-team dataset of adversarial prompts using sdg_hub, then uses that dataset in Garak to probe a target LLM and produce a risk assessment report.

## Requirements

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) (recommended) or pip

## Quick Start

### Option 1: Using UV (Recommended)

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Start Jupyter Lab
jupyter lab
```

### Option 2: Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter Lab
jupyter lab
```

> **Data directory:** Notebooks write output to `$XDG_DATA_HOME` (defaults to `/tmp/.local/share` if unset — writable in containers). Set it explicitly to keep data across sessions:
> ```bash
> export XDG_DATA_HOME=$HOME/.local/share
> ```

## Running Against OpenShift AI (Remote Cluster)

If the target model is deployed on OpenShift AI and has no external route, use `oc port-forward` to expose it locally before running the notebooks or garak.

**Target model** (required for notebooks 01 and 03, and `data/garak.yaml`):

```bash
oc port-forward -n stuart-testing pod/ilyagusevgemma-2-9b-it-abliterated-predictor-54597b8fb-cxlhk 8080:8080
```

The model will then be reachable at `http://localhost:8080/v1`.

**Workbench** (required when running notebooks from a local IDE connected to a remote Jupyter kernel):

```bash
oc port-forward pod/summit-demo-0 8888:8888
```

Then point your local IDE (e.g. VS Code) to `http://localhost:8888` as the Jupyter server.

## Notebooks

Run these in order to execute the full red-teaming pipeline:

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `notebooks/01-red-team-prompt-generation.ipynb` | Generate adversarial prompts by sampling multi-dimensional attribute pools and using an LLM to produce contextually-tailored red-team datasets |
| 2 | `notebooks/02-garak-to-sdg.ipynb` | Convert sdg_hub output into Garak's expected format: a trait typology JSON and intent stub text files |
| 3 | `notebooks/03-run-garak.ipynb` | Execute Garak probes against a target LLM using the converted intent typology, producing a JSONL vulnerability report |
| 4 | `notebooks/04-generate-report.ipynb` | Render the Garak JSONL report into a human-readable HTML risk assessment (ART report) |
| — | `notebooks/prompt-generation-financial.ipynb` | Domain-specific variant targeting financial fraud scenarios (South West Bank example) |

## Pipeline Data Flow

```
Policy document
      │
      ▼
01-red-team-prompt-generation.ipynb
      │  writes: $XDG_DATA_HOME/red_team_prompts_<timestamp>.json
      │          $XDG_DATA_HOME/red_team_prompts_<timestamp>_explorer.html
      ▼
02-garak-to-sdg.ipynb
      │  reads:  $XDG_DATA_HOME/*.json (most recent)
      │  writes: $XDG_DATA_HOME/garak/data/cas/
      ▼
03-run-garak.ipynb  (or run_garak.py)
      │  reads:  $XDG_DATA_HOME/garak/data/cas/
      │  writes: $XDG_DATA_HOME/garak/garak_runs/garak.<UUID>.report.jsonl
      ▼
04-generate-report.ipynb  (or generate_report.py)
      │  reads:  $XDG_DATA_HOME/garak/garak_runs/*.report.jsonl (most recent)
      │  writes: $XDG_DATA_HOME/garak/garak_runs/garak.<UUID>.report.html
      ▼
HTML risk assessment report
```

## Project Structure

```
rh-summit-demos/
├── notebooks/          # Pipeline notebooks (numbered in run order)
├── data/               # Garak configuration (garak.yaml)
├── tools/              # HTML dataset explorer (build_explorer.py)
├── pipelines/          # sdg_hub pipeline definitions
├── run_garak.py        # Script version of notebook 03
├── generate_report.py  # Script version of notebook 04
├── pyproject.toml      # Project configuration
└── requirements.txt    # Pip-compatible dependencies
```

## Adding Dependencies

If using UV:

```bash
# Add new package
uv pip install package-name

# Update pyproject.toml manually, then regenerate requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# Commit both files
git add pyproject.toml requirements.txt uv.lock
git commit -m "Add package-name dependency"
```

## License

Internal Red Hat demos for Summit presentations.
