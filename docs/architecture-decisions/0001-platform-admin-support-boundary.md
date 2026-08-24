# ADR 0001: Platform Admin support boundary

- **Status:** Accepted for prototype and implementation planning
- **Date:** 2026-08-24

## Context

The application will hold sensitive competency records and depends on Azure
platform support for deployment, monitoring, backup, recovery, and incident
resolution. Platform support personnel must be able to diagnose production
failures without inheriting assessment or signature authority.

## Decision

SQUAD Admin and Platform Admin remain separate roles. Platform Admins receive
continuous, named, least-privilege diagnostic/read access across environments,
including production, subject to logging and periodic review.

Platform Admin access does not grant authority to assess, sign, approve,
configure business policy, or perform ordinary workflow mutations. Every access
to competency-record context is attributable. A record correction requires a
separately authorized repair or amendment operation that preserves the original
version and audit history.

## Consequences

- Platform support can investigate failures without waiting for temporary
  account creation.
- Diagnostic fields, support-purpose recording, log retention, review cadence,
  and the repair/amendment procedure must be finalized before production.
- Authorization tests must prove both the required diagnostic access and denial
  of business-workflow actions.
- This decision does not authorize production use or replace privacy, security,
  records, and platform review.
