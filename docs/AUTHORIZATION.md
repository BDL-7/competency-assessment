# Authorization Model

Authentication and UI visibility are not authorization. Every record query,
document retrieval, export, and state-changing action is checked server-side.

## Roles and scopes

| Role | Scope | Permitted responsibility |
| --- | --- | --- |
| Employee / Testing Personnel | Own assignments and records | View own work/history, review the exact assessment version, and sign as Testing Personnel |
| Assessor / Assigned Team Lead | Explicitly assigned team and assessment scope | Manage assigned work, document assessments/evidence/follow-up, receive submissions, and use team-scoped reporting/export |
| Technical Supervisor / final signer | Explicitly assigned records awaiting final review | Review the assessment and Testing Personnel signature, return when allowed, and provide the final signature |
| SQUAD Admin | Approved application-administration scope | Maintain approved users, teams, assignments, role scopes, catalog/configuration, reporting, notifications, and exceptions |
| Platform Admin | Continuous least-privilege diagnostic/read support scope | Maintain Azure platform operations and investigate failures with attributable access |
| Service identity | Specific approved application resources | Access only the Azure resources needed by its component |

Center/quality viewer access is outside the first coding sprint and is not an
active prototype role.

## Action matrix

| Action | Employee | Assessor / Team Lead | Technical Supervisor | SQUAD Admin | Platform Admin |
| --- | --- | --- | --- | --- | --- |
| View own record | Yes | When explicitly assigned | When explicitly assigned | Approved support scope | Diagnostic/read only and audited |
| Document assessment | No | Assigned assessment only | No | No authority from admin membership | No |
| Sign as Testing Personnel | Own exact version only | No | No | No | No |
| Final sign | No | No | Assigned exact version only | No | No |
| Maintain approved application configuration | No | No | No | Yes, within approved policy | No |
| Produce report/export | Own history | Assigned-team scope | Assigned scope | Approved administrative scope | Diagnostics only |
| Perform ordinary workflow mutation | Participant action only | Assigned action only | Assigned action only | Approved administrative actions only | No |
| Amend finalized record | Only through later approved procedure | Only through later approved procedure | Only through later approved procedure | Administer only when separately approved | No ordinary authority |

## Required controls

- Resolve Entra identity to an active Application User and effective Role
  Assignment.
- Keep SQUAD Admin and Platform Admin groups separate.
- Keep administrative role assignments separate from assessment participants.
- Apply team/record scope to queries before returning data.
- Audit role changes, denied actions, exports, document access, signatures,
  finalization, and administrative actions.
- Audit every Platform Admin access to competency-record context with actor,
  record/action, time, outcome, correlation identifier, and support purpose or
  reference when available, without logging sensitive content.

Granting administrative access, changing the matrix, or enabling a finalized
record repair/amendment action requires explicit human approval.
