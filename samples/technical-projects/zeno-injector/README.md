# Zeno RAG Ingestion Platform

- **Evidence status:** Code-derived architecture
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Implementation archive
- **Intelligence type:** RAG / document AI
- **Category:** Knowledge, RAG & document AI
- **Project family:** Zeno & enterprise knowledge
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

See [`PUBLIC_EVIDENCE_MAP.md`](PUBLIC_EVIDENCE_MAP.md) for a claim-to-sample map and the complete anonymized sample inventory. Original archive-member paths are intentionally not published.

## Attribution, outcomes and decisions

- **Personal ownership:** Not established from the supplied archive.
- **Measured outcomes:** Not established from the supplied archive.

- ACL metadata is preserved through ingestion and vector persistence.
- Embedding contracts, delete guards and a recovery ledger bound repeatable ingestion.

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Meaningful anonymized source samples: **15**
- Retained empty source placeholders: **9**
- Total included source files: **24**
- Included sanitized source bytes: **96,283**
