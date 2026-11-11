from types import SimpleNamespace

from scripts import agent_preflight


def version(monkeypatch, major, minor, micro=0):
    monkeypatch.setattr(
        agent_preflight.sys,
        "version_info",
        SimpleNamespace(major=major, minor=minor, micro=micro),
    )


def test_preflight_reports_supported_version_and_selected_task(tmp_path, monkeypatch, capsys):
    tasks = tmp_path / "agent-tasks"
    tasks.mkdir()
    (tasks / "example.md").write_text("Synthetic task", encoding="utf-8")
    monkeypatch.setattr(agent_preflight, "ROOT", tmp_path)
    version(monkeypatch, 3, 12, 4)

    assert agent_preflight.main(["--task", "example.md"]) == 0
    output = capsys.readouterr().out
    assert "Python: 3.12.4" in output
    assert "Selected task: example.md" in output
    assert "does not establish approval" in output


def test_preflight_warns_for_unsupported_version(tmp_path, monkeypatch, capsys):
    tasks = tmp_path / "agent-tasks"
    tasks.mkdir()
    (tasks / "example.md").write_text("Synthetic task", encoding="utf-8")
    monkeypatch.setattr(agent_preflight, "ROOT", tmp_path)
    version(monkeypatch, 3, 14, 2)

    assert agent_preflight.main(["--task", "example.md"]) == 1
    assert "requires Python 3.12" in capsys.readouterr().out


def test_preflight_requires_existing_task_filename(tmp_path, monkeypatch, capsys):
    (tmp_path / "agent-tasks").mkdir()
    monkeypatch.setattr(agent_preflight, "ROOT", tmp_path)
    version(monkeypatch, 3, 12)

    assert agent_preflight.main([]) == 1
    assert agent_preflight.main(["--task", "../example.md"]) == 1
    assert agent_preflight.main(["--task", "missing.md"]) == 1
    output = capsys.readouterr().out
    assert "Select an approved task contract" in output
    assert "directly under agent-tasks" in output
    assert "not found" in output
