> **Edizione italiana.** [English version](../en/16-decision-records.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 16 · Architecture Decision Records

Tutti gli ADR hanno stato **PROPOSED**. Nessuno è descritto come accettato. Le alternative restano utili anche se la raccomandazione cambia.

## ADR-001 · Modello di autorizzazione

**Stato: PROPOSED**

### Contesto
ValueFlows rappresenta responsabilità/custodia; F01/F02 mostrano che non sono ACL.

### Problema
Supportare collaborazione e organizzazioni senza conferire vendita o amministrazione da attributi economici.

### Opzioni
RBAC globale; ACL per oggetto; ReBAC generalizzata; ibrido scoped.

### Decisione proposta
RBAC scoped con membership e grant espliciti, attributi di stato e delega acting_for; controller distinto da primaryAccountable/custodian.

### Conseguenze
Nuove strutture additive, policy testabile per azione, migrazione storica esplicita.

### Rischi
Eredità poco comprensibile e grant troppo ampi; vietare fonti metadata liberamente modificabili.

### Questioni aperte
Q03–Q05, Q14–Q15; definizione controller e attributi privati. Vedi [domande del team](14-open-questions.md) e [registro evidenze](04-authorization-audit.md).

## ADR-002 · Autorità dei permessi

**Stato: PROPOSED**

### Contesto
Zenflows possiede risorse/PostgreSQL; DPP oggi non consulta i relativi diritti.

### Problema
Evitare ACL divergenti senza imporre un nuovo servizio operativo.

### Opzioni
Policy locali; modulo Zenflows; authz service dedicato; engine esterno.

### Decisione proposta
Permission module in Zenflows con API decisionale interna stabile e permission data autorevoli nello stesso PostgreSQL.

### Conseguenze
Transazioni locali più semplici; DPP dipende dall’autorità, estrazione futura possibile.

### Rischi
Disponibilità e carico Zenflows; ownership del contratto va assegnata.

### Questioni aperte
Q01–Q02 e Q12; SLO, volumi e organizzazione del team. Vedi [domande del team](14-open-questions.md) e [registro evidenze](04-authorization-audit.md).

## ADR-003 · Enforcement cross-service

**Stato: PROPOSED**

### Contesto
Proxy inoltra header; handler DPP non invocano una policy condivisa (F03/F04).

### Problema
Non consentire un bypass tramite altro servizio o dominio interno.

### Opzioni
Gateway-only; ACL duplicate; decisione remota; capability pre-emesse.

### Decisione proposta
PEP in ogni application service, authz online per write iniziali, fail-closed e contratto principal/action/object/versione/digest; regole locali solo restrittive.

### Conseguenze
Migrazione coordinata Zenflows→consumer; no positive cache iniziale; policy CAS e audit necessari.

### Rischi
TOCTOU cross-DB e outage; non promettere atomicità con semplice allow remoto.

### Questioni aperte
Q06, Q11–Q12: finestra in-flight e protocollo permit/drain per azioni critiche. Vedi [domande del team](14-open-questions.md) e [registro evidenze](04-authorization-audit.md).

## ADR-004 · Autorizzazione e lifecycle DPP

**Stato: PROPOSED**

### Contesto
Modello sezioni ma nessun ledger repair o binding resource validato; generic PUT e status diversi.

### Problema
Consentire riparazioni senza riscrivere le specifiche del produttore.

### Opzioni
DPP indipendente; stessi diritti editor; policy derivata e comandi per sezione.

### Decisione proposta
Binding tipizzato e versionato alla risorsa, publish/withdraw separati, specifiche versionate, riparazioni append-only e allegati subordinati alla sezione.

### Conseguenze
Migration dati e API comandi; generic PUT ristretto, public projection distinta.

### Rischi
Ambiguità model/batch/unit, documenti già pubblicati e orfani storage.

### Questioni aperte
Q07 e Q13; requisiti normativi, retention, ruoli certifier/manufacturer. Vedi [domande del team](14-open-questions.md) e [registro evidenze](04-authorization-audit.md).

## ADR-005 · Identità servizio e delega

**Stato: PROPOSED**

### Contesto
Esistono keyring/env e account tecnici, non una delega universale verificata.

### Problema
Distinguere il processo chiamante dall’umano per cui opera.

### Opzioni
Chiave globale; per-service token su TLS; mTLS/workload identity.

### Decisione proposta
Identità distinte per servizio/ambiente con scope e audience, prova utente o assertion delegata limitata; rotazione e revoca centralmente inventariate.

### Conseguenze
Client protocollo condivisi Go/Elixir/TS, secret storage server-side, audit actor+service.

### Rischi
Servizio compromesso con accesso DB; mTLS da solo non limita azioni business.

### Questioni aperte
Q08 e Q17; infrastruttura disponibile, trust DID e federation. Vedi [domande del team](14-open-questions.md) e [registro evidenze](04-authorization-audit.md).

## ADR-006 · Identità commerce e Medusa

**Stato: PROPOSED**

### Contesto
Preview mock senza backend; seller stringa non coincide con risorsa collaborativa.

### Problema
Separare customer, seller, organization member, inventory e finance.

### Opzioni
Editor=venditore; seller solo org; seller entity con legal subject; marketplace multi-vendor immediato.

### Decisione proposta
Seller entity distinta legata a persona/org verificata, mapping principal/customer, ruoli commerciali separati; partire da scope limitato e versione Medusa valutata con spike.

### Conseguenze
Adapter e test multi-seller obbligatori, ordini/stock/pagamenti autorevoli in Medusa, eventi idempotenti verso VF/DPP.

### Rischi
Doppio stock master, PII ordini e payout; license/mandato non equivalenti.

### Questioni aperte
Q09–Q10, Q18; single vs multi-seller, PSP, normative e authority inventario. Vedi [domande del team](14-open-questions.md) e [registro evidenze](04-authorization-audit.md).
