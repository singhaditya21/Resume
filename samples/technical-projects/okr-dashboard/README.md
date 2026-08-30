# AI-Assisted OKR Strategy Dashboard

- **Evidence status:** Code-derived architecture
- **Category:** Data & decision intelligence
- **Source package:** `OKRDashboard.zip`

A balanced-scorecard workspace that combines live OKR measures, strategy maps and streaming executive analysis.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Role- and period-scoped context is streamed to an OpenAI-compatible model for grounded executive answers and chart specifications.

## Technical stack

Python · Flask · PostgreSQL · React · Vite · Recharts · SSE

## Skills demonstrated

- OKR analytics
- Streaming AI UX
- Prompt grounding
- Dynamic chart generation
- Connection pooling
- Strategy visualization

## Primary system flow

OKR DataMart → Background synchronizer → Live metric store → Dashboard APIs → Scoped LLM analysis → Narrative and chart

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

- `TECHNICAL_SPEC.md`
- `server.py`
- `dashboard/src/App.jsx`
- `dashboard/src/components/DeliveryDashboard.jsx`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **438,357**
