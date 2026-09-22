> **Edizione italiana.** [English version](../en/07-cross-service-authorization.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 07 · Autorizzazione cross-service

## Oggi non c'è una catena di fiducia unica

| Passaggio | Cosa prova davvero | Cosa non prova |
|---|---|---|
| GUI→Zenflows firmato | Possesso chiave della Person risolta per username | Diritto sull'ID target o rappresentanza dell'organization |
| GUI→DPP create | Firma con chiave dichiarata e URL DID che restituisce 200 | Membership, diritto sul productId, legame x-user-id/chiave |
| GUI→feedback | Firma del body e disponibilità DID | Principal copiato dall'header non è autenticato |
| Proxy→backend | Il proxy ha inoltrato i byte/header | Nessuna attestazione di identità o decisione |
| Inbox→Zenflows | Lookup chiave di sender/receiver | Non una policy universale per le attività social |
| Fabaccess→macchina | Azione dell'account Fabaccess configurato | Diritto individuale sulla macchina non verificato da una policy Interfacer |

Evidenze: [zenflows/src/zenflows/gql/mw/sign.ex:28–72](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/gql/mw/sign.ex#L28-L72); [interfacer-dpp/internal/auth/auth.go:98–151](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/auth/auth.go#L98-L151); [interfacer-feedback-service/internal/auth/middleware.go:15–88](https://github.com/interfacerproject/interfacer-feedback-service/blob/d905a82a02d4115b13c87557591b7ddca6eb39b1/internal/auth/middleware.go#L15-L88); [interfacer-proxy/main.go:160–241](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L160-L241); [zenflows-inbox/inbox.go:80–243](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/inbox.go#L80-L243); [zenflows-fabaccess/main.py:55–123](https://github.com/interfacerproject/zenflows-fabaccess/blob/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc/main.py#L55-L123).

DPP non verifica una credenziale del proxy e non richiede che il traffico passi attraverso di esso. Il compose rende l'app raggiungibile sull'host. Firewall e ingress reali sono una domanda aperta, non un confine garantito. Il proxy inoltra header senza derivare un principal trusted. CORS non autentica client non browser.

## Regola di coerenza proposta

Una scrittura sul DPP associato alla risorsa R deve richiedere il **permesso corrispondente su R**, non solo `createdBy == subject` nel DB DPP. Nessun servizio può attribuire da sé un ruolo organizzativo usando dati client. La policy DPP può essere più restrittiva, mai un secondo percorso per ottenere generic resource edit negato da Zenflows.

Esempio: `dpp.spec.update` implica il diritto tecnico sulla risorsa più delega specifiche; `dpp.repair.append` è un'azione distinta e limitata, legata alla medesima risorsa/istanza. Non concedere generic PUT al repair operator.

## Valutazione delle alternative

| Soluzione | Sicurezza | Complessità e manutenzione | Prestazioni / failure mode | Compatibilità e deploy |
|---|---|---|---|---|
| A. Policy indipendente in ogni servizio | Isolamento locale, ma divergenza e revoche incoerenti | Bassa all'inizio, alta nel tempo | Veloce; split-brain su grant e parent | Facile aggiunta, difficile semantica comune |
| B. Tutte le decisioni in Zenflows | Dati autorevoli vicini alle risorse | Media; rischio god service se decide dettagli DPP | Chiamate remote; blocco scritture se Zenflows down | Naturale per Ecto, meno per documenti/ordini |
| C. Servizio authz dedicato | Buona separazione se dati e protocollo corretti | Alta: sync, HA, osservabilità, migrazioni | Nuovo hop e failure domain | Non giustificato come prerequisito iniziale |
| D. Libreria/SDK condiviso | Contratto uniforme; non crea autorità comune | TS/Go/Elixir: non basta una libreria unica | Locale veloce, stale data se replicati | Utile per client protocollo e test vector |
| E. Ibrida: autorità in Zenflows + PEP locali | Revoca centrale e regole documentali locali | Media e incrementale | Remote decision iniziale, fallimento chiuso | Raccomandata; nessun nuovo container iniziale |
| F. OPA/Cedar/OpenFGA o simili | Linguaggio/relazioni formali, ma non sanano principal falsi | Medio-alta: ownership dati, adapter, policy deployment | Cache/freshness e disponibilità da progettare | Valutare solo dopo schema e carico reali |

La **E** usa la B per dati comuni e la D per contratto, evitando la A per membership condivise. Un motore di policy non deve diventare il primo progetto prima di aver chiuso gli handler scoperti.

## Contratto minimo, ancora da implementare

Richiesta decisionale: principal verificato, eventuale delega, service identity, action registrata, object type/id, parent binding/versione, digest operazione, request ID. Risposta: allow/deny, reason code non sensibile, policy version, permission epoch e obligations (campi/sezioni ammesse, scadenza). Un client non può scegliere action più debole o parent alternativo per un handler più privilegiato.

Gli handler derivano action dal codice; il DPP carica parent dal proprio binding immutabile validato e non dal nuovo payload. La chiamata all'autorità usa TLS e credenziale dedicata con audience/scopo; inviare solo `subject=Alice` da un servizio non dimostra che Alice abbia autorizzato l'operazione. Servono prova utente verificabile o assertion delegata limitata all'operazione.

## Disponibilità e revoca

- Prima versione: decisioni online senza cache positiva per scritture. Timeout/risposta non valida → deny/retry-safe, non fallback alla vecchia API libera.
- Letture pubbliche: possono continuare su snapshot pubblicato, dopo rimozione dei dati privati. Le private falliscono chiuse; non usare cache public.
- Revoca: incrementare epoch e registrare audit; invalidare sessioni/grant locali derivati. La prossima decisione dopo commit della revoca ne vede l'effetto. **Un controllo online non rende atomici due database**: operazioni già autorizzate in volo vanno governate come descritto nell'[architettura proposta](09-proposed-architecture.md).
- Le invalidazioni push sono un'accelerazione, non la sola garanzia. Per alta disponibilità futura: più repliche del modulo decisionale con DB autorevole; non copie liberamente modificabili delle ACL in MongoDB.

## Credenziali tecniche compromesse

Un servizio DPP deve poter chiedere decisioni ed eseguire solo il proprio dominio; non creare grant globali o firmare per ogni utente. Un account worker commercio può emettere passport da eventi fulfillment validati, non trasferire ownership di tutte le risorse. DB users distinti e ingress interni riducono il blast radius, ma non sostituiscono i PEP. Una compromissione con accesso diretto al DB DPP resta grave: audit esterno, backup e controlli integrità servono anche dopo authz.
