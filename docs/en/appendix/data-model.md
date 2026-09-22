> **English edition.** [Italian version](../../it/appendix/data-model.md) · Technical terms and commit-pinned evidence are shared across both editions.

# Data model · current and proposed

## Current: evidence

| Concept | Structure observed | Do not infer |
|---|---|---|
| Person | `vf_agent`, type per, name/user/email, public keys, is_verified | Server, membership or seller session |
| Organization | Economic agent managed by the relevant domain | Tenant with implicit ACL |
| AgentRelationship | `vf_agent_relationship`, subject/object/relationship, note | Invitation accepted, administrative role protected |
| EconomicResource | `vf_economic_resource`, primary_accountable/custodian, quantity, conforms_to, lot/contained_in, metadata | Administrative Controller or Verified Creator |
| EconomicEvent | Action/provider/receiver/process/resources/quantity; effects in the domain | Log authenticated human actor |
| Process | Input/output activities with nesting/grouping | An already implemented permission project scope |
| Proposal/ProposedIntent | Proposal and link with Intent | Medusa product, seller send or checkout |
| DPP | Mongo struct with productId/batchType/batchId/createdBy/status and sections | FK to resource/org, ACL or ledger repair |
| Zenflows Files | SHA-512 hash and `zf_file` / `zf_file_join` bindings | Hash as proof of authorization |
| Feedback | SQLite reviews/comments with project_ulid/user_ulid | Authenticated public key corresponding to ULID |

[zenflows/src/zenflows/vf/person.ex:44–111](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person.ex#L44-L111); [zenflows/src/zenflows/vf/agent_relationship.ex:34–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/agent_relationship.ex#L34-L64); [zenflows/src/zenflows/vf/economic_resource.ex:83–157](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource.ex#L83-L157); [zenflows/src/zenflows/vf/economic_event.ex:101–175](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event.ex#L101-L175); [zenflows/src/zenflows/vf/process/domain.ex:102–162](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/process/domain.ex#L102-L162); [zenflows/src/zenflows/vf/proposal/resolv.ex:25–71](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/proposal/resolv.ex#L25-L71); [interfacer-dpp/internal/model/model.go:25–51](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/model/model.go#L25-L51); [zenflows/src/zenflows/file/domain.ex:67–123](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/file/domain.ex#L67-L123); [interfacer-feedback-service/internal/database/database.go:18–116](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/database/database.go#L18-L116).

Person.email is ordinary GraphQL field without dedicated policy resolver: [person/type.ex:55–97](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person/type.ex#L55-L97). A public root that returns a Person can expose selectable fields; authorizing only the `person` query is not enough.

## Proposed, not existing

[Permission model](../08-permission-model.md) defines Principal, Membership, ResourceControl, Grant, Delegation, Invitation, and ExternalBinding. Use stable IDs and namespaces for services, separate subject person/org/service, versioned role templates, grant validity and provenance. Controller and primaryAccountable remain different data.

DPP maintains documents/versions/sections, authority maintains bindings and rights to the resource. Medusa maintains seller/customer/order IDs with controlled mapping, not copied from client metadata. Each relationship used as a policy must be write protected and tracked; each new FK/constrain must have orphan record migration and management.
