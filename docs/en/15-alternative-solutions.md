> **English edition.** [Italian version](../it/15-alternative-solutions.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 15 · Alternatives and selection criteria

The full A–F comparison is in [cross-service authorization](07-cross-service-authorization.md). Here the reversible choices and the reasons for not introducing premature complexity are explained.

## Minimal solution: owner check in each handler

**Pros:** Quick for a single object; low deployment overhead. **Cons in real code:** primaryAccountable is not principal; missing organizations/delegations; events indirectly modify the resource; DPP/feedback have different identities. **Reasonable use:** Temporary gate for records with verified controller, never final solution nor indiscriminate backfill. Evidence F01–F04.

## Gateway as sole enforcement

**Pros:** one entry point to protect; uniform rate limiting and identity normalization. **Cons:** the current proxy does not semantically understand mutations, objects and side effects; direct access to origins and internal domain paths can bypass it. Even an advanced gateway does not know the Ecto/Mongo transactional state. **Choice:** Gateway for TLS/boundaries, PEP in service and domain. [interfacer-proxy/main.go:67–143](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L67-L143); [zenflows/src/zenflows/vf/economic_event/resolv.ex:38–49](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/resolv.ex#L38-L49).

## Modular Zenflows before an authz service

**Pro:** resources and permissions in the same transaction; deployment already managed; integrates Elixir domain calls. **Cons:** DPP depends on its availability and the Zenflows team becomes the owner of the contract. **Triggers for future extraction:** multiple federated authorities, independent release policies, metered load, dedicated operations team, or scalability incompatible with the core service. Extracting without these triggers creates a distributed problem before solving the application one.

## External policy engine

- **OPA/Rego:** good for attribution rules and distribution bundles; membership, freshness and PEP data still need to be managed. JSON logic does not replace transactions.
- **Cedar:** typed entity/action/context model useful for revisions; requires adapter and correct data supply.
- **OpenFGA/SpiceDB:** suitable for complex ReBAC models and tuples; they add a service, storage, and consistency semantics that the team must operate correctly.

No engine was integrated or benchmarked. If the graph remains org→project→resource with contained roles, normal tables and tested policy module are easier to manage. Policy engine does not fix a spoofable `x-user-id` or a mutation that does not invoke PEP.

## Database RLS

PostgreSQL RLS can defend against some Zenflows query errors, but requires context propagation for connection/pool, job management, privileged functions, transactions, and relationship coverage. MongoDB/MinIO don't magically get that policy. **Proposal:** Second line of defense after a correct application model, not a substitute for multi-object authorization and side effects.

## JWT/sessions vs signature on each request

Current signatures maintain compatibility but increase browser key management and replay context. BFF sessions reduce exposure of long-lived private keys to the frontend during ordinary use, but introduce session stores, CSRF risk, cookie handling, and federation concerns. Short JWTs make transport simple, but require reliable revocation/audience and proof/delegation. **Proposal:** first fix authorization and binding, then migrate authn with versioned compatibility; don't attempt both rewrites in one sprint.

## When to change recommendation

If maintainers require offline DPP with authorized edit, allow very narrow capabilities and clarify deferred revocation; do not promise immediate revocation. If the federation requires more authority, introduce namespace issuer, trust agreement and role mapping, without accepting remote grants equivalent to platform admin. If the online load becomes prohibitive, measure scoped/versioned cache with staleness budget before duplicating the entire permission store.
