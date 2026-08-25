# Agent Task Contracts

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
