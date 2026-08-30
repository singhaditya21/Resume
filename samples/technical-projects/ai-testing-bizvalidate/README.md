# BizValidate Agentic Quality Platform

- **Evidence status:** Code-derived architecture
- **Category:** AI testing & quality
- **Source package:** `AITESTING.zip`

An AI-assisted web and API validation platform spanning browser journeys, DOM and accessibility analysis, HAR evidence, visual regression and selector healing.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

A bounded model classifies elements, proposes selectors and tests, analyzes failures and supports healing while Playwright and deterministic validators own execution and evidence.

## Technical stack

Python · FastAPI · SQLAlchemy · PostgreSQL · Playwright · Next.js · React · WebSockets

## Skills demonstrated

- AI-assisted QA
- Browser automation
- Self-healing selectors
- HAR analysis
- Visual regression
- Experimentation

## Primary system flow

Test configuration → Encrypted credential seam → Playwright run → DOM AX HAR discovery → LLM enrichment → Evidence and results

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

- `backend/app/services/pipeline.py`
- `backend/app/services/playwright_engine.py`
- `backend/app/services/dom_analyzer.py`
- `backend/app/services/llm_service.py`
- `backend/app/services/healing_engine.py`
- `backend/app/autoresearch/`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **159,481**
