> **English edition.** [Italian version](../it/01-executive-summary.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 01 · Executive summary

## Conclusion

The premise is **confirmed for concrete paths**, but it should be clarified: Zenflows is not without controls. Verifies signatures, distinguishes some administrative operations and validates ValueFlows invariants. The systematic connection between **authenticated person, requested action and involved objects** is missing. Furthermore, DPP and feedback do not share a reliable notion of principal and permission.

This is a model and enforcement problem, not solvable by hiding buttons in the GUI or just adding a control to `updateEconomicResource`.

## Five priority results

| ID | Result confirmed | Consequence | Technical priority |
|---|---|---|---|
| F01 | `req_user` created by middleware not used in CRUD resource, organization and other resolvers | Valid signature of another person does not prevent changes to ID, if given constraints are met P0 |
| F02 | Events control stated provider/custody/liability, without tying them to the signatory | Indirect mutations can bypass future CRUD-only protection | P0 |
| F03 | DPP router without general auth middleware; multiple write handlers without auth | Integrity and publication of the passport are not subject to Zenflows | rights P0 |
| F04 | Feedback verifies the key but takes the principal from `x-user-id` | An ownership SQL check may be correct but based on unauthenticated identity | P0 |
| F05 | DPP GET/list do not filter by policy; guest resources expose nested relationships | Draft does not mean private; new confidential information cannot be added safely | P1 |

[Details, evidence, conditions and uncertainty for each survey](04-authorization-audit.md). P0 indicates triage urgency, **not a CVSS score or evidence of live exploitation**. Network exposure, configuration and real data have not been verified against production.

## Recommended first milestone: Minimum verifiable boundary

Indicative timebox: **1–2 sprints**, to be estimated with maintainers. Two backend developers plus frontend/DevOps support and security review, not a timetable promise.

- Private triage of credentials/configurations and administrative surfaces.
- Temporarily close unprotected DPP writes until server-side enforcement exists, even on the direct source.
- Define verified principal and first policy `resource.update`, with Alice/Bob fixture; inventory **even events and internal writes** before declaring a resource protected.
- Resolve key→person bindings in feedback; do not trust identity headers provided by the client.
- Approve a conservative rule for records without a certain administrator: manual review, not automatic assignment.

**Acceptance:** No known DPP write path remains open without a verifiable gate; a negative API test and a negative domain test for Alice/Bob are reproducible in an isolated environment; versioned inventory and assigned technical owner. This milestone is containment, not completion of the permission system.

## What to keep

Preserve ValueFlows, PostgreSQL/Ecto, existing signatures during migration, APIs and GUIs where possible. Add an explicit execution context and a policy module, don't rewrite all the services. The economic model remains distinct from administrative control.

## What not to decide implicitly

`primaryAccountable` is not an ACL, `custodian` is not an administrator, a contribution is not a delegation, a resolvable DID is not a permission, an open hardware resource is not automatically sellable by every editor. [Decision Questions](14-open-questions.md).

## Essential limits

Static review and safe local unit testing; no mutation testing on remote systems. Medusa is not a backend implemented in the analyzed repositories. We do not certify the security of cryptographic dependencies, controller DIDs, or external federated services. The GUI depends on SDK 0.6.1 installed, while the SDK checkout declares 0.1.0: the conceptual path is verified, binary equivalence must be certified in release.
