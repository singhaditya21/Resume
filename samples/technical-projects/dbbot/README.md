# Autonomous AI SQL Assistant

- **Evidence status:** Source-backed prototype
- **Category:** Agentic AI & automation
- **Source package:** `DBBOT.zip`

A conversational CRM and ERP analytics assistant with intent routing, schema retrieval, guarded SQL generation, result narration and MCP tools.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Provider-routed LLMs classify intent, plan and generate SQL or functions; deterministic direct paths, retrieval and SQL guards constrain execution.

## Technical stack

Node.js · Express · React · Vite · PostgreSQL · Groq · NVIDIA NIM · MCP

## Skills demonstrated

- Multi-provider inference
- Text-to-SQL
- Schema retrieval
- MCP tooling
- Provider failover
- Query safety

## Primary system flow

Conversational query → Intent router → Direct path or catalog retrieval → SQL agent → Validation and PostgreSQL → Analyst narrative

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

- `backend/routes/query.js`
- `backend/agents/intentClassifier.js`
- `backend/agents/retrievalAgent.js`
- `backend/agents/sqlAgent.js`
- `backend/utils/providerManager.js`
- `backend/mcpServer.js`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **71,541**
