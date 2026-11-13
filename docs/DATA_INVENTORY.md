# Buildathon data and knowledge index

The local `data/` folder is **entirely Git-ignored**. Generate the following
fictional files directly in that folder from the tracked
[synthetic fixtures](../tests/fixtures/synthetic/records.json). They are not
present in a fresh clone until generated. Nothing here is approved laboratory
guidance or production data.

| Category | Local file in `data/` | Sheets or contents | Intended use |
| --- | --- | --- | --- |
| Teams, people, mock identities and explicit scopes | `people-and-teams.xlsx` | `team`, `employee`, `application_user`, `role_assignment` | App fixture; 70 humans, 5 teams and 2 separate service identities |
| Synthetic systems, groupings, configuration and assignments | `systems-and-assignments.xlsx` | `test_system`, `process_grouping`, `process_grouping_test_system`, `assignment` | App fixture; 5 fictional systems and 25 assignments |
| Assessment records, evidence, versions, signatures and events | `assessments-and-history.xlsx` | Assessment/draft/element/version, signature, document, renewal, notification/attempt and audit sheets | App fixture; 25 assessments and 50 versions over 2022–2026 |
| Future planning | `future-planning.xlsx` | `projections`: 25 explicitly projected items for 2027–2031 | Planning only; never loaded as completed records |
| Competency chatbot example | `competency-demo.txt` | Fictional field, workflow, role, terminology and escalation guidance | Candidate chatbot upload only after platform/source approval |
| Fictional example attachment | `synthetic-attachment.txt` | Harmless text referenced by assessment document metadata | Local attachment example; not real evidence |

Each workbook has a `README` sheet and stable identifiers linking its sheets to
the other workbooks. A `role_context` description is not an authorization;
only explicit `role_assignment` rows represent synthetic application scopes.
The 12-month setting and 40 example signatures are fictional—not laboratory
requirements or valid signatures. Only five people have assessment history.
The records illustrate pending and finalized snapshots, not every lifecycle
transition. A finalized-record amendment example is not included.

## Generate, validate and load

Install the pinned Python **3.12** development environment from
[DEVELOPMENT.md](DEVELOPMENT.md). From the repository root:

```powershell
.venv\Scripts\python.exe scripts\buildathon_workbooks.py generate
.venv\Scripts\python.exe scripts\buildathon_workbooks.py validate
```

Generation refuses to overwrite **any** of its six output files. Preserve
existing files and choose a different empty output directory with `--directory`
if needed. The loader also refuses existing databases. It validates workbook
headers, synthetic markers, relationships, counts, projections and attachment
hashes; formulas are rejected.

```powershell
if (Test-Path Env:DATABASE_URL) { Remove-Item Env:DATABASE_URL }
New-Item -ItemType Directory -Force instance | Out-Null
.venv\Scripts\python.exe scripts\buildathon_workbooks.py load --database instance\workbook-pack.db
```

Loading creates a **new dedicated synthetic SQLite database**, never modifies
an existing database and never loads projected plans as events. The current
read-only UI requires its original demo ownership marker and does **not** open
this separate database; use [BUILDATHON.md](BUILDATHON.md) for the UI. Do not
copy or forge its marker. Real workbooks are not drop-in substitutes: any real
source needs separately approved mapping, staging and reconciliation.

## Sources, missing inputs and checks

| Category | Where to find it | Status |
| --- | --- | --- |
| App source data | [records.json](../tests/fixtures/synthetic/records.json), [projections.json](../tests/fixtures/synthetic/projections.json) | Tracked fictional inputs for generating workbooks |
| Data quality and invalid cases | [edge-cases.json](../tests/fixtures/synthetic/edge-cases.json), [invalid-cases.json](../tests/fixtures/synthetic/invalid-cases.json) | Tracked scenarios and validation cases; not app records |
| Chatbot source metadata and test specifications | [source-registry.json](../tests/fixtures/synthetic/source-registry.json), [evaluations.json](../tests/fixtures/synthetic/evaluations.json) | Synthetic metadata and 9 test specifications; not a live evaluation or active registry |
| Form and instructions | [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md) | Controlled current form not in public Git; owner approval and access required |
| QMML/NCIRD guidance | [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md), [CAT_KB.md](CAT_KB.md) | Approved full corpus not acquired; synthetic demo text does not replace it |
| Approved Test Systems catalog | [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md) | Governed catalog not in public Git; owner approval required |
| Workflow, roles and terminology | [WORKFLOW.md](WORKFLOW.md), [AUTHORIZATION.md](AUTHORIZATION.md), [TERMINOLOGY.md](TERMINOLOGY.md) | Public prototype explanations, not automatically approved bot sources |
| Governing project/architecture/business sources | [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md) | Obtain authorized current copies; not automatic chatbot uploads |
| Support and escalation | [CAT_KB.md](CAT_KB.md) | Real support contacts not supplied; escalate to designated owner/SME |
| MIST/HIR and CA Relational Tables | [SOURCE_AUTHORITY.md](SOURCE_AUTHORITY.md), [DATA_MIGRATION.md](DATA_MIGRATION.md) | Migration-only or non-authoritative reference; not synthetic-data inputs |

The separate equipment-manual chatbot is outside this buildathon pack. Do not
upload individual assessment data to the competency chatbot. Platform
selection, upload, retrieval, model safety evaluation and access filtering remain
unverified; source creation is not authorization. Follow
[DATA_CLASSIFICATION.md](DATA_CLASSIFICATION.md) and
[AI_BOUNDARY.md](AI_BOUNDARY.md).
