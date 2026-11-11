#!/usr/bin/env python3
"""Check that the public repository contains only approved source material."""

from __future__ import annotations

import ast
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    ".env.example",
    ".gitattributes",
    ".gitignore",
    ".python-version",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "README.md",
    "SECURITY.md",
    "data/DATA_CLASSIFICATION.md",
    "docs/SOURCE_MANIFEST.md",
    "presentations/html-workshop/example.html",
    "requirements-docs.txt",
}
FORBIDDEN_PREFIXES = (
    "artifacts/generated/",
    "artifacts/renders/",
    "data/migration/",
)
FORBIDDEN_EXACT = {
    "presentations/html-workshop/deck-content.js",
    "presentations/html-workshop/speaker-notes.js",
    "presentations/html-workshop/index.html",
    "presentations/html-workshop/presenter.html",
}
FORBIDDEN_SUFFIXES = (".pem", ".key", ".pfx", ".p12", ".sqlite", ".sqlite3")
SECRET_PATTERN = re.compile(
    rb"(?:api[_-]?key|client[_-]?secret|access[_-]?token|refresh[_-]?token|"
    rb"accountkey=|begin [a-z ]*private key)",
    re.IGNORECASE,
)
TEXT_SUFFIXES = {
    "",
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [os.fsdecode(name) for name in result.stdout.split(b"\0") if name]


def staged_files() -> dict[str, str]:
    result = subprocess.run(
        ["git", "ls-files", "--stage", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    files: dict[str, str] = {}
    for entry in result.stdout.split(b"\0"):
        if not entry:
            continue
        metadata, name = entry.split(b"\t", 1)
        mode, object_id, stage = metadata.split()
        path = os.fsdecode(name)
        if stage != b"0":
            raise ValueError(f"Unresolved index conflict: {path}")
        if mode not in (b"100644", b"100755", b"120000"):
            raise ValueError(f"Unsupported index entry: {path}")
        files[path] = object_id.decode("ascii")
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--staged",
        action="store_true",
        help="inspect the complete Git index and its staged bytes",
    )
    args = parser.parse_args(argv)
    errors: list[str] = []
    try:
        index = staged_files() if args.staged else None
        tracked = list(index) if index is not None else tracked_files()
    except (subprocess.CalledProcessError, ValueError) as exc:
        print(f"Repository verification failed: unable to inspect Git index ({exc}).")
        return 1
    tracked_set = set(tracked)

    missing = sorted(REQUIRED - tracked_set)
    if missing:
        errors.append("Missing required tracked files: " + ", ".join(missing))

    for name in tracked:
        lower = name.lower()
        if lower == ".env" or (lower.startswith(".env.") and lower != ".env.example"):
            errors.append(f"Environment file must not be tracked: {name}")
        forbidden_prefix = name.startswith(FORBIDDEN_PREFIXES) and not name.endswith("/README.md")
        if name in FORBIDDEN_EXACT or forbidden_prefix:
            errors.append(f"Controlled/generated path must not be tracked: {name}")
        if lower.endswith(FORBIDDEN_SUFFIXES):
            errors.append(f"Credential or runtime file must not be tracked: {name}")
        if lower.endswith((".docx", ".xlsx")) and not name.startswith("tests/fixtures/synthetic/"):
            errors.append(f"Office binary requires explicit public-release review: {name}")
        if name.startswith("artifacts/archive/") and lower.endswith((".pdf", ".png", ".webp")):
            errors.append(f"Historical binary belongs in archive storage or Git LFS: {name}")

        path = ROOT / name
        if path.suffix.lower() in TEXT_SUFFIXES and (index is not None or path.is_file()):
            if index is not None:
                try:
                    content = subprocess.run(
                        ["git", "cat-file", "blob", index[name]],
                        cwd=ROOT,
                        check=True,
                        capture_output=True,
                    ).stdout
                except subprocess.CalledProcessError:
                    errors.append(f"Could not read staged content: {name}")
                    continue
            else:
                content = path.read_bytes()
            if name != "scripts/verify_repository.py" and SECRET_PATTERN.search(content):
                errors.append(f"Potential secret marker requires review: {name}")
            if path.suffix.lower() == ".py":
                try:
                    ast.parse(content.decode("utf-8"), filename=name)
                except (SyntaxError, UnicodeDecodeError) as exc:
                    errors.append(f"Python parse failed for {name}: {exc}")

    if errors:
        print("Repository verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    source = "staged" if args.staged else "tracked"
    print(f"Repository verification passed for {len(tracked)} {source} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
