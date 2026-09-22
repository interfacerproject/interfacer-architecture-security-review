> **English edition.** [Italian version](../../it/appendix/glossary.md) · Technical terms and commit-pinned evidence are shared across both editions.

# Glossary

| Term | Usage in this review |
|---|---|
| Authn | Authentication: who has proven possession of the credential |
| Authz | Authorization: Can that principal do that action on those objects? |
| Principal / subject | Verified stable identity, distinct from ID declared in the payload |
| Acting for | Representation of an organization verified by delegation |
| Administrative Controller | Person who manages access/control of the resource; proposed concept |
| primaryAccountable | ValueFlows Economic Responsibility, not ACL |
| custodian | Custody of the resource, not universal administration |
| PEP | Policy Enforcement Point in the service/domain that enforces the decision |
| PDP | Policy Decision Point; proposed in the Zenflows | module
| RBAC / ABAC / ReBAC | Policy based on roles, attributes and relationships respectively |
| BOLA / IDOR | Accessed or modified by object ID without proper authorization |
| BFLA | Access to a privileged function without rights |
| DID | Decentralized identifier; resolving it is not the same as verifying a permission |
| Zenroom / Zencode | Cryptographic Runtime and Contract Language |
| Restroom | Contract execution HTTP service used by Zenflows |
| DPP | Digital Product Passport, distinct from commercial listing |
| TOCTOU | Status/permission changes between control and use |
| Epoch / fencing | Authority version used to invalidate decisions or obsolete writers |
| Fail-closed | Unknown failure/decision does not grant access |
| Outbox | Durable recording of events in local transaction, subsequent delivery |
| Idempotence | Repeating the same operation does not produce a second effect |
| PROPOSED | ADR to be discussed, not accepted by the team |
