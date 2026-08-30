# Autonomous AI Data Stack

- **Evidence status:** Source-backed prototype
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Prototype archive
- **Intelligence type:** AI-assisted intelligence
- **Category:** Data & decision intelligence
- **Project family:** Database & analytics copilots
- **Source package:** `DATAMART-DWH.zip`

A warehouse and natural-language analytics prototype that transforms operational CRM data into dimensional models and interactive analysis.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

NVIDIA and Gemini adapters generate SQL, summaries and chart choices over an introspected warehouse; the current direct-execution path requires stronger SQL controls.

## Technical stack

Python · PostgreSQL · pandas · Streamlit · Plotly · Flask · NVIDIA NIM · Gemini

## Skills demonstrated

- Data warehousing
- ETL
- Dimensional modeling
- NL-to-SQL
- Analytical UX
- Deployment automation

## Primary system flow

Operational CRM → Python rebuild ETL → Bronze and silver models → Schema introspection → LLM-generated SQL → Chart and narrative

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

- Meaningful anonymized source samples: **18**
- Retained empty source placeholders: **0**
- Total included source files: **18**
- Included sanitized source bytes: **29,348**
