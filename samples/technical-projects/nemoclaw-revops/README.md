# NEMOCLAW RevOps Intelligence

- **Evidence status:** Source-backed prototype
- **Category:** Agentic AI & automation
- **Source package:** `NEMOCLAWFORMY.zip`

A multi-agent revenue-operations platform for natural-language analytics, opportunity intelligence, research and executive reporting.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

LangGraph coordinates NL-to-SQL, research, portfolio and reporting agents using hosted or local models, semantic cache and self-correcting execution.

## Technical stack

Python · FastAPI · LangGraph · LangChain · Chroma · SentenceTransformers · SQLite · React

## Skills demonstrated

- Agent orchestration
- NL-to-SQL
- Semantic caching
- Provider failover
- Scheduled agents
- Executive reporting

## Primary system flow

CRM and Redash → Ingestion and cache → SQLite and Chroma → Schema-aware planner → Specialized agent DAG → Reports and alerts

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

- `backend/main.py`
- `backend/orchestrator.py`
- `backend/llm_client.py`
- `backend/data_ingestion.py`
- `backend/sqlite_engine.py`
- `backend/agents/`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **75,868**
