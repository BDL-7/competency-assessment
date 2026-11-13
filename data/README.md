# Buildathon data and knowledge index

Start here to find the actual files. All public demonstration records and
chatbot examples are **fictional**, not copied or inferred from operational
workbooks. The equipment-manual chatbot is a separate future pilot.

**App inputs and chatbot uploads are different sets.** Do not upload individual
assessment records, identity/scope files or evaluation expectations as chatbot
knowledge. No upload or live integration is performed by this repository.

## File index

`READY` means a tracked file is usable for the stated **synthetic** purpose.
It does not mean production readiness, laboratory approval or a live bot.
`MISSING` means the actual authorized input is not provided in public Git.
`REFERENCE` means guidance, code or a deferred source, not a loadable dataset.

Multiple categories deliberately share one relational JSON file: the table key
identifies where to look inside it. These are not duplicate datasets.

| Category | Exact file path / table key | What is there | Destination | Status |
| --- | --- | --- | --- | --- |
| Fictional people and team memberships | [records.json](examples/buildathon/app/records.json): `employee`, `team` | 70 humans, 5 teams of 14; stable IDs; optional role descriptions | Synthetic app database | READY |
| Application identities and person links | [records.json](examples/buildathon/app/records.json): `application_user` | 70 mock human identities linked to people; 2 unlinked mock service identities | Synthetic app database | READY |
| Explicit application roles and scopes | [records.json](examples/buildathon/app/records.json): `role_assignment` | 175 explicit synthetic scope rows, including out-of-scope and diagnostic personas; roster labels grant nothing | Synthetic app database | READY |
| Test systems, groupings, configuration and mappings | [records.json](examples/buildathon/app/records.json): `test_system`, `process_grouping`, `process_grouping_test_system` | 5 fictional systems/groupings/mappings; reused 12-month demo setting, not laboratory policy | Synthetic app database | READY |
| Assignments, participants, dates and states | [records.json](examples/buildathon/app/records.json): `assignment`, `assessment` | 25 representative assessments, 5 assessed people across 5 historical years; explicit lead/assessor/supervisor links | Synthetic app database | READY, representative subset |
| Assessment drafts, versions, elements, evidence and follow-up | [records.json](examples/buildathon/app/records.json): `assessment_draft`, `assessment_draft_element`, `assessment_version`, `assessment_element` | 50 versions and corresponding drafts/elements; earlier missing follow-up retained, current follow-up documented | Synthetic app database | READY |
| Synthetic signatures and finalization | [records.json](examples/buildathon/app/records.json): `signature`, `assessment_version` | 20 locked finalized examples, 40 fictional version-bound signatures; 5 unsigned pending examples | Synthetic app database | READY; not legal signatures |
| Renewal examples | [records.json](examples/buildathon/app/records.json): `renewal` | 20 synthetic completion/next-date snapshots | Synthetic app database | READY; no real policy |
| Artifact metadata and sample attachment | [records.json](examples/buildathon/app/records.json): `assessment_document`; [synthetic-attachment.txt](examples/buildathon/app/synthetic-attachment.txt) | 25 metadata references to one harmless fictional text attachment and its SHA-256 | Database plus local fixture file | READY; no Blob integration |
| Notification and attempt examples | [records.json](examples/buildathon/app/records.json): `notification_event`, `notification_attempt` | 25 events/attempts explicitly marked not delivered | Synthetic app database | READY; no email |
| Audit examples | [records.json](examples/buildathon/app/records.json): `audit_event` | 25 fictional snapshot observations, not proof of actual historical actions | Synthetic app database | READY |
| Historical coverage | [records.json](examples/buildathon/app/records.json) | Assessment years 2022-2026; reference date 2026-11-13; assignments may begin earlier | Synthetic app database | READY |
| Future planning | [projections.json](examples/buildathon/app/projections.json) | 25 explicitly projected items for 2027-2031; no completed assessments/signatures/events | Planning input only; never loaded as transactions | READY |
| Invalid input and relationship examples | [invalid-cases.json](examples/buildathon/app/invalid-cases.json) | 8 mutation cases rejected by the pack validator | Validation only, never seed | READY |
| Other data-quality scenarios | [edge-cases.json](examples/edge-cases.json) | 5 existing scenario descriptions: missing/incomplete information, conflicts, projections and source-format variation | Scenario design/testing | READY as scenarios, not records |
| Chatbot demonstration corpus | [demo-guide.txt](examples/buildathon/chatbot/demo-guide.txt) | Fictional field/evidence guidance, catalog, roles, workflow, signing/locking/amendment explanation, dates, terms, navigation, notifications and escalation | Only this text file is a candidate knowledge upload | READY as synthetic text; platform approval/import untested |
| Chatbot source metadata and upload allowlist | [source-registry.json](examples/buildathon/chatbot/source-registry.json) | Source ID, version, owner label, effective date, hash, classification and explicit synthetic status | Maintainer/platform configuration; not general retrieval content | READY as fixture; not active app registry |
| Cited answers and safety/evaluation examples | [evaluations.json](examples/buildathon/chatbot/evaluations.json) | Supported/cited answer; unsupported, conflicting, retired, restricted, insufficient, injection, prohibited-action and individual-record cases | Manual/platform evaluation; do not upload as knowledge | READY as specifications; live bot not evaluated |
| Loader, generator and validation | [buildathon_pack.py](../scripts/buildathon_pack.py); [test_buildathon_pack.py](../tests/unit/test_buildathon_pack.py) | Repeatable generation, integrity checks, explicit new-database loading and regressions | Local Python tools | READY; supported-version CI evidence required |
| Original 70-person example | [generate_users.py](examples/generate_users.py) | Existing generator reused by the pack; its standalone `users.csv` remains ignored | Optional local roster experiment | REFERENCE; use tracked pack for app inputs |
| Original one-record UI demo | [demo.py](../app/data/demo.py); [BUILDATHON.md](../docs/BUILDATHON.md) | Existing read-only UI setup, unchanged | Original dedicated demo database | READY for original walkthrough |
| Governing project, architecture and business documents | [SOURCE_MANIFEST.md](../docs/SOURCE_MANIFEST.md) | Source requirements only; obtain controlled copies through approved channel | Authorized planning/review | MISSING actual sources in public Git |
| Current approved Non-CLIA form and instructions | [SOURCE_MANIFEST.md](../docs/SOURCE_MANIFEST.md) | Current-version/owner verification requirements, not the controlled form | Approved corpus after access/ingestion approval | MISSING; synthetic guide is not a substitute for real guidance |
| Actual QMML/NCIRD laboratory guidance | [SOURCE_MANIFEST.md](../docs/SOURCE_MANIFEST.md); [CAT_KB.md](../docs/CAT_KB.md) | Source requirements and knowledge-format recommendations, not the approved full corpus | Approved corpus after access/ingestion approval | MISSING |
| Actual Approved Test Systems catalog | [SOURCE_MANIFEST.md](../docs/SOURCE_MANIFEST.md) | Governed-source approval requirements; no catalog rows | Approved configuration/corpus only after owner review | MISSING; fictional systems are not approved catalog values |
| Canonical public workflow/role/term explanations | [WORKFLOW.md](../docs/WORKFLOW.md), [AUTHORIZATION.md](../docs/AUTHORIZATION.md), [TERMINOLOGY.md](../docs/TERMINOLOGY.md) | Maintained prototype explanations underlying the fictional guide | Implementation reference; not automatically approved bot sources | REFERENCE |
| Real support/SME directory | [CAT_KB.md](../docs/CAT_KB.md) | Identifies need; fictional guide requests review without inventing real contacts | Source-owner-approved support route | MISSING actual directory |
| MIST/HIR trackers | [DATA_MIGRATION.md](../docs/DATA_MIGRATION.md) | Local ignored migration inputs described, never app feeds or synthetic inputs | Separately approved restricted migration only | REFERENCE; not a buildathon dependency |
| CA Relational Tables workbook | [SOURCE_AUTHORITY.md](../docs/SOURCE_AUTHORITY.md) | Local ignored non-authoritative design reference described | Optional authorized design review only | REFERENCE; not the canonical dataset |

## Use the pack

Use the pinned environment in [DEVELOPMENT.md](../docs/DEVELOPMENT.md).
Python **3.12** is the supported validation runtime. From the repository root:

```powershell
.venv\Scripts\python.exe scripts\buildathon_pack.py validate
.venv\Scripts\python.exe -m pytest tests\unit\test_buildathon_pack.py -q
```

The files are already tracked; generation is **not** required to find them.
To reproduce them under an approved task:

```powershell
.venv\Scripts\python.exe scripts\buildathon_pack.py generate
```

Load valid app records into a **new** dedicated SQLite file:

```powershell
if (Test-Path Env:DATABASE_URL) { Remove-Item Env:DATABASE_URL }
New-Item -ItemType Directory -Force instance | Out-Null
.venv\Scripts\python.exe scripts\buildathon_pack.py load --database instance\buildathon-pack.db
```

The loader uses the existing Alembic migration and foreign-key enforcement.
It rejects existing files, including its own previous output: select a new
filename rather than reset. It does not load projections, invalid cases or
chatbot text into app tables. Failed targets are preserved for inspection;
never reuse an unknown/partial database. No production connection is supported.
Text fixture hashes use canonical UTF-8/LF content so Git's Windows checkout
line endings do not change the expected values. These are fixture integrity
checks, not governed source approval.

**The larger database is an import/service fixture, not a new UI mode.** The
current UI requires its original ownership marker and reference date, so it
deliberately rejects this separate pack database. Do not copy or forge that
marker. Use [BUILDATHON.md](../docs/BUILDATHON.md) for the unchanged UI walkthrough.
Connecting a larger fixture to that UI requires a separately approved app task.

For chatbot preparation, the allowlist contains **only**
[demo-guide.txt](examples/buildathon/chatbot/demo-guide.txt). Keep the registry
and evaluation cases alongside it for maintainers. Select an approved platform,
confirm text import, source/citation behavior and access controls before upload.
The source registry leaves `assistant_available` false: creating these files
does not activate them in the app's mock assistant. Evaluation validation checks
fixture coverage/citation text, not live model behavior.

## Boundaries and remaining gaps

- The pack represents finalization and pending-signature snapshots, not every
  lifecycle transition. Only five people have assessment history; the other
  people exercise roster, participant, administrative or no-access cases.
- Earlier issued versions are preserved. A correction to an already finalized
  record is not seeded; actual amendment execution remains a separate app task,
  not a capability supplied by this pack.
- Knowledge documents are fictional software examples, not laboratory advice.
  Real guidance/form/catalog and actual escalation contacts remain owner gates.
- SQL Server/Azure SQL, Entra ID, Blob, email, telemetry, live AI and deployment
  are not enabled. No credentials or operational inputs are needed here.
- Real-data replacement uses the existing app columns, stable IDs and explicit
  references. It still requires approved per-source mapping, restricted staging,
  lineage and reconciliation; real workbooks are not drop-in substitutes.

Follow [classification](DATA_CLASSIFICATION.md),
[source authority](../docs/SOURCE_AUTHORITY.md), and
[assistant boundaries](../docs/AI_BOUNDARY.md). A local controlled filename,
schema, source index or mock citation is not proof of usable approved content.
