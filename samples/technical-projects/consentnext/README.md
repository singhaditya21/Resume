# ConsentNext Governance Platform

- **Evidence status:** Code-derived architecture
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Implementation archive
- **Intelligence type:** AI-assisted intelligence
- **Category:** Governance, risk & security
- **Project family:** Independent system
- **Source package:** `Consent Management.zip`

A multi-tenant consent and preference platform with signed append-only evidence, maker-checker governance and reliable downstream propagation.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Risk monitoring is deterministic and explainable rather than model-based, using rules and anomaly scores over governed consent-ledger read models.

## Technical stack

FastAPI · SQLAlchemy · PostgreSQL · Next.js · React · Kafka · RabbitMQ · OIDC

## Skills demonstrated

- Domain-driven design
- Cryptographic ledgers
- Transactional outbox
- Tenant isolation
- Maker-checker workflows
- Regulatory evidence

## Primary system flow

Consent channel → Identity and policy validation → Signed append-only version → Audit and outbox → Kafka or RabbitMQ → Downstream read models

## Architecture image pack

- `architecture/01-executive-architecture.svg`
- `architecture/02-runtime-data-flow.svg`
- `architecture/03-system-context-deployment.svg`
- `architecture/04-authenticated-lifecycle.svg`
- `architecture/05-data-architecture.svg`
- `architecture/06-workflow-orchestration.svg`
- `architecture/07-ai-control-plane.svg`
- `architecture/08-trust-boundaries.svg`
- `architecture/09-target-architecture-roadmap.svg`

IdeaStorm additionally includes the nine supplied PNG reference diagrams under `architecture/reference-pack/`.

## Source evidence reviewed

See [`PUBLIC_EVIDENCE_MAP.md`](PUBLIC_EVIDENCE_MAP.md) for a claim-to-sample map and the complete anonymized sample inventory. Original archive-member paths are intentionally not published.

## Attribution, outcomes and decisions

- **Personal ownership:** Not established from the supplied archive.
- **Measured outcomes:** Not established from the supplied archive.

- Consent evidence uses insert-only signed versions rather than mutable history.
- Tenant/purpose isolation and maker-checker approval gate governed changes.

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Meaningful anonymized source samples: **12**
- Retained empty source placeholders: **12**
- Total included source files: **24**
- Included sanitized source bytes: **12,511**
