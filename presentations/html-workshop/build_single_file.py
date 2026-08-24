#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
DEFAULT_OUT = REPO_ROOT / "artifacts" / "generated" / "html-workshop" / "presentation-example-single-file.html"


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def local_file(name: str) -> Path:
    path = (ROOT / name).resolve()
    if ROOT not in path.parents:
        raise ValueError(f"Input must remain inside {ROOT}: {name}")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a portable audience deck")
    parser.add_argument("--index", default="example.html")
    parser.add_argument("--content", default="example-content.js")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    index_path = local_file(args.index)
    content_path = local_file(args.content)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    html = index_path.read_text(encoding="utf-8")
    css = (ROOT / "theme.css").read_text(encoding="utf-8")
    content = content_path.read_text(encoding="utf-8")
    runtime = (ROOT / "deck.js").read_text(encoding="utf-8")

    for asset in sorted((ROOT / "assets").glob("*")):
        if asset.is_file():
            content = content.replace(f"assets/{asset.name}", data_uri(asset))

    html = re.sub(r'<link\s+rel="stylesheet"\s+href="theme\.css">', lambda _: f"<style>\n{css}\n</style>", html, count=1)
    html = re.sub(rf'<script\s+src="{re.escape(args.content)}"></script>', lambda _: f"<script>\n{content}\n</script>", html, count=1)
    html = re.sub(r'<script\s+src="deck\.js"></script>', lambda _: f"<script>\n{runtime}\n</script>", html, count=1)

    output.write_text(html, encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
