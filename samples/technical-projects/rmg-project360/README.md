# BusinessNext Project360 & Resource Budgeting

- **Evidence status:** Deterministic / AI-enabling
- **Category:** Enterprise operations
- **Source package:** `RMG.zip`

Resource planning and project economics across allocation, burdened cost, P&L, margin gates, approvals and version history.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

No inference model is implemented. Transparent shared rules and a server-authoritative calculation engine supply the decision intelligence.

## Technical stack

React · TypeScript · Vite · FastAPI · Python · PostgreSQL · Entra OIDC · Excel

## Skills demonstrated

- Resource planning
- Financial modeling
- Calculation parity
- Immutable versioning
- Approval governance
- Excel interchange

## Primary system flow

Planner workspace → Shared rules engine → FastAPI validation → Authoritative recomputation → Versioned PostgreSQL → Approval and export

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

- `Budgeting/shared/src/engine.ts`
- `Budgeting/backend/app/engine.py`
- `Budgeting/backend/app/main.py`
- `Budgeting/backend/app/schema.sql`
- `Budgeting/backend/app/sso.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **90,031**
