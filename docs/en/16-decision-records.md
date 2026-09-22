> **English edition.** [Italian version](../it/16-decision-records.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 16 · Architecture Decision Records

All ADRs have been **PROPOSED**. None are described as accepted. The alternatives remain useful even if the recommendation changes.

## ADR-001 · Authorization form

**Status: PROPOSED**

### Context
ValueFlows represents responsibility/custody; F01/F02 show that they are not ACLs.

### Problem
Support collaboration and organizations without conferring sales or administration from economic attributes.

### Options
Global RBAC; ACL for object; Generalized ReBAC; hybrid scoped.

### Proposed decision
Scoped RBAC with explicit membership and grant, status attributes and acting_for delegation; controller distinct from primaryAccountable/custodian.

### Consequences
New additive structures, action-testable policy, explicit historical migration.

### Risks
Incomprehensible legacy and too large grants; prohibit freely editable metadata sources.

### Open questions
Q03–Q05, Q14–Q15; controller definition and private attributes. See [team questions](14-open-questions.md) and [evidence log](04-authorization-audit.md).

## ADR-002 · Permissions Authority

**Status: PROPOSED**

### Context
Zenflows owns resources/PostgreSQL; DPP does not consult the relevant rights today.

### Problem
Avoid divergent ACLs without imposing a new operational service.

### Options
Local policies; Zenflows module; dedicated authz service; external engine.

### Proposed decision
Permission module in Zenflows with stable internal decision API and authoritative permission data in PostgreSQL itself.

### Consequences
Easier local transactions; DPP depends on authority, future extraction possible.

### Risks
Zenflows availability and load; ownership of the contract must be assigned.

### Open questions
Q01–Q02 and Q12; SLO, volumes and team organization. See [team questions](14-open-questions.md) and [evidence log](04-authorization-audit.md).

## ADR-003 · Cross-service enforcement

**Status: PROPOSED**

### Context
Proxy forward header; DPP handlers do not invoke a shared policy (F03/F04).

### Problem
Do not allow a bypass through another internal service or domain.

### Options
Gateway-only; duplicate ACLs; remote decision; pre-issued capabilities.

### Proposed decision
PEP in each application service, online authz for initial writes, fail-closed and principal/action/object/version/digest contracts; local rules only restrictive.

### Consequences
Coordinated migration Zenflows→consumer; no positive initial cache; CAS policy and necessary audits.

### Risks
TOCTOU cross-DB and outage; don't promise atomicity with simple remote allow.

### Open questions
Q06, Q11–Q12: in-flight window and permit/drain protocol for critical actions. See [team questions](14-open-questions.md) and [evidence log](04-authorization-audit.md).

## ADR-004 · DPP authorization and lifecycle

**Status: PROPOSED**

### Context
Sections model but no validated ledger repair or binding resource; different generic PUT and status.

### Problem
Allow repairs without rewriting manufacturer specifications.

### Options
Independent DPP; same editor rights; derived policy and commands per section.

### Proposed decision
Typed and versioned resource bindings, separate publish/withdraw, versioned specs, append-only repairs, and section-subordinate attachments.

### Consequences
Data migration and command API; restricted generic PUT, distinct public projection.

### Risks
Model/batch/unit ambiguity, documents already published and orphaned storage.

### Open questions
Q07 and Q13; regulatory requirements, retention, certifier/manufacturer roles. See [team questions](14-open-questions.md) and [evidence log](04-authorization-audit.md).

## ADR-005 · Service identity and delegation

**Status: PROPOSED**

### Context
There are keyrings/envs and technical accounts, not a verified universal delegation.

### Problem
Distinguish the calling process from the human it operates for.

### Options
Global key; per-service token over TLS; mTLS/workload identity.

### Proposed decision
Distinct identities per service/environment with scope and audience, user proof or limited delegated assertion; centrally inventoried rotation and revocation.

### Consequences
Go/Elixir/TS shared protocol clients, server-side secret storage, audit actor+service.

### Risks
Service compromised with DB access; mTLS alone does not limit business actions.

### Open questions
Q08 and Q17; available infrastructure, DID trust and federation. See [team questions](14-open-questions.md) and [evidence log](04-authorization-audit.md).

## ADR-006 · Commerce identity and Medusa

**Status: PROPOSED**

### Context
Preview mock without backend; seller string does not match collaborative resource.

### Problem
Separate customer, seller, organization member, inventory and finance.

### Options
Editor=seller; seller only org; seller entity with legal subject; immediate multi-vendor marketplace.

### Proposed decision
distinct seller entity linked to verified person/org, principal/customer mapping, separate commercial roles; starting from limited scope and Medusa version evaluated with spike.

### Consequences
Adapter and mandatory multi-seller testing, authoritative orders/stocks/payments in Medusa, idempotent events towards VF/DPP.

### Risks
Double master stock, PII orders and payout; non-equivalent license/mandate.

### Open questions
Q09–Q10, Q18; single vs multi-seller, PSP, regulations and authority inventory. See [team questions](14-open-questions.md) and [evidence log](04-authorization-audit.md).
