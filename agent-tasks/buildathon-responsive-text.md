# BR-05 Responsive Text Repair

## Task contract

| Field | Value |
| --- | --- |
| Task ID | BR-05 |
| Tracking issue | #17 |
| Owner Agent | Flask Application presentation; Orchestrator integration |
| Goal | Repair page-wide overflow reproduced during BR-04 at 200% root text. |
| Business Reason | The existing six-screen demo must remain readable at narrow widths and enlarged text without clipping or hiding content. |
| Required Context | `AGENTS.md`, `docs/SOURCE_AUTHORITY.md`, `docs/PRODUCT.md`, `agent-tasks/s0-07-local-pilot-ui.md`, current stylesheet and synthetic browser results. |
| Source-of-Truth Files | Existing local pilot templates and stylesheet; S0-07 behavior and visual boundaries remain unchanged. |
| Dependencies | BR-04 reproduced eight enlarged-text overflow failures; requester delegated the corrective scope decision after escalation. |
| Approved Assumptions | Synthetic loopback validation only; preserve normal layout, all record and guide behavior, system fonts and existing colors. |
| Allowed Files | `app/static/styles.css`, this contract. |
| Review-Only Files | All other repository files, controlled sources, operational workbooks and existing local state. BR-01 owns related runbook updates. |
| Prohibited Actions | Hidden/clipped overflow workarounds, text-size reduction, new packages, template or application changes, schema/data/authorization changes, live AI and deployment. |
| Expected Outputs | Inherited emergency word wrapping and wrapping participant rows, with current browser regression evidence. |
| Acceptance Criteria | All six screens at 360/390/768/1024px and 16/32px root text have no page-wide horizontal overflow; table overflow remains local; content and mock forms remain available. |
| Validation Commands | Existing Python 3.12 web/full pytest suite; integrated-browser layout checks and guide POST checks; repository verifier and `git diff --check`. |
| Security and Privacy Considerations | Public synthetic content only; no external requests or business-record mutation. |
| Definition of Done | Exact browser threshold checks pass, existing tests pass, independent review is recorded and the draft PR targets `dev`; specialist sign-off and merge remain separate. |
| Handoff Format | Exact changed paths, baseline/final browser results, test results, review and outstanding gates. |
| Stop Conditions | Application behavior, controlled authority, new dependencies or edits outside the lease become necessary. |
| Human Approval Gate | After the overflow finding and explicit scope choices, the requester responded: "you are the expert, do whatever works best". The Orchestrator selects only this bounded presentation correction. |
| Path Lease Owner and Expiry | Exclusive BR-05 lease on the two allowed files; historical S0-07 lease ended with its merged PR. Expires when #17 is merged or abandoned. |

## Validation and handoff

Baseline inspection reproduced emergency-word-width overflow in branding,
inline links and breadcrumbs, and participant text extending past its narrow
assignment panel. Eight of 24 enlarged-text page checks failed; all 24 normal-text
checks passed. No business behavior change is needed.

- Changed paths: `app/static/styles.css` and this contract. Only two existing
  stylesheet declarations changed: body emergency wrapping and participant-row
  wrapping. No size reduction, hidden-overflow workaround or breakpoint redesign.
- Final integrated-browser regression: 48 passed, comprising six screens at
  360/390/768/1024px and exactly 16/32px root text. Page scroll width never exceeded
  viewport client width by more than one pixel. Table overflow remained local.
  No captured page errors or external requests occurred.
- Both guides retained their sample synthetic citations and unsupported-question
  escalation through native DOM form submissions. Exactly 500-character
  unbroken questions also passed at 360px/32px without page-wide overflow.
- Full Python 3.12 regression suite: 77 passed; pinned dependency check passed.
  Browser requests preserved the exact one-assessment/two-version/zero-signature
  fixture and valid foreign keys.
- Programmatic focus inspection is not keyboard acceptance. The browser input
  bridge did not dispatch Tab/Enter; manual activation/visible-focus checks and
  specialist accessibility conformance remain explicitly outstanding.
- Independent read-only review of the complete 13-path change reported no
  significant issues. The configured custom reviewer was unavailable; the
  standard reviewer completed the review without rerunning browser/tests or
  claiming specialist conformance sign-off.
- Final staged repository verification passed for all 133 tracked files;
  staged whitespace checks passed. No merge or deployment occurred;
  next owner is the draft-PR requester.
