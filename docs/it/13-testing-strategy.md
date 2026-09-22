> **Edizione italiana.** [English version](../en/13-testing-strategy.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 13 · Strategia di test

## Risultati effettivamente eseguiti

Nel checkout SDK: `./node_modules/.bin/vitest run src/__tests__/unit.test.ts` → **31/31 pass**, Vitest 2.1.9. Sono test storage/tagging/types, non prove di enforcement backend. È stato selezionato il solo file unitario dopo lettura; non eseguito il comando generico che include `real-backend.test.ts`.

Eseguita anche una verifica Elixir della sola espressione temporale di `Email.Domain.token_validate` con timestamp sintetici: confermata la discrepanza descritta in [F11](04-authorization-audit.md). Non è stato generato o verificato un token reale.

I contract test feedback presenti usano stub e router senza middleware auth: [internal/handler/test_helper_test.go:10–32](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/handler/test_helper_test.go#L10-L32). Anche se superati, non dimostrerebbero la correttezza del binding delle identità.

Non eseguiti test Zenflows con database/Restroom, test DPP con Mongo/MinIO/DID né test browser collegati a servizi condivisi. Go non disponibile nel PATH della sessione; non si è installato/eseguito un ambiente server live. ExUnit usa SQL Sandbox ma la configurazione runtime può puntare a DB non isolati: non è una garanzia sufficiente senza setup dedicato.

Risultati build sito, link, Mermaid e inventory checker: [rapporto di validazione](appendix/validation.md). I test seguenti sono **specifiche da implementare**, non successi già ottenuti.

## Harness isolato proposto

Compose di test separato con PostgreSQL, MongoDB, MinIO privato, SQLite temporaneo, fake DID/Restroom e clock controllato; rete senza accesso a produzione. Chiavi generate esclusivamente per fixture. Test di contratto crittografico separati con Zenroom reale e vettori sintetici. All'avvio rifiutare URL non loopback/allowlist test, DB name non test, credenziali condivise; deny egress esterno. Seed esplicito, snapshot before/after, teardown confinato ai volumi del test.

## Matrice minima Alice/Bob

Ogni riga verifica risposta **e assenza/presenza degli effetti** su DB, file, quantità, binding e audit. Deny HTTP può essere 403/404 secondo policy; GraphQL può usare HTTP 200 con error code e nessun side effect.

| ID | Scenario | Atteso |
|---|---|---|
| T01 | Alice crea R personale con firma valida | Allow; controller Alice, attore audit Alice, primaryAccountable economico coerente |
| T02 | Bob e anonimo leggono proiezione pubblica R | Allow; nessuna email/draft/privato nelle relazioni |
| T03 | Bob modifica R di Alice via GraphQL diretto | Deny; nessun cambiamento |
| T04 | Bob elimina R | Deny per policy, non soltanto un errore FK |
| T05 | Alice invita Bob come editor; Bob accetta | Allow dopo accettazione; invito pending non basta |
| T06 | Bob modifica name/note consentiti | Allow; actor Bob, grant provenance |
| T07 | Bob tenta delete/transfer/grant/sell/pubblicazione non concessi | Deny per ogni azione, inclusi campi extra |
| T08 | Alice revoca grant Bob | Allow, epoch aumentato, audit; vietata revoca da Bob senza delega |
| T09 | Bob ripete edit dopo revoca e con tab/token vecchi | Deny per nuove decisioni; test separato per operazioni in volo |
| T10 | Bob usa DPP update/status/delete/attachment dopo revoca | Deny su tutte le rotte e sul parent binding |
| T11 | Bob salta SDK/proxy e chiama backend o dominio direttamente | Deny; ExecutionContext obbligatorio; Repo raw non ingresso applicativo |
| T12 | Bob dichiara acting_for org di Alice o provider org | Deny; ID e firma propria non provano membership |
| T13 | Seller Bob accede a listing/ordine/stock/payout seller Alice | Deny; query, count e export scoped |
| T14 | Servizio senza scope o compromesso dichiara Alice | Deny senza prova/delega; nessun grant globale o scrittura arbitraria |

## Test unitari policy

Ruoli × azioni × scope × stato account/membership × attributi. Tabelle di esempi condivise tra Elixir/Go/TS, non tre implementazioni divergenti della stessa policy. Test di precedence deny, grants multipli, ereditarietà disabilitata, scadenza, delega non transitiva, inviti riutilizzati, ultimo org admin e trasferimento controller con destinatario non consenziente. Property tests: aggiungere un riferimento business non crea un grant; editor non può ampliare i propri diritti.

## Test di integrazione dominio Zenflows

- `createEconomicEvent` firmato Bob con provider/receiver Alice: deny, anche se le invarianti ValueFlows sarebbero valide.
- Per transfer/custody/rights/move: permessi su origine e destinazione; container e risorse contenute; rollback atomico degli effetti su quantità/stato.
- `accept`/`modify`, cite/use e metadata: non devono diventare percorsi indiretti di edit non autorizzato.
- Organization/AgentRelationship/role behavior: non auto-assegnare admin. Proteggere unit/spec/global catalog da normale membro se policy richiede curator.
- Nested resolver, `traceDpp`, immagini, pagination/count: niente bypass della policy di lettura o disclosure indiretta.
- Multiple root mutation e alias: per ognuna decisione, nessun riutilizzo scorretto di context/allow di un altro campo; gestione partial success esplicita.
- Import/job: service principal e scope obbligatori, record ambigui quarantinati; audit actor diverso da provider.

## DPP e storage

Verificare create su product di altro scope, `x-user-id` difforme dalla chiave, parent substitution nel PUT, campi di sistema immodificabili, sezione non allowlisted, bypass transizione tramite generic update, draft non restituito a guest, ID esistente/non esistente indistinguibile dove necessario. Mongo `$set` non deve tentare di mutare `_id`.

Repair operator può appendere una riparazione sulla sola istanza delegata; non modifica specifiche, vecchi eventi o autore produttore. Certifier non modifica dati di proprietà. Test upload dimensione/MIME/checksum, firma checksum raw vs base64, target ID/sezione inclusi nella firma v2, cleanup orfani, delete replay, bucket origin e route GUI senza bypass private policy. Cache pubblica esclusa per documenti privati; contenuto attivo mai stessa origine privilegiata.

## Cross-service e fault injection

- Stessa decisione resource↔DPP per edit equivalente, senza copiare ACL liberamente.
- Autorità down/timeout/risposta malformata→deny; nessun fallback legacy.
- Revoca dopo allow prima di CAS: test della finestra dichiarata e del protocollo drain per operazioni critiche; il test non può pretendere atomicità inesistente.
- Decision token audience/action/digest/epoch sbagliati→deny; request ID duplicato→stesso esito, non doppio effetto.
- Service credential scaduta/ruotata, evento duplicato/fuori ordine, crash post-commit pre-response e retry proxy.
- Feedback: firma propria non può sostituire user header; ownership SQL negata anche con ID valido.
- Inbox: receiver Bob non può leggere/set/delete messaggi Alice; social richiede policy separata.
- Wallet: solo issuer può assegnare premi; stesso evento non emette due volte.

## Medusa: test futuri obbligatori

Due seller e un customer comuni; listing ID del seller A in route seller B, inventory location di A in payload B, ricerca/export order non autorizzata, ex dipendente con sessione ancora valida, refund oltre soglia, payout edit senza step-up. PSP sandbox, webhook firmati/invalidi/duplicati, totale browser manipolato, fulfillment→DPP una sola volta per unità, refund non elimina provenance.

## Regressione e criterio release

Eseguire unit policy a ogni PR; integrazione e schema coverage prima del merge; cross-service e failure/revoca in staging **isolato** prima del deploy; canary e monitoraggio deny/conflitti. Ogni endpoint write della matrice deve avere almeno una prova positiva, una negativa cross-owner e una senza autenticazione, oltre alle azioni indirette. Test frontend solo dopo quelli API/domain. Non segnare «sicuro» un test che fallisce per DB down, payload invalido o FK: distinguere denial autorizzativo dal guasto tecnico.
