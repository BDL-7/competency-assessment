# Task #58: Simplify root tooling and public presentation layout

- Owner Agent / Path Lease: Orchestrator / Engineering Lead, exclusive from
  this contract through implementation handoff, revocation or abandonment.
- Goal / Business Reason: reduce root clutter while preserving working setup,
  migrations, public presentation behavior and publication safeguards.
- Required Context / Source of Truth: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`,
  `docs/PRODUCT.md`, `docs/DEVELOPMENT.md`, current task index, approved plan P8
  and root section 4a; affected public tooling and consumers only.
- Dependencies: reviewed #54/#55 and #56/#57. Their implementation leases ended
  at handoff; human acceptance/merge remains pending. Branch from `01e7dfd`.
- Approved Assumptions: requester approved these moves, unchanged dependency
  pins, retained WSGI, dependent issue branches with draft PRs targeting `dev`,
  and a contract-only bootstrap commit/push before PR creation.
- Review-Only Files: all paths outside the exact lease below. Protected data,
  source documents, private presentation remnants and unknown databases are
  excluded from traversal, content inspection and modification.
- Prohibited Actions: whole-directory moves; local deletion; governance export;
  package upgrades; schema revision changes; laboratory-policy changes; cloud
  calls/deployment; blanket staging; merge or history rewrite.
- Expected Outputs: relocated public source/configuration, updated callers,
  checks/tests/docs and actual before/after root table with retained-item reasons.
- Acceptance Criteria: same dependency versions and includes; working explicit
  Alembic configuration, repeat empty synthetic upgrade and existing demo setup;
  presentation source/generated modes preserved; old and new private paths
  excluded; current links resolve; WSGI remains usable.
- Validation Commands: Python 3.12 selected-task preflight; targeted verifier,
  presentation, persistence, migration and demo tests; isolated repeated Alembic
  upgrade; dependency check; public working/staged verification; whitespace;
  final-head CI and bounded browser validation.
- Security and Privacy: tests use fictional content and owned temporary files.
  Keep old protected-path rules for local remnants and add destination rules.
  No protected reads, external source processing or operational connections.
- Independent Review: review relocation paths, dependency resolution, migration
  configuration, protected-path handling and public presentation behavior.
- Definition of Done / Handoff: record exact changed paths, checks and untested
  behavior; independent review clear; final-head CI passes; remaining human
  gates explicit. Implementation handoff is not human acceptance.
- Human Approval Gates: governance transfer/replacement, exact local cleanup,
  build/deployment readiness and all existing laboratory/platform gates remain.
- Stop Conditions: overlapping writer, missing authority, unsafe source access,
  required unleased edits or a move that would overwrite another file.

## Allowed Files

Each row leases both exact source and destination; never move the parent
directory. Filenames not listed remain untouched.

| Source | Destination |
| --- | --- |
| `SECURITY.md` | `.github/SECURITY.md` |
| `CONTRIBUTING.md` | `.github/CONTRIBUTING.md` |
| `requirements.in` | `scripts/requirements/requirements.in` |
| `requirements.lock` | `scripts/requirements/requirements.lock` |
| `requirements-dev.in` | `scripts/requirements/requirements-dev.in` |
| `requirements-dev.lock` | `scripts/requirements/requirements-dev.lock` |
| `requirements-docs.txt` | `scripts/requirements/requirements-docs.txt` |
| `alembic.ini` | `migrations/alembic.ini` |
| `presentations/html-workshop/AGENT_HANDOFF.md` | `docs/presentations/html-workshop/AGENT_HANDOFF.md` |
| `presentations/html-workshop/CONTENT_SCHEMA.md` | `docs/presentations/html-workshop/CONTENT_SCHEMA.md` |
| `presentations/html-workshop/README.md` | `docs/presentations/html-workshop/README.md` |
| `presentations/html-workshop/build_single_file.py` | `docs/presentations/html-workshop/build_single_file.py` |
| `presentations/html-workshop/deck.js` | `docs/presentations/html-workshop/deck.js` |
| `presentations/html-workshop/example-content.js` | `docs/presentations/html-workshop/example-content.js` |
| `presentations/html-workshop/example-notes.js` | `docs/presentations/html-workshop/example-notes.js` |
| `presentations/html-workshop/example-presenter.html` | `docs/presentations/html-workshop/example-presenter.html` |
| `presentations/html-workshop/example.html` | `docs/presentations/html-workshop/example.html` |
| `presentations/html-workshop/theme.css` | `docs/presentations/html-workshop/theme.css` |
| `presentations/html-workshop/assets/closing-placeholder.svg` | `docs/presentations/html-workshop/assets/closing-placeholder.svg` |
| `presentations/html-workshop/assets/dashboard-placeholder.svg` | `docs/presentations/html-workshop/assets/dashboard-placeholder.svg` |
| `presentations/html-workshop/assets/hero-placeholder.svg` | `docs/presentations/html-workshop/assets/hero-placeholder.svg` |

Coupled consumers and integration records:

- `agent-tasks/58-simplify-root-layout.md`
- `agent-tasks/README.md`
- `.gitignore`
- `README.md`
- `.github/copilot-instructions.md`
- `.github/workflows/repository-checks.yml`
- `docs/README.md`
- `docs/DEVELOPMENT.md`
- `docs/BUILDATHON.md`
- `docs/DATA_CLASSIFICATION.md`
- `docs/DATA_INVENTORY.md`
- `docs/archive/README.md`
- `scripts/verify_repository.py`
- `tests/unit/test_repository_verification.py`
- `app/data/demo.py`
- `scripts/buildathon_pack.py`
- `tests/integration/test_persistence.py`
- `tests/migration/test_schema_migration.py`
- `tests/test_presentation_example.py`

## Shared interfaces

- Existing `.in`/`.lock` relative includes remain valid within the new folder.
  No App Service automatic dependency discovery is claimed; explicit cloud
  build strategy remains a readiness decision.
- CLI uses `alembic -c migrations/alembic.ini`; programmatic callers select the
  same file. `DATABASE_URL` selects the owned CI migration target, not merely
  `APP_DATABASE_URL`. Schema and logging behavior remain unchanged.
- Public builder defaults to ignored `instance/buildathon/presentation/`;
  tests/build review use explicit owned temporary outputs.
- `AGENTS.md`, `agent-tasks/` and tracked artifact provenance remain in place.
  No exact tool has yet justified a permanent root AGENTS stub.

The initial commit contains this contract only. No implementation or local
cleanup has occurred under this lease yet.
