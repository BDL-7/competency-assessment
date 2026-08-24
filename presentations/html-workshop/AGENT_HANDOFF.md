# Agent Handoff Prompt

Use the following prompt with the modular workshop folder.

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
2. Edit `.workshop/deck-state.json` for content, notes, and transitions; regenerate runtime files from state. Change `theme.css` or `deck.js` only when a genuinely new capability is required.
3. Select from the existing layouts: title, image, cards, metrics, split, process, loop, timeline, closing, or custom.
4. Do not copy project-specific wording, names, dates, survey links, or embedded images from the reference deck.
5. Put images in `assets/` and use relative paths. Do not embed large base64 strings during drafting.
6. Keep titles to two lines, subtitles to one sentence, cards to 35-55 words, and most bullets to one line.
7. Use exact, evidence-oriented language. Distinguish observations, inferences, limitations, and decisions.
8. Add accessible alt text for every image.
9. Open the deck with `?debug=1`, review every slide, and fix all overflow warnings.
10. Use the `build-html-slide-workshop` Node scripts to validate state, materialize runtime files, build both portable modes, and record QA receipts.
11. Preview visual-style changes with `set-visual-style.mjs`; write them only after explicit confirmation.

Before writing slides, propose a concise slide map that links each slide to the audience decision. Follow the workshop's approval gates unless I explicitly authorize fast-track behavior.

---
