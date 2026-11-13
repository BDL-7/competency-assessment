# Data: examples and protected inputs

This directory does **not** contain the laboratory's operational datasets.
Its public contents are handling guidance and [fictional examples](examples/README.md).
The application's SQL persistence code lives separately in [app/data](../app/data/).

## Choose the right synthetic resource

| Resource | Purpose | Loaded by the app? |
| --- | --- | --- |
| [Local pilot fixture](../docs/BUILDATHON.md) | One assessment, two issued versions and seven synthetic identities for the current read-only UI | Yes, only through explicit `init-demo` setup |
| [Fictional examples](examples/README.md) | Deterministic generator for 70 fictional people and five data-quality scenarios | No; illustrative roles grant no access |

These are purpose-built fictional resources, not samples or anonymized copies
of operational trackers. Keep projections distinct from completed activity.

## Competency-Assessment app: data-source inventory

The repository defines source requirements, while the local prototype runs on
synthetic data. The table describes each source's role, location/status, and
access boundary. Controlled workbook and document contents are not part of
public Git and must not be used to create synthetic fixtures.

| Data source/category | Where it lives and current status | Access and buildathon use |
| --- | --- | --- |
| Governing project, technical, and business documents | Controlled copies are outside public Git; requirements and metadata fields are listed in the [source manifest](../docs/SOURCE_MANIFEST.md). | Obtain through the approved internal channel. Verify owner, current version, approval date, and hash before relying on them; do not reproduce controlled contents here. |
| Approved Non-CLIA assessment form V04 | Controlled source; not published in the repository. | Use only the authorized current copy and verify its document control/version/effective date. Its prototype field baseline is provisional. |
| QMML and NCIRD laboratory guidance | [CAT_KB.md](../docs/CAT_KB.md) is an advisory link index; the full approved corpus is not acquired in the repository. | Request approved, versioned materials from the source owner. The index is not sufficient for answers; assistant use requires approval and active source registration. |
| Approved Test Systems catalog | Governed workbook is excluded from public Git; the [source manifest](../docs/SOURCE_MANIFEST.md) records its approval requirements. | Obtain/use the owner-approved version. Approval is required before operational loading or public release; record authorized source metadata. Do not copy workbook rows into examples. |
| MIST and HIR legacy trackers | Local operational workbooks are ignored by Git and are not application data feeds. | Migration-only, through the authorized custodian and restricted staging. Preserve workbook/sheet/row lineage. Raw rows and derivatives must not enter public Git or synthetic fixtures; migration execution is outside the local pilot. |
| CA Relational Tables workbook | Local, ignored, non-authoritative design reference. | Optional design context only. Current project decisions, controlled sources, and implemented app models take precedence. |
| App records and configuration | Entities are defined in [models.py](../app/data/models.py) and [migrations](../migrations/). The local pilot uses a dedicated synthetic SQLite file configured through `APP_DATABASE_URL`; see [database.py](../app/data/database.py) and [.env.example](../.env.example). | Local demo access is through scoped app reads. Initialize only a new dedicated synthetic database as described in [BUILDATHON.md](../docs/BUILDATHON.md). Production Azure SQL access is not enabled and requires platform approval and the approved managed-identity path. |
| Identity and authorization | Local synthetic identity support is in [identity.py](../app/auth/identity.py); app roles and scopes are represented in app data. Microsoft Entra ID is the production direction. | Mock identity is for development/testing and does not itself grant roles. Production identity/access is not enabled; do not treat illustrative roster labels as permissions. |
| Assessment artifacts | Metadata is represented with app records; private Azure Blob Storage is the intended production direction in [ARCHITECTURE.md](../docs/ARCHITECTURE.md). | Blob access is not implemented in the local pilot. Intended access is private and authorized per request, not public links or direct workbook sharing. |
| Competency assistant source corpus | The intended design is a bounded, approved, versioned corpus. Current [mock.py](../app/ai/mock.py) contains deterministic synthetic answers; no live corpus or model calls are enabled. | Future sources must be owner-approved, access-filtered, cited, and versioned. The assistant remains read-only; see [AI_BOUNDARY.md](../docs/AI_BOUNDARY.md). |
| Synthetic demo and test data | [demo.py](../app/data/demo.py), [the 70-person generator](examples/generate_users.py), [the edge-case catalog](examples/edge-cases.json), and synthetic fixtures under [tests](../tests/). | Use these resources for local development and tests. The app demo is one assessment and is not representative operational data. Build on them rather than copying workforce or assessment records. |
| Other planned integrations | Email delivery and Azure Monitor/Application Insights telemetry are in architecture/operations direction but are not enabled in the local pilot. EDAV OpenAI is the documented assistant-provider direction; Microsoft Foundry is an evaluation option. | These are planned integrations, not current data sources. Do not treat them as active services or upload controlled sources without approval. |

### Existing synthetic coverage and gaps

| Category | Already present | Possible buildathon coverage to add under an approved task |
| --- | --- | --- |
| People and roles | 70 fictional human rows with varied illustrative role combinations; seven mock identities in the one-team app demo | Distinguish roster roles from app authorization. Add service identities separately and more group relationships only if the approved demo needs them. |
| Test systems and process groupings | One synthetic test system, grouping, and mapping in the app demo | Add fictional relationships for UI variety; do not use governed catalog values or invent laboratory rules. |
| Assignments and assessment history | One assignment and one assessment with two versions; the first preserves missing follow-up and the second records synthetic follow-up | Add synthetic examples for UI states and history only within approved workflow behavior. Current demo has zero signatures and is read-only. |
| Data-quality cases | Five cataloged scenarios: optional information missing, incomplete work in progress, conflicting candidate values, future projection, and source-format variation | Consider duplicate/unlinked identities, unmatched relationships, missing/inactive configuration, and due-date/reference-date boundaries. Surface ambiguity; do not silently merge, map, or resolve it. |
| Scale and time | Current demo is one record; product planning describes a multi-lab example and five years of synthetic history plus five years of future planning | Treat broader scale as a future synthetic-data task. Keep projected items separate from completed assessments, signatures, or events. |
| Competency chatbot | Synthetic mock answer/citation and unsupported-question escalation | Add synthetic evaluations for supported answers with citations, unsupported/conflicting/retired/inaccessible sources, and prompt injection after an approved corpus is available. The bot has no individual assessment-record access by default. |
| Equipment-manual chatbot | Documentation may mention this as a future add-on/separate pilot | No equipment manuals or knowledge base are needed for this buildathon. |

The examples above are candidate coverage, not authorization to change schema,
workflow, roles, data sources, or policy. Follow [data
classification](DATA_CLASSIFICATION.md), the [source
manifest](../docs/SOURCE_MANIFEST.md), and [migration
controls](../docs/DATA_MIGRATION.md). Preserve source workbook, sheet, row,
and source-identifier lineage; do not silently resolve ambiguous values. Do
not copy identifiable workforce data into documentation, fixtures,
demonstrations, logs, or AI prompts.
