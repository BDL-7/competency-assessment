# Controlled Terminology for Implementation

This dictionary prevents legacy tracker labels from silently becoming product
requirements. Laboratory owners must approve changes to controlled meanings.

| Term | Current implementation meaning | Boundary |
| --- | --- | --- |
| Employee / Testing Personnel | Person being assessed and signer of the current acknowledgement event | Separate from login account |
| Application User | Entra-backed identity allowed to enter the application | Does not itself grant assessment authority |
| Assigned Team Lead | Person responsible for the assignment/work queue | Does not automatically grant final-signature authority |
| Assessor | Person authorized to conduct and document the assessment | Stored separately from Team Lead and final signer |
| Technical Supervisor / final signer | Authorized person providing the final required signature | Authority must be explicit for the assessment |
| SQUAD Admin | Designated application administrator | No assessment or signature authority from membership alone |
| Platform Admin | Azure support role with continuous, attributable, least-privilege diagnostic/read access | No business-policy, assessment, signature, approval, or ordinary workflow-mutation authority |
| Test System | Governed catalog item approved for competency tracking | Legacy values require approved mapping |
| Process Grouping | Approved higher-level process or competency grouping | Do not infer it from ambiguous legacy test-system types |
| Assessment Element | Required evaluated item with its result, evidence/comments, gap, and follow-up status | No generic weighted scoring or proficiency levels |
| Testing Personnel acknowledgement | The Testing Personnel signature for the current prototype baseline | No separate event unless later approved |
| Finalized | Exact approved version is signed, retained, audited, and locked | Normal editing is prohibited |
| Amendment | Attributable superseding version that preserves the finalized original | Full procedure remains a human approval gate |
| Overdue | Due action exceeded its date | Preserves the underlying active workflow state |

Legacy wording remains stored with source lineage. Crosswalks translate only
after owner approval; they never overwrite the original source value.
