# BR-02 Public Presentation Example

## Task contract

| Field | Value |
| --- | --- |
| Task ID | BR-02 |
| Tracking issue | #17 |
| Owner Agent | Orchestrator integration; independent QA review |
| Goal | Repair the public example's runtime contract and verify usable audience, presenter and portable audience views. |
| Business Reason | Successful HTML packaging currently hides a JavaScript startup failure in the public example. |
| Required Context | `AGENTS.md`, source authority, product, public presentation content/notes/entry pages, runtime, builder, verifier and CI. |
| Source-of-Truth Files | `presentations/html-workshop/deck.js`, public example entry pages and Python builder; repository publication policy. |
| Dependencies | Human approval recorded on 2026-11-06; issue #17 and exclusive file leases. Independent of BR-01. |
| Approved Assumptions | `window.DECK` is the established runtime contract; two public synthetic slides; existing standard-library builder and pytest only. |
| Allowed Files | `presentations/html-workshop/example-content.js`, `presentations/html-workshop/README.md`, `presentations/html-workshop/AGENT_HANDOFF.md`, `presentations/html-workshop/CONTENT_SCHEMA.md`, `.github/workflows/repository-checks.yml`, `tests/test_presentation_example.py`, this contract. |
| Review-Only Files | All other files, especially runtime JS/CSS, existing HTML/notes/builder, application/schema, verifier rules and controlled local deck content. |
| Prohibited Actions | Runtime rewrites/compatibility aliases, new packages/platforms, Node scaffolding, controlled content publication, source uploads or deployment. |
| Expected Outputs | Corrected public data global, existing-tooling regression tests and public/internal workflow distinction. |
| Acceptance Criteria | Regression detects the original global mismatch; both public entry pages render two slides with working navigation; presenter notes match slide IDs; portable audience output renders offline with no missing local script/style references. |
| Validation Commands | `python -m pytest tests/test_presentation_example.py`, full existing pytest CI suite, builder with explicit temporary output, browser inspection of all three modes, repository verifier and diff check. |
| Security and Privacy Considerations | Public synthetic content only; no controlled deck/notes reads or publication. |
| Definition of Done | Regression and exact browser output verified; independent review recorded; dev-targeted draft PR; merge approval separate. |
| Handoff Format | Exact paths, tests/build/browser results, regression proof, limitations and next owner. |
| Stop Conditions | Wider builder/runtime edits needed, unavailable tooling, sensitive inputs or overlapping leases. |
| Human Approval Gate | Requester approved this bounded fix on 2026-11-06; deletion, reference moves, workbook publication and deployment remain excluded. |
| Path Lease Owner and Expiry | Exclusive Orchestrator integration lease on the seven allowed files, expires when #17 is merged or abandoned. |

## Validation and handoff

The new regression module runs automatically in the existing full pytest CI job;
no additional dependency or duplicate test job is required.
Tests check the source/packaging contract; browser inspection independently
checks executable rendering, navigation and presenter notes.

- Changed paths: `example-content.js`, `README.md`, `AGENT_HANDOFF.md` and
  `CONTENT_SCHEMA.md` in `presentations/html-workshop/`, the new
  `tests/test_presentation_example.py`, and this contract. CI remains unchanged.
- Six targeted regression cases passed, including rejection of the original
  `DECK_CONTENT` mismatch. The final Python 3.12 full suite passed all 77 tests.
- The existing Python builder produced a dedicated temporary portable audience
  file. It embedded required sources without external script/style references
  or presenter notes.
- Modular audience, presenter and portable audience each rendered exactly two
  slides. Navigation reached `example-controls`; presenter notes matched slide
  IDs and reverse navigation returned to the cover. Debug overflow count was
  zero in all three views; no captured page errors occurred.
- No runtime/builder rewrite, compatibility alias, package installation
  requirement, controlled-content copy or deployment was introduced.
- Independent read-only review of the complete 13-path change reported no
  significant issues. The configured custom reviewer was unavailable; the
  standard independent reviewer completed the review without rerunning the
  clean Python 3.12 tests or browser checks.
- Final staged repository verification passed for all 133 tracked files;
  staged whitespace checks passed.
  Next owner: requester reviewing the dev-targeted draft PR.
