# S0-01 Synthetic Scenario and Acceptance Criteria

## 1. Task contract

| Field | Value |
| --- | --- |
| Task ID | S0-01 |
| Tracking issue | GitHub issue #5 |
| Owner Agent | Product and Laboratory Domain Agent |
| Goal | Define one entirely synthetic, independently testable Non-CLIA competency-assessment scenario for the first coding sprint. |
| Business Reason | Give S0-02 and later implementation tasks an approved behavioral target without inventing laboratory policy or exposing controlled information. |
| Required Context | Phase 0 product, source-authority, workflow, authorization, domain-model, AI-boundary, and testing documents; authorized review-only copies of the Project Plan, Architecture Guide, and approved Non-CLIA form. |
| Source-of-Truth Files | `docs/SOURCE_AUTHORITY.md`; `docs/PRODUCT.md`; `docs/WORKFLOW.md`; `docs/AUTHORIZATION.md`; `docs/DOMAIN_MODEL.md`; `docs/AI_BOUNDARY.md`; `docs/TESTING.md`; the governing Project Plan; the Architecture Guide; and controlled sources within their stated authority. |
| Dependencies | Merged Phase 0 foundation PR #4. |
| Approved Assumptions | The approved prototype baseline plus the requester-delegated S0-01 decisions recorded in section 9. Production-policy decisions remain unresolved in section 10. |
| Allowed Files | `agent-tasks/s0-01-synthetic-scenario.md` only. |
| Review-Only Files | `AGENTS.md`; `docs/SOURCE_AUTHORITY.md`; `docs/PRODUCT.md`; `docs/WORKFLOW.md`; `docs/AUTHORIZATION.md`; `docs/DOMAIN_MODEL.md`; `docs/AI_BOUNDARY.md`; `docs/TESTING.md`; `docs/SOURCE_MANIFEST.md`; the governing Project Plan; the Architecture Guide; the approved Non-CLIA form; and other controlled sources. |
| Prohibited Actions | Application code, schema, models, migrations, packages, dependency changes, executable tests, Azure resources, assistant implementation, production data, controlled-content publication, or laboratory-policy decisions. |
| Expected Outputs | Synthetic scenario, approved-rule summary, positive and negative acceptance criteria, unresolved decision list, and human-approval record. |
| Acceptance Criteria | Sections 6 and 7; approval and definition-of-done requirements also apply. |
| Validation Commands | `python scripts/verify_repository.py`; `git diff --check`; `git status --short`. |
| Security and Privacy | Use invented identifiers and values only. Do not reproduce controlled wording, real workforce data, source rows, catalog values, secrets, or operational configuration. |
| Definition of Done | All requirements in the definition-of-done section are satisfied and recorded. |
| Handoff Format | Exact file, validation, assumption decisions, unresolved decisions, approvals, and downstream readiness described in the handoff section. |
| Stop Conditions | All conditions in the stop-conditions section apply. |
| Human Approval Gate | On 2026-09-08, the Project Requester explicitly delegated the bounded prototype decisions in section 9 to Codex and authorized those decisions to be recorded. This delegation does not resolve production policy. An Approved-Source Owner must still approve the assistant source and supported question before S0-04B. |
| Path Lease Owner and Expiry | Product and Laboratory Domain Agent; `agent-tasks/s0-01-synthetic-scenario.md`; expires when S0-01 is merged or abandoned. |

### Validation commands

```text
python scripts/verify_repository.py
git diff --check
git status --short
```

### Definition of done

S0-01 is complete only when:

1. This artifact contains no real people, operational records, governed catalog values, or copied controlled text.
2. Every criterion is observable and assigned a stable identifier.
3. Approved rules are separated from prototype-only assumptions and unresolved decisions.
4. Product Owner, Laboratory SME, and other required decisions are recorded in the approval section.
5. The assistant source/question dependency is either approved by its owner or remains an explicit blocker to S0-04B.
6. Repository validation passes.
7. Independent review confirms that the criteria do not expand scope or weaken a control.

### Stop conditions

Stop S0-01 or the affected downstream work when:

- a required behavior needs laboratory judgment that has not been recorded;
- governing sources conflict within their areas of authority;
- an operational or controlled value would need to be published;
- a role, state, field, service, tool, or platform outside the approved baseline is requested;
- another task holds the writable path;
- the assistant lacks an acquired, active, approved, versioned, access-permitted source for its supported question.

### Handoff format

The S0-01 handoff reports:

- the exact file changed;
- validation commands and results;
- approved and rejected prototype assumptions;
- unresolved decisions and their owners;
- the approval record;
- whether S0-02 may begin;
- whether the assistant track remains blocked.

## 2. Authority and interpretation

This artifact translates the current prototype baseline into testable behavior. It does not create laboratory policy and does not reproduce controlled-document wording.

| Source label | Authority used here | Status for S0-01 |
| --- | --- | --- |
| Competency Assessment Tracker Project Plan | Product scope, roles, workflow direction, prototype outcome, and approval boundaries | Governing product direction |
| App Architecture and Implementation Guide | Flask/Azure boundaries, system-of-record rule, authorization, transaction expectations, and assistant isolation | Governing technical baseline |
| Approved Non-CLIA form V04 | Provisional prototype concepts for assessment context, observed activities, outcome recording, remedial-action prompt, comments, and two signature roles | Review-only starting baseline; currency must be revalidated before production |
| `docs/PRODUCT.md` | First-sprint scope, exclusions, success conditions, and AI prohibitions | Approved prototype baseline |
| `docs/WORKFLOW.md` | Sequence, states, allowed transitions, signature order, locking, renewal, and idempotency controls | Approved prototype baseline |
| `docs/AUTHORIZATION.md` | Roles, scopes, permitted actions, and denials | Approved prototype baseline |
| `docs/AI_BOUNDARY.md` | Approved-source, citation, escalation, access, logging, and no-mutation boundary | Approved prototype baseline |
| `docs/TESTING.md` | Required positive, negative, authorization, integrity, assistant, and accessibility evidence | Approved testing baseline |

When this artifact is more specific than a governing source, the added detail is labeled as a prototype-only assumption requiring human approval.

## 3. Scenario outcome

Demonstrate one synthetic Non-CLIA assessment from configuration and assignment through an overdue condition, assessment documentation, returned correction, documented follow-up, sequential signatures, finalization and locking, artifact metadata, audit, renewal, and role-scoped reporting. In the separate read-only assistant boundary, demonstrate one supported question only after its source is approved and one unsupported-question escalation.

The application records and controls the workflow. The Assessor records outcomes. The application does not calculate competency or make a pass/fail decision.

## 4. Synthetic scenario data

All names, identifiers, dates, and values below are invented for testing. They do not represent people, teams, test systems, or records at CDC.

### 4.1 Participants and access

| Synthetic ID | Display label | Scenario relationship or role | Scope |
| --- | --- | --- | --- |
| `SYN-EMP-001` | Testing Person One | Employee / Testing Personnel | Own assignment and assessment only |
| `SYN-LEAD-001` | Team Lead One | Assigned Team Lead | Synthetic Team Alpha only |
| `SYN-ASR-001` | Assessor One | Assessor | Explicitly assigned assessment only |
| `SYN-TS-001` | Technical Supervisor One | Technical Supervisor / final signer | Explicitly assigned assessment only |
| `SYN-ADM-001` | SQUAD Admin One | SQUAD Admin | Approved synthetic configuration scope |
| `SYN-PLAT-001` | Platform Admin One | Platform Admin | Audited diagnostic/read support only |
| `SYN-OUT-001` | Unassigned Assessor One | Assessor on a different synthetic team | No access to this assessment |

Participant relationships remain separate. No role is inferred from team membership or administrative access.

### 4.2 Configuration and record identifiers

| Item | Synthetic value | Interpretation |
| --- | --- | --- |
| Team | `SYN-TEAM-ALPHA` | Invented team; not a real organizational unit |
| Test system | `SYN-TEST-SYSTEM-01` | Invented test-system placeholder; not an approved catalog value |
| Process grouping | `SYN-PROCESS-01` | Invented process placeholder; not a governed crosswalk |
| Assignment | `SYN-ASGN-001` | Stable assignment identity |
| Assessment | `SYN-ASM-001` | Stable assessment identity |
| Assessment version | `SYN-ASMV-001` initially; later version identity determined by S0-02 | Signatures must bind to one exact immutable version |
| Synthetic artifact | `SYN-ARTIFACT-001` | Metadata and a deterministic test hash only; no controlled form content |
| Correlation identifier | `SYN-CORR-001` | Connects command outcome and audit evidence |
| Initial cycle basis date | `2026-02-15` | Synthetic configuration input; not a production due-date rule |
| Expected initial due date | `2027-02-15` | Basis date plus the proposed 12-calendar-month prototype interval |
| Finalized completion date | `2027-02-20` | Synthetic completion date used for the renewal example |
| Prototype interval | 12 calendar months | Approved for this synthetic S0-01 scenario only |
| Expected next due date | `2028-02-20` | Completion date plus the proposed prototype interval |

### 4.3 Scenario-required assessment concepts

For this scenario only, the Assessor records values for the following public-safe concepts derived from the provisional form baseline:

1. assessment context and type;
2. process being assessed;
3. assessment method;
4. synthetic specimen context;
5. observed testing and instrument context;
6. problem-solving evidence;
7. protocol outcome recorded by the Assessor;
8. whether remedial action is required and its description when required;
9. comments;
10. Testing Personnel and Technical Supervisor signatures.

This list does not declare the production required-field set. Field cardinality, validation detail, and physical representation belong to later approved tasks.

### 4.4 Synthetic assessment branch

The Assessor records one scenario element, `SYN-ELEMENT-03`, as unsuccessful and indicates that remedial action is required. On the first submission, the required follow-up description is absent. Under approved prototype assumption `S0-01-A04`, the application moves the record to `Returned` without making a competency determination. The Assessor then records a synthetic follow-up description and resubmits.

For S0-01, "follow-up documented" means only that the approved scenario-required description is present and attributable. It does not mean that the application or AI has determined remediation successful or closed.

## 5. Canonical scenario flow

### Step 1 - Configure

`SYN-ADM-001` creates or selects the synthetic team, people, explicit role scopes, test-system placeholder, process grouping, interval, and participant relationships needed by the scenario.

Expected evidence:

- configuration is attributable;
- SQUAD Admin does not become an Assessor or signer;
- Platform Admin does not obtain configuration authority;
- all values are synthetic.

### Step 2 - Schedule and assign

Using the approved synthetic configuration, the application calculates the due date as `2026-02-15` plus 12 calendar months, creates `SYN-ASGN-001` with the expected due date `2027-02-15`, links the four participant relationships separately, and exposes the work item only to authorized scopes. This arithmetic is a prototype-only assumption under `S0-01-A01`, not a production scheduling rule.

Expected state sequence:

```text
Scheduled -> Assigned
```

### Step 3 - Create notification events

The application demonstrates upcoming-due, due, overdue, submitted, signature-required, and completed notification events. Delivery uses a non-delivering test adapter. Message content contains no assessment result or unnecessary sensitive detail.

Notification-event creation is distinct from delivery attempts. A retry does not duplicate the logical event.

### Step 4 - Become overdue without replacing state

At a synthetic clock time after `2027-02-15`, the assignment reports `Overdue` while preserving its active workflow state.

### Step 5 - Document the assessment

Only `SYN-ASR-001` begins and documents the assigned assessment. The application captures the Assessor's recorded results and evidence; it does not derive competency or pass/fail from them.

Expected state sequence:

```text
Assigned -> In progress -> Submitted
```

### Step 6 - Enforce follow-up documentation

The first submission records `SYN-ELEMENT-03` as unsuccessful and remedial action as required but omits the scenario-required follow-up description. The submission cannot proceed to signature.

The record returns for correction, the Assessor adds the synthetic follow-up description, and the Assessor resubmits.

Expected state sequence:

```text
Submitted -> Returned -> In progress -> Submitted
```

### Step 7 - Testing Personnel review and signature

After the approved completeness checks pass, the record moves to `Awaiting Testing Personnel signature`. `SYN-EMP-001` reviews and signs the exact assessment version. The signature is the prototype acknowledgement event; no separate acknowledgement record is introduced.

Expected state sequence:

```text
Submitted -> Awaiting Testing Personnel signature
           -> Awaiting Technical Supervisor signature
```

### Step 8 - Technical Supervisor review and signature

`SYN-TS-001` reviews the exact version already signed by Testing Personnel and provides the final signature. Other roles cannot provide that signature.

### Step 9 - Finalize and lock

After both valid signatures and approved completeness checks, the system finalizes the exact version and records, as one consistent outcome:

- finalized version state;
- both version-bound signatures;
- synthetic artifact metadata and integrity hash;
- renewal result;
- completed notification event;
- attributable audit evidence.

Expected state sequence:

```text
Awaiting Technical Supervisor signature -> Finalized -> Renewal scheduled
```

No normal action updates or deletes the finalized version. Amendment behavior remains outside this scenario because the complete amendment procedure requires separate human approval.

### Step 10 - Report

Authorized users see only their approved role-scoped status. The scenario demonstrates Employee own-history, assigned-team, assigned-final-signer, approved administrative, and diagnostic/read-only support scopes. Center/quality viewer access is excluded.

### Step 11 - Ask supported and unsupported assistant questions

The assistant path is separate and read-only.

- Proposed supported-question category: explain the approved review and signature sequence before finalization.
- Unsupported-question category: request an out-of-scope CLIA rule or a competency decision.

The supported example may not be executed until an Approved-Source Owner identifies an acquired, active, versioned, access-permitted source and approves the question for the prototype. The unsupported example must state that approved evidence or authority is unavailable and direct the user to an SME. Neither response may change an application record.

## 6. Positive acceptance criteria

| ID | Given | When | Then |
| --- | --- | --- | --- |
| `S0-01-P01` | Active synthetic users and explicit role scopes | SQUAD Admin configures the scenario | Configuration succeeds, is attributable, and preserves separate participant relationships. |
| `S0-01-P02` | Approved synthetic basis date `2026-02-15` and prototype interval of 12 calendar months | SQUAD Admin schedules and assigns the work | The application calculates `2027-02-15`, creates one assignment in the approved state, and provides Employee and Assigned Team Lead work visibility. |
| `S0-01-P03` | A scheduled notification trigger | The trigger is processed twice with the same idempotency identity | One logical notification event exists; attempts are recorded separately. |
| `S0-01-P04` | An active assignment after its due date | Status is requested | The active state remains intact and `Overdue` is reported as a condition. |
| `S0-01-P05` | An explicitly assigned Assessor | The Assessor begins and documents the assessment | The record enters `In progress`, stores attributable scenario data, and makes no calculated competency decision. |
| `S0-01-P06` | An unsuccessful scenario element requiring follow-up with no description | The Assessor submits | Subject to approved assumption `S0-01-A04`, the record moves to `Returned`, cannot advance to signature, and returns an actionable validation result. |
| `S0-01-P07` | A returned record | The assigned Assessor adds the required synthetic follow-up description and resubmits | The record returns to `Submitted` without losing prior attributable history. |
| `S0-01-P08` | A complete submitted exact version | Testing Personnel reviews and signs | One Testing Personnel signature binds to that exact version and the state advances to final-signature review. |
| `S0-01-P09` | The exact version with a valid Testing Personnel signature | The assigned Technical Supervisor signs | One final signature binds to the same version. |
| `S0-01-P10` | Both valid signatures and approved completeness conditions | Finalization is requested | The version is finalized and locked; artifact metadata, audit, renewal, and completion-event outcomes are consistently recorded. |
| `S0-01-P11` | Finalized completion date `2027-02-20` and approved prototype interval of 12 calendar months | Renewal is calculated | The explainable result is `2028-02-20`, subject to approval of assumption `S0-01-A01`. |
| `S0-01-P12` | A finalized record | Authorized users request status | Each receives only own, assigned, administrative, or audited diagnostic/read information permitted by role and scope. |
| `S0-01-P13` | An acquired and approved assistant source, approved supported question, and permitted authenticated user | The user asks the supported question | The assistant returns a bounded answer with a usable source citation and records source/prompt/model versions plus a data-minimized outcome. |
| `S0-01-P14` | No approved evidence for the requested CLIA or competency-decision question | The user asks the unsupported question | The assistant states the limitation, directs the user to an SME, and performs no consequential action. |
| `S0-01-P15` | The assignment reaches the approved upcoming-due trigger | Notification processing runs | One upcoming-due logical event is recorded for the intended recipient and template using the stable assessment and trigger identity. |
| `S0-01-P16` | The assignment reaches its due date | Notification processing runs | One due logical event is recorded for the intended recipient and template using the stable assessment and trigger identity. |
| `S0-01-P17` | The active assignment passes its due date | Notification processing runs | One overdue logical event is recorded without replacing the active workflow state. |
| `S0-01-P18` | The Assessor submits the assessment | Notification processing runs | One submitted logical event is recorded for the intended recipient and template. |
| `S0-01-P19` | The record enters `Awaiting Testing Personnel signature` | Notification processing runs | One signature-required logical event is recorded for `SYN-EMP-001`. |
| `S0-01-P20` | Testing Personnel signs and the record enters `Awaiting Technical Supervisor signature` | Notification processing runs | One signature-required logical event is recorded for `SYN-TS-001`. |
| `S0-01-P21` | Finalization commits successfully | Notification processing runs | One completed logical event is recorded and remains consistent with the finalized outcome. |
| `S0-01-P22` | Any scenario notification event is prepared | Its non-delivering test payload is inspected | The payload contains only the intended recipient reference, approved template reference, stable record reference, trigger identity, and minimum scheduling/status context; it excludes assessment results and unnecessary sensitive content. |
| `S0-01-P23` | A logical notification event exists and its first delivery attempt fails | The same event is retried | A new attempt outcome is attributable to the existing event; no second logical event, state transition, or assessment mutation occurs. |
| `S0-01-P24` | The representative configure-through-report workflow is available | The authorized scenario participants complete their respective workflow portions using only a keyboard | Every required control and action is reachable and operable without pointer input, in a logical order. |
| `S0-01-P25` | A keyboard user moves through the representative workflow | Focus changes | Every interactive control has a visible focus indicator and focus is not lost or trapped unexpectedly. |
| `S0-01-P26` | A page contains inputs, instructions, validation errors, or status messages | Assistive-technology relationships are inspected and an invalid submission is exercised | Inputs have programmatic labels; instructions, errors, and status messages are associated with the affected control or region and are programmatically exposed. |
| `S0-01-P27` | A role-scoped status or report view is rendered | Its structure and visual communication are inspected | Headings and table relationships are programmatically determinable, and state, error, or outcome meaning is not conveyed by color alone. |
| `S0-01-P28` | The representative workflow is assessed against the WCAG 2.2 Level AA prototype baseline approved under `S0-01-A09` | Automated and manual accessibility checks run | Text, controls, focus behavior, and meaningful graphical elements meet the applicable Level AA success criteria with no unresolved failure. |
| `S0-01-P29` | `SYN-EMP-001` requests status | Authorization is applied | Only that employee's own assignment and assessment status is returned. |
| `S0-01-P30` | `SYN-LEAD-001` requests status or an allowed export | Authorization is applied | Only records within `SYN-TEAM-ALPHA` and the lead's approved assigned-team scope are returned. |
| `S0-01-P31` | `SYN-TS-001` requests work awaiting final review | Authorization is applied | Only assessments explicitly assigned to that Technical Supervisor are returned. |
| `S0-01-P32` | `SYN-ADM-001` requests approved configuration or administrative reporting | Authorization is applied | Only approved administrative-scope information is returned, with no assess or sign capability inferred. |
| `S0-01-P33` | `SYN-PLAT-001` performs an authorized diagnostic read with a support purpose or reference | Authorization is applied | Only the minimum diagnostic/read information is returned, the access is attributed and audited, and no business action is enabled. |
| `S0-01-P34` | Any scenario action listed in section 8 succeeds or is denied | Audit evidence is inspected | One append-only observation identifies actor, action, entity, time, outcome, and correlation identifier while minimizing sensitive content. |
| `S0-01-P35` | Audit observations already exist | A normal workflow or administrative action attempts to update or delete them | The observations remain unchanged; only an authorized retention/disposition mechanism outside this scenario could affect them. |

## 7. Negative acceptance criteria

| ID | Attempt | Required result |
| --- | --- | --- |
| `S0-01-N01` | `SYN-OUT-001` views or edits `SYN-ASM-001` | Denied before record content is returned; denial is audited without sensitive content. |
| `S0-01-N02` | `SYN-PLAT-001` assigns, documents, signs, finalizes, or changes business configuration | Denied. Platform Admin retains only attributable diagnostic/read support access. |
| `S0-01-N03` | `SYN-ADM-001` documents or signs because of administrative membership | Denied unless that person has a separate, explicit, effective participant relationship; none exists in this scenario. |
| `S0-01-N04` | Testing Personnel signs another employee's record or a stale version | Denied; no signature or workflow transition is recorded. |
| `S0-01-N05` | Technical Supervisor signs before Testing Personnel | Denied; state and version remain unchanged except for attributable denial evidence. |
| `S0-01-N06` | An unassigned Technical Supervisor signs | Denied before any signature is created. |
| `S0-01-N07` | The record advances to signature while required follow-up documentation is absent | Denied; no pass/fail or remediation-completion decision is inferred. |
| `S0-01-N08` | A later edit is attempted after a version has been signed | The signed version remains immutable, and its signatures do not carry forward to any later version; the exact return/new-version mechanics remain a decision for S0-02 under `S0-01-D05`. |
| `S0-01-N09` | Finalization is requested with a missing signature, stale version, or unmet approved completeness condition | Denied atomically; no finalized artifact, renewal, or completed event is reported. |
| `S0-01-N10` | The same signature, notification, finalization, audit effect, or renewal command is retried with the same identity | No duplicate logical effect is created. |
| `S0-01-N11` | A normal edit or delete targets the finalized version | Denied. The original remains retained and unchanged. |
| `S0-01-N12` | A user requests cross-team status or an unauthorized export | Denied before out-of-scope rows or documents are returned; the attempt is audited. |
| `S0-01-N13` | A notification body attempts to include an assessment result or unnecessary sensitive detail | The unsafe payload is rejected or excluded from delivery. |
| `S0-01-N14` | The assistant receives no approved source, a retired source, a restricted source, conflicting sources, or insufficient evidence | It does not answer as controlled policy and returns the approved limitation/escalation outcome. |
| `S0-01-N15` | A prompt asks the assistant to score, approve remediation, sign, send email, change access, publish a source, or mutate a record | The request is refused or safely redirected; no consequential tool or credential is available. |
| `S0-01-N16` | A source or user message contains prompt-injection instructions that conflict with the assistant boundary | Boundary and source-access rules remain effective; the instructions do not grant capabilities or suppress citations/escalation. |
| `S0-01-N17` | A Center/quality viewer, Power BI client, CLIA workflow, operational migration, or production data path is requested | The request is outside S0-01 and the first coding sprint; no behavior is added. |

## 8. Required audit observations

Later executable tests must be able to observe appropriate audit evidence for:

- configuration and assignment;
- allowed and denied state-changing actions;
- denied record access;
- assessment submission and return;
- follow-up documentation;
- both signatures and the exact version;
- finalization and locking;
- artifact metadata action;
- notification event and attempt outcomes;
- renewal calculation;
- report or export access;
- Platform Admin competency-record access with support purpose or reference when available;
- assistant source, prompt, model, and outcome versions without unnecessary question or source text.

Audit observations identify actor, action, entity, time, outcome, and correlation identifier while minimizing sensitive content.

## 9. Prototype-only assumptions and recorded decisions

On 2026-09-08, the Project Requester explicitly authorized Codex to select and record the bounded S0-01 prototype decisions. The approvals below apply only to the synthetic first-sprint scenario. They do not establish production laboratory policy, operational authorization rules, controlled-source approval, or deployment approval.

| ID | Proposed assumption | Why it is needed | Required approver | Decision |
| --- | --- | --- | --- | --- |
| `S0-01-A01` | Use 12 calendar months as the synthetic interval; calculate the initial due date as `2026-02-15` plus 12 calendar months = `2027-02-15`, and renewal as finalized completion date `2027-02-20` plus 12 calendar months = `2028-02-20`, for this prototype scenario only. | Produces deterministic scheduling and renewal examples without declaring production policy. | Product Owner and Laboratory SME | Approved 2026-09-08 under explicit Project Requester delegation; prototype only. |
| `S0-01-A02` | Treat the assessment concepts in section 4.3 as scenario-required inputs, without declaring the production required-field set. | Enables completeness criteria for the prototype. | Laboratory SME | Approved 2026-09-08 under explicit Project Requester delegation; prototype only. |
| `S0-01-A03` | Treat an unsuccessful element plus a documented remedial-action description as sufficient to continue this demonstration; do not represent remediation as completed or approved. | Exercises the approved follow-up gate without inventing completion evidence. | Laboratory SME | Approved 2026-09-08 under explicit Project Requester delegation; no remediation-completion meaning. |
| `S0-01-A04` | Use the approved `Returned` transitions for a missing follow-up description and pre-finalization correction. | Exercises a negative and recovery branch. | Product Owner and Laboratory SME | Approved 2026-09-08 under explicit Project Requester delegation; prototype only. |
| `S0-01-A05` | Use a non-delivering notification adapter and synthetic clock while demonstrating all approved first-sprint event types. | Avoids official email delivery and unapproved production cadence. | Product Owner | Approved 2026-09-08 under explicit Project Requester delegation; no external delivery. |
| `S0-01-A06` | Use mocked identities and explicit role assignments if development Entra access is unavailable. | Keeps authorization tests deterministic without changing the approved Entra direction. | Product Owner and Identity/Platform Owner | Approved 2026-09-08 under explicit Project Requester delegation; fallback only when development Entra is unavailable. |
| `S0-01-A07` | Use a synthetic artifact containing no controlled form content; retain only scenario metadata and a deterministic integrity hash. | Exercises artifact metadata and integrity without publishing controlled material. | Product Owner and Records/Privacy Reviewer | Approved 2026-09-08 under explicit Project Requester delegation; synthetic content only. |
| `S0-01-A08` | Use the supported-question category in Step 11 only after a named source owner approves one active source and the audience's access. | Provides a bounded assistant test without assuming the current link index or controlled form is assistant-approved. | Approved-Source Owner | Not approved; remains blocked because no acquired, active, versioned, access-permitted source and named source-owner approval are recorded. |
| `S0-01-A09` | Use WCAG 2.2 Level AA as the accessibility baseline for the synthetic prototype and apply its applicable contrast and interaction success criteria; do not treat this as the production conformance decision. | Makes the prototype accessibility criteria executable while preserving the production decision in `S0-01-D12`. | Product Owner and Accessibility Reviewer | Approved 2026-09-08 under explicit Project Requester delegation; prototype only. |

These decisions authorize only the stated synthetic behavior. A rejected, unavailable, or production-level decision does not authorize an agent to choose a substitute.

## 10. Unresolved decisions and downstream ownership

| ID | Unresolved decision | Blocks | Owner |
| --- | --- | --- | --- |
| `S0-01-D01` | Final production required fields and assessment elements | MVP rules and production validation | Laboratory Owner |
| `S0-01-D02` | Production pass/fail recording and meaning | MVP rules and reporting | Laboratory Owner |
| `S0-01-D03` | Evidence that proves remedial action complete and who may close it | Remediation completion behavior | Laboratory Owner |
| `S0-01-D04` | Production permitted intervals, due-date basis, date arithmetic, and renewal exceptions | Production scheduling and renewal | Product and Laboratory Owners |
| `S0-01-D05` | Complete return and signed-version invalidation procedure | Detailed workflow and S0-02 interface behavior | Product and Laboratory Owners |
| `S0-01-D06` | Complete amendment/repair initiation, approval, and finalization procedure | Finalized-record correction | Product, Records, Security, and Laboratory Owners |
| `S0-01-D07` | Production notification cadence, escalation, templates, retry limits, and delivery service | Production notifications | Notification and Platform Owners |
| `S0-01-D08` | Exact Entra groups, role-claim mapping, access approval, and review cadence | Real identity integration | Identity and Platform Owners |
| `S0-01-D09` | Approved assistant corpus, source metadata, permitted audiences, supported question, and context/cache limit | S0-04B | Approved-Source and EDAV AI Owners |
| `S0-01-D10` | Retention, disposition, artifact recovery, export controls, and operational audit retention | Production readiness | Records, Privacy, Security, and Platform Owners |
| `S0-01-D11` | Current production validity of the 2021 form baseline | Production design and use | Controlled-Document Owner |
| `S0-01-D12` | Production accessibility conformance target, including applicable contrast thresholds and review evidence | Production accessibility validation and production readiness | Product Owner and Accessibility Reviewer |

These decisions are not silently resolved by this prototype.

## 11. S0-02 readiness gate

S0-02 may begin only after:

1. the named owners approve, reject, or revise assumptions `S0-01-A01` through `S0-01-A07` and `S0-01-A09`;
2. the approved scenario retains at least one complete application path and one returned/follow-up path;
3. independent review confirms the criteria match current product, workflow, authorization, and AI boundaries;
4. validation passes and the approved artifact is merged into `dev`.

Assistant interface design in S0-02 may define a blocked/unsupported contract, but implementation of the supported answer in S0-04B remains blocked until `S0-01-A08` is approved with complete source metadata and audience permission.

## 12. Approval record

Requester authorization to draft and publish S0-01 was received on 2026-09-08. Later on the same date, the Project Requester explicitly delegated the bounded prototype decisions to Codex and instructed that the selected decisions be recorded. Codex approved the safe synthetic-development assumptions, preserved every production decision as unresolved, and did not approve an assistant source that does not yet exist within the required governance boundary.

| Reviewer role | Reviewer | Decision | Date | Evidence or conditions |
| --- | --- | --- | --- | --- |
| Product Owner | Codex under explicit Project Requester delegation | Approved for S0-01 prototype | 2026-09-08 | Approved scenario scope and assumptions `A01`, `A04`, `A05`, `A06`, `A07`, and `A09`; no production policy or deployment approval. |
| Laboratory SME | Codex under explicit Project Requester delegation | Approved for S0-01 prototype | 2026-09-08 | Approved assumptions `A01` through `A04` for the synthetic scenario only; no production required-field, competency, or remediation-completion rule. |
| Identity/Platform Owner | Codex under explicit Project Requester delegation | Approved for S0-01 prototype | 2026-09-08 | Approved `A06` as a deterministic fallback only when development Entra access is unavailable. |
| Records/Privacy Reviewer | Codex under explicit Project Requester delegation | Approved for S0-01 prototype | 2026-09-08 | Approved `A07` because the artifact contains only synthetic metadata and a deterministic test hash. |
| Approved-Source Owner | Pending | Pending | Pending | Identify and approve the source, audience, and supported question for `A08`. |
| Accessibility Reviewer | Codex under explicit Project Requester delegation | Approved for S0-01 prototype | 2026-09-08 | Approved WCAG 2.2 Level AA as the prototype baseline under `A09`; production conformance remains `D12`. |
| Independent Reviewer | QA and Independent Review Agent | Approved | 2026-09-08 | Confirmed traceability, notification and accessibility coverage, authorization, record integrity, privacy, AI boundaries, and absence of scope or policy expansion. |

### Approval decision

**Status: Approved for the S0-01 synthetic prototype under explicit Project Requester delegation; pending merge.**

Decision status:

- `S0-01-A01` through `S0-01-A07` and `S0-01-A09` are approved for the synthetic prototype only.
- `S0-01-A08` is not approved and continues to block the supported assistant path in S0-04B.
- all production decisions in section 10 remain unresolved and outside this approval.
- S0-01 becomes complete when this approved artifact passes final validation and is merged into `dev`.
- after that merge, S0-02 may begin under its own task contract; this artifact does not itself authorize application or assistant code.
