# Zeno RAG Ingestion Platform

- **Evidence status:** Code-derived architecture
- **Category:** Knowledge, RAG & document AI
- **Source package:** `Prod_Data_Injection.zip`

Production document ingestion with multimodal parsing, governed chunking, embeddings and ACL-aware vector persistence.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Qwen embedding and vision services transform structured and scanned documents into retrieval-ready chunks while enforcing embedding parity and metadata contracts.

## Technical stack

Python · FastAPI · Milvus · PostgreSQL · LlamaIndex · MinIO · Prometheus · OpenShift

## Skills demonstrated

- RAG ingestion
- Multimodal OCR
- Vector schema governance
- ACL propagation
- Idempotent orchestration
- Observability

## Primary system flow

Enterprise documents → Discovery and diff → Parser / OCR router → Token-aware chunker → Embedding gateway → Milvus collection

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

- `ARCHITECTURE.md`
- `src/zeno_injector/orchestrator/run.py`
- `src/zeno_injector/parsing/router.py`
- `src/zeno_injector/processing/chunker.py`
- `src/zeno_injector/store/milvus_sink.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **96,283**
