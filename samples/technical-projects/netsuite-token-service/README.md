# NetSuite OAuth Token & Wrapper Service

- **Evidence status:** Deterministic / AI-enabling
- **Category:** Enterprise operations
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

- `NetsuiteAPI/Services/TokenService.cs`
- `NetsuiteAPI/NetSuiteConfigurationHelper.cs`
- `NetsuiteAPI/Controllers/HomeController.cs`
- `NetsuiteAPI/Program.cs`

## Public-package boundary

This is a curated, non-runnable portfolio snapshot rather than the original production archive. Credentials, environment files, customer datasets, contract documents, employee records, database backups, vector indexes, model weights, generated dependencies, media and live deployment state are excluded. Selected source text is anonymized, scanned and redacted for credential-like values, known customer names, identity literals, email addresses, phone numbers, identifiers, service URLs, network addresses and local filesystem paths.

- Included source files: **8**
- Included sanitized source bytes: **13,121**
