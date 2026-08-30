# Resource Allocation & Project Budgeting

- **Evidence status:** Deterministic / AI-enabling
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Deterministic implementation archive
- **Intelligence type:** Deterministic / AI-enabling
- **Category:** Enterprise operations
- **Project family:** RMG & workforce planning
- **Source package:** `RMG_Budgeting.zip`

A deterministic resource-planning, burdened-cost, P&L and margin-gated approval system with immutable versions.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

No runtime AI is implemented; intelligence comes from transparent costing, signatures and approval rules rather than an LLM.

## Technical stack

React · TypeScript · FastAPI · Python · PostgreSQL · Entra OIDC · Docker · Excel

## Skills demonstrated

- Financial-domain modeling
- Cross-language parity
- Immutable versioning
- Approval workflows
- OIDC/RBAC
- Audit logging

## Primary system flow

Budget planner → Shared rules engine → Server recomputation → Signature and margin gate → PostgreSQL version → Approval / export

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

- **Technical decision rationale:** Not established from the supplied archive.

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Meaningful anonymized source samples: **23**
- Retained empty source placeholders: **1**
- Total included source files: **24**
- Included sanitized source bytes: **62,956**
