> **Edizione italiana.** [English version](../../en/appendix/data-model.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# Modello dati · attuale e proposto

## Attuale: evidenze

| Concetto | Struttura osservata | Non inferire |
|---|---|---|
| Person | `vf_agent`, type per, name/user/email, chiavi pubbliche, is_verified | Sessione server, membership o seller |
| Organization | Agent economico gestito dal relativo dominio | Tenant con ACL implicita |
| AgentRelationship | `vf_agent_relationship`, subject/object/relationship, note | Invito accettato, ruolo amministrativo protetto |
| EconomicResource | `vf_economic_resource`, primary_accountable/custodian, quantità, conforms_to, lot/contained_in, metadata | Controller amministrativo o creator verificato |
| EconomicEvent | Azione/provider/receiver/processo/risorse/quantità; effetti nel dominio | Attore umano autenticato del log |
| Process | Attività input/output con nesting/grouping | Un project scope di permission già implementato |
| Proposal/ProposedIntent | Proposta e legame con Intent | Prodotto Medusa, seller mandate o checkout |
| DPP | Mongo struct con productId/batchType/batchId/createdBy/status e sezioni | FK verso risorsa/org, ACL o ledger repair |
| File Zenflows | Hash SHA-512 e associazioni `zf_file` / `zf_file_join` | Hash come prova di autorizzazione |
| Feedback | SQLite reviews/comments con project_ulid/user_ulid | Chiave pubblica autenticata corrispondente all'ULID |

[zenflows/src/zenflows/vf/person.ex:44–111](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person.ex#L44-L111); [zenflows/src/zenflows/vf/agent_relationship.ex:34–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/agent_relationship.ex#L34-L64); [zenflows/src/zenflows/vf/economic_resource.ex:83–157](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource.ex#L83-L157); [zenflows/src/zenflows/vf/economic_event.ex:101–175](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event.ex#L101-L175); [zenflows/src/zenflows/vf/process/domain.ex:102–162](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/process/domain.ex#L102-L162); [zenflows/src/zenflows/vf/proposal/resolv.ex:25–71](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/proposal/resolv.ex#L25-L71); [interfacer-dpp/internal/model/model.go:25–51](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/model/model.go#L25-L51); [zenflows/src/zenflows/file/domain.ex:67–123](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/file/domain.ex#L67-L123); [interfacer-feedback-service/internal/database/database.go:18–116](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/database/database.go#L18-L116).

Person.email è campo GraphQL ordinario senza resolver di policy dedicato: [person/type.ex:55–97](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person/type.ex#L55-L97). Un root pubblico che restituisce una Person può esporre i campi selezionabili; autorizzare solo la query `person` non basta.

## Proposto, non esistente

[Permission model](../08-permission-model.md) definisce Principal, Membership, ResourceControl, Grant, Delegation, Invitation e ExternalBinding. Usare ID stabili e namespace per servizi, separare subject person/org/service, role templates versionati, validità e provenance del grant. Controller e primaryAccountable rimangono dati diversi.

DPP conserva documenti/versioni/sezioni, l'autorità conserva binding e diritti sulla risorsa. Medusa conserva seller/customer/order IDs con mapping controllato, non copiato da metadata client. Ogni relazione usata come policy deve essere protetta in scrittura e tracciata; ogni nuova FK/constrain deve avere migrazione e gestione record orfani.
