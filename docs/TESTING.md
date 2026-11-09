# Testing Strategy

Testing proves the approved workflow and boundaries; it does not invent
requirements. All committed fixtures are synthetic.

## Required layers

| Layer | Required coverage |
| --- | --- |
| Domain/unit | State transitions, completeness gates, follow-up, signature sequence, locking, renewal, and idempotency |
| Integration | SQL transactions, authorization-scoped repositories, artifact metadata, notification event/attempt separation, audit creation, and assistant adapter contracts |
| Authorization | Own-record and assigned-team access, explicit final-signer scope, SQUAD Admin boundaries, Platform Admin diagnostic/read access, and denial of business actions |
| End to end | One synthetic assignment through finalization, audit, renewal, reporting, and a return/remedial branch |
| AI evaluations | Supported cited answer, unsupported escalation, conflicting/retired/restricted source, injection resistance, and all prohibited actions |
| Accessibility | Keyboard operation, focus, labels, validation messages, table semantics, and contrast for the server-rendered UI |
| Migration | Synthetic lineage, idempotent batch behavior, exception handling, and reconciliation logic; no operational rows in the first sprint |

## Control assertions

- No finalized version is edited through normal workflow.
- No signature applies to a different assessment version.
- No role obtains authority solely through UI visibility or administrative
  membership.
- No retry duplicates a notification, signature, audit effect, or renewal.
- No email body contains an assessment result or unnecessary sensitive detail.
- No assistant response changes a record or makes a consequential decision.
- No raw workforce data, credentials, or controlled content appears in test
  fixtures, logs, snapshots, or failure output.

## Evidence and gates

Each task contract supplies validation commands after the application
dependency manifest is approved. A pull request records commands and results.
Independent QA reviews acceptance criteria and negative tests before human
approval. Critical authorization, record-integrity, or AI-boundary defects block
the task; prototype completion does not waive production reviews.
