# S0-07 Local Read-Only Pilot UI

## Contract

- Issue: #15; owner: Orchestrator; authorized by the requester through the
  approved local UI plan on 2026-11-02.
- Baseline: merged S0-04A implementation and issue #13 planning requirements.
- Scope: opt-in local SQLite demo using the existing synthetic scenario,
  scoped read-only dashboard, queue, assessment detail/history, and two
  explicitly synthetic mock chat surfaces.
- Exclusive writable lease: this contract; `app/__init__.py`, `app/config.py`,
  `app/web/**`, `app/templates/**`, `app/static/**`, `app/services/**`,
  `app/data/**`, `app/ai/**`, directly related `tests/**`, `README.md`, and
  `.env.example`. The lease expires when #15 is merged or abandoned.
- Shared interface: services own read DTOs and scope resolution; Data implements
  SQL reads and minimized access auditing; routes never access ORM objects.
- No schema changes, new packages, workflow mutation forms, expanded population,
  CLIA implementation, external AI/email, resource provisioning, or deployment.
- Mock answers are UI demonstrations, not approval of controlled sources under
  A08. No manual procedures or personal record answers are generated.
- Visual direction: requester selected Soft Studio on 2026-11-03: lavender
  navigation rail, ivory canvas, peach attention surface, sage accents,
  asymmetric overview, assessment dossier, version timeline and conversational
  mock guides. Reopened #15 continues the same pending UI work; no second task
  holds these paths. Preserve actual counts and existing safe behavior.
- Superseding visual selection: requester rejected Soft Studio's appearance
  and selected **Lab Atlas - scientific, precise, professional** on 2026-11-03.
  Continue #15 and draft PR #16 with a structured scope strip/register,
  blue-gray shell, blue/sage accents, restrained scientific grid motifs and
  precise record typography. This changes presentation only, not authority,
  schema, data, functionality or deployment scope.
- Subsequent requester refinement removes the Lab Atlas title, uses one
  system-font family throughout and adds coordinated lavender, peach, sage
  and powder-blue component/page backgrounds. Scientific composition and all
  read-only boundaries remain unchanged.
- Pastel refinement validation: 12 web tests and all six responsive/browser
  journeys passed, including 200% text and 57 keyboard-focus controls. Live
  preview verified concept-name removal and one computed system-font family
  for headings, labels, record IDs, branding and buttons. Sampled text contrast
  across the revised pastel surfaces is at least 4.69:1.

## Acceptance

1. Explicit setup creates a dedicated synthetic SQLite demo; HTTP requests never
   create or seed tables. Unknown populated targets and production demo mode fail.
2. Authorized users see only scoped records/counts/detail/history. Inactive and
   out-of-scope identities cannot see record content. Platform diagnostic views
   require purpose/reference, are minimized, and audited.
3. Dashboard, queue filtering/pagination, detail, and two issued versions are
   navigable with keyboard and at narrow widths.
4. The visible reference date and all data/citations are clearly synthetic.
   The pending signature is never presented as a completed signature.
5. Two mock assistant forms use CSRF and bounded input, escape output, and make
   no external calls or business mutations.
6. Existing home/health behavior remains available outside opt-in demo mode.
7. Tests, browser checks, repository verification, and diff checks are recorded.
   Required independent application/data/QA/privacy/accessibility review results
   or unresolved blockers must be explicit before merge readiness.

## Validation and handoff

Run targeted UI tests, the full pytest suite after factory changes, compilation,
repository verifier, and diff checks. Validate local browser navigation,
responsive layout, keyboard/focus, labels and chat errors. Publish a PR to `dev`;
merge only with explicit requester approval; do not deploy. Exact evidence and limitations are recorded below after
implementation.

### Recorded evidence

- Full regression suite: `python -m pytest -q`, 71 passed on local Python
  3.14.2. Final template/control changes: 12 targeted web tests passed.
  CI validates the required Python 3.12 environment; local results do not
  substitute for that check.
- Compilation and `git diff --check` passed. Repository verifier passed
  against all 128 tracked files after staging the complete inventory.
- Loopback-only Edge inspection covered overview, queue, detail, history and
  both guides at desktop and 360/390/768/1024px widths. All six screens passed
  200% root-text checks without page-wide overflow. The table retains local
  horizontal scrolling. An enlarged-text guide-grid overflow was corrected.
- Keyboard skip-link activation, main-content focus, and visible outlines on
  57 keyboard controls passed. Reduced-motion transitions are disabled.
- Filtering/clear-filter recovery, detail/history links, real sample-question
  POSTs, citations, SME escalation, blank-input validation and a 500-character
  narrow-screen question passed. No failed asset requests, unexpected console
  errors, page exceptions or external requests occurred on valid journeys.
  Deliberate invalid requests retained their expected HTTP error statuses.
- Separate browser checks passed for an outsider's empty queue and
  non-disclosing 404, Platform Admin support-context entry and minimized detail,
  and an uninitialized target's 503 without database creation.
- Measured 16 representative text/surface pairs: minimum 4.75:1. Control
  boundaries across five surfaces: minimum 3.69:1; focus: minimum 5.86:1.
  These checks and semantic review target WCAG 2.2 AA, not certified conformance.
- Before screenshots and six desktop/six mobile after screenshots remain in
  the session workspace, not public Git. The browser scripts also remain there.
  Temporary validation servers were stopped; no deployment was performed.
- Independent pre-redesign application/data review reported no significant
  issues. A separate bounded independent Soft Studio template/CSS/interface
  review reported no significant issues, but did not rerun browser/tests or
  provide specialist conformance sign-off. The configured custom reviewer was
  unavailable. Application/data/QA/privacy/accessibility owner sign-off was
  originally a draft-PR merge gate; the requester explicitly deferred it for
  local-only integration as recorded below. This is not specialist sign-off.

### Local-only integration approval

On 2026-11-03, the requester approved the current UI and explicitly deferred
specialist sign-off, authorizing PR #16 to merge into `dev` for this local-only
pilot. All CI checks passed for the reviewed feature head. Specialist
application/data/QA/privacy/accessibility review remains outstanding before
any operational-use or deployment decision. This approval does not authorize
deployment, controlled-source use, production identity/data, or broader scope.

### Exact changed-file inventory

This includes the preserved pending UI implementation and its redesign:

- Configuration/composition: [`.env.example`](../../../.env.example),
  [`app/__init__.py`](../../../app/__init__.py), [`app/config.py`](../../../app/config.py).
- Read services/data/setup: [`app/services/pilot.py`](../../../app/services/pilot.py),
  [`app/services/workflow.py`](../../../app/services/workflow.py),
  [`app/data/pilot.py`](../../../app/data/pilot.py),
  [`app/data/demo.py`](../../../app/data/demo.py).
- Routes/mock answers: [`app/web/routes.py`](../../../app/web/routes.py),
  [`app/ai/mock.py`](../../../app/ai/mock.py).
- Visual system/shell: [`app/static/styles.css`](../../../app/static/styles.css),
  [`app/templates/base.html`](../../../app/templates/base.html),
  [`app/templates/pilot/components.html`](../../../app/templates/pilot/components.html).
- Screens: [`dashboard.html`](../../../app/templates/pilot/dashboard.html),
  [`work.html`](../../../app/templates/pilot/work.html),
  [`detail.html`](../../../app/templates/pilot/detail.html),
  [`history.html`](../../../app/templates/pilot/history.html),
  [`assistant.html`](../../../app/templates/pilot/assistant.html),
  [`error.html`](../../../app/templates/pilot/error.html).
- Tests/documentation: [`tests/web/test_pilot.py`](../../../tests/web/test_pilot.py),
  [`README.md`](../../../README.md), this task contract.

### Remaining limitations

One record, two issued versions and seven existing synthetic identities remain
the entire scenario. No multi-lab population, CLIA workflow, approved assistant
corpus, equipment manual, live AI, record mutation or deployment is added.
Conversation responses are deterministic and not retained. Screen-reader and
specialist accessibility review remain outstanding. This slice is for local
review, not operational use or laboratory-policy approval.

### Lab Atlas revision evidence

- Supersedes Soft Studio presentation; its screenshots/evidence above remain
  historical. Only templates, CSS, the shell regression test, README and this
  contract changed. No route, service, database or role changes.
- `python -m pytest tests/web/test_pilot.py -q`: 12 passed. Browser rechecked
  all six screens at 360/390/768/1024px and 200% root text, 57 focus controls,
  sample submissions, long input, filters and error recovery. No page errors,
  unexpected console/asset errors or external requests on valid journeys.
- Outsider non-disclosure, minimized diagnostic views and uninitialized
  503/no-database-creation checks passed again. Minimum sampled text contrast:
  5.14:1; control boundaries: 3.41:1; focus: 6.05:1.
- Lab Atlas desktop/mobile screenshots remain in the session workspace;
  before evidence is preserved. Independent bounded revision review found no
  significant issues; it did not independently rerun the passing tests.
  Specialist review remains outstanding; requester visual acceptance and
  local-only integration approval are recorded above.
