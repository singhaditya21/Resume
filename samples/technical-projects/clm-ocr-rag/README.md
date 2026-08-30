# Contract OCR & Local RAG

- **Evidence status:** Code-derived architecture
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Implementation archive
- **Intelligence type:** RAG / document AI
- **Category:** Knowledge, RAG & document AI
- **Project family:** Independent system
- **Source package:** `CLMOCR.zip`

A private contract-intelligence pipeline for OCR, hybrid retrieval, local generation, citations, summaries and obligation extraction.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

OCR and digital extraction feed dense and BM25 retrieval, cross-encoder reranking and local Qwen generation with source citations.

## Technical stack

Python · FastAPI · Tesseract · pdfplumber · Chroma · BM25 · SentenceTransformers · llama.cpp

## Skills demonstrated

- Document OCR
- Hybrid RAG
- Cross-encoder reranking
- Citation grounding
- Local inference
- Contract analytics

## Primary system flow

PDF or image → Digital extraction or OCR → Chunk and metadata pipeline → Chroma and BM25 → Cross-encoder rerank → Local cited answer

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

- The inference boundary stays local while dense and lexical retrieval are combined before reranking.
- Answer citations remain tied to retrieved chunks rather than model-only assertions.

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Meaningful anonymized source samples: **24**
- Retained empty source placeholders: **0**
- Total included source files: **24**
- Included sanitized source bytes: **64,702**
