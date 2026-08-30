# IdeaStorm AI Opportunity & Agent Governance

- **Evidence status:** Code-derived architecture
- **Category:** Agentic AI & automation
- **Source package:** `Ideastorm.zip`

An enterprise idea-to-outcome platform with AI triage, duplicate detection, governed agents, human review, POC tracking and ROI evidence.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

A scheduler and event plane coordinate specialized agents behind policy, budget, guardrail and kill-switch gates, with deterministic fallback and human approval.

## Technical stack

React · TypeScript · Vite · Fastify · PostgreSQL · Playwright · JWT · Agent SDK

## Skills demonstrated

- Agent governance
- Human-in-the-loop
- Policy and budget gates
- Run tracing
- Event orchestration
- Outcome measurement

## Primary system flow

Idea portal → Idea service → PostgreSQL and event bus → Policy-gated agent runtime → AI proposal → Human review and outcome

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

- `server/src/agents.ts`
- `server/src/agent-scheduler.ts`
- `server/src/llm.ts`
- `server/src/agent-reflection.ts`
- `server/src/bn-agents.ts`
- `packages/agent-sdk/`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **24**
- Included sanitized source bytes: **112,769**
