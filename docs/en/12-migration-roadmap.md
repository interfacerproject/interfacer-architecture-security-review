> **English edition.** [Italian version](../it/12-migration-roadmap.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 12 · Incremental Roadmap

## Principles

Contain first, shape then; no mandatory rewriting. Overlapping phases where indicated. Estimates must be made by the team after DevOps/QA availability; the first milestone is indicative 1–2 sprints, while the entire program depends on historical data and commerce requirements. Each phase has a backend contact and a cross-service reviewer; don't leave authorization as an implied responsibility of the frontend.

## Phase 0 · Containment and confidential triage

- **Goal:** Immediately reduce uncontrolled writes and exposed privileges.
- **Repository:** dpp, proxy/deployment, gui, client, feedback; wallet/fabaccess if active.
- **Dependencies:** inventory of actual inputs and operational owner; no ACL migration required.
- **Changes/tasks:** temporary blocking of unprotected DPP writes on input and source; audit credentials/browser and administrative routes; restricted server-side registration; feedback key/person binding; rate/body limits and logging without secrets; Verify Zenflows auth enabled.
- **Risks:** DPP editor/signup interruption, consumer admin not registered. Communicate selective maintenance mode.
- **Test:** direct and proxy access, no header and different identity; browser bundle inspection without printing values; smoke signup on sandbox.
- **Deliverable:** documented containment, consumer/rotation inventory, decision on disabled routes.
- **Acceptance:** no known DPP write is accessible without gate; no administrative credentials needed for the new browser; feedback identity resolved server-side or writes disabled.
- **Rollback:** keep routes blocked/read-only, do not restore revoked secrets or allow anonymous; server signup compatibility.

## Phase 1 · Complete operational inventory

- **Objective:** Associate the source matrix with the real deployment.
- **Repository:** all applications, deployments and SDKs.
- **Dependencies:** phase 0; authorized access to the configuration, not to the plaintext secrets.
- **Task:** associate images/digest/commit; SDL/runtime routes offline or isolated environment; search for jobs/import/CLI/script and client outside GUI; classify actions and data; extend array with owner and test ID.
- **Risks:** Different SDK build from checkout, uninitialized submodules, forgotten legacy services.
- **Test:** coverage check static root fields/routes and isolated staging comparison; inventory review with maintainer.
- **Deliverable:** versioned baseline of effective API and trust boundaries.
- **Acceptance:** each enabled write has principal source, planned and responsible PEP; no unknown endpoints in runtime.
- **Rollback:** documentary; no DB alteration.

## Phase 2 · Model and authoritative data

- **Objective:** define controller, membership, grants, delegations and public projection.
- **Repository:** zenflows (migration additive), dpp (binding), gui/client for contract.
- **Dependencies:** Q1–Q5 decisions and inventory.
- **Task:** permission scheme separate from VF, invitation/grants management API, delegation constraints, epoch/versions, audit; dry-run backfill with confidence and provenance; queue records disputed.
- **Risks:** unreliable historical primaryAccountable, granting of permissions too broad, unintentional public default.
- **Test:** forward/backward migrations on synthetic copy; grant cycles, self-escalation, expired invitations, revoked membership.
- **Deliverable:** additive scheme, proposed ADRs approved by the team if agreed, dry-run report and dispute procedure.
- **Acceptance:** zero unjustified automatic assignments; all new objects have controller checked; distinguishable ambiguous records.
- **Rollback:** preserve new tables/audits; disable new features, do not delete control tests.

## Phase 3 · Enforcement Zenflows

- **Goal:** no ordinary writes without ExecutionContext/policy.
- **Repository:** zenflows; SDK for errors and compatible fields.
- **Dependencies:** phase 2; containment remains active.
- **Task:** principal in domain and internal entrypoints, secure CRUD and catalogs, createEconomicEvent/action and all effects, relationships and files, private/nested queries, import service-scoped; transactional audit and idempotence.
- **Risks:** protect CRUD but leave events; guest queries that expose subfields; legacy jobs with direct Repo.
- **Test:** permission matrix, GraphQL alias/multiple root fields, domain calls, signed requests with other agent providers, grant/update concurrency and VF invariant regression.
- **Deliverable:** enforcement for groups of operations, feature flags for scope; shadow telemetry only where it does not leave a vulnerable write open.
- **Acceptance:** each enabled inventory mutation has a deny/allow test; Alice/Bob not bypassable via events or public internal primitives.
- **Rollback:** for failed scopes read-only, not global auth-off; additive scheme remains compatible.

## Phase 4 · DPP and cross-service consistency

- **Objective:** consistent resource rights and passport actions.
- **Repository:** zenflows, dpp, feedback, proxy; then inbox/wallet/fabaccess.
- **Dependencies:** phases 2–3 and principal contract; Decision API available before consumers.
- **Task:** verified identity/assertion, parent binding, local PEP, allowlist fields, section/status policies, CAS, private projections and storage; S2S authentication; versions, idempotence, audit/outbox; agreed revocation protocol.
- **Risks:** outage authority; permit/drain incompleteness; Orphan DPPs; already public files impossible to "make secret" retroactively.
- **Tests:** direct/proxy/SDK, parent substitution, revoked grants, timeout, cross-user/cross-org, attachment replays, crash between Mongo and MinIO, cache and storage origin.
- **Deliverable:** End-to-end secure DPP, dependency runbook, migration mapping and reconciliation.
- **Acceptance:** each mutant DPP route or private read requires policy; impossible to bypass via generic PUT/status/attachments; deny on authority down; no private drafts published in list/file/cache.
- **Rollback:** previous version can only be used behind write block; rollback cannot open legacy API.

## Phase 5 · GUI and SDK

- **Goal:** Consistent UX without becoming primary enforcement.
- **Repository:** gui, client, SDK documentation.
- **Dependencies:** contracts of phases 2–4; can start in parallel on mock contracts.
- **Task:** `capabilities`/`can` scoped for UI, management of 401/403/409/503 and GraphQL error code, invitations/delegation/revocation, explicit acting_for; signing fail-closed on writes; file signature unification; dist/package provenance.
- **Risks:** hide allowed actions or show grant status; draft losses on deny; legacy storage.
- **Test:** unit/mock contract + API, two tabs with revocation, org switch, session expired, network error do not blindly retry.
- **Deliverable:** compatible release, migration note, permission source UI and read-only management.
- **Acceptance:** no browser admin credential; each deny backend made clearly; API continues to deny without GUI.
- **Rollback:** old GUI tolerated only if backend remains protected; Read-only UX fallback.

## Phase 6 · Prerequisites Medusa

- **Objective:** commercial identity and seller/collaborator separation before money.
- **Repository:** zenflows, gui/client, futuro adapter commerce.
- **Dependencies:** phases 2–5; legal seller decisions, single/multi-seller, stock authorities.
- **Task:** principal/customer/seller mapping, seller grants, order privacy, finance/payout roles, onboarding/step-up, offboarding, webhook/outbox/DPP issuance contracts; spike Medusa version and multi-vendor.
- **Risks:** confusing license with mandate; two stock masters; seller ID editable.
- **Test:** fixture two seller, former member, support without global access, permissions for each admin operation.
- **Deliverable:** updated contracts, threat commerce model, non-monetary proof-of-concept and ADR.
- **Acceptance:** contributor cannot sell in other people's scope; order/customer isolation verified; no real payment.
- **Rollback:** keep mock preview and feature flag off.

## Phase 7 · Marketplace

- **Objective:** integrate commerce backend without expanding collaborative privileges.
- **Repository:** future adapter/Medusa, gui/client, zenflows, dpp.
- **Dependencies:** phase 6 and pilot with limited dataset.
- **Tasks:** seller-scoped API, server-authoritative checkout, PSP verified, idempotency, stock reservations, fulfillment→VF/DPP, returns and reconciliation.
- **Risks:** double orders/charges, multi-seller leakage, incorrect DPP issues.
- **Tests:** PSP sandbox, duplicate/out-of-order webhooks, crash retry, same serial, SQL/API cross-seller, manipulated amounts.
- **Deliverable:** pilot commerce and runbook reconciliation/incident.
- **Accettazione:** audit dal pagamento al passport; no double effect; approval business/security before activation.
- **Rollback:** stop new checkouts, continue management of existing orders/refunds in controlled channel; do not delete ledger.

## Phase 8 · Hardening and rollout

- **Objective:** make the protected system sustainable.
- **Repositories:** all and infrastructure.
- **Dependencies:** enforcement and pilot; Basic hardening begins already in phase 0.
- **Task:** independent threat review, dependency scan, GraphQL/query complexity limits, load/chaos, key rotation drill, restore backup, audit retention, revocation dashboard; canary and break-glass runbooks.
- **Risks:** cache introduced for performance without freshness; permanent emergency bypass.
- **Test:** realistic load, authorities/DBs unavailable, permissions revoked in flight, restore with consistent permission epoch.
- **Deliverable:** SLO, monitoring, release security procedures and policies.
- **Acceptance:** no matrix regression, measured deadline/cancellation, documented and proven recovery.
- **Rollback:** canary per tenant/action and selective read-only, no global policy downgrade.

## Coordination and independent work

Independent: inventory, audit redaction, fixture/test matrix, adapter SDK on mock, public read projections, OSH sandbox, credential review. Coordinates: registration→GUI→rotation; schema permission→Zenflows enforcement; decision API→DPP/feedback; private file storage→URL/cache GUI; envelope v2→server/client verifiers; seller mapping→Medusa/worker.

Expand/contract order: add new contracts, deploy consumers, verify that old clients are no longer present, then retire the legacy path. Don't keep "legacy allow" undefined for critical writes.

## Ambiguous historical records

Classify each record: controller proven; candidate with evidence to verify; disputed; no evidence. Store creator/events/import/email/primaryAccountable/custodian as **distinct clues**, never interchangeable. For disputed/unknown objects: blocked administrative edits, reading according to approved policy, claim with evidence, two-person human verification for high impact transfers, notification and dispute period; reversible audit of the grant, not rewriting of economic history. No one can self-assign the first claimed record. Mixed `createdBy` organizations and DPPs also require provenance migration.
