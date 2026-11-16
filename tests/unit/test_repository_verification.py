from pathlib import Path
import os
import subprocess

import pytest

from scripts import verify_repository


def git(root, *args, input=None):
    return subprocess.run(
        ["git", *args],
        cwd=root,
        input=input,
        capture_output=True,
        check=True,
    )


@pytest.fixture
def repository(tmp_path, monkeypatch):
    git(tmp_path, "init", "-q")
    monkeypatch.setattr(verify_repository, "ROOT", tmp_path)
    for name in verify_repository.REQUIRED:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("" if name == ".gitignore" else "synthetic\n", encoding="utf-8")
    git(tmp_path, "add", "--", *sorted(verify_repository.REQUIRED))
    return tmp_path


def test_staged_verification_reads_index_not_worktree(repository, capsys):
    path = repository / "example.txt"
    path.write_text("client_" + "secret = placeholder\n", encoding="utf-8")
    git(repository, "add", "--", "example.txt")
    path.write_text("clean working copy\n", encoding="utf-8")

    assert verify_repository.main(["--staged"]) == 1
    output = capsys.readouterr().out
    assert "Potential secret marker requires review: example.txt" in output
    assert "placeholder" not in output
    assert verify_repository.main([]) == 0


def test_staged_clean_content_does_not_read_dirty_worktree(repository, capsys):
    path = repository / "example.txt"
    path.write_text("clean staged content\n", encoding="utf-8")
    git(repository, "add", "--", "example.txt")
    path.write_text("access_" + "token = placeholder\n", encoding="utf-8")

    assert verify_repository.main(["--staged"]) == 0
    assert verify_repository.main([]) == 1
    assert "placeholder" not in capsys.readouterr().out


def test_staged_path_policy_and_synthetic_fixture_exception(repository, capsys):
    bad = repository / "data" / "migration" / "raw.xlsx"
    good = repository / "tests" / "fixtures" / "synthetic" / "example.xlsx"
    for path in (bad, good):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"synthetic fixture")
        git(repository, "add", "--", str(path.relative_to(repository)))

    assert verify_repository.main(["--staged"]) == 1
    output = capsys.readouterr().out
    assert "Protected indexed material must not be tracked" in output
    assert "raw.xlsx" not in output
    assert "tests/fixtures/synthetic/example.xlsx" not in output


def test_staged_data_directory_is_never_public(repository, capsys):
    local = repository / "data" / "notes.txt"
    local.parent.mkdir()
    local.write_text("synthetic\n", encoding="utf-8")
    git(repository, "add", "--", "data/notes.txt")
    assert verify_repository.main(["--staged"]) == 1
    output = capsys.readouterr().out
    assert "Protected indexed material must not be tracked" in output
    assert "notes.txt" not in output


def test_staged_invalid_python_and_required_deletion(repository, capsys):
    (repository / "broken.py").write_text("def broken(:\n", encoding="utf-8")
    git(repository, "add", "--", "broken.py")
    git(repository, "rm", "--cached", "--", "README.md")

    assert verify_repository.main(["--staged"]) == 1
    output = capsys.readouterr().out
    assert "Python parse failed for broken.py" in output
    assert "Missing required tracked files: README.md" in output


def test_staged_conflict_is_reported(repository, capsys):
    object_id = git(repository, "hash-object", "-w", "--stdin", input=b"synthetic\n").stdout.strip()
    git(
        repository,
        "update-index",
        "--index-info",
        input=b"100644 " + object_id + b" 1\tconflict.txt\n",
    )

    assert verify_repository.main(["--staged"]) == 1
    assert "Unresolved index conflict: conflict.txt" in capsys.readouterr().out


@pytest.mark.parametrize("staged", [False, True])
def test_protected_paths_are_pruned_before_names_or_content_are_read(
    repository, monkeypatch, capsys, staged,
):
    paths = (
        "data/private-marker.txt",
        "docs/project/private-marker.md",
        "docs/controlled-sources/private-marker.txt",
        "docs/buildathon-resources/private-marker.json",
        "scripts/documents/private-marker.py",
        "artifacts/archive/example/brief/source/private-marker.py",
        ".env.private-marker",
        "instance/private-marker.db",
    )
    for name in paths:
        path = repository / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"private-marker\n")
        git(repository, "add", "--", name)

    original_run = subprocess.run

    def guarded_run(args, **kwargs):
        if args[:2] == ["git", "cat-file"]:
            result = original_run(args, **kwargs)
            assert b"private-marker" not in result.stdout
            return result
        result = original_run(args, **kwargs)
        if args[:2] == ["git", "ls-files"] and kwargs.get("capture_output"):
            assert b"private-marker" not in result.stdout
        return result

    original_read = verify_repository.read_worktree_file

    def guarded_read(name):
        assert "private-marker" not in name
        return original_read(name)

    monkeypatch.setattr(subprocess, "run", guarded_run)
    monkeypatch.setattr(verify_repository, "read_worktree_file", guarded_read)
    assert verify_repository.main(["--staged"] if staged else []) == 1
    assert "private-marker" not in capsys.readouterr().out


def test_public_data_source_and_scaffolds_remain_checked(repository, capsys):
    for name in ("app/data/example.py", "artifacts/generated/README.md"):
        path = repository / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# synthetic\n", encoding="utf-8")
        git(repository, "add", "--", name)
    assert verify_repository.main(["--staged"]) == 0

    path.write_text("client_" + "secret = placeholder\n", encoding="utf-8")
    git(repository, "add", "--", str(path.relative_to(repository)))
    assert verify_repository.main(["--staged"]) == 1
    assert "Potential secret marker" in capsys.readouterr().out


@pytest.mark.parametrize("staged", [False, True])
def test_public_exceptions_do_not_admit_directory_descendants(
    repository, monkeypatch, capsys, staged,
):
    for name in verify_repository.PUBLIC_EXCEPTIONS:
        path = repository / name
        if path.is_file():
            git(repository, "rm", "--cached", "--", name)
            path.unlink()
        path.mkdir(parents=True)
        child = path / "private-marker" / "README.md"
        child.parent.mkdir()
        child.write_text("private-marker\n", encoding="utf-8")
        git(repository, "add", "--", str(child.relative_to(repository)))

    original_run = subprocess.run

    def guarded_run(args, **kwargs):
        result = original_run(args, **kwargs)
        if kwargs.get("capture_output"):
            assert b"private-marker" not in result.stdout
        return result

    monkeypatch.setattr(subprocess, "run", guarded_run)
    assert verify_repository.main(["--staged"] if staged else []) == 1
    output = capsys.readouterr().out
    assert "Protected indexed material" in output
    assert "private-marker" not in output


def test_staged_link_is_rejected_without_reading_target(repository, capsys):
    object_id = git(repository, "hash-object", "-w", "--stdin", input=b"data/unknown\n").stdout.strip()
    git(repository, "update-index", "--add", "--cacheinfo",
        f"120000,{object_id.decode()},link.txt")
    assert verify_repository.main(["--staged"]) == 1
    assert "links are not allowed" in capsys.readouterr().out


@pytest.mark.parametrize("junction", [False, True])
def test_worktree_link_parent_is_not_followed(repository, monkeypatch, capsys, junction):
    from types import SimpleNamespace
    import stat

    target = repository / "public" / "example.txt"
    target.parent.mkdir()
    target.write_text("synthetic\n", encoding="utf-8")
    git(repository, "add", "--", "public/example.txt")
    original_lstat = Path.lstat

    def link_stat(path):
        if path == target.parent:
            return SimpleNamespace(
                st_mode=stat.S_IFDIR if junction else stat.S_IFLNK,
                st_reparse_tag=0xA0000003 if junction else 0,
            )
        assert path != target, "Must reject parent before inspecting its descendant"
        return original_lstat(path)

    monkeypatch.setattr(Path, "lstat", link_stat)
    assert verify_repository.main([]) == 1
    assert "Could not safely read tracked content: public/example.txt" in capsys.readouterr().out


def test_missing_tracked_text_fails_explicitly(repository, capsys):
    (repository / "README.md").unlink()
    assert verify_repository.main([]) == 1
    assert "Could not safely read tracked content: README.md" in capsys.readouterr().out


def test_parent_replaced_after_lstat_is_not_followed(repository, monkeypatch):
    import stat

    public = repository / "public"
    public.mkdir()
    source = public / "example.txt"
    source.write_bytes(b"public\n")
    private = repository / "data"
    private.mkdir()
    (private / "example.txt").write_bytes(b"private-marker\n")
    original_lstat = Path.lstat
    replaced = False

    def replace_parent(path):
        nonlocal replaced
        info = original_lstat(path)
        if path == source and not replaced:
            assert stat.S_ISREG(info.st_mode)
            replaced = True
            public.rename(repository / "original")
            if os.name == "nt":
                import _winapi
                _winapi.CreateJunction(str(private), str(public))
            else:
                public.symlink_to(private, target_is_directory=True)
        return info

    monkeypatch.setattr(Path, "lstat", replace_parent)
    with pytest.raises((ValueError, OSError)):
        verify_repository.read_worktree_file("public/example.txt")
    assert replaced


@pytest.mark.skipif(os.name != "nt", reason="Windows directory sharing semantics")
def test_windows_parent_is_pinned_during_child_acquisition(repository, monkeypatch):
    import ctypes
    from ctypes import wintypes

    public = repository / "public"
    public.mkdir()
    (public / "example.txt").write_bytes(b"public\n")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    original_info = kernel.GetFileInformationByHandleEx
    original_info.argtypes = (
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
    )
    original_info.restype = wintypes.BOOL
    calls = 0
    blocked = []

    def inspect_and_attempt_replacement(handle, kind, buffer, size):
        nonlocal calls
        result = original_info(handle, kind, buffer, size)
        calls += 1
        if calls == 2:
            # Interleave after the public parent is validated, before its child
            # is opened. Both rename and reparse-point writes must be blocked.
            with pytest.raises(OSError) as error:
                public.rename(repository / "replaced")
            assert error.value.winerror == 32
            blocked.append("rename")
            competitor = kernel.CreateFileW(
                str(public), 0x40000000, 0x7, None, 3, 0x02000000, None,
            )
            failure = ctypes.get_last_error()
            if competitor != wintypes.HANDLE(-1).value:
                kernel.CloseHandle(competitor)
            assert competitor == wintypes.HANDLE(-1).value and failure == 32
            blocked.append("write")
        return result

    monkeypatch.setattr(kernel, "GetFileInformationByHandleEx", inspect_and_attempt_replacement)
    monkeypatch.setattr(ctypes, "WinDLL", lambda *args, **kwargs: kernel)
    assert verify_repository.read_worktree_file("public/example.txt") == b"public\n"
    assert blocked == ["rename", "write"]
