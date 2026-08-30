# OneView Customer & Project Intelligence

- **Evidence status:** Code-derived architecture
- **Category:** Data & decision intelligence
- **Source package:** `Oneview.zip`

A multi-service account 360, adoption, project-health and executive reporting platform with grounded AI narratives.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Scoped customer and portfolio context feeds internal and hosted model services for summaries, risks, actions and adoption narratives with caching and deterministic health scoring.

## Technical stack

Python · FastAPI · React · Vite · SQLite · OpenAI API · Nginx · Docker

## Skills demonstrated

- Multi-service analytics
- Grounded AI
- Multimodal analysis
- Prompt governance
- Report automation
- RBAC

## Primary system flow

Enterprise sources → Refresh pipelines → JSON / SQLite stores → Three application services → Grounded LLM gateway → Executive reports

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

- `scripts/build_data.py`
- `scripts/summary.py`
- `adoption-analytics/backend/insights.py`
- `adoption-analytics/backend/qbr_report.py`
- `coe-dashboard/main.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **278,720**
