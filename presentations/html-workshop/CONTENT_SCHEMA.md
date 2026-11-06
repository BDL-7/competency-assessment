# Content Schema

## Public runtime contract

The tracked `example-content.js` defines `window.DECK` with `meta` and `slides`
properties; `deck.js` reads that exact global. Each runtime slide has a stable
`id`, `layout`, `section`, `title`, optional `highlight`/`subtitle`, and the
layout-specific fields directly on the slide. For example:

```javascript
window.DECK = {
  meta: { title: "Synthetic example" },
  slides: [{
    id: "example-card",
    layout: "cards",
    section: "Example",
    title: "Synthetic content",
    columns: 1,
    cards: [{ title: "Source", body: "Public-safe example only." }]
  }]
};
```

`example-notes.js` defines `window.SPEAKER_NOTES`, keyed by runtime slide ID.
The presenter loads it before `deck.js`. Both entry pages load content before
the runtime. Trusted HTML fields are author-controlled content, not a channel
for untrusted user input.

## Optional internal workshop state

In an authorized environment with the separate materialization tools available,
workshop state is authoritative. This is an intermediate format, **not** the
object consumed directly by the public runtime. Every approved state slide
supplies controlled fields and exact layout-specific runtime data:

```json
{
  "id": "s03-goals",
  "order": 3,
  "section": "Goals",
  "layout": "cards",
  "content": {
    "title": "What the project will determine",
    "highlight": "determine",
    "subtitle": "One concise sentence.",
    "renderData": {
      "columns": 3,
      "numbered": true,
      "cards": [
        { "accent": "cyan", "title": "Value", "body": "One claim." },
        { "accent": "purple", "title": "Evidence", "bullets": ["Point one", "Point two"] }
      ]
    }
  }
}
```

Keep `id` stable when slides are reordered. `content.renderData` must not repeat `id`, `layout`, `section`, `title`, `highlight`, or `subtitle`.

Supported runtime fields follow the public `example-content.js` and the
renderers in `deck.js`; release-controlled `deck-content.js` is not required:

- `title`: `kicker`, `bullets`, `image`, `imageAlt`, `credits`.
- `image`: `image`, `imageAlt`, `imageBackground`.
- `cards`: `columns`, `numbered`, `cards`.
- `metrics`: `stats`, `barTitle`, `bars`.
- `split`: `columns`, `left`, `right`.
- `process`: `steps`.
- `loop`: `leftTitle`, `cycle`, `cycleNote`, `rightTitle`, `stack`.
- `timeline`: `stages`, `deliverables`.
- `closing`: `actionsTitle`, `actions`, `intakeTitle`, `intake`, `linkLabel`, `link`, `image`, `imageAlt`.
- `custom`: trusted themed `html`.

Store speaker notes and transitions in the slide's `speakerNotes` and `transition` fields. Materialization generates the presenter-only runtime object keyed by slide ID.
These state/materialization tools are optional external prerequisites, not
scripts shipped in this checkout. The Python builder packages existing runtime
content; it does not materialize workshop state or build portable presenter notes.
