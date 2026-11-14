# Assessment Workflow

## Canonical sequence

This sequence is the existing Non-CLIA prototype baseline. Shared software
mechanics may be reused, but CLIA-specific fields, qualifications, signatures
and dates must not be inferred from it.

1. A designated SQUAD Admin configures the approved people, team, test system
   or process grouping, interval, and assignment relationships needed for the
   prototype.
2. The application calculates the due date from approved configuration and
   creates the Employee and Assigned Team Lead work items.
3. The application creates minimal-content notification events and records
   delivery attempts.
4. The authorized Assessor conducts and documents the assessment using the
   approved fields and required elements.
5. Any unsuccessful required element records a gap and the required follow-up
   or remedial action. Required follow-up must be documented before closure.
6. Testing Personnel reviews the exact assessment version and signs. This is
   the current employee acknowledgement event.
7. The Technical Supervisor/final signer reviews that version and signs.
8. The system finalizes and locks the signed version, retains artifact
   metadata, writes audit events, and calculates the next due date.
9. Authorized users view role-scoped status and reports.

## State model

| State | Meaning | Allowed next states |
| --- | --- | --- |
| Scheduled | Due date exists; work is not yet released | Assigned, Cancelled |
| Assigned | Employee and Team Lead work item is available | In progress, Cancelled |
| In progress | Assessment documentation is underway | Submitted, Cancelled |
| Submitted | Assessor documentation is ready for review | Returned, Awaiting Testing Personnel signature |
| Returned | Correction or additional evidence is required | In progress, Submitted, Cancelled |
| Awaiting Testing Personnel signature | Testing Personnel must review and sign | Returned, Awaiting Technical Supervisor signature |
| Awaiting Technical Supervisor signature | Testing Personnel signed; final signer must review and sign | Returned, Finalized |
| Finalized | Approved version is locked and retained | Superseded by amendment, Renewal scheduled |
| Cancelled | Assignment closed before finalization with an attributable reason | None; a new assignment is required |
| Superseded by amendment | Original finalized version remains retained and a corrected version governs | Finalized only through the approved amendment flow |
| Renewal scheduled | Next cycle was calculated from approved completion date and interval | Scheduled, Assigned, Cancelled |

`Overdue` is a reportable condition on an active state, not a replacement for
that state.

## Deterministic controls

- Every action checks actor, role, team/record scope, current state, and exact
  version on the server.
- The application does not infer pass/fail or competency from free text.
- A signature is bound to the exact version reviewed.
- A later edit invalidates signatures and returns the record to the applicable
  approved state.
- Finalization requires the two approved signatures in sequence and all
  approved completeness/follow-up rules.
- Renewal uses the finalized completion date and configured approved interval.
- Repeated commands must not duplicate signatures, notifications, audit
  effects, finalized artifacts, or renewals.

## Open human decisions

Before the relevant behavior can become MVP or production policy, the
laboratory owner must confirm required fields/elements, pass/fail recording,
what proves remedial action complete, return rules, permitted intervals, and
the complete amendment procedure. Notification owners must confirm production
cadence and escalation.

## Dual-workflow evidence and integration contract

Both executable workflows are required by the current
[product target](PRODUCT.md#current-dual-workflow-delivery-requirements).
The table records permitted public evidence, not a new laboratory policy.
Closed historical issues do not supply missing CLIA requirements.

| Behavior | Existing public evidence / implementation | CLIA evidence or integration gap | Next owner / acceptance |
| --- | --- | --- | --- |
| Applicability | `TestSystem.is_non_clia_applicable` and `ProcessGrouping.applicability`; [domain model](DOMAIN_MODEL.md) | No executable two-profile mapping; false non-CLIA flag does not imply CLIA | Product/laboratory owner confirms mapping; Data adds only approved schema delta and profile tests |
| Fields and assessment elements | [Non-CLIA scenario](archive/tasks/s0-01-synthetic-scenario.md), provisional form V04 label in [source manifest](SOURCE_MANIFEST.md) | Public inspected evidence does not establish the CLIA required field/element set | Laboratory/source owner supplies an approved public rule decision; tests enforce each profile's actual required inputs |
| Participant relationships | Separate employee, team lead, assessor and final signer; [authorization matrix](AUTHORIZATION.md) | CLIA participant qualifications/role meanings cannot be inferred from a roster or non-CLIA participant labels | Laboratory/authorization owners confirm any differences; no administrative membership grants signing rights |
| Evidence and follow-up | Assessor-recorded result and required follow-up before existing finalization; no calculated competency | CLIA-specific sufficiency/completion rules not established by inspected public sources | Laboratory owner resolves the exact rule; preserve no-AI-decision boundary |
| Review/signatures | Existing Testing Personnel then Technical Supervisor sequence bound to one version | CLIA signature meaning/sequence and authentication requirements are not established by the existing Non-CLIA scenario | Laboratory/signature owner decision before affected actions; no relabeling as valid CLIA signatures |
| Completion, interval and renewal | Approved completion basis plus configured interval; existing scenario uses fictional values | Do not reuse a fictional 12-month interval as CLIA policy or infer special schedules | Laboratory owner confirms applicable basis/interval rules; source-linked boundary-date tests |
| Versions, locking and retries | [shared interfaces](archive/tasks/s0-02-interface-schema-contract.md), domain/service controls | Persistent SQL service adapters missing; existing service integration tests use fake ports | Data/App implement scoped atomic writes, stale-version rejection, rollback and idempotency |
| Multi-lab queues and reports | SQL scoped pilot reader; separate multi-lab fixture loader | UI requires old ownership marker/reference date; larger pack is not integrated | App/Data implement one versioned owned setup boundary and prove cross-lab counts/denials |
| Notifications and artifacts | Event/attempt ports and synthetic metadata | Not live email or private Blob retrieval | Platform approvals and separate real adapter checks; an event is not delivery |
| Amendments and post-signature repair | Existing open human gate; original versions retained | No approved full amendment procedure for either expanded profile | Records/laboratory owner; no ordinary mutation of finalized records |

Implementation must connect `web -> services -> domain` with SQL adapters behind
the existing service ports. Normal commands must accept authorized target
identities instead of hard-coded single-scenario IDs. Keep the old demonstration
helper as an explicit compatibility path, not a general authorization shortcut.

For every rule row, record source/version, permitted profile, implementation
state and acceptance evidence in the implementing contract. Reconcile remaining
permitted public evidence first. If a governed difference remains unresolved,
name that specific action and owner; do not invent defaults, remove CLIA from
the target, or claim dual-workflow completion. Protected documents remain
unopened by agents in this transition.
