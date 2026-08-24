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
python build_single_file.py
```

The output is written beneath `artifacts/generated/` and is ignored by Git.
Use `--help` to select another approved index/content pair and output path.

Project-specific workshop state, generated content, portable releases, and
presenter notes require release approval and are intentionally excluded from
the public repository. Presenter notes are inspectable in HTML and must never
be treated as confidential.
