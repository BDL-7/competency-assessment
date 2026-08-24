# Content Schema

Workshop state is authoritative. Every approved slide supplies controlled fields and exact layout-specific runtime data:

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

Supported runtime fields follow the examples in the initial `deck-content.js` template:

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
