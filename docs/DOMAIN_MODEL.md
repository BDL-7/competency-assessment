# Minimum Domain Model

This is the conceptual model for interface agreement. It is not a database
schema or authorization to create migrations.

## Application-first entities

| Entity | Purpose and essential relationships |
| --- | --- |
| Team | Organizational owner for employees, assignments, approved test systems, and reporting scope |
| Employee | Person assessed, team, active status, role/job context, and source identifiers; separate from login |
| ApplicationUser | Entra-backed application identity linked to an Employee only when applicable |
| RoleAssignment | Effective-dated role, scope, approver, active dates, and review date |
| TestSystem | Governed approved catalog item with owner, approval identifiers, and active/CLIA status |
| ProcessGrouping | Approved process/competency grouping, interval, applicability, owner, and mapped tests |
| Assignment | Employee, grouping, Assigned Team Lead, Assessor, Technical Supervisor, interval, due date, status, and source lineage |
| Assessment | Stable assessment identity and current lifecycle status |
| AssessmentVersion | Immutable version containing participant relationships, dates, method, outcome, comments, and follow-up state |
| AssessmentElement | Required element, result, evidence/comments, gap flag, and follow-up status |
| RemedialAction | Gap-linked required action, description, status, evidence, and attributable completion review |
| Signature | Testing Personnel or Technical Supervisor signature meaning, signer, time, exact assessment version, and authentication context |
| AssessmentDocument | Private Blob reference, document type, version, SHA-256, uploader, and timestamps |
| NotificationEvent | Approved trigger, recipient, template version, idempotency identity, and assessment reference |
| NotificationAttempt | Delivery attempt, outcome, retry information, failure reason, and timestamps |
| AuditEvent | Append-only actor, action, entity, time, outcome, correlation identifier, and appropriate change summary |
| MigrationBatch | Controlled source set, hashes, custodian, extraction context, status, and approval evidence |
| MigrationSourceRecord | Workbook, sheet, row/source identifier, original value lineage, and target relationship |
| MigrationException | Unresolved conflict, ambiguity, missing value, decision, owner, and resolution evidence |

`Acknowledgement` is not a separate prototype entity. The Testing Personnel
signature is the current acknowledgement event. A separate event requires a
later approved change.

## Knowledge-assistant entity for the first coding sprint

| Entity | Purpose |
| --- | --- |
| ApprovedKnowledgeSource | Document identifier, title, owner, version, effective/retired dates, hash, access classification, active status, and assistant availability |

## Invariants

- Administrative membership never implies assessment or signature authority.
- Participant relationships are explicit and effective for the assignment.
- Signatures reference one immutable AssessmentVersion.
- Finalized versions are not updated or deleted through normal workflow.
- An amendment creates a superseding version and preserves the original.
- Document and approved-source hashes are integrity metadata, not access
  controls.
- Migration lineage never silently replaces original workbook values.
- Due dates and renewals are deterministic from approved configuration.

Field types, indexes, uniqueness constraints, retention behavior, and physical
table design are outputs of later approved implementation tasks.
