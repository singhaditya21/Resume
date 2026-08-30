# Zeno Enterprise Knowledge Assistant

- **Evidence status:** Code-derived architecture
- **Category:** Knowledge, RAG & document AI
- **Source package:** `KB.zip`

An enterprise knowledge assistant with ACL-aware hybrid retrieval, confidence refusal, streaming answers, OTP access and production observability.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Dense and BM25 retrieval are fused and reranked before guarded model generation; ACL and confidence gates decide whether context may be used or the system must refuse.

## Technical stack

Python · FastAPI · LlamaIndex · Milvus · Redis · PostgreSQL · Next.js · Kubernetes

## Skills demonstrated

- Production RAG
- ACL-aware retrieval
- Reciprocal-rank fusion
- Guardrails
- Streaming UX
- Observability

## Primary system flow

Authenticated portal → Input guard → Dense and BM25 retrieval → RRF and rerank → ACL and confidence gate → Streamed cited answer

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

- `backend/retrieval/retrieval.py`
- `backend/retrieval/agentic_rag.py`
- `backend/retrieval/self_reflection.py`
- `backend/app/llm_client.py`
- `backend/app/guardrails.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **172,370**
