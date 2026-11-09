"""Public presentation data, entry-point and portable-packaging contracts."""

from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
WORKSHOP = ROOT / "presentations" / "html-workshop"


class AssetReferences(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.scripts: list[str] = []
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        source = values.get("src")
        stylesheet = values.get("href")
        if tag == "script" and source:
            self.scripts.append(source)
        if tag == "link" and values.get("rel") == "stylesheet" and stylesheet:
            self.stylesheets.append(stylesheet)


def assert_runtime_global(content: str, runtime: str) -> None:
    expected = re.search(r"const deckData = window\.(\w+);", runtime)
    defined = re.search(r"^window\.(\w+) = \{", content, re.MULTILINE)
    assert expected is not None, "Runtime deck global was not found."
    assert defined is not None, "Content deck global was not found."
    assert defined[1] == expected[1] == "DECK", "Content and runtime deck globals must match."


def test_example_defines_the_runtime_deck_global() -> None:
    assert_runtime_global(
        (WORKSHOP / "example-content.js").read_text(encoding="utf-8"),
        (WORKSHOP / "deck.js").read_text(encoding="utf-8"),
    )


def test_contract_rejects_the_original_global_mismatch() -> None:
    content = (WORKSHOP / "example-content.js").read_text(encoding="utf-8")
    original = content.replace("window.DECK = {", "window.DECK_CONTENT = {", 1)
    with pytest.raises(AssertionError, match="deck globals must match"):
        assert_runtime_global(original, (WORKSHOP / "deck.js").read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    ("entry", "scripts"),
    [
        ("example.html", ["example-content.js", "deck.js"]),
        ("example-presenter.html", ["example-content.js", "example-notes.js", "deck.js"]),
    ],
)
def test_public_entry_points_load_existing_assets_in_order(
    entry: str, scripts: list[str],
) -> None:
    references = AssetReferences()
    references.feed((WORKSHOP / entry).read_text(encoding="utf-8"))
    assert references.scripts == scripts
    assert references.stylesheets == ["theme.css"]
    for name in references.scripts + references.stylesheets:
        assert (WORKSHOP / name).is_file()


def test_presenter_notes_match_both_synthetic_slide_ids() -> None:
    content = (WORKSHOP / "example-content.js").read_text(encoding="utf-8")
    notes = (WORKSHOP / "example-notes.js").read_text(encoding="utf-8")
    slide_ids = re.findall(r'^\s+id: "([^"]+)",', content, re.MULTILINE)
    note_ids = re.findall(r'^  "([^"]+)": \{', notes, re.MULTILINE)
    assert slide_ids == ["example-cover", "example-controls"]
    assert note_ids == slide_ids


def test_portable_audience_inlines_the_public_source_assets(tmp_path: Path) -> None:
    output = tmp_path / "presentation.html"
    result = subprocess.run(
        [sys.executable, str(WORKSHOP / "build_single_file.py"), "--output", str(output)],
        cwd=ROOT, check=True, capture_output=True, text=True,
    )
    assert "Wrote" in result.stdout
    html = output.read_text(encoding="utf-8")
    references = AssetReferences()
    references.feed(html)
    assert references.scripts == []
    assert references.stylesheets == []
    for name in ("theme.css", "example-content.js", "deck.js"):
        assert (WORKSHOP / name).read_text(encoding="utf-8") in html
    assert "window.SPEAKER_NOTES =" not in html
