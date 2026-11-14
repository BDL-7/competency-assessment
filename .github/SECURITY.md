# Security and sensitive-data handling

This repository is public. Do not commit:

- credentials, tokens, keys, certificates, or connection strings;
- `.env` files other than the empty `.env.example` template;
- identifiable employee, assessor, supervisor, or workforce records;
- raw migration trackers or operational exports;
- controlled documents without explicit release approval;
- confidential presenter notes or internal-only decision material.

Use synthetic data in tests and examples. Production secrets belong in the
approved secret-management service, currently expected to be Azure Key Vault.

Before publishing a binary Office document, inspect its content, external
links, comments, hidden sheets, embedded objects, and author metadata.

If sensitive information is committed, do not describe it in a public issue.
Immediately notify the repository owner through an approved private channel,
revoke exposed credentials, and follow the organization's incident process.
