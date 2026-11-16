# Agent Handoff Prompt

Use the following prompt with the public modular example. Project-specific
inputs and releases still require the applicable owner approval.

---

Create a new presentation using the attached HTML template.

Project inputs:
- Project title: [TITLE]
- Presenter(s): [NAMES]
- Organization: [ORGANIZATION]
- Date: [DATE]
- Audience: [AUDIENCE]
- Objective or decision: [OBJECTIVE]
- Source material: [FILES OR NOTES]
- Desired slide count: [NUMBER OR RANGE]
- Font family: [system-sans | humanist-sans | scientific-serif]
- Font scale: [compact | standard | large]
- Color scheme: [midnight | graphite | deep-ocean]

Rules:
1. Preserve the 1280 x 720 design system, top bar, progress bars, named visual-style profiles, card styling, animation, navigation, and print behavior.
2. For the public example, edit `example-content.js` (`window.DECK`) and `example-notes.js` (notes keyed by slide ID). Change `theme.css` or `deck.js` only when an approved new capability is required. Do not use controlled project content as a public fixture.
3. Select from the existing layouts: title, image, cards, metrics, split, process, loop, timeline, closing, or custom.
4. Do not copy project-specific wording, names, dates, survey links, or embedded images from the reference deck.
5. Put images in `assets/` and use relative paths. Do not embed large base64 strings during drafting.
6. Keep titles to two lines, subtitles to one sentence, cards to 35-55 words, and most bullets to one line.
7. Use exact, evidence-oriented language. Distinguish observations, inferences, limitations, and decisions.
8. Add accessible alt text for every image.
9. Open the deck with `?debug=1`, review every slide, and fix all overflow warnings.
10. Run the existing Python audience builder and presentation regression from the repository root as documented in this folder's README. Open modular audience/presenter and generated audience views in a browser; verify rendering and notes as well as build success.
11. Preview visual-style changes and write them only after explicit confirmation.

Before writing slides, propose a concise slide map that links each slide to the audience decision. Follow the workshop's approval gates unless I explicitly authorize fast-track behavior.

---

## Optional authorized internal workflow

An internal environment may supply `.workshop/deck-state.json` and
`build-html-slide-workshop` Node materialization/QA tools, including
`set-visual-style.mjs` and portable presenter generation. They are not included
in this public checkout. When that workflow is explicitly authorized and
available, treat its state as authoritative and regenerate its project runtime
files rather than editing generated content. Do not install new tooling,
publish state/notes, or substitute internal project files merely to run the
public example.
