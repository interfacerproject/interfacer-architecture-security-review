> **English edition.** [Italian version](../it/13-testing-strategy.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 13 · Testing strategy

## Results actually executed

In the SDK checkout: `./node_modules/.bin/vitest run src/__tests__/unit.test.ts` → **31/31 pass**, Vitest 2.1.9. These are storage/tagging/types tests, not backend enforcement tests. Only the single file after reading was selected; the generic command that includes `real-backend.test.ts` was not executed.

An Elixir verification of the temporal expression of `Email.Domain.token_validate` with synthetic timestamps was also performed: the discrepancy described in [F11](04-authorization-audit.md) was confirmed. A real token has not been generated or verified.

The current test feedback contracts use stubs and routers without auth middleware: [internal/handler/test_helper_test.go:10–32](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/handler/test_helper_test.go#L10-L32). Even if passed, they would not prove the correctness of identity binding.

No Zenflows tests with database/Restroom, DPP tests with Mongo/MinIO/DID, or browser tests connected to shared services. Go not available in session PATH; You have not installed/run a live server environment. ExUnit uses SQL Sandbox but the runtime configuration can point to non-isolated DBs: this is not a sufficient guarantee without dedicated setup.

Site build, link, Mermaid and inventory checker results: [validation report](appendix/validation.md). The following tests are **specifications to be implemented**, not already achieved successes.

## Proposed insulated harness

Composed of separate tests with PostgreSQL, MongoDB, private MinIO, temporary SQLite, fake DID/Restroom and controlled clock; network without access to production. Keys generated exclusively for fixtures. Separate crypto contract tests with real Zenroom and synthetic vectors. At startup reject URL not loopback/allowlist test, DB name not test, shared credentials; deny external egress. Explicit seeding, before/after snapshots, teardown confined to test volumes.

## Minimum Alice/Bob matrix

Each line checks response **and absence/presence of effects** on DB, file, quantity, binding and audit. Deny HTTP can be 403/404 according to policy; GraphQL can use HTTP 200 with error code and no side effects.

| ID | Scenario | Expected |
|---|---|---|
| T01 | Alice creates personal R with valid signature | Allow; Alice controller, Alice audit actor, consistent economic primaryAccountable |
| T02 | Bob and Anonymous read public screening R | Allow; no email/draft/private in relationships |
| T03 | Bob modifies Alice's R via direct GraphQL | Deny; no change |
| T04 | Bob eliminates R | Deny for policy, not just a mistake FK |
| T05 | Alice invites Bob as editor; Bob accepts | Allow after acceptance; pending invitation is not enough |
| T06 | Bob edit name/notes allowed | Allow; actor Bob, grant provenance |
| T07 | Bob tries delete/transfer/grant/sell/publish not granted | Deny for every action, including extra fields |
| T08 | Alice revokes grant Bob | Allow, increased epoch, audit; revocation prohibited by Bob without delegation |
| T09 | Bob repeats edit after revocation and with old tabs/tokens | Deny for new decisions; separate test for in-flight operations |
| T10 | Bob uses DPP update/status/delete/attachment after revocation | Deny on all routes and parent binding |
| T11 | Bob skips SDK/proxy and calls backend or domain directly | Deny; ExecutionContext required; Raw repo not application input |
| T12 | Bob declares Alice's acting_for org or provider org | Deny; ID and signature do not prove membership |
| T13 | Seller Bob accesses listing/order/stock/payout seller Alice | Deny; query, count and export scoped |
| T14 | Service without scope or compromise declares Alice | Deny without proof/delegation; no global grants or arbitrary writing |

## Policy unit tests

Roles × actions × scope × account/membership status × attributes. Example tables shared between Elixir/Go/TS, not three divergent implementations of the same policy. Tests for precedence deny, multiple grants, inheritance disabled, expiration, non-transitive delegation, reused invitations, last org admin, and controller transfer with non-consenting recipient. Property tests: adding a business reference does not create a grant; editor cannot expand its rights.

## Zenflows domain integration test

- `createEconomicEvent` signed Bob with provider/receiver Alice: deny, even though ValueFlows invariants would be valid.
- For transfer/custody/rights/move: permissions on origin and destination; containers and contained resources; atomic rollback of quantity/state effects.
- `accept`/`modify`, cite/use and metadata: must not become indirect paths for unauthorized editing.
- Organization/AgentRelationship/role behavior: do not auto-assign admin. Protect unit/spec/global catalog from normal member if policy requires curator.
- Nested resolver, `traceDpp`, images, pagination/count: no reading policy bypass or indirect disclosure.
- Multiple root mutation and alias: for each decision, no incorrect reuse of context/allow of another field; explicit partial success management.
- Import/job: mandatory service principal and scope, ambiguous records quarantined; audit actor other than provider.

## DPP and storage

Check created on product of another scope, `x-user-id` differs from the key, parent substitution in the PUT, unmodifiable system fields, section not allowlisted, bypass transition via generic update, draft not returned to guest, existing/non-existing ID indistinguishable where necessary. Mongo `$set` must not attempt to mutate `_id`.

Repair operator can hang a repair on the delegated instance only; does not change specifications, old events or producer author. Certifier does not modify proprietary data. Test upload size/MIME/checksum, raw vs base64 checksum signature, target ID/section included in v2 signature, orphan cleanup, delete replay, bucket origin and GUI route without private policy bypass. Public cache excluded for private documents; active content never same privileged origin.

## Cross-service and fault injection

- Same resource↔DPP decision for equivalent edit, without copying ACL freely.
- Authority down/timeout/malformed response→deny; no legacy fallbacks.
- Revocation after allow and before CAS: test the declared window and the drain protocol for critical operations; the test cannot claim non-existent atomicity.
- Decision token audience/action/digest/epoch wrong→deny; request ID duplicate→same outcome, not double effect.
- Service credential expired/rotated, duplicate/out-of-order event, pre-response post-commit crash and retry proxy.
- Feedback: own signature cannot replace user header; SQL ownership denied even with valid ID.
- Inbox: receiver Bob cannot read/set/delete Alice messages; social requires separate policy.
- Wallet: only issuers can assign prizes; same event does not emit twice.

## Medusa: mandatory future testing

Two common sellers and one common customer; listing ID of seller A in route seller B, inventory location of A in payload B, unauthorized search/export order, former employee with session still valid, refund beyond threshold, payout edit without step-up. PSP sandbox, signed/invalid/duplicate webhooks, total browser manipulation, fulfillment→DPP only once per unit, refund does not eliminate provenance.

## Regression and release criterion

Run unit policy at each PR; integration and schema coverage before merge; cross-service and failure/revocation in staging **isolated** before deployment; canary and deny/conflict monitoring. Each write endpoint in the array must have at least one positive, one negative cross-owner, and one non-authentication proof, in addition to indirect actions. Frontend tests only after API/domain tests. Do not mark "safe" a test that fails due to DB down, invalid payload or FK: distinguish authorization denial from technical failure.
