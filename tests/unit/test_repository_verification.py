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
    assert "data/migration/raw.xlsx" in output
    assert "tests/fixtures/synthetic/example.xlsx" not in output


def test_staged_data_directory_is_never_public(repository, capsys):
    local = repository / "data" / "notes.txt"
    local.parent.mkdir()
    local.write_text("synthetic\n", encoding="utf-8")
    git(repository, "add", "--", "data/notes.txt")
    assert verify_repository.main(["--staged"]) == 1
    assert "Local data directory must not be tracked: data/notes.txt" in capsys.readouterr().out


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
