#!/usr/bin/env python3
"""Check that the public repository contains only approved source material."""

from __future__ import annotations

import ast
import argparse
from contextlib import ExitStack
import os
import re
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath

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
    "docs/DATA_CLASSIFICATION.md",
    "docs/SOURCE_MANIFEST.md",
    "presentations/html-workshop/example.html",
    "requirements-docs.txt",
}
FORBIDDEN_PREFIXES = (
    "artifacts/generated/",
    "artifacts/renders/",
)
FORBIDDEN_EXACT = {
    "presentations/html-workshop/deck-content.js",
    "presentations/html-workshop/speaker-notes.js",
    "presentations/html-workshop/index.html",
    "presentations/html-workshop/presenter.html",
}
FORBIDDEN_SUFFIXES = (".pem", ".key", ".pfx", ".p12", ".sqlite", ".sqlite3")
PROTECTED_PATTERNS = (
    "data", "data/**",
    "docs/project", "docs/project/**",
    "docs/controlled-sources", "docs/controlled-sources/**",
    "docs/buildathon-resources", "docs/buildathon-resources/**",
    "scripts/documents", "scripts/documents/**",
    "scripts/maintenance", "scripts/maintenance/**",
    ".venv/**", "venv/**", "instance/**", "tmp/**",
    "secrets/**", "logs/**", "uploads/**", "**/__pycache__/**",
    "**/.env", "**/.env/**", "**/.env.*", "**/.env.*/**",
    "**/credentials*.json", "**/local.settings.json",
    "**/*.pem", "**/*.key", "**/*.pfx", "**/*.p12", "**/*.cer", "**/*.crt",
    "**/*.db", "**/*.sqlite", "**/*.sqlite3", "**/*.zip",
    "artifacts/generated/**", "artifacts/renders/**",
    "artifacts/archive/**/source/**", "artifacts/archive/**/renders/**",
    "artifacts/archive/**/*.pdf", "artifacts/archive/**/*.png",
    "artifacts/archive/**/*.webp", "artifacts/archive/**/*.html",
    "presentations/html-workshop/.workshop/**",
    "presentations/html-workshop/deck-content.js",
    "presentations/html-workshop/speaker-notes.js",
    "presentations/html-workshop/index.html",
    "presentations/html-workshop/presenter.html",
    "presentations/html-workshop/CRVLB-competency-assessment-system.html",
    "presentations/html-workshop/competency-assessment-system-presenter.html",
)
PUBLIC_EXCEPTIONS = (
    ".env.example",
    "artifacts/generated/README.md",
    "artifacts/renders/README.md",
)
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


def exact_file_selector(name: str, *, exclude: bool = False) -> str:
    # A literal pathspec also matches descendants. Force a filename-only glob.
    magic = "top,glob,exclude" if exclude else "top,glob"
    return f":({magic}){name[:-1]}[{name[-1]}]"


def protected_index_errors() -> list[str]:
    # A constant format detects matches without retrieving private filenames.
    # --error-unmatch is unsuitable: it counts matches before exclusions.
    result = subprocess.run(
        ["git", "ls-files", "--format=PROTECTED", "-z", "--",
         *(f":(top,glob,icase){pattern}" for pattern in PROTECTED_PATTERNS),
         *(exact_file_selector(name, exclude=True) for name in PUBLIC_EXCEPTIONS)],
        cwd=ROOT, check=True, capture_output=True,
    )
    if result.stdout:
        return ["Protected indexed material must not be tracked; review the public path policy."]
    return []


def staged_files() -> dict[str, str]:
    files: dict[str, str] = {}
    selectors = (
        [".", *(f":(top,exclude,glob,icase){p}" for p in PROTECTED_PATTERNS)],
        [exact_file_selector(name) for name in PUBLIC_EXCEPTIONS],
    )
    for paths in selectors:
        result = subprocess.run(
            ["git", "ls-files", "--stage", "-z", "--", *paths],
            cwd=ROOT, check=True, capture_output=True,
        )
        for entry in result.stdout.split(b"\0"):
            if not entry:
                continue
            metadata, name = entry.split(b"\t", 1)
            mode, object_id, stage = metadata.split()
            path = os.fsdecode(name)
            parts = PurePosixPath(path).parts
            if (not parts or PurePosixPath(path).is_absolute()
                    or any(p in {".", ".."} for p in parts)
                    or "\\" in path or ":" in path):
                raise ValueError("Unsafe indexed path.")
            if stage != b"0":
                raise ValueError(f"Unresolved index conflict: {path}")
            if mode not in (b"100644", b"100755"):
                raise ValueError(f"Unsupported index entry (links are not allowed): {path}")
            files[path] = object_id.decode("ascii")
    return files


def read_worktree_file(name: str) -> bytes:
    path = ROOT
    for part in ("", *PurePosixPath(name).parts):
        path = path / part
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_reparse_tag", 0) & 0x20000000:
            raise ValueError("Symbolic links and junctions are not allowed.")
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("Expected a regular tracked file.")
    if os.name == "nt":
        return read_windows_file(name)
    with ExitStack() as handles:
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        directory = os.open(ROOT, flags)
        handles.callback(os.close, directory)
        parts = PurePosixPath(name).parts
        for part in parts[:-1]:
            directory = os.open(part, flags, dir_fd=directory)
            handles.callback(os.close, directory)
        descriptor = os.open(
            parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory,
        )
        handles.callback(os.close, descriptor)
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ValueError("Expected a regular tracked file.")
        with os.fdopen(os.dup(descriptor), "rb") as source:
            return source.read()


def read_windows_file(name: str) -> bytes:
    import ctypes
    from ctypes import wintypes

    class AttributeTagInfo(ctypes.Structure):
        _fields_ = [("attributes", wintypes.DWORD), ("tag", wintypes.DWORD)]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = (
        wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
    )
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.GetFileInformationByHandleEx.argtypes = (
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
    )
    kernel.GetFileInformationByHandleEx.restype = wintypes.BOOL
    kernel.ReadFile.argtypes = (
        wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID,
    )
    kernel.ReadFile.restype = wintypes.BOOL
    kernel.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel.CloseHandle.restype = wintypes.BOOL

    parts = PurePosixPath(name).parts
    path = ROOT
    with ExitStack() as handles:
        for position, part in enumerate(("", *parts)):
            path = path / part
            is_directory = position < len(parts)
            handle = kernel.CreateFileW(
                str(path), 0x1 if is_directory else 0x80000000,
                0x1, None, 3, 0x00200000 | 0x02000000, None,
            )
            if handle == wintypes.HANDLE(-1).value:
                raise OSError(ctypes.get_last_error(), "Cannot acquire a safe file handle.")
            handles.callback(kernel.CloseHandle, handle)
            info = AttributeTagInfo()
            if not kernel.GetFileInformationByHandleEx(
                handle, 9, ctypes.byref(info), ctypes.sizeof(info),
            ):
                raise OSError(ctypes.get_last_error(), "Cannot inspect file handle.")
            # OPEN_REPARSE_POINT avoids following the final component. Retaining
            # read-share-only handles prevents parent replacement or retargeting.
            if info.tag & 0x20000000 or bool(info.attributes & 0x10) != is_directory:
                raise ValueError("Unsafe link or unexpected file type.")
        chunks = []
        buffer = ctypes.create_string_buffer(65536)
        size = wintypes.DWORD()
        while True:
            if not kernel.ReadFile(handle, buffer, len(buffer), ctypes.byref(size), None):
                raise OSError(ctypes.get_last_error(), "Cannot read file handle.")
            if not size.value:
                return b"".join(chunks)
            chunks.append(buffer.raw[:size.value])


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
        errors.extend(protected_index_errors())
        index = staged_files()
        tracked = list(index)
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
        if lower.startswith("data/"):
            errors.append(f"Local data directory must not be tracked: {name}")
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
        if path.suffix.lower() in TEXT_SUFFIXES:
            if args.staged:
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
                try:
                    content = read_worktree_file(name)
                except (OSError, ValueError):
                    errors.append(f"Could not safely read tracked content: {name}")
                    continue
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
