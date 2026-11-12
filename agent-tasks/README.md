# Current Tasks

Use this directory to select current work. A file's presence is not approval
or a writable lease. Implementation proceeds through separately approved app
changes, not the historical first-sprint execution sequence.

## Current work

| Contract | Scope |
| --- | --- |
| [Archive completed plans (#34)](34-archive-completed-plans.md) | Historical documentation and navigation only; no runtime, policy or private-file changes |

## Requirements and retained decisions

| Need | Start here |
| --- | --- |
| Current scope, controls and implementation guidance | [Documentation guide](../docs/README.md) |
| Current demo and outstanding reviews | [Local walkthrough](../docs/BUILDATHON.md) |
| Original acceptance criteria, prototype decisions, interface agreements and approval evidence | [Archived baselines and open gates](../docs/archive/README.md#retained-baselines-and-open-gates) |

Completed tasks and the old sprint graph are [archived](../docs/archive/README.md),
not current work. Archiving does not revoke still-applicable decisions, approve
pending reviews or make historical feature targets implemented today.
Preflight accepts only a contract filename directly in this directory; it does
not select archived work or establish authorization.

## Contract template

Every implementation or review task uses this contract. It prevents
uncontrolled edits, scope expansion, and conflicting concurrent work.

```text
Task ID:
Owner Agent:
Goal:
Business Reason:
Required Context:
Source-of-Truth Files:
Dependencies:
Approved Assumptions:
Allowed Files:
Review-Only Files:
Prohibited Actions:
Expected Outputs:
Acceptance Criteria:
Validation Commands:
Security and Privacy Considerations:
Definition of Done:
Handoff Format:
Stop Conditions:
Human Approval Gate:
Path Lease Owner and Expiry:
```

## Contract rules

- Goals describe one reviewable outcome.
- Allowed Files are explicit paths, not broad repository ownership.
- Review-Only Files include controlled sources and operational workbooks.
- Assumptions cite an approved decision; an agent cannot create one.
- Stop Conditions include missing authority, sensitive-data exposure, scope
  expansion, interface conflict, and overlapping leases.
- A task reports changed files, validation results, unresolved decisions, and
  the next owner at handoff.
- A task is not complete until required independent and human reviews are
  recorded.
