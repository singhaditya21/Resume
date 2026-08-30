# NetSuite OAuth Token & Wrapper Service

- **Evidence status:** Deterministic / AI-enabling
- **Source evidence:** Sanitized source samples
- **Verification:** Static review only · code not executed
- **Delivery maturity:** Deterministic implementation archive
- **Intelligence type:** Deterministic / AI-enabling
- **Category:** Enterprise operations
- **Project family:** Independent system
- **Source package:** `NetSuiteToken.zip`

A .NET service for RSA-PSS client assertions, OAuth token exchange and controlled NetSuite API integration.

The technical claims below are grounded in the supplied source archive.

## AI or automation role

No AI capability is implemented; the technical value is secure enterprise authentication and integration design.

## Technical stack

C# · .NET 8 · ASP.NET Core · JWT · RSA-PSS · Swagger · Docker

## Skills demonstrated

- OAuth client assertions
- JWT signing
- Certificate handling
- API integration
- Dependency injection
- Security hardening

## Primary system flow

Authorized caller → Token controller → Key and configuration → Signed JWT assertion → NetSuite OAuth → Bounded API call

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

- Meaningful anonymized source samples: **8**
- Retained empty source placeholders: **0**
- Total included source files: **8**
- Included sanitized source bytes: **13,121**
