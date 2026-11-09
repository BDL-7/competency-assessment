# Read-Only Knowledge Assistant Boundary

## Purpose

The in-product assistant explains supported competency requirements to
authenticated employees and assessors. It is separate from the development
agents that build and review the system and separate from the application
system of record.

## Approved prototype path

```text
Application
  -> read-only assistant adapter
  -> active approved-source registry and bounded corpus
  -> versioned prompt/model configuration
  -> EDAV OpenAI
  -> structured answer with citations
  -> coverage check
  -> answer or SME escalation
```

The application and assistant are developed in parallel in the first coding
sprint, but the assistant receives no record-mutation authority. The current
QMML/NCIRD file is only a link index; the bounded prototype may use only sources
that are actually acquired, approved, versioned, and permitted for its users.

## Required controls

- Named source owner, identifier, version, effective/retired dates, hash,
  access classification, active status, and assistant availability.
- Source access filtering before context is assembled.
- Versioned prompt and model configuration.
- Human-usable citations identifying the supporting source and location when
  available.
- An explicit unsupported answer and SME escalation when coverage is absent,
  insufficient, conflicting, retired, or inaccessible.
- Evaluation cases for supported, unsupported, conflicting, retired-source,
  access-restricted, and prompt-injection questions.
- Approved token, retry, and time limits.
- Data-minimized logs that do not store unnecessary question or source text.

## Prohibited capabilities

The assistant has no credentials or tools for database mutation, competency
scoring, pass/fail decisions, remediation completion, assessment approval,
signatures, email delivery, permission changes, source publication, or any
consequential workforce decision. It never presents generated content as
controlled policy.

## Prototype exit evidence

The assistant returns at least one supported answer with a usable citation,
rejects or escalates an unsupported question, respects source access, records
source/prompt/model versions and outcome without sensitive content, and passes
prohibited-action and prompt-injection tests.
