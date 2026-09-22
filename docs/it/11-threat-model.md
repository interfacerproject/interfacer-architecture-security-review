> **Edizione italiana.** [English version](../en/11-threat-model.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 11 · Threat model

## Asset, attori e confini

Asset: chiavi/seed, persone e contatti, membership/deleghe, contenuti progetto, stato inventario, provenance, documenti/certificati DPP, allegati, punti, comandi macchina e futuri dati commerciali. Attori: anonimo, utente autenticato di altro scope, ex collaboratore, servizio compromesso, browser compromesso, insider amministrativo e peer federato non fidato.

[Architettura e confini](02-current-architecture.md); [registro delle evidenze](04-authorization-audit.md). Non viene assegnato un CVSS senza inventario deploy, classificazione dati e condizioni operative.

| Minaccia | Stato / evidenza | Condizioni e impatto | Difesa incrementale |
|---|---|---|---|
| BOLA/IDOR resource | F01 confermato staticamente | Person firmata, target valido → edit non scoped | Principal nel dominio, policy oggetto |
| BFLA su organization/cataloghi | F01 e mutation matrix | Utente ordinario può invocare funzioni non legate a ruolo | Azioni registrate, ruoli scoped/catalog manager |
| Escalation via membership | Rischio da F01/F09 | Riutilizzare relazioni oggi editabili come ACL | Proteggere grant/membership prima di ReBAC |
| Transfer non autorizzato | F02 | Provider input non uguale a principal verificato | Acting_for e permessi su origine/destinazione |
| Bypass attraverso DPP | F03 | Backend DPP raggiungibile, handler non protetto | Enforcement locale + authority comune |
| Identity spoofing | F04 | Firma propria + user ID separato | Binding server-side chiave/principal |
| Lettura privata via guest/nested | F05 | Dati sensibili su root pubblico o relazioni | Proiezioni, field-level policy, query filtering |
| Replay / duplicate effect | F06 | Richiesta valida riutilizzata o retry post-commit | Nonce, TTL, audience e idempotenza |
| Service credential compromise | Rischio architetturale | DPP/Fabaccess/worker con privilegi eccessivi | Scopi minimi, credenziali distinte, audit e rotazione |
| Manipolazione punti | F07 | DID valido con richiesta token | Issuer limitato e premio derivato da evento |
| Peer social / egress non fidato | F08 potenziale SSRF | URL actor/object verso destinazioni non autorizzate | Signature/provenance e egress policy |
| Browser key theft | Storage confermato, exploit non osservato | XSS o dipendenza malevola same-origin | CSP, origine file separata, riduzione key exposure |
| DPP link substitution | Limite del modello confermato | productId non validato e parent editabile | Binding immutabile, cambio parent privilegiato |
| Audit incompleto | Limite dei percorsi esaminati | Log HTTP/eventi non ricostruiscono attore/decisione negata | Audit dedicato e correlazione |
| Webhook falso / cross-seller | Requisito futuro | Commerce non ancora implementato | Firma, replay defense, seller-scoped order queries |
| TOCTOU grant/stato | Rischio architetturale; status DPP read-then-write | Revoca o stato cambia tra check e commit | Versioni, lock locali, workflow cross-service esplicito |

## Frontend e NEXT_PUBLIC

Tutte le variabili `NEXT_PUBLIC_*` utilizzate da codice browser devono essere considerate pubbliche: URL/spec/feature flag possono esserlo; credenziali privilegiate no. La creazione del client GUI include configurazione admin e la registrazione SDK la usa in header; questo è un meccanismo di esposizione **condizionato al valore inserito in build**, non una prova del contenuto del sito live. [interfacer-gui/contexts/AuthContext.tsx:81–109](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/contexts/AuthContext.tsx#L81-L109); [interfacer-client/src/auth/AuthClient.ts:51–241](https://github.com/interfacerproject/interfacer-client/blob/dfb1baabf16516a845957d5587ccb933c1874221/src/auth/AuthClient.ts#L51-L241).

Il dettaglio di file locali con valori, stato di tracking e verifica dei chunk è nel rapporto riservato. Non sono stampati valori o hash dei segreti. Raccomandazione: registrazione mediata server-side, inventario consumer, rotazione dopo cutover, invalidazione artifact/caches e controllo cronologia. Spostare una variabile dall'env a un altro file frontend non la protegge.

Chiavi e seed sono accessibili a JavaScript nel localStorage. [interfacer-gui/contexts/AuthContext.tsx:242–302](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/contexts/AuthContext.tsx#L242-L302); [interfacer-client/src/config/storage.ts:1–40](https://github.com/interfacerproject/interfacer-client/blob/dfb1baabf16516a845957d5587ccb933c1874221/src/config/storage.ts#L1-L40). La severità cresce se file utente vengono resi come contenuto attivo dalla stessa origine: dettagli di route e remediation riservati, senza payload dimostrativi.

## Deployment

- `GQL_AUTH_CALLS` può disabilitare Sign e Admin; default true. Renderlo non disattivabile in produzione senza break-glass documentato e allarme. [zenflows/conf/runtime.exs:89–131](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/conf/runtime.exs#L89-L131); [zenflows/src/zenflows/gql/mw/admin.ex:28–42](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/mw/admin.ex#L28-L42).
- Compose DPP pubblica porte DB/storage e abilita download anonimo; separare template dev da production, bind privati, storage privato per contenuti non pubblicati. [interfacer-dpp/docker-compose.yml:3–61](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/docker-compose.yml#L3-L61).
- Restroom riceve materiale crittografico server-side in alcuni flussi; rete privata, TLS appropriato, no body logging, allowlist contratti e quote. [zenflows/src/zenflows/restroom.ex:47–133](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/restroom.ex#L47-L133); [zenflows/src/zenflows/did.ex:63–112](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/did.ex#L63-L112).
- Proxy con read-all body/retry generalizzato: limiti, timeout, propagazione status e retry idempotenti vanno verificati; non affidargli la semantica di auth. [interfacer-proxy/main.go:160–241](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L160-L241).
- Le versioni di dipendenze e immagini sono una superficie di manutenzione. Non è stato eseguito un CVE audit completo; non dedurre vulnerabilità da sola anzianità di Next/Elixir/Postgres.

## Attacchi composti da discutere

1. Limitare `updateEconomicResource` ma lasciare createEconomicEvent: integrità ancora modificabile tramite effetti indiretti.
2. Limitare GUI a «miei DPP» ma lasciare PUT/delete diretti: filtro UI non è ACL.
3. SQL ownership corretto con principal non autenticato: il database applica fedelmente la decisione sbagliata.
4. Revocare un membro org ma lasciare token seller/worker e grant derivati: offboarding parziale.
5. Rendere privato un DPP senza rimuovere bucket anonimo, cache GUI e copie pubblicate: riservatezza non retroattiva.

## Validazione sicura

Riprodurre solo su fixture locali e origin disconnessi dai servizi condivisi. Usare fake DID resolver/Restroom, chiavi di test generate, DB effimeri; acquisire stato prima/dopo e audit. Nessun esempio di richiesta contro produzione è incluso. Per superfici critiche leggere prima il rapporto riservato e pianificare disclosure/coordinamento con i maintainer.
