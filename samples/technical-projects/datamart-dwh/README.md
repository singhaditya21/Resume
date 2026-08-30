# Autonomous AI Data Stack

- **Evidence status:** Source-backed prototype
- **Category:** Data & decision intelligence
- **Source package:** `DATAMART-DWH.zip`

A warehouse and natural-language analytics prototype that transforms operational CRM data into dimensional models and interactive analysis.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

NVIDIA and Gemini adapters generate SQL, summaries and chart choices over an introspected warehouse; the current direct-execution path requires stronger SQL controls.

## Technical stack

Python · PostgreSQL · pandas · Streamlit · Plotly · Flask · NVIDIA NIM · Gemini

## Skills demonstrated

- Data warehousing
- ETL
- Dimensional modeling
- NL-to-SQL
- Analytical UX
- Deployment automation

## Primary system flow

Operational CRM → Python rebuild ETL → Bronze and silver models → Schema introspection → LLM-generated SQL → Chart and narrative

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

- `run_dwh_etl.py`
- `deploy_dashboard_nvidia.py`
- `deploy_dashboard_nlp.py`
- `dwh_setup.py`
- `autonomous_ai_data_stack.md`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **18**
- Included sanitized source bytes: **29,348**
