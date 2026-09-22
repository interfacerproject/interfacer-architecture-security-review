> **Edizione italiana.** [English version](../en/15-alternative-solutions.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 15 · Alternative e criteri di scelta

Il confronto A–F completo è in [autorizzazione cross-service](07-cross-service-authorization.md). Qui si esplicitano le scelte reversibili e i motivi per non introdurre complessità prematura.

## Soluzione minima: owner check in ogni handler

**Pro:** rapida per un singolo oggetto; poco deployment. **Contro nel codice reale:** primaryAccountable non è principal; organizzazioni/deleghe mancanti; eventi modificano indirettamente la risorsa; DPP/feedback hanno identità diverse. **Uso ragionevole:** gate temporaneo per record con controller verificato, mai soluzione finale né backfill indiscriminato. Evidenze F01–F04.

## Gateway come unico enforcement

**Pro:** un ingresso da proteggere; rate limiting e identity normalization uniformi. **Contro:** il proxy attuale non conosce semanticamente mutation, oggetti e side effects; origine diretta e dominio interno lo bypassano. Anche un gateway evoluto non conosce lo stato transazionale Ecto/Mongo. **Scelta:** gateway per TLS/limiti, PEP nel servizio e dominio. [interfacer-proxy/main.go:67–143](https://github.com/interfacerproject/interfacer-proxy/blob/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb/main.go#L67-L143); [zenflows/src/zenflows/vf/economic_event/resolv.ex:38–49](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/resolv.ex#L38-L49).

## Zenflows modulare prima di un authz service

**Pro:** resource e permissions nella stessa transazione; deployment già gestito; integra le chiamate dominio Elixir. **Contro:** DPP dipende dalla sua disponibilità e il team Zenflows diventa owner del contratto. **Trigger per estrazione futura:** più authority federate, release policy indipendenti, carico misurato, team operativo dedicato o scalabilità incompatibile col servizio principale. Estrarre senza questi trigger crea un problema distribuito prima di risolvere quello applicativo.

## Motore esterno

- **OPA/Rego:** buono per regole attributive e distribution bundle; bisogna ancora gestire dati membership, freshness e PEP. Logica JSON non sostituisce transazioni.
- **Cedar:** modello tipizzato di entity/action/context utile per revisioni; richiede adapter e alimentazione dati corretta.
- **OpenFGA/SpiceDB:** indicati per ReBAC complesse e tuple; aggiungono servizio/storage e semantica consistency da padroneggiare.

Non si è integrato né benchmarkato alcun motore. Se il grafo resta org→project→resource con ruoli contenuti, normali tabelle e modulo policy testato sono più facili da gestire. Policy engine non corregge un `x-user-id` spoofabile o una mutation che non invoca il PEP.

## Database RLS

PostgreSQL RLS può difendere contro alcuni errori di query Zenflows, ma richiede propagazione contesto per connessione/pool, gestione job, funzioni privilegiate, transazioni e copertura relazioni. MongoDB/MinIO non ricevono magicamente quella policy. **Proposta:** seconda linea di difesa dopo un modello applicativo corretto, non sostituto di autorizzazione multi-oggetto e side effects.

## JWT/sessioni vs firma a ogni richiesta

Firme attuali mantengono compatibilità ma aumentano gestione chiavi browser e replay context. Sessioni BFF riducono esposizione di long-lived private keys al frontend durante l'uso ordinario, ma introducono session store, CSRF, cookie e federazione. JWT brevi rendono il trasporto semplice, ma richiedono revoca/audience e proof/delega affidabili. **Proposta:** prima correggere authorization e binding, poi migrare authn con compatibilità versionata; non tentare entrambe le riscritture in un solo sprint.

## Quando cambiare raccomandazione

Se i maintainer richiedono DPP offline con edit autorizzato, consentire capability molto ristrette e chiarire revoca differita; non promettere revoca immediata. Se la federazione richiede più authority, introdurre namespace issuer, trust agreement e mapping dei ruoli, senza accettare grants remoti equivalenti a platform admin. Se il carico online diventa proibitivo, misurare cache scoped/versionata con staleness budget prima di duplicare tutto il permission store.
