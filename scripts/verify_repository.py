#!/usr/bin/env python3
"""Check that the public repository contains only approved source material."""

from __future__ import annotations

import ast
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
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    tracked = tracked_files()
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
        if path.suffix.lower() in TEXT_SUFFIXES and path.is_file():
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

    print(f"Repository verification passed for {len(tracked)} tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
