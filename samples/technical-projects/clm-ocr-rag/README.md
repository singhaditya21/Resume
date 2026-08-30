# Contract OCR & Local RAG

- **Evidence status:** Code-derived architecture
- **Category:** Knowledge, RAG & document AI
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

- `app/ocr/ocr_pipeline.py`
- `app/ingest/ingest_service.py`
- `app/retrieval/retriever.py`
- `app/rag/generate.py`
- `app/rag/cite.py`
- `app/main.py`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **64,702**
