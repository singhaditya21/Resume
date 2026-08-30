# AIbot Production RAG API

- **Evidence status:** Source-backed prototype
- **Category:** Knowledge, RAG & document AI
- **Source package:** `KB PROD.zip`

A backend RAG service decomposition for embedding, Milvus retrieval, reranking, model generation and telemetry.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

The archived services implement the core RAG pipeline, but missing imported routes and the referenced root application prevent a verified runnable claim.

## Technical stack

Python · FastAPI · Milvus · SentenceTransformers · llama.cpp · OpenTelemetry · Docker

## Skills demonstrated

- RAG service boundaries
- Vector retrieval
- Provider abstraction
- Telemetry
- Deployment packaging
- Gap analysis

## Primary system flow

Client request → Incomplete API shell → Query embedding → Milvus retrieval → Rerank and generation → Answer with sources

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

- `app/services/rag_pipeline.py`
- `app/services/retriever.py`
- `llm/providers/chat_client.py`
- `vector_store/`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **11,629**
