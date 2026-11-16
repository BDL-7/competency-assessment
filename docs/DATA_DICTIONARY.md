# Generated synthetic data dictionary

This dictionary describes the **current tracked fictional fixtures**, not
operational data, approved laboratory rules, a live chatbot corpus, or the
requested future integrated multi-lab UI. The sources are
[`records.json`](../tests/fixtures/synthetic/records.json),
[`projections.json`](../tests/fixtures/synthetic/projections.json),
[`edge-cases.json`](../tests/fixtures/synthetic/edge-cases.json),
[`invalid-cases.json`](../tests/fixtures/synthetic/invalid-cases.json),
[`source-registry.json`](../tests/fixtures/synthetic/source-registry.json),
[`evaluations.json`](../tests/fixtures/synthetic/evaluations.json),
the [physical SQLAlchemy schema](../app/data/models.py), the
[pack generator/validator](../scripts/buildathon_pack.py), the
[workbook exporter](../scripts/buildathon_workbooks.py), and the
[roster generator](../scripts/generate_users.py). It describes no files under
the protected, ignored root `data/`.

## Reading the field tables

The **Type** column gives the physical SQLAlchemy type for app tables and the
JSON representation (dates/datetimes are ISO strings). `S(64)` means
`String(64)` / JSON string, `T` means `Text` / JSON string, `I` integer,
`B` boolean, `D` `Date` / `YYYY-MM-DD` string, and `DT` `DateTime` / ISO-8601
string. The string length is a physical column limit, **not** an enumerated
business domain. Workbook cells are exported from JSON rows as values or text;
date/datetime values remain text, not Excel date formulas. `Required` means
SQL `NOT NULL` and present in the current nonempty fixture; `nullable` means
SQL `NULL` is allowed, **not** that the current rows necessarily contain null.
For non-SQL datasets, `required`/`optional` describes JSON key presence.
`PK` means table primary key; `FK table.column` means an enforced SQL foreign
key. A plain `ref` or `snapshot` is a logical identifier, **not** an FK. All
`id` columns in the app tables are `S(64)` primary keys unless stated
otherwise; IDs are synthetic and stable only within this fixture.

The **Meaning; current values / generation** column describes *observed
fictional values* and the generator's rule, not all allowed production values.
No live role grant follows from `role_context`. A string `null` in the tables
below means JSON `null` / SQL `NULL`, not the literal text `"null"`. Tables
with zero rows have schema columns but no observed values.

The pack uses a fixed `2026-11-13` reference date, years 2022–2026 for
snapshots, and separately projected 2027–2031 dates. The generator clones an
existing **one-record Non-CLIA demo**, rewrites IDs and year components, and
stamps fictional timestamps. The 12-calendar-month setting is a synthetic
example, **not a CLIA interval or approved renewal policy**. The multi-lab
pack has 70 employees in five teams of 14, 72 login identities (two without
employees), 25 assessments (only five people represented in history), and 25
future projections. It is not connected to the current one-record UI demo.
Dates are fixed in the fixture; loading does not recalculate them relative to
today. The UI demo separately uses a fixed `2027-02-20` reference date; see
the [walkthrough](BUILDATHON.md#demonstration-boundary).

## JSON envelopes and output mapping

`records.json` and `projections.json` share these envelope keys:

| Key | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `dataset_id` | string; required | Pack identifier `SYN-BUILDATHON-PACK-1`, fixed by generator. |
| `synthetic_only` | boolean; required | Must be `true`; marks fictional fixture, not source approval. |
| `reference_date` | ISO date string; required | Fixed `2026-11-13`; validator requires exactly this value. |
| `basis` | string; required | Explains invented/demo and roster basis, not operational provenance. |
| `limitation` | string; required | Warns snapshots are not legally valid signatures or event replay. |

`records.json` additionally has required `tables` (object keyed by the **20**
names below, each an array of row objects). `projections.json` instead has
required `projections` (array of 25 planning rows). The exporter writes the
20 table arrays to three workbooks and the projections array to a fourth:

| Generated workbook | Dataset/sheet names; current row counts |
| --- | --- |
| `people-and-teams.xlsx` | `team` 5; `employee` 70; `application_user` 72; `role_assignment` 175 |
| `systems-and-assignments.xlsx` | `test_system` 5; `process_grouping` 5; `process_grouping_test_system` 5; `assignment` 25 |
| `assessments-and-history.xlsx` | `assessment` 25; `assessment_draft` 50; `assessment_draft_element` 50; `assessment_version` 50; `assessment_element` 50; `signature` 40; `assessment_document` 25; `renewal` 20; `notification_event` 25; `notification_attempt` 25; `audit_event` 25; `idempotency_record` **0** |
| `future-planning.xlsx` | `projections` 25; *not* loaded as completed app records |

Each workbook also has a `README` sheet without column headers: `A1` is the
fixed synthetic-demonstration marker; `A2` explains that IDs join sheets;
`A3` is the label `Reference date` and `B3` is the ISO reference date;
`A4` warns against interpreting synthetic signatures, settings or results
as real. The `README` cells are explanatory text, not another app table.
For nonempty sheets, the exporter takes headers from fixture row keys. These
are the field names below **except** `application_user.tenant_ref` and
`audit_event.support_purpose` / `audit_event.support_reference`: these
nullable schema columns are absent from every current JSON row and workbook
sheet, rather than present as null cells. For the empty `idempotency_record`,
SQL model columns supply the header.
No workbook is regenerated or read from root `data/` for this dictionary.

### `team` (5 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Fictional lab/team identifier `SYN-L1-TEAM` through `SYN-L5-TEAM`. |
| `display_label` | S(200) | Required | `Synthetic Lab N team`; display only, not a governed lab name. |
| `is_active` | B | Required | `true` in all five rows; fixture availability flag. |
| `configuration_owner_ref` | S(128) | Required | `SYN-LN-CONFIG` logical owner/config reference, **not** an FK or actual approval. |
| `created_at` | DT | Required | Fixed `2021-01-01T00:00:00+00:00`; synthetic setup timestamp. |

### `employee` (70 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | `SYN-HUMAN-001` through `SYN-HUMAN-070` from roster. |
| `team_id` | S(64) | Required FK `team.id` | Five lab identifiers, 14 people per lab. |
| `display_label` | S(200) | Required | Fictional `Synthetic User NNN` display name from roster. |
| `is_active` | B | Required | `true`; row availability flag. |
| `role_context` | S(200) | Nullable; populated | One of nine semicolon-joined *illustrative* roster role combinations; **not** an authorization grant. |
| `source_lineage` | T | Nullable; populated | Explicit synthetic-roster provenance warning; not real workforce lineage. |
| `created_at` | DT | Required | Fixed synthetic setup timestamp `2021-01-01T00:00:00+00:00`. |

### `application_user` (72 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | 70 `SYN-HUMAN-*` identities plus `SYN-SERVICE-001/002` mock identities. |
| `identity_provider_subject` | S(200) | Required; unique | Same fictional identifier as `id`; **not** an Entra claim. |
| `tenant_ref` | S(128) | Nullable; key absent in all rows | No tenant supplied by fixture; no exported sheet column. |
| `is_mock_identity` | B | Required | `true` for every identity; not production authentication. |
| `is_active` | B | Required | `true` in this fixture. |
| `employee_id` | S(64) | Nullable FK `employee.id`; unique | Same ID for 70 humans; null for the two mock service identities. Does not create service-principal/capability rows. |
| `created_at` | DT | Required | Fixed synthetic setup timestamp. |

### `test_system` (5 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Fictional `SYN-LN-SYSTEM` per lab. |
| `display_label` | S(200) | Required | `Synthetic Lab N test system`, not a controlled catalog value. |
| `owner_ref` | S(128) | Required | `SYN-OWNER` placeholder; not an owner approval. |
| `approval_ref` | S(128) | Required | `SYN-DEMO-ONLY` placeholder, not a real approved-system reference. |
| `is_active` | B | Required | `true` for all fixture systems. |
| `is_non_clia_applicable` | B | Required | `true` for the *Non-CLIA synthetic prototype*. `false` would **not** prove CLIA applicability. |
| `created_at` | DT | Required | Fixed synthetic setup timestamp. |

### `process_grouping` (5 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Fictional `SYN-LN-PROCESS` per lab. |
| `team_id` | S(64) | Required FK `team.id` | Owning lab/team. |
| `display_label` | S(200) | Required | `Synthetic Lab N process grouping` display text. |
| `owner_ref` | S(128) | Required | `SYN-OWNER` fictional owner label; not an approval. |
| `applicability` | S(100) | Required | `Non-CLIA synthetic prototype`; descriptive text, not a two-profile rule mapping. |
| `configuration_version` | S(64) | Required | `SYN-LN-CONFIG` logical configuration ID; no separate configuration table/FK. |
| `interval_value` | I | Required | `12` in this synthetic sample; must be positive in SQL, not an approved interval. |
| `interval_unit` | S(32) | Required | `calendar_months` sample unit; not a regulatory schedule. |
| `is_active` | B | Required | `true` in fixture. |
| `created_at` | DT | Required | Fixed synthetic setup timestamp. |

### `process_grouping_test_system` (5 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | `SYN-LN-MAP` mapping-row ID. |
| `process_grouping_id` | S(64) | Required FK `process_grouping.id` | Parent grouping; pair with `test_system_id` is unique in SQL. |
| `test_system_id` | S(64) | Required FK `test_system.id` | Linked fictional system for the lab. |
| `created_at` | DT | Required | Fixed synthetic setup timestamp. |

### `assignment` (25 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year-specific assignment ID cloned from the one-record demo. |
| `employee_id` | S(64) | Required FK `employee.id` | Testing Person; one of five lab-specific people across years. |
| `team_id` | S(64) | Required FK `team.id` | Lab owning the assignment. |
| `process_grouping_id` | S(64) | Required FK `process_grouping.id` | Fictional grouping selected for that lab. |
| `assigned_team_lead_id` | S(64) | Required FK `employee.id` | Separate team-lead participant per lab. |
| `assessor_id` | S(64) | Required FK `employee.id` | Separate assessor participant per lab. |
| `technical_supervisor_id` | S(64) | Required FK `employee.id` | Separate final-review participant per lab. |
| `interval_value_snapshot` | I | Required | Copied fictional `12`-month configuration for this assignment. |
| `interval_unit_snapshot` | S(32) | Required | `calendar_months` from fictional grouping. |
| `configuration_version_snapshot` | S(64) | Required | Lab's `SYN-LN-CONFIG`; logical snapshot, not an FK. |
| `basis_date` | D | Required | February 15 of 2021–2025, year-shifted from original demo. |
| `due_date` | D | Required | February 15 of 2022–2026, shifted from demo; no live recalculation on loading. |
| `scheduling_state` | S(32) | Required | `Assigned` in every fixture row; does not show all transitions. |
| `predecessor_assignment_id` | S(64) | Nullable FK `assignment.id`; all null | Optional previous-cycle link, absent in this pack. |
| `successor_assignment_id` | S(64) | Nullable FK `assignment.id`; all null | Optional next-cycle link, absent in this pack. |
| `source_lineage` | T | Nullable; all null | Reserved lineage text; not an operational import. |
| `lock_version` | I | Required | `1`, positive synthetic concurrency counter. |
| `updated_at` | DT | Required | February 18 at 12:00 UTC in corresponding assessment year. |
| `created_at` | DT | Required | February 15 at 00:00 UTC in preceding year. |

### `assessment` (25 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year-specific stable assessment ID. |
| `assignment_id` | S(64) | Required FK `assignment.id`; unique | One assessment per assignment in this schema. |
| `lifecycle_state` | S(64) | Required | `Finalized` for 2022–2025 or `Awaiting Testing Personnel signature` for 2026; snapshot, not a transition replay. |
| `current_draft_id` | S(64) | Nullable; populated | Current draft navigation ID; **no physical FK** (cycle avoided); points to a fixture draft. |
| `current_version_id` | S(64) | Nullable; populated | Current issued-version navigation ID; **no physical FK**; points to version 2. |
| `lock_version` | I | Required | `7` for finalized snapshots, `5` for pending; positive concurrency counter. |
| `updated_at` | DT | Required | February 18 at 12:00 UTC in corresponding year. |
| `created_at` | DT | Required | February 16 at 12:00 UTC in corresponding year. |

### `role_assignment` (175 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year-specific synthetic scope record ID. |
| `user_id` | S(64) | Required FK `application_user.id` | Identity receiving explicit role; one of 35 represented mock users. |
| `role_name` | S(64) | Required | Observed `employee`, `team_lead`, `assessor`, `technical_supervisor`, `squad_admin`, `platform_admin`; actual scope must still be checked. |
| `team_id` | S(64) | Nullable FK `team.id` | Present for team-lead scope, null for other scopes in this fixture. |
| `assessment_id` | S(64) | Nullable FK `assessment.id` | Present for individual employee/assessor/supervisor scopes; null otherwise. |
| `configuration_scope` | S(128) | Nullable | Lab configuration ID, `diagnostic`, or unassigned synthetic scope depending on role; not an FK. SQL requires at least one of the three scope fields. |
| `starts_at` | DT | Required | Cloned effective date, January 1 of previous year; fixture JSON has **no timezone offset** for this field. |
| `ends_at` | DT | Nullable; all null | Optional end of role validity; not provided. |
| `approved_by_user_id` | S(64) | Required FK `application_user.id` | Fictional lab admin identifier cloned from demo, not actual approval evidence. |
| `review_due_date` | D | Nullable; all null | Optional periodic-review date, absent. |
| `created_at` | DT | Required | February 18 at 12:00 UTC in assessment year; distinct from `starts_at`. |

### `assessment_draft` (50 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Two cloned mutable draft snapshots per assessment. |
| `assessment_id` | S(64) | Required FK `assessment.id` | Parent assessment. |
| `lock_version` | I | Required | `1`; positive draft concurrency counter. |
| `employee_id` | S(64) | Required FK `employee.id` | Assessed participant snapshot. |
| `assessor_id` | S(64) | Required FK `employee.id` | Assessor participant snapshot. |
| `technical_supervisor_id` | S(64) | Required FK `employee.id` | Final-review participant snapshot. |
| `configuration_version_snapshot` | S(64) | Required | `SYN-LN-CONFIG`; logical copied version, not an FK. |
| `assessment_context` | T | Nullable; populated | `Synthetic Non-CLIA demonstration` descriptive context. |
| `assessment_type` | T | Nullable; populated | `Initial` synthetic assessment type. |
| `process` | T | Nullable; populated | Lab's `SYN-LN-PROCESS` text; not a physical FK here. |
| `assessment_method` | T | Nullable; populated | `Synthetic observation`; not a governed method catalog. |
| `specimen_context` | T | Nullable; populated | `Synthetic specimen` text. |
| `testing_context` | T | Nullable; populated | `Synthetic instrument context` text. |
| `problem_solving_evidence` | T | Nullable; populated | Fictional evidence narrative, not actual performance. |
| `protocol_outcome` | T | Nullable; populated | Assessor-recorded synthetic outcome; application does not calculate competency. |
| `comments` | T | Nullable; all null | Optional comments, omitted in this fixture. |
| `followup_required` | B | Required | `true` for synthetic gap; not a universal rule. |
| `followup_description` | T | Nullable; half null | Missing in earlier draft, fictional documented follow-up in later draft. |
| `created_by_user_id` | S(64) | Required FK `application_user.id` | Fictional assessor identity that created draft. |
| `updated_by_user_id` | S(64) | Required FK `application_user.id` | Fictional assessor identity that last updated draft. |
| `updated_at` | DT | Required | Generator's February 18 UTC stamp for assessment year. |
| `created_at` | DT | Required | Generator's February 18 UTC stamp for assessment year. |

### `assessment_draft_element` (50 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | One mutable element snapshot per draft. |
| `assessment_draft_id` | S(64) | Required FK `assessment_draft.id` | Owning draft; pair with `element_ref` is unique in SQL. |
| `element_ref` | S(64) | Required | `SYN-ELEMENT-03` synthetic element label; not a controlled element definition. |
| `recorded_result` | S(64) | Nullable; populated | `unsuccessful` fictional assessor entry; not calculated by app. |
| `evidence` | T | Nullable; populated | `Synthetic evidence only`. |
| `comments` | T | Nullable; all null | Optional per-element comments. |
| `has_gap` | B | Required | `true` for the one demonstrated element. |
| `followup_status` | S(64) | Nullable; all null | No separately recorded status in this fixture. |
| `followup_description` | T | Nullable; half null | Missing in earlier draft, fictional text in later draft. |
| `updated_at` | DT | Required | February 18 UTC stamp in assessment year. |
| `created_at` | DT | Required | February 18 UTC stamp in assessment year. |

### `assessment_version` (50 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Two immutable issued-version IDs per assessment. |
| `assessment_id` | S(64) | Required FK `assessment.id` | Owning assessment; `(assessment_id, version_number)` unique. |
| `version_number` | I | Required | Positive integer `1` or `2`, copied from old demo. |
| `source_draft_id` | S(64) | Required FK `assessment_draft.id` | Draft from which version was copied. |
| `employee_id` | S(64) | Required FK `employee.id` | Assessed participant snapshot. |
| `assigned_team_lead_id` | S(64) | Required FK `employee.id` | Team-lead participant snapshot. |
| `assessor_id` | S(64) | Required FK `employee.id` | Assessor participant snapshot. |
| `technical_supervisor_id` | S(64) | Required FK `employee.id` | Final-review participant snapshot. |
| `configuration_version_snapshot` | S(64) | Required | Lab `SYN-LN-CONFIG` text, not an FK. |
| `assessment_context` | T | Required | `Synthetic Non-CLIA demonstration`. |
| `assessment_type` | T | Required | `Initial` synthetic type. |
| `process` | T | Required | Fictional `SYN-LN-PROCESS` text; not an FK. |
| `assessment_method` | T | Required | `Synthetic observation`; illustrative method. |
| `specimen_context` | T | Required | `Synthetic specimen` text. |
| `testing_context` | T | Required | `Synthetic instrument context` text. |
| `problem_solving_evidence` | T | Required | Fictional narrative, not measured competency. |
| `protocol_outcome` | T | Required | Assessor-recorded synthetic outcome; no automated pass/fail. |
| `comments` | T | Nullable; all null | Optional version comments, omitted. |
| `followup_required` | B | Required | `true` in fixture; reflects its synthetic gap. |
| `followup_description` | T | Nullable; half null | Earlier issued version preserves missing text; current version includes fictional follow-up. |
| `created_by_user_id` | S(64) | Required FK `application_user.id` | Fictional assessor identity that issued version. |
| `supersedes_version_id` | S(64) | Nullable FK `assessment_version.id`; all null | No approved amendment flow or superseding link in this pack. |
| `is_locked` | B | Required | `true` for current versions finalized in 2022–2025; otherwise `false`. |
| `finalized_at` | DT | Nullable; 30 null | February 20 UTC for 20 finalized current versions; no timestamp for others. |
| `created_at` | DT | Required | February 18 UTC stamp in assessment year. |

### `assessment_element` (50 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Immutable copied element row per issued version. |
| `assessment_version_id` | S(64) | Required FK `assessment_version.id` | Owning version; pair with `element_ref` unique. |
| `element_ref` | S(64) | Required | `SYN-ELEMENT-03`, synthetic identifier. |
| `recorded_result` | S(64) | Required | `unsuccessful` fictional assessor entry. |
| `evidence` | T | Required | `Synthetic evidence only`. |
| `comments` | T | Nullable; all null | Optional element comments, omitted. |
| `has_gap` | B | Required | `true` for this element. |
| `followup_status` | S(64) | Nullable; all null | No separate status provided. |
| `followup_description` | T | Nullable; half null | Missing in version 1; fictional follow-up preserved in version 2. |
| `created_at` | DT | Required | February 18 UTC stamp for assessment year. |

### `signature` (40 rows)

These are **fictional fixture rows, not legally valid signatures**; only
20 finalized current versions have the two illustrated roles.

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year/role-specific fictional signature row ID. |
| `assessment_version_id` | S(64) | Required FK `assessment_version.id` | Exact issued version being illustrated; `(version, role)` unique. |
| `signature_role` | S(64) | Required | Observed `testing_personnel` then `technical_supervisor` for Non-CLIA example only. |
| `signer_user_id` | S(64) | Required FK `application_user.id` | Mock human identity: employee or technical supervisor for illustrated role. |
| `signed_at` | DT | Required | February 19 or 20 at noon UTC in finalized year; generated fixture time. |
| `authentication_context` | S(200) | Required | `synthetic_fixture_not_legal_signature`, explicitly not authentic e-sign evidence. |
| `request_identity` | S(128) | Required | Distinct `SYN-*` fictional request identifier; unique with version, role and signer. |
| `created_at` | DT | Required | Same synthetic timestamp as `signed_at`. |

### `assessment_document` (25 rows)

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year-specific synthetic document metadata ID. |
| `assessment_version_id` | S(64) | Required FK `assessment_version.id` | Exact version linked to metadata; `(version, kind)` unique. |
| `private_object_ref` | S(500) | Required | `synthetic-fixture:synthetic-attachment.txt` logical reference; **not** a Blob URL or access grant. |
| `document_kind` | S(64) | Required | `synthetic_example`; fictional attachment type. |
| `document_version` | S(64) | Required | `SYN-1` fictional document version. |
| `sha256` | S(64) | Required | Lowercase 64-hex SHA-256 of tracked fictional attachment's UTF-8/LF text; integrity metadata, not access control. |
| `uploaded_by_user_id` | S(64) | Required FK `application_user.id` | Mock assessor identity; metadata is not evidence of live upload. |
| `verified_at` | DT | Nullable; populated | February 20 UTC in corresponding year; fictional verification time. |
| `created_at` | DT | Required | February 20 UTC stamp. |

### `renewal` (20 rows)

All rows correspond to fictional finalized current versions in 2022–2025;
there is no renewal for pending 2026 records.

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Synthetic lab/year renewal ID. |
| `finalized_assessment_version_id` | S(64) | Required FK `assessment_version.id`; unique | Exact finalized version to which this renewal refers. |
| `assignment_id` | S(64) | Required FK `assignment.id` | Prior cycle assignment. |
| `completion_date` | D | Required | February 20 of finalized year, fixed in generator. |
| `interval_value` | I | Required | `12` for fictional 12-month example, **not approved policy**. |
| `interval_unit` | S(32) | Required | `calendar_months` sample unit. |
| `next_due_date` | D | Required | February 20 in following year (`completion_date` plus one calendar year in this fixture). |
| `configuration_version_snapshot` | S(64) | Required | Lab's fictional `SYN-LN-CONFIG` reference; not FK. |
| `created_at` | DT | Required | February 20 at noon UTC in completion year. |

### `notification_event` (25 rows)

Logical events only; **no real email is sent**.

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year synthetic event ID. |
| `assignment_id` | S(64) | Required FK `assignment.id` | Related assignment. |
| `assessment_id` | S(64) | Nullable FK `assessment.id`; populated | Related assessment. |
| `trigger_name` | S(64) | Required | `completed` for finalized years; `testing_personnel_signature_required` for pending 2026. |
| `recipient_user_id` | S(64) | Required FK `application_user.id` | Fictional employee identity, not proof of delivery. |
| `template_version` | S(64) | Required | `SYN-1` fictional template. |
| `record_ref` | S(128) | Required | Assessment ID as logical record reference (not an FK). |
| `scheduled_occurrence` | DT | Required | February 20 UTC in assessment year; fictional logical occurrence. |
| `status_context` | S(64) | Nullable; populated | Snapshot `Finalized` or `Awaiting Testing Personnel signature`. |
| `date_context` | D | Nullable; populated | February 15 due-date context for that year. |
| `idempotency_identity` | S(200) | Required; unique | Same logical identity as fixture event ID; prevents duplicate logical event. |
| `event_status` | S(32) | Required | `not_delivered_prototype`; no external delivery. |
| `correlation_id` | S(128) | Required | Event's fictional correlation identifier, equal to event ID. |
| `created_at` | DT | Required | February 20 UTC stamp. |

### `notification_attempt` (25 rows)

Fixture attempt rows are **synthetic non-delivery observations**, not
evidence of an email adapter or actual attempted send.

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Event ID plus `-ATTEMPT`. |
| `notification_event_id` | S(64) | Required FK `notification_event.id` | Logical event observed; `(event, ordinal)` and `(event, adapter request)` unique. |
| `attempt_ordinal` | I | Required | `1`, positive first synthetic observation. |
| `adapter_request_ref` | S(128) | Required | Event-specific `*-REQUEST` identifier; **no live adapter**. |
| `attempted_at` | DT | Required | February 20 UTC stamp in year of event. |
| `outcome` | S(32) | Required | `not_delivered_prototype`; not a send result. |
| `retry_eligible` | B | Required | `false`; fictional retry flag. |
| `failure_category` | S(64) | Nullable; populated | `synthetic_non_delivery` explanatory category. |
| `created_at` | DT | Required | February 20 UTC stamp. |

### `audit_event` (25 rows)

These are labeled imported **fictional snapshots**, not genuine event histories.

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Lab/year-specific synthetic audit ID. |
| `actor_user_id` | S(64) | Required FK `application_user.id` | Fictional assessor identity; not evidence of an actual action. |
| `action` | S(100) | Required | `synthetic_fixture`; distinguishes artificial rows. |
| `entity_type` | S(64) | Required | `assessment`. |
| `entity_id` | S(64) | Required | Assessment ID as generic entity reference; not an FK. |
| `assessment_id` | S(64) | Nullable FK `assessment.id`; populated | Related assessment. |
| `assignment_id` | S(64) | Nullable FK `assignment.id`; populated | Related assignment. |
| `observed_at` | DT | Required | February 20 UTC synthetic stamp. |
| `outcome` | S(32) | Required | `synthetic`, not a real success assertion. |
| `request_identity` | S(128) | Required | Fictional audit request ID; combined with action/type/entity must be unique. |
| `correlation_id` | S(128) | Required | Matching synthetic event identifier. |
| `change_summary` | T | Nullable; populated | Explicit imported-snapshot/non-replay warning. |
| `support_purpose` | S(200) | Nullable; key absent in all rows | No support-session purpose supplied; no exported sheet column. |
| `support_reference` | S(128) | Nullable; key absent in all rows | No support-session ticket/reference supplied; no exported sheet column. |

### `idempotency_record` (**0 rows**)

The empty sheet/schema is included for structural completeness. No observed
result types or stored requests can be inferred from this fixture.

| Column | Type | Null | Meaning; current values / generation |
| --- | --- | --- | --- |
| `id` | S(64) | Required PK | Persistent result-row ID; no fixture values. |
| `operation_name` | S(100) | Required | Command name; no fixture values. |
| `target_ref` | S(128) | Required | Logical command target, not an FK. |
| `actor_user_id` | S(64) | Required FK `application_user.id` | User actor; no service-principal mapping in this schema. |
| `request_identity` | S(128) | Required | Client/server request token; unique with operation, target and actor. |
| `request_fingerprint` | S(64) | Required | Request-input fingerprint; no fixture value, not a credential. |
| `result_type` | S(32) | Required | Stored command outcome; empty fixture does not establish a value domain. |
| `result_ref` | S(128) | Nullable | Optional logical result identifier, not an FK. |
| `resulting_state` | S(64) | Nullable | Optional resulting workflow state text. |
| `resulting_version` | I | Nullable | Optional resulting optimistic version number. |
| `reason_code` | S(64) | Nullable | Optional domain rejection/failure code. |
| `safe_message` | S(500) | Nullable | Optional client-safe result message. |
| `correlation_id` | S(128) | Required | Request correlation token. |
| `completed_at` | DT | Required | Database creation timestamp if written at runtime; no fixture values. |

## Future planning (`projections.json`; `projections` worksheet)

The 25 planning rows are **not** assessment, signature, renewal, notification
or audit records. All seven keys are required in each JSON row; there is no
SQL `projections` table or physical FK for these references. The validator
checks each logical reference against the app fixture.

| Column | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `id` | string; required | Unique `SYN-LN-YYYY-PROJECTION` planning ID for each of five labs and 2027–2031. |
| `team_id` | string; required logical ref `team.id` | Fictional lab/team for plan; checked against fixture IDs. |
| `employee_id` | string; required logical ref `employee.id` | One example employee per lab; does **not** assign a future assessment. |
| `process_grouping_id` | string; required logical ref `process_grouping.id` | Fictional lab grouping; checked against fixture IDs. |
| `planned_date` | ISO date string; required | February 15 in each projected year 2027–2031; must exceed fixed pack reference date. |
| `status` | string; required | Exactly `projected`; no completed state. |
| `note` | string; required | Explicit planning-only warning; not a business record. |

## Roster (`people.csv` intermediate; `users.csv` standalone)

The [roster generator](../scripts/generate_users.py) writes these five CSV
headers. The pack generates `people.csv` in an owned temporary directory
as an intermediate and uses its rows to build `employee` and
`application_user`; the standalone command defaults to an ignored location
that this task **does not execute or inspect**. CSV values are strings, even
when they depict a boolean. Neither file grants roles; actual scopes are
separate `role_assignment` records.

| Column | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `synthetic_user_id` | CSV string; required | Unique `SYN-HUMAN-001` through `SYN-HUMAN-070`; joins to `employee.id` and human `application_user.id`. |
| `display_name` | CSV string; required | `Synthetic User NNN`, fictional display label. |
| `identity_type` | CSV string; required | Literal `human`; the two mock service identities are added separately to the pack, not roster rows. |
| `illustrative_demo_roles` | CSV string; required | One or more semicolon-separated labels from `employee`, `team_lead`, `assessor`, `technical_supervisor`, `squad_admin`, `platform_admin`, as assigned by nine fixed role groups; illustrative only. |
| `synthetic_only` | CSV string; required | Text `true`, not a CSV boolean or approval. |

## Companion synthetic scenario and assistant-specification datasets

These are **test/specification inputs**, not application tables or automatically
approved assistant sources. Their envelopes and nested record fields are
listed explicitly. For JSON case arrays, `optional` means the key is absent
in some cases, not present as `null`. Missing/retired/conflicting-source
overlays are test scenarios, not changes to an authorized corpus.

### `edge-cases.json`

| Field | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `dataset_id` | string; required envelope | `SYN-BUILDATHON-EDGE-CASES-V1` specification identifier. |
| `synthetic_only` | boolean; required envelope | `true`; no operational-source derivation. |
| `source_basis` | string; required envelope | Purpose-built scenario provenance. |
| `cases` | array of 5 objects; required envelope | Edge-case specifications, **not** valid/invalid database rows. |
| `cases[].case_id` | string; required | Unique `SYN-EDGE-001` through `005`. |
| `cases[].kind` | string; required | One of `optional_information_missing`, `work_in_progress_incomplete`, `conflicting_candidate_values`, `future_projection`, `source_format_variation`. |
| `cases[].scenario` | string; required | Fictional scenario description, not a loaded field value. |
| `cases[].expected_handling` | string; required | Expected human/validator treatment; no silent normalization or premature finalization. |

### `invalid-cases.json`

The validator **copies** the valid pack for each of eight cases, replaces the
named indexed field with `value`, then checks that validation rejects it.
These cases are deliberately excluded from valid seeded rows.

| Field | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `synthetic_only` | boolean; required envelope | `true`; negative test marker. |
| `cases` | array of 8 objects; required envelope | Separate mutation/rejection specifications. |
| `cases[].id` | string; required | Unique `SYN-BAD-001` through `008`. |
| `cases[].table` | string; required | Target table in `records.json`; observed `employee`, `application_user`, `assessment_version`, `signature`, `assessment_document`. |
| `cases[].row` | integer; required | Zero-based row index, observed `0` or `1`; **not** a source worksheet row number. |
| `cases[].field` | string; required | Existing column of target table to mutate, such as `id`, `employee_id`, `is_locked` or `sha256`. |
| `cases[].value` | JSON string, boolean or null; required key | Deliberately invalid replacement, including an unknown FK, future timestamp, incorrect hash or null required display label. |
| `cases[].expected_error` | string; required | Expected validator error substring, not a valid data value. |

### `source-registry.json`

One fictional text source is described but `assistant_available` is
`false`; no model upload or actual audience enforcement has occurred.

| Field | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `synthetic_only` | boolean; required envelope | `true`; source content is fictional. |
| `hash_basis` | string; required envelope | SHA-256 over UTF-8 text with LF line endings. |
| `upload_files` | array of strings; required envelope | Exactly `["demo-guide.txt"]` in fixture; a **candidate allowlist**, not upload permission. |
| `note` | string; required envelope | Warns registry is not active and app records/evaluation expectations must not be uploaded. |
| `sources` | array of 1 object; required envelope | Source metadata, not approved laboratory guidance. |
| `sources[].source_id` | string; required | `SYN-COMPETENCY-GUIDE-1` fictional citation/source ID. |
| `sources[].file` | string; required | `demo-guide.txt` tracked text basename, matching candidate allowlist. |
| `sources[].title` | string; required | Fictional guide title, not a controlled document title. |
| `sources[].owner` | string; required | Synthetic-maintainer label, not a source-owner approval. |
| `sources[].version` | string; required | `SYN-1` fictional version. |
| `sources[].effective_date` | ISO date string; required | `2026-11-13` fictional effective date. |
| `sources[].retired_date` | ISO date string or null; required key, null now | Optional retirement date in the *record value*, not an absent JSON key. |
| `sources[].active` | boolean; required | `true` for synthetic metadata; does not override unavailable assistant setting. |
| `sources[].access_classification` | string; required | `synthetic_buildathon_demo`, not a real access authorization. |
| `sources[].approval_status` | string; required | `synthetic_demo_only_not_laboratory_approved`. |
| `sources[].assistant_available` | boolean; required | `false`; source is not enabled for live assistant retrieval. |
| `sources[].sha256` | 64-hex string; required | Digest of tracked `demo-guide.txt` using declared hash basis; verifies integrity, not authority. |

### `evaluations.json`

Nine **manual/platform evaluation specifications**; they are not results
from a live model. Overlay fields must remain test-only.

| Field | Type / presence | Meaning; current values / generation |
| --- | --- | --- |
| `synthetic_only` | boolean; required envelope | `true`; evaluation input marker. |
| `note` | string; required envelope | Warns expectations and overlays are not live evaluation evidence or governing uploads. |
| `cases` | array of 9 objects; required envelope | Test specifications spanning supported, unsupported, conflict, retired, inaccessible, insufficient, injection, prohibited-action and individual-record cases. |
| `cases[].id` | string; required | `SYN-EVAL-001` through `009`. |
| `cases[].kind` | string; required | Exactly one of `supported`, `unsupported`, `conflicting`, `retired`, `inaccessible`, `insufficient`, `prompt_injection`, `prohibited_action`, `individual_record`. |
| `cases[].question` | string; required | Fictional test question; not a stored user conversation. |
| `cases[].source_id` | string; optional | Present only for supported case; logical ref to `sources[].source_id`. |
| `cases[].location` | string; optional | Supported case's `[S4]` citation location in fictional guide. |
| `cases[].supporting_quote` | string; optional | Fictional guide excerpt for supported citation check; not controlled text. |
| `cases[].expected_outcome` | string; required | `answer_with_citation`, `escalate`, or `refuse`; expected, **not observed**, answer behavior. |
| `cases[].expected_answer` | string; optional | Supported case's target answer text; not a generated model answer. |
| `cases[].citation` | string; optional | Supported case's expected `source_id version [location]` citation string. |
| `cases[].reason` | string; optional | Human-readable expected escalation/refusal reason for eight other cases. |
| `cases[].test_overlay` | object; optional | Three hypothetical conflict/retirement/access changes applied for evaluation only. |
| `cases[].test_overlay.conflicting_candidates` | array of strings; optional | Two contradictory synthetic settings in conflict case; no real source ranking. |
| `cases[].test_overlay.source_id` | string; optional | Target fictional source ID in retirement/access overlays. |
| `cases[].test_overlay.active` | boolean; optional | `false` in retirement test, not a registry update. |
| `cases[].test_overlay.retired_date` | ISO date string; optional | `2026-11-12` in retirement test, not the current source value. |
| `cases[].test_overlay.user_has_access` | boolean; optional | `false` in inaccessible-source test; test precondition, not live authorization. |

## Non-tabular generated companions and exclusions

The workbook exporter copies the public fictional
[`demo-guide.txt`](../tests/fixtures/synthetic/demo-guide.txt) as
`competency-demo.txt` and
[`synthetic-attachment.txt`](../tests/fixtures/synthetic/synthetic-attachment.txt)
unchanged. They are **text files, not columnar datasets**: the first is
fictional demonstration guidance with location labels for expected citations;
the second is a synthetic attachment whose content digest is referenced by
`assessment_document.sha256`. Neither is approved guidance, a real artifact,
or a permission to upload. The generated workbooks use the fixture keys
described above (with the stated absent nullable schema columns), not extra
undisclosed columns.
`edge-cases.json`, `invalid-cases.json`, `source-registry.json` and
`evaluations.json` remain separate tracked specifications rather than workbook
sheets or loaded application rows.
