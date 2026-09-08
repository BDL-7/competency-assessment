# Agent Operating Contract

This repository uses a small, bounded agent team. Agents implement approved
tasks; they do not create laboratory policy or expand product scope.

## Required reading

Before working, every agent reads:

1. This file.
2. `docs/SOURCE_AUTHORITY.md`.
3. `docs/PRODUCT.md`.
4. The task contract under `agent-tasks/`.
5. Only the additional canonical documents needed for its assigned task.

Controlled documents and operational workbooks remain review-only. Do not copy
controlled content or identifiable workforce data into public files, prompts,
fixtures, logs, issues, or pull requests.

## Core roles

| Role | Mission | Future writable scope | Mandatory stop conditions |
| --- | --- | --- | --- |
| Orchestrator / Engineering Lead | Decompose, sequence, integrate, and escalate | Agent contracts, architecture documents, ADRs, integration-only files | Missing authority, conflicting sources, overlapping file leases, or an unapproved boundary change |
| Product and Laboratory Domain | Translate approved sources into terminology, rules, states, and acceptance criteria | Product, terminology, workflow, and acceptance documents | A rule requires laboratory judgment or unavailable controlled guidance |
| Flask Application | Implement the server-rendered application and application services | `app/web/`, `app/auth/`, `app/services/`, templates, and static assets | The task requires an unapproved role, state, field, service, tool, or platform |
| Data and Migration | Implement persistence, schema changes, staging, lineage, and reconciliation | `app/data/`, `migrations/`, and migration tests/tools | A mapping is ambiguous, source lineage would be lost, or source data would be changed |
| QA and Independent Review | Convert acceptance criteria into tests and review behavior independently | `tests/` and testing evidence | Acceptance criteria are missing, implementation weakens a control, or synthetic data is insufficient |
| Knowledge Assistant | Implement the separate read-only assistant boundary | `app/ai/` and `tests/ai_evals/` after an approved task | A task would enable scoring, approval, signing, notification delivery, permission changes, publication, or record mutation |

Architecture remains an Orchestrator responsibility. Security/privacy/records,
accessibility, Azure operations, UX, database performance, migration
reconciliation, and adversarial AI review are temporary review functions
invoked only when an approved task triggers them.

## File leases and collaboration

- Each task lists every allowed writable path.
- Only one active task may hold a writable path.
- Shared interfaces are agreed and recorded before parallel work begins.
- A cross-owned edit becomes a separate Orchestrator integration task.
- Agents never stash, reset, overwrite, or discard another task's work.
- Work uses issue-numbered branches and pull requests targeting `dev`.

## Human approval gates

Explicit human approval is required before changing controlled assessment
rules, authorization policy, due-date or renewal logic, signature meaning or
sequence, approved AI sources, administrative access, migration reconciliation,
finalized records by amendment, deployment to test or production, or record
disposition.

## Definition of done

A task is complete only when its expected outputs exist, acceptance criteria
are met, validation evidence is recorded, an independent review is complete
when required, unresolved decisions are explicit, and the handoff reports the
exact files changed without exposing sensitive information.
