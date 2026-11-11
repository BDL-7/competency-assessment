#!/usr/bin/env python3
"""Report the interpreter and selected agent task before beginning work."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", help="task contract filename under agent-tasks")
    args = parser.parse_args(argv)

    version = sys.version_info
    print(f"Running Python: {version.major}.{version.minor}.{version.micro}")
    supported = (version.major, version.minor) == (3, 12)
    if not supported:
        print("WARNING: supported project validation requires Python 3.12.")

    task = args.task
    if not task:
        print("Select an approved task contract before editing (--task FILENAME).")
        return 1
    if Path(task).name != task or not task.endswith(".md"):
        print("Task must be a Markdown filename directly under agent-tasks.")
        return 1
    if not (ROOT / "agent-tasks" / task).is_file() or task == "README.md":
        print("Task contract not found under agent-tasks.")
        return 1
    print(f"Selected task: {task}")
    print("Confirm its scope, path lease, validation, and human gates before editing.")
    print("Finding a task file does not establish approval or authorization.")
    return 0 if supported else 1


if __name__ == "__main__":
    sys.exit(main())
