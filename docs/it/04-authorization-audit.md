> **Edizione italiana.** [English version](../en/04-authorization-audit.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 04 · Audit dell'autorizzazione

## Metodo e classificazione

**Confermato** significa proprietà dimostrabile del codice ai commit indicati, non exploit eseguito su produzione. **Potenziale** richiede una verifica aggiuntiva. **Rischio architetturale** descrive un confine di fiducia fragile. **Limite di design** indica una funzionalità/policy non rappresentata. **Questione aperta** richiede decisione del team. **Proposta** non descrive il sistema attuale.

Inventario statico di tutti i campi root importati nello schema GraphQL, lettura dei resolver di mutazione e ispezione delle funzioni di persistenza; tracing approfondito di risorse/eventi/person/org/DPP/feedback. Non si afferma una verifica dinamica esaustiva di tutte le combinazioni di input.

[Mutation matrix](appendix/mutation-matrix.md) · [Endpoint matrix](appendix/endpoint-matrix.md) · [Query matrix](appendix/query-matrix.md).

## F01 · Firma valida senza autorizzazione per oggetto — CONFERMATO, P0

**Componente:** Zenflows. Sign produce `req_user`, ma `update_economic_resource(..., _)` e `delete_economic_resource(..., _)` lo ignorano. Il dominio carica per ID ed esegue update/delete via Ecto senza principal. Lo stesso pattern è osservabile su Organization e AgentRelationship; `updatePerson` non è self-only.

**Evidenza:** [zenflows/src/zenflows/gql/mw/sign.ex:28–72](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/mw/sign.ex#L28-L72); [zenflows/src/zenflows/vf/economic_resource/resolv.ex:28–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/resolv.ex#L28-L64); [zenflows/src/zenflows/vf/economic_resource/domain.ex:246–332](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/domain.ex#L246-L332); [zenflows/src/zenflows/vf/organization/resolv.ex:25–51](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/organization/resolv.ex#L25-L51); [zenflows/src/zenflows/vf/organization/domain.ex:58–150](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/organization/domain.ex#L58-L150); [zenflows/src/zenflows/vf/agent_relationship/resolv.ex:36–51](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/agent_relationship/resolv.ex#L36-L51); [zenflows/src/zenflows/vf/person/resolv.ex:38–85](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person/resolv.ex#L38-L85).

**Condizioni:** endpoint raggiungibile, firma valida di una Person se auth abilitata, ID esistente e input accettato dal changeset/DB. Una cancellazione può essere impedita da FK: non è corretto promettere la cancellazione di qualsiasi record. Il difetto è l'assenza della decisione per attore prima della persistenza.

**Impatto:** modifica di contenuti/relazioni altrui e gestione di organizzazioni senza delega; API diretta non vincolata alle scelte UI. **Rimedio:** contesto principal obbligatorio e policy nel dominio, più enforcement degli oggetti referenziati. **Incertezza:** regole infrastrutturali esterne e commit live. Nessun test offensivo remoto eseguito.

## F02 · Invarianti economiche basate su agenti dichiarati — CONFERMATO, P0

**Componente:** creazione EconomicEvent. Il resolver passa input al dominio senza identità. Il dominio confronta `evt.provider_id` con `primary_accountable_id`/`custodian_id`; gli agenti sono input validati per esistenza e coerenza economica, non per diritto del firmatario di rappresentarli.

**Evidenza:** [zenflows/src/zenflows/vf/economic_event/resolv.ex:38–49](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/resolv.ex#L38-L49); [zenflows/src/zenflows/vf/economic_event.ex:101–175](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event.ex#L101-L175); [zenflows/src/zenflows/vf/economic_event/domain.ex:124–285](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L124-L285); [zenflows/src/zenflows/vf/economic_event/domain.ex:782–909](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L782-L909).

**Condizioni:** firmatario valido, riferimenti e quantità/unità coerenti con i vincoli dell'azione. **Impatto:** transizioni di accountability, custodia, quantità, metadata o lineage possono essere richieste senza autorizzazione del soggetto che firma. **Rimedio:** autorizzare azione, delega `acting_for`, risorsa origine, destinazione, processo ed effetti su contenuti prima della transazione; mantenere le validazioni ValueFlows.

**Precisione importante:** `updateEconomicResource` espone soltanto id/name/note/images/classifiedAs/repo, non primaryAccountable o custodian. Il cambio dei campi economici passa dagli eventi o da funzioni interne più ampie. `updateEconomicEvent` non consente di riscrivere provider/action, ma solo un sottoinsieme descrittivo. [zenflows/src/zenflows/vf/economic_resource/type.ex:224–353](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/type.ex#L224-L353); [zenflows/src/zenflows/vf/economic_event.ex:294–308](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event.ex#L294-L308). **Incertezza:** esiti di ogni specifica transizione non testati dinamicamente.

## F03 · Enforcement DPP incompleto — CONFERMATO, P0

**Componente:** DPP Gin. Il router applica logging/recovery e CORS, non auth generale. Update, delete, status e delete attachment non chiamano VerifyDid/IsAuth. Create e upload/add attachment lo fanno, ma non decidono il diritto sul prodotto/passaporto.

**Evidenza:** [interfacer-dpp/cmd/main/main.go:30–54](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/cmd/main/main.go#L30-L54); [interfacer-dpp/internal/handler/handler.go:154–224](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L154-L224); [interfacer-dpp/internal/handler/handler.go:480–551](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L480-L551); [interfacer-dpp/internal/handler/handler.go:676–753](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L676-L753); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116); [interfacer-dpp/internal/handler/handler.go:553–674](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L553-L674).

**Condizioni:** accesso alla rotta del servizio o al proxy che la inoltra; DB/storage funzionanti; ID e input validi. Per `PUT /dpp/:id`, il `$set` dell'intera struct include `_id`: MongoDB può rifiutare un cambiamento di ID. La mancanza di auth è certa, ma un body generico non garantisce update riuscito. Le altre scritture sono percorsi distinti e non dipendono da questo problema.

**Impatto:** integrità DPP e workflow di pubblicazione non subordinati ai diritti Zenflows; proteggere solo Zenflows non risolve il bypass. **Rimedio:** gate temporaneo su tutte le scritture, poi auth+policy in ogni handler/domain function, allowlist dei campi, vincolo DPP→risorsa autorevole. **Incertezza:** esposizione live, configurazione del gateway esterno e documenti reali.

## F04 · Principal dichiarato separatamente dalla firma — CONFERMATO, P0

**Componente:** feedback; DPP per attribuzione autore. Nel feedback il body viene verificato con `did-pk`, ma `user_ulid` è copiato da `x-user-id` senza risolvere il legame tra i due. SQL filtra correttamente per user ULID: è il valore di quel principal a non essere autenticato. In DPP Create `CreatedBy` preferisce lo stesso header; fallback è una public key, quindi il campo ha anche due semantiche diverse.

**Evidenza:** [interfacer-feedback-service/internal/auth/middleware.go:15–88](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/auth/middleware.go#L15-L88); [interfacer-feedback-service/internal/database/comment_repo.go:88–105](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/database/comment_repo.go#L88-L105); [interfacer-feedback-service/internal/database/review_repo.go:115–129](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/database/review_repo.go#L115-L129); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Condizioni:** propria firma accettata e DID risolvibile; identificatore target noto; nessun livello esterno che sostituisca e attesti l'header. **Impatto:** attribuzione falsa e controlli di ownership feedback basati su identità non provata. **Rimedio:** derivare principal da chiave registrata o assertion verificata; ignorare header arbitrari; migrare `createdBy` con provenance. **Incertezza:** mapping DID effettivamente disponibile e policy di federazione.

## F05 · Pubblico, bozza e informazioni riservate non separati — CONFERMATO come comportamento; P1

**Componente:** DPP, Zenflows, file e cache GUI. GetDPP/GetAllDPPs non richiedono auth né impongono status active. I filtri `createdBy`/`status` sono filtri client facoltativi, non policy. Le query economicResource/economicResources sono guest; `primaryAccountable` può risolvere una Person il cui tipo include email. Il middleware globale è applicato ai root field, non automaticamente ai campi annidati.

**Evidenza:** [interfacer-dpp/internal/handler/handler.go:117–153](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L117-L153); [interfacer-dpp/internal/handler/handler.go:226–329](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L226-L329); [zenflows/src/zenflows/vf/economic_resource/type.ex:224–353](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/type.ex#L224-L353); [zenflows/src/zenflows/gql/schema.ex:130–193](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/schema.ex#L130-L193); [zenflows/src/zenflows/vf/person/type.ex:179–270](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/person/type.ex#L179-L270); [interfacer-gui/pages/api/dpp-file/[id]/[filename].ts:1–35](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/pages/api/dpp-file/[id]/[filename].ts#L1-L35). Il campo Person.email è in `person/type.ex:77–78` (vedi [modello dati](appendix/data-model.md)).

**Condizioni:** dati presenti e percorsi raggiungibili. **Impatto:** manca una garanzia di riservatezza di bozze, sezioni e allegati. Non ogni lettura pubblica è una vulnerabilità: dipende dalla classificazione attesa. **Rimedio:** proiezione pubblica esplicita, policy anche nei resolver annidati, filtri server per liste/facet, bucket privati e cache coerenti. **Incertezza:** contenuti realmente sensibili e consenso alla pubblicazione.

## F06 · Replay e confusione tra contesti di firma — limite CONFERMATO, P1

**Componente:** firma GraphQL e DID. Il contratto verifica contenuto normalizzato; nessun nonce, scadenza, metodo, path o audience. Nel DPP addAttachment viene firmato il checksum, non il destinatario o la sezione. Il proxy ritenta anche richieste di scrittura dopo errori di trasporto.

**Evidenza:** [zenflows-crypto/src/verify_graphql.zen:17–44](https://github.com/interfacerproject/zenflows-crypto/blob/0ffcce9b90799c9cb61f11fc594aeb513a01326f/src/verify_graphql.zen#L17-L44); [interfacer-client/src/crypto/sign.ts:36–137](https://github.com/interfacerproject/interfacer-client/blob/dfb1baabf16516a845957d5587ccb933c1874221/src/crypto/sign.ts#L36-L137); [interfacer-dpp/internal/handler/handler.go:553–674](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L553-L674); [interfacer-proxy/main.go:160–241](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L160-L241).

**Condizioni:** disponibilità di una richiesta/firma già valida o errore di rete dopo commit backend. Non è stata osservata intercettazione di traffico. **Impatto:** replay/duplicazioni o riutilizzo in contesti compatibili; effetti reali dipendono da vincoli e idempotenza dell'operazione. **Rimedio:** envelope versionato, request ID, deduplica transazionale, niente retry indiscriminati; deadline. **Incertezza:** comportamento deployed Zenroom e protezioni esterne.

## F07 · Wallet: autenticare non significa poter emettere — CONFERMATO, P1/P0 secondo uso

**Componente:** zenflows-wallet. Dopo DID/firma, `addTokensHandler` passa owner/token/amount a `AddDiff` senza ruolo issuer o binding owner→firmatario. Non si tratta necessariamente di denaro: il SDK/GUI usa punti idea/strengths. Bank dispone di un comando airdrop da dati importati: non si assume che sia in uso né automaticamente collegato.

**Evidenza:** [zenflows-wallet/wallet.go:83–136](https://github.com/interfacerproject/zenflows-wallet/blob/f5cf1668afe371329ed827d0bb56557e0bedcda6/wallet.go#L83-L136); [zenflows-wallet/did-auth.go:43–78](https://github.com/interfacerproject/zenflows-wallet/blob/f5cf1668afe371329ed827d0bb56557e0bedcda6/did-auth.go#L43-L78); [interfacer-gui/hooks/useProjectCRUD.ts:67–119](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/hooks/useProjectCRUD.ts#L67-L119); [zenflows-bank/cmd/airdrop.go:31–125](https://github.com/interfacerproject/zenflows-bank/blob/e5c2d2e6bd1ad072d1575de0a2be983854429b35/cmd/airdrop.go#L31-L125).

**Condizioni:** DID accettato, input numerico e DB disponibile. **Impatto:** emissione di punti non autorizzata se l'intento è premiare eventi reali. **Rimedio:** issuer service-scoped, evento business validato, idempotenza e ledger; vietare conversioni commerciali fino alla decisione. **Incertezza:** policy intenzionale e valore dei punti attuale.

## F08 · Social inbox e chiamate esterne — CONFERMATO/POTENZIALE, P1

**Componente:** zenflows-inbox. Messaggistica send/read/set/delete lega la firma alla chiave sender/receiver; storage set/delete include receiver nella chiave. È un controllo positivo da conservare. Gli handler social inbox/outbox invece persistono attività senza quel percorso di verifica e possono fare POST verso URL derivati da actor/object.

**Evidenza:** [zenflows-inbox/inbox.go:80–243](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L80-L243); [zenflows-inbox/storage.go:59–120](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/storage.go#L59-L120); [zenflows-inbox/inbox.go:427–588](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L427-L588); [zenflows-inbox/inbox.go:697–725](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L697-L725).

**Condizioni:** raggiungibilità della rotta social e input valido. **Impatto confermato:** attività non attribuite crittograficamente nello stesso modo dei messaggi; **potenziale:** SSRF/egress verso reti non consentite, da validare soltanto in sandbox. **Rimedio:** identity/provenance federata, policy per attività, allowlist protocolli/egress, verifica HTTP signatures ove adottate. **Incertezza:** gateway e peer fidati di deployment.

## F09 · Esecuzione interna e import saltano l'API — rischio CONFERMATO nel design, P1

**Componente:** Zenflows dominio e SWPass. API di dominio accettano id/params/repo, non un contesto autorizzativo. L'import crea agenti/eventi/risorse direttamente e usa una prima persona ricavata dalle email come sostituto dell'organizzazione.

**Evidenza:** [zenflows/src/zenflows/vf/economic_resource/domain.ex:246–332](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/domain.ex#L246-L332); [zenflows/src/zenflows/vf/process/domain.ex:102–162](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/process/domain.ex#L102-L162); [zenflows/src/zenflows/sw_pass/domain.ex:108–197](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/sw_pass/domain.ex#L108-L197).

**Condizioni:** codice interno/job/import privilegiato in esecuzione; non è di per sé un ingresso anonimo. **Impatto:** patch solo nei resolver lascia vie interne e dati storici senza amministrazione affidabile. **Rimedio:** application service con principal obbligatorio, primitive raw private e separate; import con service identity limitata e provenance. **Incertezza:** utilizzo reale dell'import e qualità dei record già creati.

## F10 · Permessi di macchina e job di analisi — rischio architetturale, P1

Fabaccess verifica DID/firma/timestamp poi usa un account configurato verso una macchina scelta dall'input; non risulta una ACL Interfacer per macchina. OSH esegue clone Git e analisi senza auth nel router. Non si afferma che Fabaccess non abbia propri limiti sull'account né che OSH esegua arbitrariamente una shell: `exec.Command` usa argomenti separati.

**Evidenza:** [zenflows-fabaccess/main.py:55–123](https://github.com/interfacerproject/zenflows-fabaccess/blob/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc/main.py#L55-L123); [zenflows-osh/web.go:45–83](https://github.com/interfacerproject/zenflows-osh/blob/56855d426ffd884d91dd72373a2292f1ae5695ed/web.go#L45-L83); [zenflows-osh/analyze.go:28–58](https://github.com/interfacerproject/zenflows-osh/blob/56855d426ffd884d91dd72373a2292f1ae5695ed/analyze.go#L28-L58). **Condizioni:** servizi abilitati e dipendenze disponibili. **Impatto:** diritti fisici/service credentials ed egress non modellati nella futura policy. **Rimedio:** scope macchina, training/abilitazione se richiesti, nonce oltre timestamp, sandbox/quote/egress per OSH. **Incertezza:** API pyfabapi e policy del server Fabaccess non analizzate integralmente.

## F11 · Predicato di scadenza email invertito — CONFERMATO, P1

**Componente:** `Zenflows.Email.Domain.token_validate`. Il token include timestamp, HMAC e ID persona; il codice confronta il timestamp di emissione con `now + expiry`, anziché confrontare `now` con `issued_at + expiry`.

**Evidenza:** [zenflows/src/zenflows/email/domain.ex:76–101](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/email/domain.ex#L76-L101).

**Condizioni:** token autentico della persona richiedente, ancora valido rispetto alla chiave HMAC; il difetto temporale non permette di forgiare token o impersonare un'altra persona. **Impatto:** i token emessi nel passato non scadono secondo la durata configurata in questo predicato. **Verifica sicura:** riprodotta soltanto l'espressione DateTime con clock e timestamp sintetici tramite Elixir, senza applicazione, chiavi, database o invio email: emissione dieci giorni prima e durata quattro giorni risultano accettate dal predicato attuale, negate da quello atteso. Non è un test end-to-end del token.

**Rimedio:** verificare `issued_at <= now < issued_at + expiry`, con skew esplicito se necessario; test bordi e token futuri/scaduti; valutare revoca/one-time use secondo requisiti. **Incertezza:** commit e configurazione deploy, eventuali controlli esterni. Conservare HMAC e binding self correttamente presenti.

## F12 · Status HTTP upstream non propagato — CONFERMATO, P2

**Componente:** interfacer-proxy `proxyRequest`. Quando `client.Do` restituisce una risposta senza errore di trasporto, il proxy copia header e body ma non esegue `WriteHeader(res.StatusCode)`. In Go la prima scrittura del body usa normalmente 200 se non è stato impostato uno status.

**Evidenza:** [interfacer-proxy/main.go:211–230](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L211-L230).

**Condizioni:** risposta upstream ricevuta correttamente con status non 200. **Impatto:** un rifiuto 401/403 o un conflitto può apparire al SDK come HTTP success; questo non autorizza la scrittura negata dal backend, ma compromette gestione errori/UX e osservabilità. **Rimedio:** propagare lo status e testare 201/204/400/401/403/409/500 con upstream HTTP locale simulato, distinguendo errori di trasporto e applicativi. **Incertezza:** nessun test runtime Go eseguito; un ingress ulteriore può cambiare il comportamento finale.

## Controlli che esistono e non vanno rimossi

Firma EdDSA; key lookup Person in Zenflows/inbox; confronto admin; validazione ID/schema/changeset; FK; email verification self-bound; invarianti eventi; transizioni DPP; limite upload DPP 10 MiB; ownership SQL feedback (da alimentare con principal corretto). Non sostituiscono una policy completa, ma sono fondamenta utili.

## Rilievi riservati

Una verifica separata tratta superfici frontend amministrative, configurazione credenziali e file-serving same-origin. Il rapporto è escluso da `docs/`, indice di ricerca e artifact Pages. Prima di pubblicare anche questa sintesi, richiedere approvazione dei maintainer: i link al sorgente non sono una procedura di disclosure coordinata.
