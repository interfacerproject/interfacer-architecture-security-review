> **English edition.** [Italian version](../it/04-authorization-audit.md) · Technical terms and commit-pinned evidence are shared across both editions.

# 04 · Authorization audit

## Method and classification

**Confirmed** means provable ownership of the code at the indicated commits, not an exploit performed on production. **Potential** requires additional verification. **Architectural risk** describes a fragile trust boundary. **Design Limit** indicates a feature/policy not represented. **Open question** requires team decision. **Proposal** does not describe the current system.

Static inventory of all root fields imported into GraphQL schema, reading mutation resolvers and inspecting persistence functions; In-depth tracing of resources/events/person/org/DPP/feedback. An exhaustive dynamic verification of all input combinations is not claimed.

[Mutation matrix](appendix/mutation-matrix.md) · [Endpoint matrix](appendix/endpoint-matrix.md) · [Query matrix](appendix/query-matrix.md).

## F01 · Valid signature without object authorization — CONFIRMED, P0

**Component:** Zenflows. Sign produces `req_user`, but `update_economic_resource(..., _)` and `delete_economic_resource(..., _)` ignore it. The domain loads by ID and performs update/delete via Ecto without principal. The same pattern is observable on Organization and AgentRelationship; `updatePerson` is not self-only.

**Evidence:** [zenflows/src/zenflows/gql/mw/sign.ex:28–72](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/mw/sign.ex#L28-L72); [zenflows/src/zenflows/vf/economic_resource/resolv.ex:28–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/resolv.ex#L28-L64); [zenflows/src/zenflows/vf/economic_resource/domain.ex:246–332](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/domain.ex#L246-L332); [zenflows/src/zenflows/vf/organization/resolv.ex:25–51](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/organization/resolv.ex#L25-L51); [zenflows/src/zenflows/vf/organization/domain.ex:58–150](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/organization/domain.ex#L58-L150); [zenflows/src/zenflows/vf/agent_relationship/resolv.ex:36–51](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/agent_relationship/resolv.ex#L36-L51); [zenflows/src/zenflows/vf/person/resolv.ex:38–85](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person/resolv.ex#L38-L85).

**Conditions:** Reachable endpoint, valid signature of a Person if auth enabled, existing ID and input accepted by the changeset/DB. A deletion can be prevented by FK: it is not correct to promise the deletion of any record. The flaw is the absence of the decision per actor before persistence.

**Impact:** modification of others' content/relationships and management of organizations without delegation; Direct API not tied to UI choices. **Remedy:** Mandatory principal context and policy in the domain, and enforcement for referenced objects. **Uncertainty:** External infrastructure rules and live commits. No remote offensive tests performed.

## F02 · Economic invariants based on declared agents — CONFIRMED, P0

**Component:** EconomicEvent creation. The resolver passes input to the identityless domain. The domain compares `evt.provider_id` to `primary_accountable_id`/`custodian_id`; agents are inputs validated by existence and economic coherence, not by the signatory's right to represent them.

**Evidence:** [zenflows/src/zenflows/vf/economic_event/resolv.ex:38–49](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/resolv.ex#L38-L49); [zenflows/src/zenflows/vf/economic_event.ex:101–175](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event.ex#L101-L175); [zenflows/src/zenflows/vf/economic_event/domain.ex:124–285](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L124-L285); [zenflows/src/zenflows/vf/economic_event/domain.ex:782–909](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L782-L909).

**Conditions:** Valid signatory, references and quantities/units consistent with the action constraints. **Impact:** Accountability, custody, quantity, metadata, or lineage transitions may be requested without authorization from the signing party. **Remedy:** Authorize action, `acting_for` delegation, resource source, destination, process, and effects on content before transaction; maintain ValueFlows validations.

**Important clarification:** `updateEconomicResource` only exposes id/name/note/images/classifiedAs/repo, not primaryAccountable or custodian. The change of economic fields passes through events or broader internal functions. `updateEconomicEvent` does not allow you to rewrite provider/action, but only a descriptive subset. [zenflows/src/zenflows/vf/economic_resource/type.ex:224–353](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/type.ex#L224-L353); [zenflows/src/zenflows/vf/economic_event.ex:294–308](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event.ex#L294-L308). **Uncertainty:** outcomes of each specific transition not dynamically tested.

## F03 · Enforcement DPP incomplete — CONFIRMED, P0

**Component:** DPP Gin. The router enforces logging/recovery and CORS, not general auth. Update, delete, status and delete attachment do not call VerifyDid/IsAuth. Create and upload/add attachment do this, but they do not decide the right to the product/passport.

**Evidence:** [interfacer-dpp/cmd/main/main.go:30–54](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/cmd/main/main.go#L30-L54); [interfacer-dpp/internal/handler/handler.go:154–224](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L154-L224); [interfacer-dpp/internal/handler/handler.go:480–551](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L480-L551); [interfacer-dpp/internal/handler/handler.go:676–753](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L676-L753); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116); [interfacer-dpp/internal/handler/handler.go:553–674](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L553-L674).

**Conditions:** access to the service route or the proxy that forwards it; DB/storage working; Valid ID and input. For `PUT /dpp/:id`, the `$set` of the entire struct includes `_id`: MongoDB can reject an ID change. The lack of auth is certain, but a generic body does not guarantee a successful update. The other writes are distinct paths and do not depend on this problem.

**Impact:** DPP integrity and publishing workflow not subject to Zenflows rights; protecting Zenflows alone does not solve the bypass. **Remedy:** Temporary gate on all writes, then auth+policy in each handler/domain function, allowlist of fields, DPP constraint→authoritative resource. **Uncertainty:** Live exposure, external gateway configuration, and real documents.

## F04 · Principal declared separately from signature — CONFIRMED, P0

**Component:** feedback; DPP for author attribution. In the feedback service, the body is verified with `did-pk`, but `user_ulid` is copied from `x-user-id` without resolving the link between the two. SQL filters correctly for user ULID: it is the value of that principal that is not authenticated. In DPP Create `CreatedBy` prefers the same header; fallback is a public key, so the field also has two different semantics.

**Evidence:** [interfacer-feedback-service/internal/auth/middleware.go:15–88](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/auth/middleware.go#L15-L88); [interfacer-feedback-service/internal/database/comment_repo.go:88–105](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/database/comment_repo.go#L88-L105); [interfacer-feedback-service/internal/database/review_repo.go:115–129](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/database/review_repo.go#L115-L129); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Conditions:** own signature accepted and DID resolvable; known target identifier; no external layer that replaces and certifies the header. **Impact:** False attribution and ownership feedback checks based on unproven identity. **Remedy:** derive principal from registered key or verified assertion; ignore arbitrary headers; migrate `createdBy` with provenance. **Uncertainty:** Actually available DID mapping and federation policy.

## F05 · Public, draft and confidential information not separated — CONFIRMED as behavior; P1

**Component:** DPP, Zenflows, files and GUI cache. GetDPP/GetAllDPPs do not require auth or enforce active status. The `createdBy`/`status` filters are optional client filters, not policy filters. The economicResource/economicResources queries are guest; `primaryAccountable` can resolve a Person whose type includes email. Global middleware is applied to root fields, not automatically to nested fields.

**Evidence:** [interfacer-dpp/internal/handler/handler.go:117–153](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L117-L153); [interfacer-dpp/internal/handler/handler.go:226–329](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L226-L329); [zenflows/src/zenflows/vf/economic_resource/type.ex:224–353](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/type.ex#L224-L353); [zenflows/src/zenflows/gql/schema.ex:130–193](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/schema.ex#L130-L193); [zenflows/src/zenflows/vf/person/type.ex:179–270](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person/type.ex#L179-L270); [interfacer-gui/pages/api/dpp-file/[id]/[filename].ts:1–35](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/pages/api/dpp-file/[id]/[filename].ts#L1-L35). The Person.email field is in `person/type.ex:77–78` (see [data model](appendix/data-model.md)).

**Conditions:** data present and reachable routes. **Impact:** Lacks a guarantee of confidentiality of drafts, sections and attachments. Not every public reading is a vulnerability: it depends on the expected classification. **Remedy:** Explicit public projection, policies even in nested resolvers, server filters for lists/facets, private buckets and consistent caches. **Uncertainty:** truly sensitive content and consent to publication.

## F06 · Replay and confusion between signature contexts — limit CONFIRMED, P1

**Component:** GraphQL and DID signature. The contract verifies normalized content; no nonce, deadline, method, path or audience. In the addAttachment DPP, the checksum is signed, not the recipient or section. The proxy also retries write requests after transport errors.

**Evidence:** [zenflows-crypto/src/verify_graphql.zen:17–44](https://github.com/interfacerproject/zenflows-crypto/blob/0ffcce9b90799c9cb61f11fc594aeb513a01326f/src/verify_graphql.zen#L17-L44); [interfacer-client/src/crypto/sign.ts:36–137](https://github.com/interfacerproject/interfacer-client/blob/dfb1baabf16516a845957d5587ccb933c1874221/src/crypto/sign.ts#L36-L137); [interfacer-dpp/internal/handler/handler.go:553–674](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L553-L674); [interfacer-proxy/main.go:160–241](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L160-L241).

**Conditions:** Availability of an already valid request/signature or network error after backend commit. No traffic interception was observed. **Impact:** replay, duplication, or reuse in compatible contexts; real effects depend on constraints and idempotence of the operation. **Remedy:** versioned envelope, request ID, transactional deduplication, no indiscriminate retry; deadline. **Uncertainty:** behavior deployed Zenroom and external protections.

## F07 · Wallet: authenticating does not mean being able to issue — CONFIRMED, P1/P0 according to use

**Component:** zenflows-wallet. After DID/signature, `addTokensHandler` passes owner/token/amount to `AddDiff` without issuer role or owner→signer binding. It's not necessarily about money: the SDK/GUI uses idea/strengths points. Bank has an airdrop command from imported data: it is not assumed to be in use or automatically connected.

**Evidence:** [zenflows-wallet/wallet.go:83–136](https://github.com/interfacerproject/zenflows-wallet/blob/f5cf1668afe371329ed827d0bb56557e0bedcda6/wallet.go#L83-L136); [zenflows-wallet/did-auth.go:43–78](https://github.com/interfacerproject/zenflows-wallet/blob/f5cf1668afe371329ed827d0bb56557e0bedcda6/did-auth.go#L43-L78); [interfacer-gui/hooks/useProjectCRUD.ts:67–119](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/hooks/useProjectCRUD.ts#L67-L119); [zenflows-bank/cmd/airdrop.go:31–125](https://github.com/interfacerproject/zenflows-bank/blob/e5c2d2e6bd1ad072d1575de0a2be983854429b35/cmd/airdrop.go#L31-L125).

**Conditions:** DID accepted, numeric input, and database available. **Impact:** Unauthorized issuing of points if the intent is to reward real events. **Remedy:** issuer service-scoped, validated business event, idempotency and ledger; prohibit commercial conversions until the decision. **Uncertainty:** Intentional policy and current point value.

## F08 · Social inbox and external calls — CONFIRMED/POTENTIAL, P1

**Component:** zenflows-inbox. Messaging send/read/set/delete binds the signature to the sender/receiver key; storage set/delete include receiver in the key. It is a positive control to keep. Inbox/outbox social handlers instead persist activity without that audit trail and can POST to URLs derived from actor/object.

**Evidence:** [zenflows-inbox/inbox.go:80–243](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L80-L243); [zenflows-inbox/storage.go:59–120](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/storage.go#L59-L120); [zenflows-inbox/inbox.go:427–588](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L427-L588); [zenflows-inbox/inbox.go:697–725](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L697-L725).

**Conditions:** reachable social route and valid input. **Confirmed Impact:** Activities not cryptographically attributed in the same way as messages; **potential:** SSRF/egress to prohibited networks, to be validated in sandbox only. **Remedy:** federated identity/provenance, activity policy, protocol/egress allowlist, HTTP signatures verification where adopted. **Uncertainty:** Trusted deployment gateways and peers.

## F09 · Internal execution and import skip API — risk CONFIRMED in design, P1

**Component:** Zenflows domain and SWPass. Domain APIs accept id/params/repo, not an authorization context. The import creates agents/events/resources directly and uses a first person from emails as a stand-in for the organization.

**Evidence:** [zenflows/src/zenflows/vf/economic_resource/domain.ex:246–332](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/domain.ex#L246-L332); [zenflows/src/zenflows/vf/process/domain.ex:102–162](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/process/domain.ex#L102-L162); [zenflows/src/zenflows/sw_pass/domain.ex:108–197](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/sw_pass/domain.ex#L108-L197).

**Conditions:** Privileged internal/job/import code running; it is not in itself an anonymous entrance. **Impact:** Patching only in resolvers leaves internal routes and historical data without reliable administration. **Remedy:** application service with mandatory principal, private and separate raw primitives; import with limited service identity and provenance. **Uncertainty:** real use of the import and quality of the records already created.

## F10 · Machine permissions and analysis jobs — architectural risk, P1

Fabaccess checks DID/signature/timestamp then uses a configured account to a machine chosen from the input; There is no Interfacer ACL per machine. OSH runs Git clone and analytics without auth on the router. It is not stated that Fabaccess has no account limits of its own nor that OSH arbitrarily runs a shell: `exec.Command` uses separate arguments.

**Evidence:** [zenflows-fabaccess/main.py:55–123](https://github.com/interfacerproject/zenflows-fabaccess/blob/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc/main.py#L55-L123); [zenflows-osh/web.go:45–83](https://github.com/interfacerproject/zenflows-osh/blob/56855d426ffd884d91dd72373a2292f1ae5695ed/web.go#L45-L83); [zenflows-osh/analyze.go:28–58](https://github.com/interfacerproject/zenflows-osh/blob/56855d426ffd884d91dd72373a2292f1ae5695ed/analyze.go#L28-L58). **Conditions:** Services enabled and dependencies available. **Impact:** physical rights/service credentials and egress not modeled in future policy. **Remedy:** Machine scope, training/enabling if required, nonce over timestamp, sandbox/quotes/egress for OSH. **Uncertainty:** pyfabapi API and Fabaccess server policies not fully analyzed.

## F11 · Inverted email expiration predicate — CONFIRMED, P1

**Component:** `Zenflows.Email.Domain.token_validate`. The token includes timestamp, HMAC and person ID; the code compares the issuing timestamp to `now + expiry`, rather than comparing `now` to `issued_at + expiry`.

**Evidence:** [zenflows/src/zenflows/email/domain.ex:76–101](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/email/domain.ex#L76-L101).

**Conditions:** authentic token of the requesting person, still valid against the HMAC key; the temporal flaw does not allow you to forge tokens or impersonate another person. **Impact:** Tokens issued in the past do not expire according to the lifetime configured in this predicate. **Secure verification:** only the DateTime expression with synthetic clock and timestamp is reproduced via Elixir, without application, keys, database or email sending: issuing ten days before and lasting four days are accepted by the current predicate, denied by the expected one. It is not an end-to-end test of the token.

**Remedy:** check `issued_at <= now < issued_at + expiry`, with explicit skew if necessary; edge testing and future/expired tokens; evaluate revocation/one-time use according to requirements. **Uncertainty:** commit and deploy configuration, possible external controls. Keep HMAC and binding self properly present.

## F12 · HTTP upstream status not propagated — CONFIRMED, P2

**Component:** interfacer-proxy `proxyRequest`. When `client.Do` returns a response without transport error, the proxy copies the header and body but does not execute `WriteHeader(res.StatusCode)`. In Go the first body write normally uses 200 if no status has been set.

**Evidence:** [interfacer-proxy/main.go:211–230](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L211-L230).

**Conditions:** Upstream response successfully received with status not 200. **Impact:** A 401/403 reject or conflict may appear to the SDK as HTTP success; this does not authorize write denied by the backend, but compromises error handling/UX and observability. **Remedy:** Propagate status and test 201/204/400/401/403/409/500 with simulated local HTTP upstream, distinguishing transport and application errors. **Uncertainty:** No Go runtime tests performed; further input can change the final behavior.

## Controls that exist and should not be removed

EdDSA signature; key lookup Person in Zenflows/inbox; admin comparison; ID/schema/changeset validation; FK; self-bound email verification; event invariants; DPP transitions; DPP upload limit 10 MiB; ownership SQL feedback (to be fed with correct principal). They are not a substitute for a comprehensive policy, but they are a useful foundation.

## Restricted findings

A separate review covers administrative frontend surfaces, credential configuration, and same-origin file-serving. The report is excluded from `docs/`, search index, and artifact pages. Before publishing this summary, request approval from the maintainers: the links to the source are not a coordinated disclosure procedure.
