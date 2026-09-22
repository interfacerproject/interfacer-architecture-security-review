> **English edition.** [Italian version](../it/11-threat-model.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 11 · Threat model

## Assets, actors and boundaries

Assets: keys/seeds, people and contacts, memberships/delegations, project contents, inventory status, provenance, DPP documents/certificates, attachments, points, machine commands and future commercial data. Actors: Anonymous, Other Scope Authenticated User, Former Contributor, Compromised Service, Compromised Browser, Administrative Insider, and Untrusted Federated Peer.

[Architecture and borders](02-current-architecture.md); [evidence register](04-authorization-audit.md). A CVSS is not assigned without deployment inventory, data classification and operating conditions.

| Threat | Status / evidence | Conditions and impact | Incremental Defense |
|---|---|---|---|
| BOLA/IDOR resource | F01 statically confirmed | Person signed, target valid → edit unscoped | Principal in domain, object policy |
| BFLA on organizations/catalogues | F01 and mutation matrix | Ordinary user can invoke non-role functions | Logged actions, roles scoped/catalog manager |
| Escalation via membership | Risk from F01/F09 | Reuse relations that are currently editable as ACL | Secure grant/membership before ReBAC |
| Unauthorized transfer | F02 | Input provider not equal to verified principal | Acting_for and permissions on origin/destination |
| Bypass through DPP | F03 | DPP backend reachable, handler unprotected | Local enforcement + common authority |
| Identity spoofing | F04 | Own signature + separate user ID | Binding server-side key/principal |
| Private reading via guest/nested | F05 | Sensitive data on public root or relationships | Projections, field-level policy, query filtering |
| Replay / duplicate effect | F06 | Valid request reused or retry post-commit | Nonce, TTL, audience and idempotence |
| Service credential compromised | Architectural risk | DPP/Fabaccess/overprivileged worker | Minimum Purposes, Distinct Credentials, Audits and Rotation |
| Point manipulation | F07 | Valid DID with token request | Limited issuer and event-derived reward |
| Untrusted social/egress peer | F08 potential SSRF | URL actor/object to unauthorized destinations | Signature/provenance and egress policy |
| Browser key theft | Storage confirmed, exploit not observed | XSS or same-origin malicious dependency | CSP, separate file source, key exposure reduction |
| DPP link substitution | Confirmed model limit | productId not validated and parent editable | Immutable binding, privileged parent change |
| Incomplete audit | Limit of examined routes | HTTP/event logs do not reconstruct actor/decision denied | Dedicated audit and correlation |
| Fake/cross-seller webhook | Future requirement | Commerce not yet implemented | Signature, replay defense, seller-scoped order queries |
| TOCTOU grant/status | Architectural risk; status DPP read-then-write | Revoke or status changes between check and commit | Versions, local locks, explicit cross-service workflow |

## Frontend and NEXT_PUBLIC

All `NEXT_PUBLIC_*` variables used by browser code must be considered public: URL/spec/feature flag can be; privileged credentials no. GUI client creation includes admin configuration and SDK registration uses it in headers; this is an exposure mechanism **conditional on the value entered in build**, not a proof of live site content. [interfacer-gui/contexts/AuthContext.tsx:81–109](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/contexts/AuthContext.tsx#L81-L109); [interfacer-client/src/auth/AuthClient.ts:51–241](https://github.com/interfacerproject/interfacer-client/blob/dfb1baabf16516a845957d5587ccb933c1874221/src/auth/AuthClient.ts#L51-L241).

The detail of local files with values, tracking status and verification of chunks is in the confidential report. No secret values ​​or hashes are printed. Recommendation: Server-side mediated logging, consumer inventory, rotation after cutover, artifact/caches invalidation, and history checking. Moving a variable from the env to another frontend file does not protect it.

Keys and seeds are accessible to JavaScript in localStorage. [interfacer-gui/contexts/AuthContext.tsx:242–302](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/contexts/AuthContext.tsx#L242-L302); [interfacer-client/src/config/storage.ts:1–40](https://github.com/interfacerproject/interfacer-client/blob/dfb1baabf16516a845957d5587ccb933c1874221/src/config/storage.ts#L1-L40). The severity increases if user files are rendered as active content from the same source: route and remediation details reserved, without demo payloads.

## Deployment

- `GQL_AUTH_CALLS` can disable Sign and Admin; default true. Make it non-deactivable in production without documented break-glass and alarm. [zenflows/conf/runtime.exs:89–131](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/conf/runtime.exs#L89-L131); [zenflows/src/zenflows/gql/mw/admin.ex:28–42](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/mw/admin.ex#L28-L42).
- Compose DPP publishes DB/storage ports and enables anonymous download; separate dev template from production, private bindings, private storage for unpublished content. [interfacer-dpp/docker-compose.yml:3–61](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/docker-compose.yml#L3-L61).
- Restroom receives server-side cryptographic material in some streams; private network, appropriate TLS, no body logging, allowlist contracts and quotas. [zenflows/src/zenflows/restroom.ex:47–133](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/restroom.ex#L47-L133); [zenflows/src/zenflows/did.ex:63–112](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/did.ex#L63-L112).
- Proxy with generalized read-all body/retry: limits, timeouts, status propagation and idempotent retry must be checked; don't trust it with the semantics of auth. [interfacer-proxy/main.go:160–241](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L160-L241).
- Dependency and image versions are a maintenance surface. A full CVE audit was not performed; do not infer vulnerabilities from Next/Elixir/Postgres seniority alone.

## Compound attacks to discuss

1. Limit `updateEconomicResource` but leave createEconomicEvent: integrity still modifiable via indirect effects.
2. Limit GUI to «my DPPs» but leave direct PUT/delete: UI filter is not ACL.
3. Correct SQL ownership with unauthenticated principal: database faithfully enforces the wrong decision.
4. Revoke an org member but leave seller/worker tokens and derivative grants: partial offboarding.
5. Make a DPP private without removing anonymous bucket, GUI cache, and published copies: non-retroactive confidentiality.

## Secure validation

Play only on local fixtures and origins disconnected from shared services. Use fake DID resolver/Restroom, generated test keys, ephemeral DBs; acquire before/after status and audit. No request versus production examples are included. For critical surfaces, read the confidential report first and plan disclosure/coordination with maintainers.
