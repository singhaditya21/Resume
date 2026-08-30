# NPS Survey & Workflow Engine

- **Evidence status:** Deterministic / AI-enabling
- **Category:** Enterprise operations
- **Source package:** `NPS.zip`

A full-stack survey platform spanning visual authoring, branching journeys, tokenized response collection, alerts and NPS analytics.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

No model inference is present; scoring, workflow transitions, alert policies and exports are deterministic and auditable.

## Technical stack

Next.js · React · TypeScript · Drizzle · PostgreSQL · Recharts · Nodemailer · Playwright

## Skills demonstrated

- Survey systems
- Graph workflows
- NPS analytics
- Email automation
- Tokenized journeys
- Export pipelines

## Primary system flow

Survey designer → Workflow graph → Next.js API → PostgreSQL → Respondent token journey → Analytics and export

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

- `README.md`
- `nps_architecture_ceo.md`
- `web-app/src/db/schema.ts`
- `web-app/src/lib/nps/engine.ts`
- `web-app/src/lib/workflow/`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **81,630**
