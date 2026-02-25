#!/usr/bin/env python3
"""Build an HTML dataset explorer by injecting a JSON file into the template."""

import argparse
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent / "explorer_template.html"
DEFAULT_TITLE = "Dataset Explorer"


def title_from_stem(stem: str) -> str:
    """Derive a human-readable title from a filename stem."""
    return stem.replace("_", " ").replace("-", " ").title()


def main():
    parser = argparse.ArgumentParser(
        description="Inject a JSON dataset into the explorer HTML template."
    )
    parser.add_argument("--data", required=True, help="Path to the JSON dataset file")
    parser.add_argument("--title", help="Override the page title and header")
    parser.add_argument("--output", help="Output HTML path (default: <data_stem>_explorer.html)")
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    with data_path.open() as f:
        data = json.load(f)

    minified = json.dumps(data, separators=(",", ":"))

    template_text = TEMPLATE.read_text()

    html = template_text.replace("__EXPLORER_DATA__", minified)

    title = args.title or title_from_stem(data_path.stem)
    html = html.replace("__EXPLORER_TITLE__", title)

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = data_path.parent / (data_path.stem + "_explorer.html")

    output_path.write_text(html)
    print(f"Written: {output_path}")


if __name__ == "__main__":
    main()
