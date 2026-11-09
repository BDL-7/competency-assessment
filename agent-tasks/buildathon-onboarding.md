# BR-01 Buildathon Onboarding

## Task contract

| Field | Value |
| --- | --- |
| Task ID | BR-01 |
| Tracking issue | #17 |
| Owner Agent | Orchestrator / Engineering Lead |
| Goal | Consolidate onboarding and document the existing local synthetic demonstration accurately. |
| Business Reason | Participants need current entry points without confusing historical planning with implemented or authorized behavior. |
| Required Context | `AGENTS.md`, source authority, product, development, operations, testing, S0-03 and S0-07; existing configuration, demo command, routes and tests. |
| Source-of-Truth Files | `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`, `docs/OPERATIONS.md`, `agent-tasks/s0-03-application-foundation.md`, `agent-tasks/s0-07-local-pilot-ui.md`; implementation is evidence of current capabilities, not new policy authority. |
| Dependencies | Human approval recorded on 2026-11-06; current `dev`; issue #17. BR-02 is independent. |
| Approved Assumptions | Python 3.12; existing one-record, two-version, seven-identity read-only pilot; deterministic mock guides; no deployment. |
| Allowed Files | `README.md`, `docs/README.md`, `docs/DEVELOPMENT.md`, `docs/BUILDATHON.md`, this contract. |
| Review-Only Files | All other repository files, controlled sources, operational workbooks, existing local runtime state and untracked training workbook. |
| Prohibited Actions | Application/schema changes, policy or authorization changes, source approval/publication, deletion, historical approval rewriting, new dependencies, live AI, provisioning or deployment. |
| Expected Outputs | Short root navigation, canonical development guide, current demo runbook and grouped docs index. |
| Acceptance Criteria | Setup/test recipes have one maintained home; demo is explicitly synthetic and read-only with reference date 2027-02-20; pending signatures and unavailable capabilities remain explicit; unknown databases are never reset. |
| Validation Commands | `python scripts/verify_repository.py`, `git diff --check`, changed-link review; BR-04 repeats existing Python 3.12 tests and dedicated local-demo acceptance. |
| Security and Privacy Considerations | Synthetic values only; no controlled content, workforce data, secrets or untracked workbook publication. |
| Definition of Done | Related documentation matches approved behavior; current validation and independent review are recorded; draft PR targets `dev`; requester merge approval remains separate. |
| Handoff Format | Exact files, commands/results, independent review, outstanding gates and next owner. |
| Stop Conditions | Missing/conflicting authority, overlapping leases, sensitive content, or a change outside the allowed files. |
| Human Approval Gate | Requester approved onboarding/documentation plus the public presentation fix and synthetic-demo validation on 2026-11-06. No merge, protected cleanup or deployment authorization. |
| Path Lease Owner and Expiry | Exclusive Orchestrator lease on the five allowed files, expires when #17 is merged or abandoned. |

## Validation and handoff

- Changed paths: `README.md`, `docs/README.md`, `docs/DEVELOPMENT.md`,
  `docs/BUILDATHON.md`, and this contract. Installation/test commands have one
  maintained home; the demo runbook links to it.
- A fresh ignored Python 3.12 environment installed the existing development
  lockfile. Full suite: 77 passed; dependency check: no broken requirements.
  No dependency manifest changed.
- Dedicated demo initialization and repeat initialization passed. After browser
  requests: one assessment, two versions, zero signatures, seven users and no
  foreign-key violations. A separate empty database passed two schema upgrades;
  all 20 application tables remained empty.
- Exact minimal healthy JSON and all six routes passed. Both native browser
  sample POSTs returned their distinct synthetic citations; unsupported and
  500-character questions escalated without page overflow at 360px/32px text.
  These were DOM form submissions, not verified keyboard activation.
- BR-05 corrected eight reproduced enlarged-text overflow cases. All 48 final
  six-screen/width/text checks passed with table-local scrolling and no captured
  page errors or external requests.
- Programmatic focus succeeded on 57 controls, but the browser input bridge did
  not dispatch Tab/Enter. Manual keyboard activation/visible-focus review remains
  an explicit limitation, not a claimed pass. Specialist conformance and
  operational-use/deployment review remain separate gates.
- Changed-document local links and whitespace checks passed. Final staged
  repository verification passed for all 133 tracked files; staged whitespace
  checks passed. The untracked training workbook was not staged.
- Independent read-only review of all 13 changed/new paths reported no significant
  issues. The configured custom reviewer could not launch; the standard
  independent code reviewer completed the review. It did not rerun browser checks
  or the clean Python 3.12 suite; the implementing agent supplied that evidence.
- Historical task evidence and protected/reference materials remain unchanged.
  No deletion, controlled-source publication, laboratory-policy change, merge
  or deployment is authorized. Next owner: requester reviewing the draft PR.
