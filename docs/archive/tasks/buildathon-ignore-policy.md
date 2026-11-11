# BR-06 Safe Local Ignore Policy

## Task contract

| Field | Value |
| --- | --- |
| Task ID | BR-06 |
| Tracking issue | #17; follow-up to draft PR #18 |
| Owner Agent | Orchestrator / Engineering Lead |
| Goal | Ignore local training workbooks and presentation release outputs without untracking or deleting files. |
| Business Reason | Safe onboarding should not leave local binary inputs or generated releases as accidental staging candidates. |
| Required Context | `AGENTS.md`, source authority, product, current ignore rules, data classification, public presentation README and repository verifier. |
| Source-of-Truth Files | `data/DATA_CLASSIFICATION.md`, existing public presentation source/build contract and `.gitignore`. |
| Dependencies | Existing issue-linked branch and dev-targeted draft PR; requester selected `safe-ignore`. |
| Approved Assumptions | Keep all currently tracked reference/source files; existing generated directories already cover default builder outputs. |
| Allowed Files | `.gitignore`, `data/DATA_CLASSIFICATION.md`, this contract. |
| Review-Only Files | All other files; especially training workbook contents, controlled sources, historical evidence and tracked knowledge-format comparisons. |
| Prohibited Actions | File deletion, untracking, broad HTML/image/document ignore rules, source publication, application/schema/authorization changes, new dependencies, merge or deployment. |
| Expected Outputs | Targeted workbook/PDF/ZIP ignore rules and documentation of tracked-source preservation. |
| Acceptance Criteria | Local training XLSX and presentation PDF/ZIP outputs are ignored; all currently tracked paths remain unignored by the effective rules; public example HTML/JS/CSS/assets and synthetic fixtures remain eligible for tracking; no local file is deleted. |
| Validation Commands | `git check-ignore --no-index --stdin` with positive and negative paths; repository verifier; `git diff --check`; exact staged path and PR-base checks. |
| Security and Privacy Considerations | Inspect filenames only, not local workbook contents. Ignore rules are not a security boundary and do not remove previously tracked files. |
| Definition of Done | Exact ignore/non-ignore behavior validated, only approved paths committed, existing draft PR updated, current CI results recorded and remaining owner decisions explicit. |
| Handoff Format | Exact changed paths, validation results, retained files, PR and unresolved gates. |
| Stop Conditions | A tracked path becomes ignored, source classification is ambiguous, or cleanup requires deleting/untracking protected files. |
| Human Approval Gate | Requester selected `safe-ignore`; tracked reference classification/untracking remains outside this task. |
| Path Lease Owner and Expiry | Exclusive Orchestrator lease on the three allowed paths; no overlap with BR-01/BR-02/BR-05. Expires when #17 is merged or abandoned. |

## Validation and handoff

- Exact NUL-delimited `git check-ignore --no-index` validation passed for 10
  positive paths and 14 negative source/reference paths. Windows text-mode stdin
  adds carriage returns, so the check uses binary NUL-delimited input/output.
- All 133 previously tracked paths remain eligible under the effective rules,
  including the public HTML/JS/CSS/assets, knowledge-format comparisons and
  synthetic workbook fixture path. The existing local training workbook remains
  on disk and is now ignored.
- Repository verification passed for 134 tracked files after staging only the
  three allowed paths; staged whitespace checks passed.
- No runtime behavior changed; existing runtime tests are not rerun for this
  configuration/documentation-only follow-up. Published CI results are checked
  for the updated draft head. No additional independent specialist review is
  claimed or required for these ignore-only changes.
- Requester draft-PR review, tracked-reference owner decisions and existing
  manual keyboard/specialist gates remain. No files were untracked or deleted.
