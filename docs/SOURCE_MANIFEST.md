# Source manifest

Do not put controlled documents or raw operational data in this public file.
Record metadata only after authorization.

| Source | Authority | Public Git | Required metadata | Status |
| --- | --- | --- | --- | --- |
| Competency Assessment Tracker Project Plan | Product scope and workflow | No | owner, version, approval date, SHA-256 | Obtain through approved channel |
| App Architecture and Implementation Guide | Technical baseline | No | owner, version, approval date, SHA-256 | Obtain through approved channel |
| CA Architecture One-Pager | Public-safe derivative for Azure AI platform support review | Yes | source authority and review date | Review alongside authorized governing documents |
| Business Value document | Business context | No | owner, version, approval date, SHA-256 | Obtain through approved channel |
| Approved Non-CLIA competency form | Record fields and signature roles | No | document control number, version, effective date, SHA-256 | Validate current version |
| QMML and NCIRD guidance | Competency requirements | No | authoritative documents, owner, version, effective date, SHA-256 | Link index alone is insufficient |
| Approved Test Systems | Governed reference data | No by default | owner, version, approval date, SHA-256 | Review before release |
| HIR and MIST trackers | Migration lineage only | Never raw | custodian, extract date, SHA-256, disposition | Use controlled staging |

Hashes verify authorized local copies without publishing their content.

The [public architecture one-pager](architecture-one-pager.md) summarizes the
technical baseline for platform support review; it does not replace the
controlled Project Plan or App Architecture and Implementation Guide.

## Obtain and verify protected sources

The Project Plan, Architecture and Implementation Guide, Business Value document,
controlled competency forms and laboratory guidance are not published here.
Obtain authorized copies through the approved internal channel and check them
against this manifest before use. The Project Plan governs scope/workflow;
the Architecture Guide governs technical implementation. A presentation may
record a newer stakeholder decision but cannot silently override either.

For approved, versioned laboratory sources, authorized environments must retain:

- document owner;
- version and effective date;
- approval status;
- cryptographic hash;
- retirement or supersession status;
- permitted use and distribution classification.

The assistant may use only the approved corpus, must cite the governing source,
and cannot assess evidence, approve competency, sign or change official records.
Availability in a local directory is not approval for publication or ingestion.
See [source authority](SOURCE_AUTHORITY.md) and the
[assistant boundary](AI_BOUNDARY.md).

Public guidance previously under `docs/project/` and `docs/controlled-sources/`
is consolidated here. Existing ignored local documents stay at their current
paths; this reorganization does not move, release or change them.
