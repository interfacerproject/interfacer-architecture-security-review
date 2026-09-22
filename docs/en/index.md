> **English edition.** [Italian version](../it/index.md) · Technical terms and commit-pinned evidence are shared across both editions.

# Interfacer · Architectural review and security

**Code analysis, not deployment attestation. Decisions proposed, not approved.**

This investigation was created to make Interfacer usable by more people, organizations and future sellers without confusing a valid signature with the right to modify an object.

## What was analyzed

Six local repositories, six additional application components retrieved from the GitHub organization, and the existing document site. Rebuild of GraphQL, REST, Keypairoom/Zenroom, ValueFlows, DPP, feedback, inbox, wallet, fabaccess and preview commerce. [Versions and depth of coverage](appendix/repository-map.md).

## Issues confirmed in source

1. **Identity not used in Zenflows domain:** the reviewed CRUD paths ignore the authenticated requester.
2. **Economic controls not equivalent to permits:** events compare the client-provided `provider` with responsibility/custody of the asset.
3. **DPP with incomplete enforcement:** several writes do not verify the caller; creation and attachments do not verify the right to the product.
4. **Inconsistent identity between services:** Feedback uses an identifier declared separately from the verified key; the proxy does not correct this separation.
5. **Public reading not separated from private data:** Resources with nested relationships, draft DPPs, and files require an explicit policy before introducing private data.

The routes, conditions and limits are in the [findings register](04-authorization-audit.md). Particularly sensitive operational issues are in a separate local report, not included in the site. No credentials are reproduced.

## Proposed direction

An authorization module **inside Zenflows**, with authoritative data in PostgreSQL; enforcement in the domain and in each service. DPP maintains data and document rules, but consults the authority for rights to the resource. Shared contract and thin clients, not a new mandatory microservice. Separate commercial permissions from collaborative ones.

## Decisions required

- Who can administer a resource and with what evidence are historical records migrated?
- What rights are inherited from the organization/project?
- What consistency is needed for revocation and cross-service writes?
- Which DPP sections are public, editable or append-only?
- Who is the legal seller, as distinct from author, collaborator and custodian?

## Reading paths

| Recipient | Path |
|---|---|
| Maintainer and tech lead | [Summary](01-executive-summary.md) → [Roadmap](12-migration-roadmap.md) → [Discussion](17-team-discussion.md) |
| Backend developers | [Current Architecture](02-current-architecture.md) → [Audit](04-authorization-audit.md) → [Permissions Model](08-permission-model.md) |
| Frontend and SDK | [Authentication](03-authentication-analysis.md) → [DPP](06-dpp-analysis.md) → [Medusa](10-medusa-implications.md) |
| DevOps and security | [Trust cross-service](07-cross-service-authorization.md) → [Threat model](11-threat-model.md) → [Test](13-testing-strategy.md) |
| Proposal Reviewers | [Alternatives](15-alternative-solutions.md) → [ADR PROPOSED](16-decision-records.md) → [Open issues](14-open-questions.md) |

[Method, limitations and validation](appendix/validation.md) · [Code reference](appendix/code-references.md) · [Glossary](appendix/glossary.md)
