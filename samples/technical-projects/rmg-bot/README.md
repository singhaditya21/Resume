# RMG Resource Allocation Assistant

- **Evidence status:** Source-backed prototype
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Prototype archive
- **Intelligence type:** RAG / document AI
- **Category:** Knowledge, RAG & document AI
- **Project family:** RMG & workforce planning
- **Source package:** `RMGBOT.zip`

A local resource-management analytics and conversational allocation assistant grounded in workforce data.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

FAISS retrieval and MiniLM embeddings ground a local Qwen assistant, with structured-query fallbacks for deterministic allocation analysis.

## Technical stack

Python · FastAPI · LangChain · FAISS · SentenceTransformers · llama.cpp · pandas · JavaScript

## Skills demonstrated

- Local inference
- RAG indexing
- Resource analytics
- Grounding
- Offline fallback
- Conversational UI

## Primary system flow

Synthetic allocation data → Resource processor → Chunk and embedding index → FAISS retrieval → Local Qwen → Allocation answer

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

- **Technical decision rationale:** Not established from the supplied archive.

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Meaningful anonymized source samples: **13**
- Retained empty source placeholders: **0**
- Total included source files: **13**
- Included sanitized source bytes: **176,328**
