# Task #60: Shared SQL persistence mechanics

- Owner / Lease: Orchestrator integration, exclusive from contract creation
  through implementation handoff, revocation or abandonment.
- Goal / Business Reason: persist schema-compatible shared workflow effects
  atomically instead of relying exclusively on in-memory support ports.
- Required Context: `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`,
  `docs/DEVELOPMENT.md`, current task index, public service ports, SQL mappings,
  existing scoped pilot query and persistence tests.
- Source of Truth: existing approved public interfaces, physical schema and
  authorization predicates. No controlled or operational inputs.
- Dependencies: reviewed #54/#56/#58, branch from `fb9a2d4`. Their implementation
  leases ended at handoff; draft PRs remain unmerged.
- Approved Assumptions: requester selected "Continue shared SQL persistence
  mechanics without profile-specific policy/schema changes." Dependent issue
  branches, contract-only bootstrap and draft PRs targeting `dev` are approved.
- Allowed Files:
  - `agent-tasks/60-shared-sql-persistence.md`
  - `agent-tasks/README.md`
  - `app/data/repositories.py`
  - `app/data/unit_of_work.py`
  - `app/data/__init__.py`
  - `app/data/pilot.py`
  - `migrations/env.py`
  - `tests/integration/test_persistence.py`
  - `docs/ARCHITECTURE.md`
  - `docs/WORKFLOW.md`
- Review-Only: all other paths. Root data, protected sources, private archives
  and unknown databases remain excluded from traversal or access.
- Prohibited: schema/revision changes; invented identity, role-approval,
  configuration or signature values; service-principal impersonation as users;
  workflow/profile/policy changes; UI mutation wiring; live delivery/cloud
  calls; private cleanup; merge or history rewrite.
- Expected Outputs: SQL implementations of existing idempotency, audit,
  notification and scoped-query ports, sharing one explicitly committed
  rollback-by-default support transaction. Reuse the existing pilot SQL scope
  predicate unchanged. Do not pretend this is a complete aggregate adapter.
- Acceptance: supported records round-trip without lost result/effect fields;
  user audit actors remain attributable; unsupported mappings fail explicitly;
  duplicate request/event/attempt constraints prevent duplicate persisted
  effects; failed transactions roll back all effects; scopes filter in SQL;
  sessions close; existing pilot behavior remains unchanged.
- Validation: Python 3.12 selected-task preflight; focused persistence and pilot
  tests; temporary migrated SQLite targets; independent competing-session
  uniqueness/rollback checks; safe working/staged checks; existing CI.
- Security / Privacy: synthetic records only. No source uploads or operational
  connections. Logs report error categories, not SQL parameters or record data.
- Independent Review: transaction boundaries, lossless mappings, SQL scoping,
  unsupported actor handling and preservation of existing behavior.
- Definition of Done / Handoff: exact paths, validation, independent review,
  final-head CI and remaining mapping gates recorded; not human approval.
- Stop: overlapping lease, required schema/policy delta, sensitive access,
  ambiguous necessary mapping or required unleased change.
- Human Gates: CLIA applicability/rules, participant/signature semantics,
  live identity/platform integrations, deployment and source approvals remain.

## Mapping boundary discovered before implementation

The current full `AggregateRepository` cannot be honestly implemented without
additional decisions: service principal/capability tables are absent;
`UserRecord` omits identity-provider subject; `RoleScopeRecord` omits approver;
`SignatureRecord` omits authentication context; configuration/version mapping
is not one-to-one. Do not manufacture values or add schema under this task.

This slice implements the four support ports only. Its support unit of work is
not a substitute for the full `WorkflowService` unit-of-work protocol and is not
injected into that service or the UI. Aggregate writes, optimistic record-update
concurrency and full SQL workflow journeys remain subsequent explicit work.
Concurrent support-effect uniqueness is exercised using existing constraints.

For the existing audit schema, only `actor_kind="user"` is representable.
Reject other kinds rather than silently discarding kind or impersonating a user.
Persist fresh idempotency results only; `replayed=True` is a response property,
not stored canonical command state. Existing notification rows must contain
the context fields required by the non-optional service record; missing values
raise a mapping error rather than being invented.

Bootstrap commit contains this contract only.

Requester approved extending this exact lease to `migrations/env.py` after a
targeted check demonstrated that Alembic logging configuration disabled the
application's transaction-failure logger. Preserve existing loggers without
changing schema, migration revisions or workflow policy.

New notification events retain the existing synthetic fixture's
`not_delivered_prototype` status. Timestamp writes require an explicit timezone
and normalize to UTC; SQLite's naive UTC reads are restored to aware values.

## Implementation handoff

The ten Allowed Files above are the exact changed paths. Implemented four
schema-compatible SQL support ports and `SqlSupportUnitOfWork`, not a full
aggregate adapter. The shared scope predicate is unchanged; current-version
number reads additionally constrain ownership in SQL without loading version
content. No service/UI mutation wiring or schema revision changed.

- Python 3.12.10 selected-task preflight passed.
- Full suite: 148 passed before the final scoped-read refinement and additional
  event-collision parameter. The final affected persistence/pilot/migration
  selection then passed all 32 cases, including the refined query.
- Tests exercise canonical success/rejection/failure results, UTC round trips,
  explicit commit, default/explicit/exception rollback, closed transaction use,
  duplicate event/attempt rollback, competing-session idempotency, attributable
  user audits, unsupported mapping rejection and non-disclosing error logs.
- All 25 local links/anchors across four changed public documents passed.
  Dependency integrity and safe working/staged verification (165 files) passed.
- Independent review of the implementation and both final bounded deltas found
  no material defects; it was not human approval.
- Final staged-content and final-head CI evidence is recorded in draft PR #61,
  targeting `dev`; no merge is authorized.

Only synthetic SQLite behavior was exercised. Full SQL aggregate writes,
optimistic assessment-update concurrency, complete workflow finalization,
service-principal storage, live Azure SQL and new CLIA/non-CLIA UI journeys
remain unimplemented/unverified. Missing mappings are listed above; the next
owner must resolve them explicitly under a new lease, without inventing
authentication, approval or laboratory metadata.
