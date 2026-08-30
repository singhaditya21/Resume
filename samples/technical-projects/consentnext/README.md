# ConsentNext Governance Platform

- **Evidence status:** Code-derived architecture
- **Category:** Governance, risk & security
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

- `consentnext/ARCHITECTURE.md`
- `consentnext/backend/app/modules/consent/`
- `consentnext/backend/app/modules/integration/`
- `consentnext/backend/app/modules/governance/`
- `consentnext/backend/app/platform/kms.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **12,511**
