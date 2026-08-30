# NewsNext Semantic News Intelligence

- **Evidence status:** Deterministic / AI-enabling
- **Category:** Data & decision intelligence
- **Source package:** `Newsnext.zip`

A zero-dependency news aggregation and personalization service with semantic image matching, trust controls and digest workflows.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

Local feature hashing, n-grams, cosine similarity, entity extraction and taxonomy scoring provide semantic ranking without an LLM runtime.

## Technical stack

Node.js · JavaScript · SQLite · Playwright · n8n · RSS / Atom · SMTP

## Skills demonstrated

- Semantic retrieval
- Feature hashing
- Feed ingestion
- Taxonomy design
- Caching
- Content governance

## Primary system flow

RSS and digest sources → Parser and normalizer → Entity and taxonomy engine → Semantic image ranker → SQLite cache → Authenticated dashboard

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

- `IMAGE-ENGINE.md`
- `lib/image-engine/text.js`
- `lib/image-engine/engine.js`
- `lib/image-engine/taxonomy.js`
- `lib/rss.js`
- `lib/db.js`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **155,417**
