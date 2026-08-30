# CRM Data Audit Framework

- **Evidence status:** Deterministic / AI-enabling
- **Category:** Data & decision intelligence
- **Source package:** `Data Audit Framework.zip`

A modular CRM data-quality cockpit with transparent SQL rules, KPI summaries, prioritized issues and record-level drilldowns.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

No LLM is implemented. Audits are deterministic SQL, thresholds and metrics with a mock/live execution boundary.

## Technical stack

Node.js · PostgreSQL · React · TypeScript · Vite · Tailwind · SVG charts

## Skills demonstrated

- Data-quality rules
- Modular audit architecture
- Custom database protocol
- Drilldown UX
- Mock/live parity
- KPI design

## Primary system flow

CRM PostgreSQL → Audit module registry → Deterministic SQL executor → KPI and issue model → Audit API → Dashboard drilldown

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

- `crm-audit/server/index.js`
- `crm-audit/server/registry.js`
- `crm-audit/server/modules/opportunity.js`
- `crm-audit/server/modules/users.js`
- `crm-audit/web/src/components/AuditDashboard.tsx`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **68,614**
