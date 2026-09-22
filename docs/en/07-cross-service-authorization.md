> **English edition.** [Italian version](../it/07-cross-service-authorization.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 07 · Cross-service authorization

## Today there is no single chain of trust

| Passage | What he really feels | What he doesn't feel |
|---|---|---|
| GUI→Zenflows signed | Person key possession resolved for username | Right to target ID or organization representation |
| GUI→DPP create | Signature with declared key and URL DID returning 200 | Membership, right to productId, link x-user-id/key |
| GUI→feedback | Bodysuit signature and availability DID | Principal copied from header is not authenticated |
| Proxy→backend | The proxy forwarded the bytes/header | No attestation of identity or decision |
| Inbox→Zenflows | Sender/receiver key lookup | Not a universal policy for social activities |
| Fabaccess→machine | Configured Fabaccess Account Action | Individual right to the machine not verified by an Interfacer policy |

Evidence: [zenflows/src/zenflows/gql/mw/sign.ex:28–72](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/mw/sign.ex#L28-L72); [interfacer-dpp/internal/auth/auth.go:98–151](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/auth/auth.go#L98-L151); [interfacer-feedback-service/internal/auth/middleware.go:15–88](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/auth/middleware.go#L15-L88); [interfacer-proxy/main.go:160–241](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L160-L241); [zenflows-inbox/inbox.go:80–243](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L80-L243); [zenflows-fabaccess/main.py:55–123](https://github.com/interfacerproject/zenflows-fabaccess/blob/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc/main.py#L55-L123).

DPP does not verify a proxy credential and does not require traffic to pass through it. Compose makes the app reachable on the host. Real firewalls and ingress are an open question, not a guaranteed boundary. The proxy forwards headers without deriving a trusted principal. CORS does not authenticate non-browser clients.

## Proposed consistency rule

A write to the DPP associated with resource R must require the **corresponding permission on R**, not just `createdBy == subject` in the DPP DB. No service can assign an organizational role by itself using client data. The DPP policy can be more restrictive, never a second path to get generic resource edit denied by Zenflows.

Example: `dpp.spec.update` implies the technical right to the resource plus specific delegations; `dpp.repair.append` is a distinct and limited action, linked to the same resource/instance. Do not grant generic PUT to the repair operator.

## Evaluation of alternatives

| Solution | Security | Complexity and maintenance | Performance / failure mode | Compatibility and deployment |
|---|---|---|---|---|
| A. Independent policy in each service | Local isolation, but divergence and inconsistent revocations | Low at the beginning, high over time | Fast; split-brain on grant and parent | Easy addition, difficult common semantics |
| B. All decisions in Zenflows | Authoritative data close to resources | Average; god service risk if he decides DPP details | Remote calls; block writes if Zenflows down | Natural for Ecto, less for documents/orders |
| C. Dedicated authz service | Good separation if data and protocol correct | High: sync, HA, observability, migrations | New hop and failure domain | Not justified as an initial prerequisite |
| D. Shared Library/SDK | Uniform contract; does not create common authority | TS/Go/Elixir: a single library is not enough | Fast local, this date if replicated | Useful for protocol clients and test vectors |
| E. Hybrid: authority in Zenflows + local PEPs | Central revocation and local document rules | Average and incremental | Initial remote decision, bankruptcy closed | Registered; no new initial container |
| F. OPA/Cedar/OpenFGA or similar | Formal language/relationships, but they do not cure false principals | Medium-high: data ownership, adapter, policy deployment | Cache/freshness and availability to be designed | Evaluate only after real scheme and load |

**E** uses B for common data and D for contract, avoiding A for shared memberships. A policy engine must not become the first project before closing discovered handlers.

## Minimum contract, yet to be implemented

Decision request: verified principal, possible delegation, service identity, registered action, object type/id, parent binding/version, operation digest, request ID. Answer: allow/deny, non-sensitive reason code, policy version, permission epoch and obligations (allowed fields/sections, expiration). A client cannot choose a weaker action or alternative parent for a more privileged handler.

Handlers derive actions from code; the DPP loads parent from its validated immutable binding and not from the new payload. Call to authority uses TLS and dedicated credential with audience/purpose; sending only `subject=Alice` from a service does not prove that Alice authorized the operation. Verifiable user proof or operation-limited delegated assertion is needed.

## Availability and revocation

- First version: online decisions without positive cache for writes. Timeout/invalid response → deny/retry-safe, not fallback to old free API.
- Public readings: can continue on published snapshot, after removal of private data. Private companies go bankrupt; do not use public cache.
- Revoke: increase epoch and log audits; invalidate derived local sessions/grants. The next decision after committing the revocation sees the effect. **An online check does not make two databases atomic**: operations already authorized in flight must be governed as described in the [proposed architecture](09-proposed-architecture.md).
- Push invalidations are an acceleration, not the only guarantee. For future high availability: multiple decision module replicas with authoritative DB; not freely editable copies of ACLs in MongoDB.

## Technical credentials compromised

A DPP service must be able to ask for decisions and execute only its own domain; do not create global grants or sign for each user. A commerce worker account can issue passports from validated fulfillment events, not transfer ownership of all assets. Distinct DB users and internal inputs reduce blast radius, but do not replace PEPs. A compromise with direct access to the DPP DB remains serious: external audit, backup and integrity checks are also needed after authz.
