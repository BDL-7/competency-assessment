# S0-04A Synthetic Application Workflow Vertical Slice

## Task contract

| Field | Value |
| --- | --- |
| Task ID | S0-04A |
| Tracking issue | GitHub issue #11 |
| Owner | Orchestrator coordinating sequential Data, Domain/Services, Flask, and QA work |
| Goal | Implement one secure, synthetic configure-through-finalization application path that realizes the approved S0-01 scenario and S0-02 interfaces. |
| Business reason | Prove the application workflow, authorization, integrity, audit, notification, renewal, and reporting boundaries before external integrations or production policy are introduced. |
| Dependencies | PR #10 merged to `dev` at `73ddf44`; S0-01 prototype assumptions A01-A07 and A09; approved S0-02 contract. |
| Source of truth | `docs/PRODUCT.md`, `docs/WORKFLOW.md`, `docs/AUTHORIZATION.md`, `docs/DOMAIN_MODEL.md`, `docs/ARCHITECTURE.md`, `docs/TESTING.md`, S0-01, and S0-02. |
| Approved physical design | Portable SQLAlchemy 2 mappings and Alembic migration; SQLite only for local synthetic development/tests; integer optimistic versions; UTC timestamps; opaque string identifiers; immutable issued-version snapshot rows; normalized signatures, notification events/attempts, documents, renewals, audits, and idempotency records. |
| Approved prototype rules | Only S0-01 A01-A07 and A09. The 12-calendar-month arithmetic, scenario-required fields, returned-follow-up branch, non-delivering notifications, mock identities, and synthetic artifact hash are not production policy. |
| Data lease | `app/data/**`, `migrations/**`, `alembic.ini`, `tests/migration/**`, and `tests/integration/test_persistence.py` while the Data layer is active. |
| Domain/service lease | `app/domain/**`, `app/services/**`, `app/audit/**`, `app/documents/**`, `app/notifications/**`, `app/reporting/**`, `tests/unit/**`, `tests/integration/test_workflow_service.py`, `tests/authorization/test_service_authorization.py`, and `tests/end_to_end/test_synthetic_workflow.py` after the Data lease releases its shared interfaces. |
| Flask lease | `app/web/**`, `app/auth/**`, `app/templates/**`, `app/static/**`, `app/__init__.py`, `tests/web/**`, and `tests/authorization/test_web_authorization.py` after service interfaces stabilize. |
| Orchestrator lease | This contract, `README.md`, `.env.example`, `app/config.py`, dependency manifests/locks, `.github/workflows/repository-checks.yml`, and integration-only changes. |
| QA lease | All implementation test leases release before QA receives `tests/**`; QA may then add or revise tests but treats implementation paths as review-only. |
| Security/privacy | Synthetic identifiers and content only. Identity, roles, scopes, states, signers, versions, and timestamps are resolved or validated server-side. Denials disclose no protected record content. |
| Human approval | The Project Requester explicitly authorized S0-04A implementation on 2026-09-12. This authorizes only the approved synthetic prototype behavior and physical implementation choices recorded here. |
| Lease expiry | All leases expire when issue #11 is merged or abandoned. Work proceeds sequentially so no writable path has concurrent owners. |

## Required outcomes

1. Configure the approved synthetic team, participants, roles, process grouping,
   and explicit participant relationships without deriving participant authority
   from administrative membership.
2. Schedule and release one assignment with the approved synthetic basis date,
   12-calendar-month interval snapshot, deterministic due date, and derived
   overdue condition.
3. Begin, save, and submit an assessment. The first incomplete submission must,
   in one transaction, issue immutable version 1, record `Submitted -> Returned`,
   create a correction draft, and block signature. The Assessor documents the
   missing follow-up and resubmits immutable version 2. No general reviewer
   return, post-signature correction, or other D05 behavior is enabled.
4. Require the approved scenario fields and a follow-up description for the
   unsuccessful synthetic element without calculating competency, pass/fail,
   or remediation completion.
5. Bind Testing Personnel and Technical Supervisor signatures to the same exact
   immutable version and enforce their order and explicit record relationships.
6. Finalize through the authorized Technical Supervisor command as one atomic
   outcome: create the Technical Supervisor signature, lock the version, retain
   synthetic artifact metadata/hash, schedule renewal, create the completed
   notification event, and append audit evidence.
7. Record minimal logical notification events separately from non-delivering
   attempts; retries must not duplicate the logical event or mutate workflow.
8. Apply role and record scope before returning own-work, team-work, assigned
   assessment, final-review, administrative-status, or diagnostic-read results.
9. Enforce optimistic concurrency, request idempotency, conflict detection,
   append-only audit, exact-version immutability, and finalized locking.
10. Provide server-rendered, keyboard-operable workflow pages and protected
    state-changing forms using post/redirect/get, CSRF validation, programmatic
    labels/errors/status, semantic tables, and visible focus.

## Approved engineering controls

### S0-04A-INT1 application/persistence integration

This cross-owned integration correction is serialized. Services own
framework-neutral record/command DTOs plus `UnitOfWork`, aggregate repository,
idempotency, audit-append, notification, and scoped-query protocols. They import
neither SQLAlchemy nor `app.data`. Data owns the SQLAlchemy implementations and
maps between service-owned records and ORM rows. The Orchestrator wires the Data
unit-of-work factory into the Flask application only after both leases release.
Routes import only `app.services` and `app.domain`; they never import ORM models,
sessions, repositories, or SQLAlchemy.

### CSRF and session security

Workflow forms use a standard-library token stored in Flask's signed session.
Generate at least 32 random bytes with `secrets`, compare submitted and session
tokens with `hmac.compare_digest`, reject missing/invalid tokens with HTTP 400
before service invocation, and rotate the token after every successful mutation.
The application requires a nonblank secret whenever workflow forms are enabled.
Session cookies are HttpOnly and SameSite=Lax; production cookies are Secure.
A valid CSRF token is not authorization. Actor, roles, scope, signer, current
state, and server time remain server-resolved. A browser may submit only the
expected concurrency version, which the service compares to authoritative state.

### Synthetic identities

Each app instance resolves one fixed identity from trusted server configuration.
Multi-actor tests use separate configured app instances sharing the same test
database. There is no browser identity/role switcher and headers, cookies, query
parameters, and form fields cannot select an identity, role, scope, or signer.

### Minimum relational integrity

- Required participant, assignment, assessment, version, signature, event,
  document, renewal, audit, and idempotency relationships use non-null foreign
  keys. SQLite foreign-key enforcement is enabled in every test connection.
- Synthetic TestSystem configuration is retained separately and connected to
  ProcessGrouping through an explicit restricted, unique association; no
  governed catalog value or operational seed is included.
- Mutable AssessmentDraftElement rows retain element result, evidence, gap, and
  follow-up work under a non-null draft foreign key and unique draft/element
  identity. Submission copies them into immutable AssessmentElement rows;
  correction drafts copy forward prior element work without editing the issued
  version.
- One signature per assessment version and signature role; signer and exact
  version are retained. One document kind and one renewal effect per finalized
  version are allowed.
- Logical notification identity is unique across record, trigger, recipient,
  template version, and occurrence. Attempt request identity and per-event
  ordinal are unique.
- Idempotency identity is unique across command, target, actor, and request ID
  and stores a canonical request fingerprint plus the original safe result.
- Issued-version snapshot content is non-null and has no update/delete repository
  operation. Audit observations are append-only and have no normal update/delete
  operation. Parent deletion is restricted rather than cascaded through retained
  workflow evidence.
- Assessment navigation IDs are convenience pointers only. Services validate
  that a referenced draft/version has the same authoritative assessment FK in
  the transaction. S0-04A leaves predecessor/successor and supersession links
  null because renewal does not create a successor assignment and amendment is
  excluded.
- Automated/scheduled actions use an explicitly configured synthetic service
  ApplicationUser so audit actor identity is never null or fabricated from an
  Employee. The service identity has a dedicated notification-only capability;
  it is never modeled as Platform Admin or another business role. Injected clock
  values are normalized to UTC before persistence.
- Scoped query ports receive the resolved actor and exact active team, record,
  configuration, or diagnostic scope so the Data adapter filters in SQL before
  materializing rows or counts. Services never request an unscoped bulk result.
- Issued-version snapshot DTOs are immutable. Persistence exposes only a narrow
  finalize-state operation for `locked` and `finalized_at`; no general issued
  content or participant replacement operation exists.
- Migration tests cover clean upgrade, repeated upgrade-to-head, foreign keys,
  uniqueness, and absence of operational/source-data seeding. Downgrade is not
  an application operation and remains excluded pending an approved recovery
  policy.

### Idempotency ordering and failure behavior

Idempotency lookup occurs before optimistic concurrency evaluation. Same key and
same fingerprint returns the original safe result even after aggregate state has
advanced. Same key with a different fingerprint returns
`IDEMPOTENCY_CONFLICT`. An injected persistence/finalization failure returns a
safe `Failed` result with `DEPENDENCY_UNAVAILABLE`, claims no partial success,
and stores no successful idempotency outcome. Retrying after rollback may run
normally with the same request identity.

## Stable result boundary

Commands return `Succeeded`, `Rejected`, or `Failed` with safe fields from the
S0-02 contract. Required rejection codes include `INVALID_INPUT`,
`UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND_OR_NOT_VISIBLE`, `STALE_VERSION`,
`INVALID_STATE`, `COMPLETENESS_FAILED`, `FOLLOWUP_REQUIRED`,
`SIGNATURE_SEQUENCE_INVALID`, `SIGNATURE_VERSION_MISMATCH`,
`IDEMPOTENCY_CONFLICT`, and `POLICY_PENDING`. Browser input never supplies an
authoritative role, scope, signer, lifecycle state, or server time.

## Acceptance criteria

1. A clean database upgrades to the S0-04A revision and supports the complete
   synthetic workflow without operational or controlled data.
2. The end-to-end scenario produces due date `2027-02-15`, a returned first
   submitted version, a corrected second immutable version, ordered signatures,
   finalization, and renewal date `2028-02-20`.
3. Stale versions, unauthorized actors, wrong signers, wrong signature order,
   post-signature edits, post-finalization edits, and conflicting idempotency
   reuse create no business mutation and return stable safe failures.
4. Same-input retries return the original safe outcome and create no duplicate
   signature, notification, audit effect, artifact, renewal, or finalization.
5. Injected finalization failure rolls back the Technical Supervisor signature,
   state/version changes, lock, artifact, renewal, completed event, success audit,
   and successful idempotency result as one transaction. It returns a minimized
   `DEPENDENCY_UNAVAILABLE` failure and the same request may be retried.
6. Notification payloads contain only recipient reference, template, stable
   record reference, trigger/occurrence, and minimum status/date context; results
   and narrative content are rejected.
   Required logical triggers are upcoming-due, due, overdue, submitted,
   Testing-Personnel-signature-required, Technical-Supervisor-signature-required,
   and completed. Upcoming-due is invoked by a synthetic occurrence; no
   production lead-time cadence is selected. Attempts use unique request IDs and
   ordinals, and a failed/non-delivering attempt cannot mutate workflow.
7. Role-scoped queries and web pages do not reveal out-of-scope rows or counts;
   Platform Admin diagnostic reads require and audit a support purpose/reference.
   Employee is own-only; Team Lead is team-only and cannot author unless also
   assigned Assessor; Assessor is assigned-only and cannot sign; Technical
   Supervisor is assigned-review-only and cannot author; SQUAD Admin configures
   and reports but cannot assess/sign; Platform Admin cannot mutate; outsiders
   receive indistinguishable not-found/not-visible failures.
8. Issued/finalized versions and audit observations have no normal update/delete
   application interface.
9. Unit, migration, integration, authorization, web, and end-to-end tests pass
   on Python 3.12; repository verification and diff checks pass.
10. README documents database upgrade, synthetic-only setup, run/test commands,
    implemented behavior, exclusions, and the absence of production readiness.
11. Audit evidence covers configuration, assignment, successful and denied
    actions/access, submission/return/follow-up, exact-version signatures,
    finalization/lock, artifact, logical events and attempts, renewal, reports,
    and Platform Admin diagnostic purpose. It retains actor/action/entity/time,
    outcome, request/correlation IDs, and only a minimized summary.
12. Overdue is false before and on the due date, true after the due date only
    while active, and never replaces lifecycle state. It is false after
    finalization.
13. Static semantic checks plus browser-based manual keyboard, focus, error
    association/status announcement, table semantics, non-color-only status,
    and contrast review provide the S0-01 A09 prototype accessibility evidence.
14. Controlled export, cancellation, signed-version return, amendment,
    remediation completion, external delivery/Blob retrieval, assistant, and
    production routes/commands are absent or return `POLICY_PENDING` where the
    S0-02 contract requires a typed outcome.
15. Artifact evidence is deterministic SHA-256 over synthetic metadata only;
    no bytes, controlled content, Blob access, or retrieval route exists.

## Stop conditions and exclusions

Stop if implementation requires a production rule, unapproved field/state/role,
controlled wording or data, a new package/platform, real Entra mapping, external
email delivery, Blob bytes/retrieval, operational migration, production database
driver, Azure resource, or cross-owned interface change not recorded here.

Do not implement cancellation, post-signature return/correction, amendment or
repair, remediation-completion approval, production cadence/retention/access,
Center/quality viewer, Power BI, CLIA behavior, assistant behavior, production
deployment, or production data. S0-04B remains blocked by S0-01 A08.

## Validation plan

The repository workflow must add a Python 3.12 application job that installs
`requirements-dev.lock`, upgrades an empty temporary SQLite database to Alembic
head, runs the entire pytest suite, and runs the repository verifier. Local
evidence uses the managed Python 3.12 runtime and an ignored clean environment.

```text
python -m alembic upgrade head
python -m pytest
python -m compileall -q app tests migrations wsgi.py
python -m pip check
python scripts/verify_repository.py
git diff --check
```

Independent Data, Flask/application, QA, security/privacy/records, and
accessibility reviews are required before the issue #11 pull request is ready
for human merge approval.

## Approval record

| Review | Status | Evidence |
| --- | --- | --- |
| Project authorization | Approved | Requester explicitly instructed implementation of S0-04A on 2026-09-12. |
| Prototype decision boundary | Approved | Uses only S0-01 A01-A07 and A09; all D01-D12 remain unresolved for production. |
| Physical implementation boundary | Approved for synthetic prototype | Portable SQLAlchemy/Alembic mapping with local/test SQLite; no production driver or deployment claim. |
| Data/persistence review | Pending | Required after persistence layer. |
| Flask/application review | Pending | Required after service and web layers. |
| Independent QA/security/accessibility review | Pending | Required after implementation. |
| Orchestrator integration | Pending | Required after final validation and exact-file review. |
