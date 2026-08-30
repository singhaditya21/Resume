# MPR Support Intelligence Hub

- **Evidence status:** Source-backed prototype
- **Category:** Knowledge, RAG & document AI
- **Source package:** `MPRBOT-1.zip`

A support intelligence workspace combining historical cases, operating procedures and hybrid retrieval for recommendations and diagnostics.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

BGE embeddings, FAISS, BM25 and a cross-encoder retrieve and rerank evidence before hosted or local Qwen generation, with feedback-aware scoring.

## Technical stack

Python · FastAPI · FAISS · SentenceTransformers · BM25 · llama.cpp · Next.js · PostgreSQL

## Skills demonstrated

- Hybrid RAG
- Cross-encoder reranking
- Case-pair extraction
- Provider failover
- Feedback loops
- Support analytics

## Primary system flow

Cases and SOPs → Cleaning and pairing → FAISS and BM25 → Cross-encoder rerank → Contextual LLM → Recommendation and feedback

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

- `services/agent.py`
- `services/llm_provider.py`
- `services/retriever.py`
- `services/indexer.py`
- `services/reranker.py`
- `backend_api/app/routers/search.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **59,393**
