# Red Hat Summit Demos

Technical demos for Red Hat Summit featuring AI/ML and data science examples using Jupyter notebooks.

## Requirements

- Python 3.11 or higher
- [UV](https://docs.astral.sh/uv/) (recommended) or pip

## Quick Start

### Option 1: Using UV (Recommended)

UV provides faster dependency resolution and installation:

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

Traditional pip installation:

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

## Project Structure

```
rh-summit-demos/
├── notebooks/          # Demo notebooks (numbered for suggested order)
├── data/              # Sample datasets
├── src/               # Shared utilities
├── docs/              # Documentation and design docs
├── pyproject.toml     # Project configuration
└── requirements.txt   # Pip-compatible dependencies
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
