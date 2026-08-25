# First Coding Sprint Task Graph

This is a Phase 0 planning artifact, not authorization to execute the sprint.
The sprint begins only after a separate human authorization.

## Sprint outcome

Demonstrate one synthetic Non-CLIA assessment from SQUAD Admin assignment
through finalization, audit, renewal, and role-scoped status while a separate
read-only assistant returns one supported cited answer and one SME escalation.

Center viewer access, Power BI, MIST/HIR migration execution, CLIA workflows,
production deployment, and production data are excluded.

## Dependency graph

```text
S0-01 Approved synthetic scenario and acceptance criteria
  -> S0-02 Domain interfaces and schema contract
      -> S0-03 Repository/application foundation
          -> S0-04A Application workflow vertical slice
          -> S0-04B Read-only assistant vertical slice
              -> S0-05 Integrated authorization and boundary tests
                  -> S0-06 Independent review and human demonstration
```

`S0-04A` and `S0-04B` may run in parallel only after the shared identity,
approved-source, audit, and error-response interfaces are agreed. They may not
modify the same file.

## Task contracts

### S0-01 — Scenario and acceptance criteria

- Owner: Product and Laboratory Domain Agent
- Inputs: canonical Phase 0 documents and controlled sources
- Outputs: one entirely synthetic scenario, rules, positive/negative acceptance
  criteria, and unresolved policy list
- Allowed files: task-owned acceptance artifact only
- Stop: a required rule is absent or needs laboratory judgment
- Gate: human approval of the scenario and prototype-only assumptions

### S0-02 — Interface and schema contract

- Owner: Orchestrator with Data and Flask review
- Inputs: approved S0-01
- Outputs: module interfaces, conceptual fields/relationships, transactions,
  authorization checks, idempotency identities, and assistant contract
- Prohibited: code, models, migrations, packages, or new platform decisions
- Gate: Orchestrator integration approval and domain consistency review

### S0-03 — Repository/application foundation

- Owner: Flask Application Agent; Data Agent owns only persistence-specific
  files assigned by the contract
- Outputs: the separately authorized Flask structure, approved dependency
  manifest/lockfile, configuration template, and test foundation
- Stop: a dependency, tool, or platform is not explicitly approved
- Validation: exact commands are recorded in the authorized implementation task

### S0-04A — Application workflow vertical slice

- Owner: Flask Application Agent with Data-owned persistence tasks
- Outputs: synthetic configuration, assignment, assessment, follow-up,
  signatures, finalization/lock, artifact metadata, notification events, audit,
  renewal, and role-scoped status
- File ownership: Flask and Data paths remain exclusive and interface-driven
- Stop: a requested behavior falls outside `docs/PRODUCT.md` or lacks a rule

### S0-04B — Read-only assistant vertical slice

- Owner: Knowledge Assistant Agent
- Outputs: approved-source registry boundary, EDAV OpenAI adapter boundary,
  cited supported response, coverage failure, SME escalation, and data-minimized
  outcome logging
- Prohibited: record mutation or any consequential tool/capability
- Stop: no source is acquired, approved, versioned, or permitted for the
  prototype question

### S0-05 — Integrated validation

- Owner: QA and Independent Review Agent
- Outputs: executable acceptance, authorization, record-integrity, assistant,
  and accessibility evidence using synthetic data
- Review-only: application and assistant implementation
- Stop: acceptance criteria were weakened or a critical boundary fails

### S0-06 — Integration and demonstration

- Owner: Orchestrator
- Inputs: validated app and assistant tracks
- Outputs: integrated branch, validation report, limitations, decision log, and
  human demonstration
- Merge gate: human approval after independent QA and required specialist
  reviews

## Handoff order

Interfaces merge before dependent implementations. Data changes merge before
services that require them; services merge before web flow; app and assistant
tracks integrate only after their individual validation; independent review is
last. Any interface revision reopens affected task approvals.
