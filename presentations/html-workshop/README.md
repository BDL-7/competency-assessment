# HTML presentation framework

This directory contains the reusable 1280 x 720 HTML presentation runtime.
The public example uses synthetic content:

- `example.html`: audience view
- `example-presenter.html`: presenter view
- `example-content.js`: example slide data
- `example-notes.js`: example speaker notes
- `theme.css` and `deck.js`: shared visual and interaction system
- `assets/`: public-safe placeholder visuals

Open `example.html` directly in a modern browser. Controls are:

- Left/Right arrows or Space: navigate
- `F`: fullscreen
- `D`: debug overflow
- `P`: print or save as PDF
- `N`: toggle presenter notes in the presenter view
- `?slide=2`: open a specific slide
- `?debug=1`: enable overflow diagnostics

Build a portable example with:

```powershell
python presentations\html-workshop\build_single_file.py
```

Run that command from the repository root with the approved Python environment
described in [DEVELOPMENT.md](../../docs/DEVELOPMENT.md). If already inside this
directory, use `python build_single_file.py`. No extra Python or Node package
is required.

The output is written beneath `artifacts/generated/` and is ignored by Git.
Use `--help` to select another approved index/content pair and output path.
The default builder produces **audience HTML only**, not a portable presenter
package. Open `example-presenter.html` for modular presenter notes.

`example-content.js` defines `window.DECK`, the object consumed by `deck.js`.
Both example entry pages load it before the runtime. Presenter notes are keyed
by the same stable slide IDs. See [CONTENT_SCHEMA.md](CONTENT_SCHEMA.md).

Validate the public source/packaging contract from the repository root:

```powershell
python -m pytest tests\test_presentation_example.py
```

The existing full pytest CI job includes this regression. Also open audience,
presenter and generated audience modes in a browser: each must render two
synthetic slides without startup errors; check navigation, presenter notes
and `?debug=1` overflow diagnostics. A successful file build alone does not
prove JavaScript rendering works.

Project-specific workshop state, generated content, portable releases, and
presenter notes require release approval and are intentionally excluded from
the public repository. Presenter notes are inspectable in HTML and must never
be treated as confidential.

The optional internal `.workshop` state/materialization workflow described in
[AGENT_HANDOFF.md](AGENT_HANDOFF.md) needs separately available authorized tools.
Those Node scripts are not in this checkout and are not required for the public
example or Python build.
