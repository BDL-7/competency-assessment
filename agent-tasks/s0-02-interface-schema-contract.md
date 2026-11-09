# S0-02 Domain Interfaces and Conceptual Schema Contract

## 1. Task contract

| Field | Value |
| --- | --- |
| Task ID | S0-02 |
| Tracking issue | GitHub issue #7 |
| Owner Agent | Orchestrator / Engineering Lead, with Data and Flask review |
| Goal | Agree the shared domain, service, persistence, authorization, audit, notification, reporting, document, and assistant interfaces required by the approved S0-01 scenario. |
| Business Reason | Prevent application, data, and assistant work from inventing incompatible rules or bypassing controls when implementation begins. |
| Required Context | Merged S0-01 scenario and the canonical product, architecture, workflow, authorization, domain-model, AI-boundary, testing, terminology, and migration-boundary documents. |
| Dependencies | S0-01 merged through PR #6 at `c9cf1744e50ceed02e315e73eebbbad3b9d2cbe9`. |
| Approved Assumptions | S0-01 A01-A07 and A09 for the synthetic prototype only. A08 remains unapproved. |
| Allowed Files | `agent-tasks/s0-02-interface-schema-contract.md`; `README.md` for workflow/status navigation. |
| Review-Only Files | All canonical documents, S0-01, controlled sources, and operational workbooks. |
| Prohibited Actions | Code, models, migrations, packages, physical tables, routes, UI design, Azure resources, production data, controlled wording, source approval, or new platform decisions. |
| Expected Outputs | Module interfaces, conceptual fields and relationships, command/query contracts, transactions, authorization checks, idempotency identities, errors, assistant boundary, traceability, and unresolved decisions. |
| Validation Commands | `python scripts/verify_repository.py`; `git diff --check`; `git status --short`. |
| Security and Privacy | Public-safe concepts and synthetic identifiers only; no workforce records, secrets, source text, or governed catalog values. |
| Human Approval Gate | The Project Requester authorized implementation of the next approved task on 2026-09-08. Any change to controlled rules, authorization, renewal, signature meaning, approved AI sources, administration, amendment, deployment, or disposition still requires separate approval. |
| Path Lease | Orchestrator owns the two allowed files until issue #7 is merged or abandoned. |

S0-02 is an interface agreement, not an executable schema or authorization to begin S0-03.

## 2. Architectural ownership

Dependency direction remains `web -> services -> domain`. Infrastructure implements ports owned by services/domain; it does not call around them.

| Boundary | Owns | Must not own |
| --- | --- | --- |
| `web` | Server-rendered request mapping, form input, response presentation | Workflow rules, direct persistence, role inference |
| `auth` | Identity resolution, effective roles/scopes, authorization decisions | UI-only enforcement, implicit participant assignment |
| `domain` | States, transitions, invariants, completeness decisions, immutable-version rules | SQL, Flask requests, email, Blob, model calls |
| `services` | Use-case orchestration, transaction coordination, ports, result contracts | Infrastructure-specific implementation |
| `data` | Repository and unit-of-work implementations | Policy decisions or bypass paths |
| `documents` | Authorized metadata/retrieval port | Public blobs or uncontrolled content |
| `notifications` | Logical events, delivery attempts, safe adapter port | Assessment decisions or official delivery in the prototype |
| `reporting` | Authorization-scoped projections/exports | Unscoped record access |
| `audit` | Append-only attributable observations | Mutable business history |
| `ai` | Separate approved-source and answer/escalation ports | Application-record mutation or consequential tools |

Shared interfaces are framework-neutral for S0-02. S0-03 may map them to the approved Flask/SQLAlchemy/Azure baseline without changing their behavior.

### 2.1 Application-owned port catalog

| Port | Capability | Boundary |
| --- | --- | --- |
| IdentityResolver | Read-only | Resolve authenticated subject to active ApplicationUser; never infer business roles from UI/session claims alone |
| AuthorizationDecision | Read-only decision | Evaluate effective roles, explicit participant relationships, action, scope, state, and version; grants no persistence capability |
| UnitOfWork | Transaction coordination | Commit or roll back one application-visible mutation and its internal effects |
| AggregateRepository | Read/write only inside UnitOfWork | Load/save Assignment, Assessment, draft, and immutable-version aggregates after authorization; never used by routes/adapters directly |
| ScopedQuery | Read-only | Apply actor scope before returning rows, counts, projections, or document references |
| Clock | Read-only | Supply deterministic current time |
| IdentityGenerator | Value generation only | Supply opaque internal identities; grants no business authority |
| DocumentMetadata | Read/write only inside approved service transaction | Record authorized private-object metadata/hash; does not expose bytes or grant access |
| AuthorizedDocumentRetrieval | Read-only | Return a private, short-lived retrieval result only after per-request scope checks |
| NotificationEvent | Write only inside UnitOfWork | Append one logical minimal-content event |
| NotificationAttempt | Append-only adapter result | Record delivery attempt against an existing event; cannot mutate assessment state |
| AuditAppend | Append-only | Record minimized attributable outcome; exposes no normal update/delete capability |
| ApprovedSourceLookup | Read-only | Return only active, approved, versioned, assistant-enabled sources accessible to the actor |
| AssistantModel | Read-only generation | Invoke the approved model configuration with bounded approved context; no application credentials |
| AssistantOutcomeLog | Append-only minimized metadata | Record versions/outcome/timing without unnecessary question/source text |

## 3. Common interface primitives

Every command carries authenticated subject context, an opaque `request_id`, `correlation_id`, expected target identity, and `expected_version` when a mutable record is targeted. Effective roles and scopes are resolved server-side; the browser never supplies authoritative role, scope, signer, state, or version values. Server time and generated identities come from injected ports so synthetic tests are deterministic.

Every command returns one of:

- `Succeeded`: result reference, resulting state/version, correlation identifier, and replay indicator;
- `Rejected`: stable reason code, safe actionable message, unchanged state/version when visible, and correlation identifier;
- `Failed`: safe dependency/transaction failure with no claim of partial business success.

Required reason codes are `INVALID_INPUT`, `UNAUTHENTICATED`, `FORBIDDEN`, `NOT_FOUND_OR_NOT_VISIBLE`, `STALE_VERSION`, `INVALID_STATE`, `COMPLETENESS_FAILED`, `FOLLOWUP_REQUIRED`, `SIGNATURE_SEQUENCE_INVALID`, `SIGNATURE_VERSION_MISMATCH`, `IDEMPOTENCY_CONFLICT`, `POLICY_PENDING`, `SOURCE_NOT_APPROVED`, `SOURCE_NOT_ACCESSIBLE`, `COVERAGE_INSUFFICIENT`, `CONFLICTING_EVIDENCE`, and `DEPENDENCY_UNAVAILABLE`. HTTP mapping and presentation belong to S0-03. Denials must not reveal an out-of-scope record's existence.

Queries carry actor context, requested scope, filters, pagination intent, and correlation identifier. Scope is applied before records or counts are returned.

## 4. Conceptual information contract

These are logical fields, not physical columns or types.

| Concept | Required logical information and relationships |
| --- | --- |
| Team | Identity, display label, active status, approved configuration ownership |
| Employee | Identity, team, active status, role/job context, optional source lineage; separate from login |
| ApplicationUser | Identity-provider subject and tenant reference or explicit mock-identity marker, active status, optional Employee link |
| RoleAssignment | User, role, explicit team/record/configuration scope, effective dates, approver, review date |
| TestSystem | Governed identity, owner/approval references, active and Non-CLIA applicability status; synthetic placeholder only in sprint one |
| ProcessGrouping | Identity, owner, applicability, approved configuration version, interval value/unit, active status, explicit mapped TestSystems |
| Assignment | Identity, Employee, Team, ProcessGrouping, distinct lead/Assessor/final-signer relationships, interval/configuration snapshot, basis/due dates, scheduling state, predecessor/successor-cycle reference when applicable, lineage, concurrency version |
| Assessment | Stable identity, Assignment, lifecycle state, current-draft reference when editable, current immutable-version reference when issued |
| AssessmentDraft | Mutable working content, Assessment, concurrency version, participant/configuration references, scenario inputs, created/updated attribution; never signed or finalized |
| AssessmentVersion | Immutable issued snapshot identity/number, exact participant and rule/configuration snapshot, scenario-required assessment concepts, dates, method/Assessor-recorded outcome/comments/follow-up state, created-by/time, supersession link when later approved |
| AssessmentElement | Version, required-element reference, Assessor-recorded result, evidence/comments, gap flag, follow-up status |
| RemedialAction | Element/gap, description, status, evidence reference, attributable review; S0-01 does not define completion approval |
| Signature | Exact AssessmentVersion, signature role, signer identity, signing time, authentication context, request identity |
| AssessmentDocument | Exact version, private object reference, document kind/version, SHA-256, uploader, timestamps |
| NotificationEvent | Trigger, recipient reference, template version, scheduled occurrence, Assignment/Assessment reference, idempotency identity, status |
| NotificationAttempt | Event, attempt identity/ordinal, adapter request reference, outcome, safe failure category, timestamps |
| AuditEvent | Append-only identity, actor/service identity, action, entity reference, time, outcome, correlation/request identifiers, minimized change summary, optional support purpose/reference |
| ApprovedKnowledgeSource | Source identity/title, named owner, version, effective/retired dates, hash, access classification, active status, assistant availability |

Conceptual relationships and invariants:

1. An Assignment references one Employee, Team, ProcessGrouping, Assigned Team Lead, Assessor, and Technical Supervisor for the scenario; those relationships never derive from administrative membership.
2. An Assessment has a stable identity. Editable work lives only in an AssessmentDraft. Successful submission snapshots the draft into a new immutable AssessmentVersion and updates the current-version reference.
3. Issued versions, their elements/follow-up snapshot, signatures, and documents bind to an exact version. An issued version is never edited; signatures never carry to another version.
4. Finalized versions are retained and locked. Amendment creation/authority remains unavailable until D05/D06 approval.
5. NotificationEvent is the logical event; NotificationAttempt is a delivery observation. A failed attempt cannot change assessment state.
6. AuditEvent is append-only and attributable. Normal application/admin operations cannot update or delete it.
7. Hashes prove integrity metadata; they never grant access.
8. `Overdue` is derived from due date, current time, and an active state; it is not persisted as a replacement lifecycle state.

### 4.1 State ownership

- Assignment owns scheduling facts and the `Scheduled`, `Assigned`, and `Cancelled` scheduling states. Cancellation exists in the canonical vocabulary but has no enabled first-sprint command because its authority and reason rules are not approved.
- Assessment owns `In progress`, `Submitted`, `Returned`, `Awaiting Testing Personnel signature`, `Awaiting Technical Supervisor signature`, and `Finalized`.
- A role-scoped workflow projection may present the combined canonical sequence, but it cannot create a second mutable source of lifecycle truth.
- `Renewal scheduled` is a separate deterministic renewal/successor-cycle result linked to the still-`Finalized` assessment version. It never overwrites finalization.
- `Overdue` remains a calculated condition over an active Assignment.

### 4.2 Deferred migration concepts

`MigrationBatch`, `MigrationSourceRecord`, and `MigrationException` remain future conceptual boundaries for source identity/hash/custodian, workbook-sheet-row/original-value lineage, target relationships, ambiguity, owner decisions, and reconciliation evidence. S0-02 defines no migration command, mapping, staging store, or operational load.

## 5. Application command contracts

| Command | Authorized actor and preconditions | Atomic outcome |
| --- | --- | --- |
| Configure synthetic scope | SQUAD Admin within approved configuration scope | Configuration references and attributable audit observation |
| ScheduleAssignment | SQUAD Admin; active synthetic relationships; approved basis date and interval | Due-date calculation, Assignment in `Scheduled`, participant snapshots, audit, logical notification event as applicable |
| ReleaseAssignment | Authorized SQUAD Admin; expected Assignment version in `Scheduled` | `Assigned`, work visibility, audit, notification event |
| BeginAssessment | Explicit Assessor; assigned scope; expected state/version | Assessment and editable draft created or selected, state `In progress`, audit |
| SaveAssessmentDraft | Explicit Assessor; `In progress` or approved returned recovery; expected draft concurrency version | Validated draft values and audit without competency inference |
| DocumentRequiredFollowUp | Explicit Assessor; unsuccessful scenario element; expected draft concurrency version | Attributable prototype description in the draft; no remediation-completion or approval meaning |
| SubmitAssessment | Explicit Assessor; expected draft version; scenario completeness/follow-up checks | Snapshot one immutable AssessmentVersion and record `In progress -> Submitted`. A complete version deterministically continues to Testing Personnel review. When required follow-up is absent, the same unit of work records `Submitted -> Returned`, preserves the submitted version, creates a correction draft, audits both transitions, and cannot advance to signature. |
| ReturnAssessment | Authorized current reviewer; allowed pre-signature review state and exact unsigned issued version | Preserve that immutable version, create a new editable draft for correction, record `Returned`, safe reason, and audit. A request affecting a signed version returns `POLICY_PENDING` without mutation until D05 is approved. |
| SignTestingPersonnel | Own Employee; exact complete version in awaiting-Testing-Personnel state | One version-bound signature, next state, audit, Technical-Supervisor signature-required event |
| SignTechnicalSupervisor | Explicit final signer; same exact version; valid Testing Personnel signature | One final version-bound signature; the authorized command deterministically continues through finalization in the same application-visible outcome |
| FinalizeAssessment (internal continuation) | Not externally invocable; inherits the already authorized Technical Supervisor command context, exact version, and request identity | One transaction records Finalized/locked version, document metadata, renewal, completion event, and audit; failure reports none as finalized |

`ReturnAssessment` defines only the approved unsigned prototype return behavior. Post-signature correction, cancellation, and finalized amendment commands remain unavailable until their required rules are approved.

## 6. Query and support contracts

| Query | Scope rule | Result boundary |
| --- | --- | --- |
| OwnWork/OwnHistory | Employee identity equals target participant | Own assignments/status/version summaries only |
| AssignedTeamWork | Effective assigned-team scope | Rows filtered to assigned Team before counts/data return |
| AssignedAssessment | Explicit Assessor relationship | Only assigned record and permitted mutable version |
| FinalReviewQueue | Explicit Technical Supervisor relationship | Only records awaiting that signer's review |
| AdministrativeStatus | Effective SQUAD Admin configuration/report scope | Approved administrative view; no assess/sign authority |
| DiagnosticRecordRead | Effective Platform Admin support scope plus attributable purpose/reference when available | Minimum diagnostic/read fields; no business command capability |
| ControlledExport | Same scope as corresponding query | Synthetic/prototype export only; denial before content generation |

Artifact retrieval additionally requires record scope and document permission on every request. Any future short-lived retrieval mechanism is an infrastructure detail, not authority.

## 7. Authorization decision interface

Authorization evaluates authenticated ApplicationUser, effective RoleAssignments, explicit participant relationships, requested action, record/team scope, current state, and exact version. The decision is made inside every state-changing transaction and before every query or document result.

| Actor | Allowed scenario capability | Explicit denial |
| --- | --- | --- |
| Employee | Own view and exact-version Testing Personnel signature | Other records, assessment documentation, final signature |
| Assigned Team Lead | Assigned-team work queue and report/export | Assessment/evidence/follow-up unless separately assigned as Assessor; Testing Personnel/final signature |
| Assessor | Explicitly assigned assessment/evidence/follow-up work and permitted reporting | Unassigned records, Testing Personnel/final signature |
| Technical Supervisor | Assigned final review, allowed return, final signature | Unassigned records, assessment authorship |
| SQUAD Admin | Approved configuration, assignment, reporting, notification/exception administration | Assessment documentation or signature by membership alone |
| Platform Admin | Attributable least-privilege diagnostic/read | Configuration, assignment, assessment, signature, finalization, ordinary mutation |

UI visibility never substitutes for this decision. A deny outcome creates minimized audit evidence without returning protected content.

## 8. Transactions, concurrency, and idempotency

1. Authorization, state/version validation, business mutation, required audit effect, and logical notification creation occur within the relevant unit of work.
2. Finalization is all-or-nothing across locked state, signature validation, verified artifact metadata, renewal, completion event, and audit. In the first sprint the artifact is synthetic metadata/hash only.
3. External email/Blob/model calls never sit inside a transaction that could falsely report business completion. The exact Blob coordination, verification, cleanup, and reconciliation mechanism is deferred; only authorized metadata may become application-visible with a successful finalization outcome. Durable notification intent commits before separate adapter attempts. S0-02 selects no worker product.
4. Optimistic concurrency compares `expected_version`; stale writes return `STALE_VERSION` and do not overwrite.
5. A replay with the same operation identity returns the original safe outcome or no-op indication and creates no duplicate logical effect.
6. Reuse of an idempotency identity with conflicting input returns `IDEMPOTENCY_CONFLICT` and creates no effect.

| Effect | Idempotency identity |
| --- | --- |
| General command | Command name, target aggregate, authenticated actor, and caller request identity |
| Assignment scheduling | General command identity plus approved cycle/target/configuration identity |
| Signature | Command request identity plus exact AssessmentVersion, signature role, and signer |
| Logical notification | Assessment/Assignment, trigger, recipient, template version, and scheduled occurrence |
| Notification attempt | NotificationEvent plus adapter request identity/attempt ordinal |
| Finalization | Command request identity plus Assessment and exact AssessmentVersion |
| Artifact metadata | Finalized AssessmentVersion, document kind/version, and integrity hash |
| Renewal | Finalized AssessmentVersion plus interval snapshot |
| Audit effect | Originating request identity, named effect/action, and entity; outcome is stored payload rather than a duplicate discriminator, and retries do not erase distinct legitimate actions |
| Assistant outcome log | Assistant request identity plus prompt/model/source-set versions; never a business mutation key |

## 9. Notification and audit ports

The notification port accepts only approved logical trigger, recipient reference, template version, stable record reference, minimum scheduling/status context, occurrence identity, and correlation identifier. Assessment results and unnecessary sensitive content are rejected. The prototype adapter does not deliver email.

The attempt recorder accepts event identity, adapter request identity, attempt time, outcome, retry eligibility, and minimized failure category. It cannot change Assignment or Assessment state.

The audit port records actor/service, action, target reference, time, outcome, request/correlation identifiers, minimized change summary, and support purpose/reference when applicable. Audit storage exposes append only; retention/disposition is not part of normal application interfaces.

## 10. Read-only assistant contract

The assistant is a separate adapter with no application unit-of-work, repository-write, notification-delivery, signature, authorization-change, source-publication, or record-mutation port.

Input: authenticated actor/access context, question, assistant request identity, approved prompt/model configuration references, limits, and correlation identifier. Assessment content is not a required input.

Source selection: filter first to acquired, active, approved, versioned, assistant-enabled sources accessible to the actor. Retired, conflicting, inaccessible, or insufficient evidence produces escalation.

User questions and retrieved source text are untrusted data. Instructions within them cannot override source-access filtering, prohibited capabilities, required citations, coverage checks, SME escalation, version logging, or the structured result contract. Attempts to suppress those controls produce a refusal or escalation and no consequential action.

Output is exactly one of:

- `SupportedAnswer`: bounded answer, usable source/location citations, source-set version, prompt/model versions, outcome metadata;
- `Escalation`: stable limitation reason and SME direction, with no invented policy;
- `SafeFailure`: minimized dependency/limit error.

Logs retain request/correlation identity, source/prompt/model versions, outcome, timings, and safe error category—not unnecessary question or source text.

Because S0-01-A08 is not approved, S0-03 may define/stub this interface and S0-04B may test denial/escalation behavior, but no supported controlled answer may be implemented until the source-owner gate is satisfied.

### 10.1 Server-rendered web implications

State-changing web requests map to protected form submissions and service commands, use post/redirect/get after success, and render safe typed failures. Templates contain no workflow or authorization decisions. Role-based navigation is convenience only. UI realization must preserve the S0-01 keyboard, focus, programmatic-label/error/status, semantic table, non-color-only, and WCAG 2.2 Level AA prototype criteria. S0-02 selects no CSRF/session package, route design, SPA, or public API.

## 11. Traceability

| S0-01 evidence | S0-02 contract location |
| --- | --- |
| P01-P02, P04-P07 | Sections 4-5 and 8 |
| P08-P11, N04-N11 | Sections 4-5 and 8 immutable/versioned transaction rules |
| P03, P15-P23, N13 | Sections 8-9 notification event/attempt contracts |
| P12, P29-P33, N01-N03, N12 | Sections 6-7 scoped authorization contracts |
| P24-P28 | Common results plus S0-01 WCAG 2.2 AA acceptance baseline; UI realization remains S0-03/S0-05 |
| P34-P35 | Sections 8-9 append-only audit contract |
| P13-P14, N14-N16 | Section 10 assistant contract and A08 blocker |
| N17 | Task contract exclusions and unresolved decisions |

## 12. Deferred decisions and stop conditions

S0-01 D01-D12 remain unresolved production decisions. S0-02 also deliberately defers physical field types, tables, indexes, constraints, Flask routes/forms, HTML structure, dependency versions, exact Blob/email/model adapters, notification execution product, Azure network configuration, retention implementation, operational migration mappings, and deployment.

Stop dependent work if it requires a production rule, amendment/repair flow, approved assistant source, new role or state, broader administrative access, controlled content, operational data, a new platform, or a cross-owned interface change not approved here.

## 13. Acceptance criteria

| ID | Required evidence |
| --- | --- |
| `S0-02-AC01` | Every S0-01 workflow step maps to a command, query, or an explicit blocked/deferred outcome. |
| `S0-02-AC02` | Conceptual relationships keep Employee, ApplicationUser, administrative roles, Assigned Team Lead, Assessor, and final signer distinct. |
| `S0-02-AC03` | Every mutation requires server-resolved authorization, current state, exact version/concurrency input, one unit of work, attributable audit, and stable result/error behavior. |
| `S0-02-AC04` | The A01 examples calculate `2027-02-15` and `2028-02-20` and retain basis, interval, and configuration provenance. |
| `S0-02-AC05` | A stale or unauthorized command changes no business record and exposes no out-of-scope content. |
| `S0-02-AC06` | Repeated signature, notification, finalization, artifact, audit-effect, and renewal operations create one logical effect; conflicting reuse of a key is rejected. |
| `S0-02-AC07` | A finalization component failure reports no finalized result, completed event, renewal, or exposed artifact metadata. |
| `S0-02-AC08` | Notification-attempt failure adds only an attempt; the logical event and assessment remain unchanged and the payload excludes result/sensitive narrative. |
| `S0-02-AC09` | Exact-version signature order, immutable issued versions, no signature carry-forward, finalized locking, and append-only audit behavior are explicit. |
| `S0-02-AC10` | Role-scoped queries filter before returning rows/counts/documents, and Platform Admin access is minimized and attributable. |
| `S0-02-AC11` | The assistant filters source access before context, resists user/source prompt injection without suppressing citations or escalation, returns a typed escalation while A08 is blocked, logs minimized versioned outcomes, and exposes no consequential capability. |
| `S0-02-AC12` | Migration concepts preserve lineage and ambiguity without enabling an operational migration path. |
| `S0-02-AC13` | Cancellation, signed-version correction, amendment, production policy, physical schema, dependency, and platform choices remain explicitly unavailable or deferred. |
| `S0-02-AC14` | Data and Flask reviews, independent boundary review, repository validation, issue/branch/PR traceability, and exact-file handoff are recorded. |

## 14. Review and approval record

| Review | Reviewer | Status | Evidence |
| --- | --- | --- | --- |
| Project authorization | Project Requester | Approved 2026-09-08 | Explicitly requested implementation of the next task. |
| Orchestrator integration | Orchestrator / Engineering Lead | Approved 2026-09-08 | Confirmed complete shared interfaces, framework-neutral ownership, S0-01 traceability, and explicit downstream stop conditions. |
| Data/domain consistency | Data and Migration Agent | Approved 2026-09-08 | Confirmed draft/version separation, state ownership, transactions, lineage, immutability, idempotency, and deferred migration boundary. |
| Flask/application consistency | Flask Application Agent | Approved 2026-09-08 | Confirmed ports, commands/queries, authorization, typed results, transactions, web implications, and assistant isolation. |
| Independent boundary review | QA and Independent Review Agent | Approved 2026-09-08 | Confirmed role separation, canonical return sequence, prompt-injection controls, privacy, records, accessibility, AI restrictions, and no production-policy expansion. |

**Status: Approved S0-02 contract; pending repository validation and merge through issue #7.**

S0-03 may not begin until this contract is validated and merged into `dev`. The exact files changed, validation evidence, issue/branch/PR links, reviews, remaining A08 blocker, and deferred decisions must be reported at handoff.
