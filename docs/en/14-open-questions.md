> **English edition.** [Italian version](../it/14-open-questions.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 14 · Open questions and team decisions

Any recommendation is provisional. Questions do not block delivery; guide the phases and ADRs.

## Q01 · Centralize decisions or just data?

**Why it matters / evidence:** F01/F03: Resources and DPPs have inconsistent PEPs; [zenflows/src/zenflows/vf/economic_resource/resolv.ex:28–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/resolv.ex#L28-L64); [interfacer-dpp/cmd/main/main.go:30–54](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/cmd/main/main.go#L30-L54).

**Possible answers, advantages and disadvantages:** Local policy in each service: autonomy and low latency, but divergence/revocation difficult. Everything central: coherence, but coupling and single failure domain. Hybrid: common consistency with local workflow, but more rigorous contract.

**Interim Recommendation and Consequences:** Zenflows module for common rights, more restrictive local DPP rules. Consequence: online call in DPP writes and failure closed.

**Information still needed:** Volumes, allowed latency, required availability and team operational capacity.

## Q02 · Permission store in Zenflows or dedicated service?

**Why it matters / evidence:** The resource authority is PostgreSQL; DPP has no resource lookup: [zenflows/src/zenflows/vf/economic_resource/domain.ex:246–332](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/domain.ex#L246-L332); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Possible answers, advantages and disadvantages:** Zenflows: Transactions with resources and less deployment, but greater service responsibility. Dedicated service: separation/independent evolution, but sync and consistency of another DB.

**Interim Recommendation and Consequences:** Keep in Zenflows at first with stable internal API, extractable if needed. Don't start with a new mandatory container.

**Information still needed:** Federation roadmap, module owner, and HA requirements.

## Q03 · What inheritance Organization→Project→Resource?

**Why it matters / evidence:** AgentRelationship does not implement administrative scope: [zenflows/src/zenflows/vf/agent_relationship.ex:34–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/agent_relationship.ex#L34-L64).

**Possible answers, advantages and disadvantages:** No inheritance: simple local revocation but many grants. Explicit single-parent inheritance: Useful UX, blast radius risk. Multiparent graph: flexible, difficult to explain deny and revoke.

**Interim recommendation and consequences:** An administrative parent, opt-in and grant of traced origin; do not inherit from citations or containedIn. Commercial permissions are excluded.

**Information still needed:** Are there personal resources in company projects? Are exceptions or multi-org consortia needed?

## Q04 · Does the creator have to become a controller?

**Why it matters / evidence:** Production assigns accountability to receiver input, import uses email first: [zenflows/src/zenflows/vf/economic_event/domain.ex:124–285](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L124-L285); [zenflows/src/zenflows/sw_pass/domain.ex:108–197](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/sw_pass/domain.ex#L108-L197).

**Possible answers, advantages and disadvantages:** Always creator: simple but takes control away from the organization. Always primaryAccountable: compatible with UI but unreliable economic data. Creator self or delegating org: more explicit, requires acting_for.

**Temporary recommendation and consequences:** New records self→creator verified; per-org→org with delegation. For historical records, never assign control automatically without evidence.

**Information still needed:** Legal/operational definition of ownership and quality of imported records.

## Q05 · How to delegate and invite people?

**Why it matters / evidence:** Contributor GUI is event/notification, not acceptance: [interfacer-gui/hooks/useProjectCRUD.ts:67–119](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/hooks/useProjectCRUD.ts#L67-L119).

**Possible answers, advantages and disadvantages:** Immediate grant: rapid, non-consensual attribution. Invitation accepted: consent and binding, multiple states. Group/org roles: less administration, but broader rights.

**Temporary recommendation and consequences:** Scoped invitation with expiry and authenticated acceptance; non-transitive delegation by default. Never grant more than can be delegated.

**Information still needed:** Can you invite external people without an account? What roles can they delegate?

## Q06 · Does the DPP need to consult Zenflows or duplicate ACLs?

**Why it matters/highlight:** DPP only has string productId and mixed createdBy: [interfacer-dpp/internal/model/model.go:25–51](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/model/model.go#L25-L51); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Possible answers, advantages and disadvantages:** Online checks: rapid revocation and single authority, runtime dependency. Replicated ACLs: autonomy, stale policy and sync. Short Capability: Fewer calls, revocation window and token management.

**Interim recommendation and consequences:** Online decisions for write, stable parent binding; do not replicate free membership. Evaluate cache only after measurements.

**Information still needed:** Offline DPP availability and maximum revocation tolerance.

## Q07 · Resource independent DPP permissions?

**Why it matters / evidence:** repairs are represented as a single section and there are no section ACLs: [interfacer-dpp/internal/model/model.go:127–147](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/model/model.go#L127-L147).

**Possible answers, advantages and disadvantages:** Identical to the resource editor: easy, too many rights. Independent: flexible but bypass. Derived by action and section: least privilege, more API commands.

**Temporary recommendation and consequences:** Scoped basic right on the same resource + DPP role/section; repair append separate from spec edit. Generic PUT restricted.

**Information still needed:** Who certifies, who repairs and which data must be immutable by law?

## Q08 · How to authenticate and limit service accounts?

**Why it matters / evidence:** Fabaccess shared account and keyring DID: [zenflows-fabaccess/main.py:55–123](https://github.com/interfacerproject/zenflows-fabaccess/blob/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc/main.py#L55-L123); [zenflows/src/zenflows/did.ex:63–112](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/did.ex#L63-L112).

**Possible answers, advantages and disadvantages:** Global single key: simple but large blast radius. TLS distinct credentials: manageable, rotation to implement. mTLS/workload identity: strong binding, more infrastructure.

**Temporary recommendation and consequences:** Identity distinct by service/environment, purposes and audience, actor/service separation; TLS and rolling credentials at a minimum.

**Information still needed:** Secret manager/PKI available, scheduler/container platform, rotation managers.

## Q09 · Are collaborator and seller separate roles?

**Why it matters / evidence:** The preview uses seller mocks with no ID or backend: [interfacer-gui/lib/previewCommerce/mockData.ts:17–183](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/lib/previewCommerce/mockData.ts#L17-L183).

**Possible answers, advantages and disadvantages:** Unify owner/editor/seller: simple UX but improper commercial mandate. Separate: Longer onboarding but isolated financial data. Independent seller on public design: favors ecosystem, requires license/compliance.

**Interim recommendation and consequences:** Separate commercial grants; edit does not give sell. Consent from the design owner is not automatically required for every use of the license.

**Information still needed:** Marketplace policy, supported licenses, manufacturer/reseller legal responsibility.

## Q10 · Does Seller have to be Organization and what happens to offboarding?

**Why it matters / evidence:** Organization is an economic agent; seller still string mock: [zenflows/src/zenflows/vf/organization/resolv.ex:25–51](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/organization/resolv.ex#L25-L51); [interfacer-gui/lib/previewCommerce/mockData.ts:207–365](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/lib/previewCommerce/mockData.ts#L207-L365).

**Possible answers, advantages and disadvantages:** Org only: clear governance, excludes individuals. Person or org with legal profile: inclusive, more checks. Separate seller account: flexible, additional mapping.

**Temporary recommendation and consequences:** Separate seller entity linked to legal subject person/org; membership manages access. Member exit revokes delegations, does not rewrite orders/seller history.

**Information still needed:** Countries, KYC/payout providers, individual sellers and account transferability.

## Q11 · What guarantee between allow, revoke and remote commit?

**Why it matters / evidence:** Zenflows and DPP have separate DBs; DPP status read-then-write: [interfacer-dpp/internal/handler/handler.go:480–551](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L480-L551).

**Possible answers, advantages and disadvantages:** Check once: cheap, allows writing in flight. Local epoch/CAS: protects versions but does not atomize authorities. Permit and drain/coordinator: stronger completed revocation, complexity and crash handling.

**Temporary recommendation and consequences:** Document bounded in-flight semantics for ordinary edit, online no cache; critical actions only after serialization/drain protocol tried.

**Information still needed:** Is a few seconds acceptable? When can UI say revocation completed? Regulatory/Commercial Requirements.

## Q12 · What to do if Zenflows/authz is not responding?

**Why it matters / evidence:** DPP today does not depend on a resource decision; introducing it changes availability: [interfacer-dpp/internal/auth/auth.go:98–151](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/auth/auth.go#L98-L151).

**Possible answers, advantages and disadvantages:** Fail-open: high availability but bypass right at the fault. Fail-closed: Secure, writes blocked. Public snapshot/limited capacity: selective continuity, complexity freshness.

**Temporary recommendation and consequences:** Fail-closed for write/private read, snapshot public only; idempotent retry and explicit SLOs.

**Information still needed:** Downtime budget and priority between offline repair, publishing and checkout.

## Q13 · How do public and private coexist?

**Why it matters / evidence:** Guest resource and DPP draft readable without policy: [zenflows/src/zenflows/vf/economic_resource/type.ex:224–353](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/type.ex#L224-L353); [interfacer-dpp/internal/handler/handler.go:226–329](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L226-L329).

**Possible answers, advantages and disadvantages:** All public: simple, PII/commercial incompatible. All authenticated: more secure, limits open data. Projections and sections: balanced, requires schema/cache maintenance.

**Temporary recommendation and consequences:** Released public projection and separate internal model; apply policy also to nested/count/file/cache.

**Information still needed:** Which data already published should remain published? Consent, retention and DPP requirements.

## Q14 · Who can transfer administrative control?

**Why it matters / evidence:** transferAllRights is economic transition, not consensus admin: [zenflows/src/zenflows/vf/economic_event/domain.ex:782–909](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L782-L909).

**Possible answers, advantages and disadvantages:** Automatically follow VF: simple, equivocal and escalation. Unilateral separate command: clear but risk of errors. Proposal/acceptance and step-up: secure, more workflow.

**Interim recommendation and consequences:** Separate command with target acceptance, policy grants after transfer and audit; double approval for contentious/high impact.

**Information still needed:** Support powers, disputes, last administrator and unregistered subjects.

## Q15 · How to migrate records without certain controller?

**Why it matters / evidence:** Import uses email as surrogates and DPP createdBy can be header: [zenflows/src/zenflows/sw_pass/domain.ex:108–197](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/sw_pass/domain.ex#L108-L197); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Possible answers, advantages and disadvantages:** Backfill primaryAccountable: fast, risks illegitimate assignments. Claim first-come: economical, favors appropriation. Review with evidence: expensive, keep trust.

**Temporary recommendation and consequences:** Confidence and disputed classes, read-only for risky edits, claims process reviewed and tracked; no automatic equivalence between custody/creation/contribution.

**Information still needed:** Dataset size, available evidence, people responsible for reviewing.

## Q16 · What value and authority do wallets and points have?

**Why it matters / evidence:** Wallet AddDiff is accessible after DID/signature; bank has airdrop: [zenflows-wallet/wallet.go:83–136](https://github.com/interfacerproject/zenflows-wallet/blob/f5cf1668afe371329ed827d0bb56557e0bedcda6/wallet.go#L83-L136); [zenflows-bank/cmd/airdrop.go:31–125](https://github.com/interfacerproject/zenflows-bank/blob/e5c2d2e6bd1ad072d1575de0a2be983854429b35/cmd/airdrop.go#L31-L125).

**Possible answers, advantages and disadvantages:** Self-reported points: simple, no financial confidence. Rewards issued servers: more credible, require events/idempotence. Commercial ledger: further compliance and control.

**Interim recommendation and consequences:** Do not link points to valuable payments/rewards prior to issuer policy and audit; decide whether to maintain their reputation.

**Information still needed:** Real bank/airdrop use, value attributed to points, management of adjustments.

## Q17 · How to manage federated identities and revoked DIDs?

**Why it matters / evidence:** DPP/wallets test HTTP 200; inbox uses Person lookup: [interfacer-dpp/internal/auth/auth.go:98–151](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/auth/auth.go#L98-L151); [zenflows-inbox/zenflows-auth.go:11–36](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/zenflows-auth.go#L11-L36).

**Possible answers, advantages and disadvantages:** Local Persons only: simple, reduces federation. Universal DID: open, poorly defined trust/issuer/revocation. Federation allowlist with mapping: auditable, governance required.

**Temporary recommendation and consequences:** Local or federated principal explicitly admitted; resolve bindings and key state, don't trust HTTP explorer alone.

**Information still needed:** Controller authoritative, deactivation semantics, trusted issuer and cross-instance users.

## Q18 · Is Medusa or Zenflows the authority of quantities?

**Why it matters / evidence:** VF changes quantity with events; preview stock is static: [zenflows/src/zenflows/vf/economic_event/domain.ex:124–285](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L124-L285); [interfacer-gui/lib/previewCommerce/mockData.ts:207–365](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/lib/previewCommerce/mockData.ts#L207-L365).

**Possible answers, advantages and disadvantages:** Zenflows master: an economical ledger, complex reservations integration. Medusa stock master: natural commerce, possible VF projection. Two masters: autonomy but conflicts/double decrease.

**Interim recommendation and consequences:** Medusa initial commercial master stock; VF idempotent projection and distinct from other quantities. Validate for fablab and production.

**Information still needed:** Non-commercial production/inventory, serialized units, and fulfillment requirements.
