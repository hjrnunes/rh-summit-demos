#!/usr/bin/env python3
"""Build an HTML dataset explorer by injecting data into the template."""

import argparse
import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).parent / "explorer_template.html"


def title_from_stem(stem: str) -> str:
    return stem.replace("_", " ").replace("-", " ").title()


def build_explorer(data, title=None, output_path=None):
    """Build an HTML dataset explorer.

    Parameters
    ----------
    data : Path | str | list | pd.DataFrame
        Source data. A Path/str is read as JSON; a DataFrame or list of dicts
        is used directly.
    title : str, optional
        Page title. Derived from output_path stem when omitted.
    output_path : Path | str, optional
        Destination HTML file. Required when data is not a file path.
        Defaults to <data_stem>_explorer.html beside the source file.

    Returns
    -------
    Path
        Path to the written HTML file.
    """
    try:
        import pandas as pd
        _is_df = isinstance(data, pd.DataFrame)
    except ImportError:
        _is_df = False

    if _is_df:
        records = json.loads(data.to_json(orient="records"))
        if output_path is None:
            raise ValueError("output_path is required when data is a DataFrame")
    elif isinstance(data, (str, Path)):
        data_path = Path(data)
        with data_path.open() as f:
            records = json.load(f)
        if output_path is None:
            output_path = data_path.parent / (data_path.stem + "_explorer.html")
        if title is None:
            title = title_from_stem(data_path.stem)
    else:
        records = data  # assume list of dicts
        if output_path is None:
            raise ValueError("output_path is required when data is a list")

    output_path = Path(output_path)
    title = title or title_from_stem(output_path.stem)

    minified = json.dumps(records, separators=(",", ":"))
    html = TEMPLATE.read_text()
    html = html.replace("__EXPLORER_DATA__", minified)
    html = html.replace("__EXPLORER_TITLE__", title)

    output_path.write_text(html)
    print(f"Written: {output_path}")
    return output_path


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

    build_explorer(
        data_path,
        title=args.title,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
