# US Project Health Dashboard

- **Evidence status:** Deterministic / AI-enabling
- **Category:** Data & decision intelligence
- **Source package:** `USProjecthealth.zip`

Portfolio-health analytics that reconcile delivery and CRM evidence into weighted red/amber/green outcomes.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

No LLM or retrieval model is present; RAG means deterministic Red/Amber/Green scoring with transparent thresholds and weights.

## Technical stack

Python · FastAPI · Azure DevOps · Redash · Jinja2 · httpx

## Skills demonstrated

- Async integration
- Source reconciliation
- Data quality
- Weighted health scoring
- TTL caching
- Graceful degradation

## Primary system flow

Delivery and CRM sources → Parallel fetch → Alias reconciliation → Metric engine → Weighted RAG score → Portfolio dashboard

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

- `main.py`
- `azure_client.py`
- `redash_client.py`
- `project_report.py`
- `rag_engine.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **14**
- Included sanitized source bytes: **192,755**
