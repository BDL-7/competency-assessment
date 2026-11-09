# Assessment Workflow

## Canonical sequence

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
