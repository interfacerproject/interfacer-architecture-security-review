> **Edizione italiana.** [English version](../en/12-migration-roadmap.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 12 · Roadmap incrementale

## Principi

Contenere prima, modellare poi; nessuna riscrittura obbligatoria. Fasi sovrapponibili dove indicato. Le stime vanno fatte dal team dopo disponibilità DevOps/QA; il primo milestone è 1–2 sprint indicativi, mentre l'intero programma dipende da dati storici e requisiti commerce. Ogni fase ha un referente backend e un reviewer cross-service; non lasciare l'autorizzazione come responsabilità implicita del frontend.

## Fase 0 · Contenimento e triage riservato

- **Obiettivo:** ridurre immediatamente le scritture senza controllo e i privilegi esposti.
- **Repository:** dpp, proxy/deployment, gui, client, feedback; wallet/fabaccess se attivi.
- **Dipendenze:** inventario degli ingress effettivi e owner operativo; nessuna migrazione ACL richiesta.
- **Modifiche/task:** blocco temporaneo delle scritture DPP non protette su ingress e origine; audit credenziali/browser e route amministrative; registration server-side ristretto; binding chiave/persona feedback; rate/body limits e logging senza segreti; verificare auth Zenflows abilitata.
- **Rischi:** interruzione editor DPP/signup, consumer admin non censiti. Comunicare maintenance mode selettivo.
- **Test:** accesso diretto e via proxy, assenza header e identità diversa; browser bundle inspection senza stampare valori; smoke signup su sandbox.
- **Deliverable:** contenimento documentato, inventario consumer/rotazioni, decisione sulle rotte disabilitate.
- **Accettazione:** nessuna scrittura nota DPP accessibile senza gate; nessuna credenziale amministrativa necessaria al nuovo browser; identità feedback risolta server-side o scritture disabilitate.
- **Rollback:** mantenere rotte bloccate/read-only, non ripristinare segreti revocati o allow anonimo; compatibilità signup via server.

## Fase 1 · Inventario operativo completo

- **Obiettivo:** associare la matrice sorgente al deployment reale.
- **Repository:** tutti gli applicativi, deployment e SDK.
- **Dipendenze:** fase 0; accesso autorizzato alla configurazione, non ai segreti in chiaro.
- **Task:** associare immagini/digest/commit; SDL/runtime routes offline o ambiente isolato; cercare job/import/CLI/script e client fuori GUI; classificare azioni e dati; estendere matrice con owner e test ID.
- **Rischi:** build SDK differente dal checkout, submodule non inizializzati, servizi legacy dimenticati.
- **Test:** coverage check statico root fields/routes e confronto staging isolato; inventory review con maintainer.
- **Deliverable:** baseline versionata di API e trust boundary effettivi.
- **Accettazione:** ogni write abilitata ha principal source, PEP pianificato e responsabile; nessun endpoint sconosciuto in runtime.
- **Rollback:** documentale; nessuna alterazione DB.

## Fase 2 · Modello e dati autorevoli

- **Obiettivo:** definire controller, membership, grants, deleghe e public projection.
- **Repository:** zenflows (migration additive), dpp (binding), gui/client per contratto.
- **Dipendenze:** decisioni Q1–Q5 e inventario.
- **Task:** schema permission separato da VF, API gestione inviti/grants, vincoli di delega, epoch/versioni, audit; backfill in dry-run con confidence e provenance; queue record disputed.
- **Rischi:** primaryAccountable storico non affidabile, conferimento permessi troppo ampio, default public non intenzionale.
- **Test:** migrazioni forward/backward su copia sintetica; grant cycles, self-escalation, inviti scaduti, membership revocata.
- **Deliverable:** schema additivo, ADR proposti approvati dal team se concordati, report dry-run e procedura contestazione.
- **Accettazione:** zero assegnazioni automatiche non giustificate; tutti i nuovi oggetti hanno controller verificato; record ambigui distinguibili.
- **Rollback:** preservare tabelle/audit nuovi; disabilitare nuove feature, non eliminare prove di controllo.

## Fase 3 · Enforcement Zenflows

- **Obiettivo:** nessuna write ordinaria senza ExecutionContext/policy.
- **Repository:** zenflows; SDK per errori e campi compatibili.
- **Dipendenze:** fase 2; contenimento resta attivo.
- **Task:** principal nel dominio e negli entrypoint interni, proteggere CRUD e cataloghi, createEconomicEvent/action e tutti gli effetti, relazioni e file, query private/annidate, import service-scoped; audit transazionale e idempotenza.
- **Rischi:** proteggere CRUD ma lasciare eventi; query guest che espongono sottocampi; job legacy con Repo diretto.
- **Test:** permission matrix, GraphQL alias/multiple root fields, domain calls, richieste firmate con provider di altro agent, concorrenza grant/update e regressione invarianti VF.
- **Deliverable:** enforcement per gruppi di operazioni, feature flags per scope; telemetria shadow solo dove non lascia aperta una write vulnerabile.
- **Accettazione:** ogni mutation inventariata abilitata ha test deny/allow; Alice/Bob non aggirabile tramite eventi o primitive interne pubbliche.
- **Rollback:** per scope in errore read-only, non auth-off globale; schema additivo resta compatibile.

## Fase 4 · DPP e coerenza cross-service

- **Obiettivo:** diritto risorsa e azioni passport coerenti.
- **Repository:** zenflows, dpp, feedback, proxy; poi inbox/wallet/fabaccess.
- **Dipendenze:** fasi 2–3 e contratto principal; API decisione disponibile prima dei consumer.
- **Task:** identity/assertion verificata, binding parent, PEP locale, allowlist campi, policy sezioni/stato, CAS, proiezioni e storage privati; autenticazione S2S; versioni, idempotenza, audit/outbox; protocollo revoca concordato.
- **Rischi:** outage authority; incompletezza permit/drain; DPP orfani; file già pubblici impossibili da «rendere segreti» retroattivamente.
- **Test:** diretto/proxy/SDK, parent substitution, grants revocati, timeout, cross-user/cross-org, replay allegati, crash tra Mongo e MinIO, cache e storage origin.
- **Deliverable:** DPP protetto end-to-end, dependency runbook, mapping migrazione e riconciliazione.
- **Accettazione:** ogni rotta DPP mutante o lettura privata richiede policy; impossibile aggirare tramite generic PUT/status/allegati; deny su authority down; nessun draft privato pubblicato in list/file/cache.
- **Rollback:** versione precedente può essere usata solo dietro blocco write; rollback non può aprire API legacy.

## Fase 5 · GUI e SDK

- **Obiettivo:** UX coerente senza diventare enforcement primario.
- **Repository:** gui, client, documentazione SDK.
- **Dipendenze:** contratti delle fasi 2–4; può iniziare in parallelo su mock contratti.
- **Task:** `capabilities`/`can` scoped per UI, gestione 401/403/409/503 e GraphQL error code, inviti/delega/revoca, acting_for esplicito; signing fail-closed sulle write; unificazione firma file; dist/package provenance.
- **Rischi:** nascondere azioni consentite o mostrare grant stale; perdite di draft al deny; storage legacy.
- **Test:** unit/mock contract + API, due tab con revoca, org switch, sessione scaduta, errore di rete non ritenta ciecamente.
- **Deliverable:** release compatibile, migration note, UI fonte del permesso e gestione read-only.
- **Accettazione:** nessuna credential admin browser; ogni deny backend reso chiaramente; API continua a negare senza GUI.
- **Rollback:** vecchia GUI tollerata solo se backend resta protetto; fallback UX read-only.

## Fase 6 · Prerequisiti Medusa

- **Obiettivo:** identità commerciale e separazione seller/collaboratore prima del denaro.
- **Repository:** zenflows, gui/client, futuro adapter commerce.
- **Dipendenze:** fasi 2–5; decisioni legal seller, single/multi-seller, autorità stock.
- **Task:** mapping principal/customer/seller, seller grants, privacy ordini, ruoli finance/payout, onboarding/step-up, offboarding, contratti webhook/outbox/DPP issuance; spike versione Medusa e multi-vendor.
- **Rischi:** confondere licenza con mandato; due stock master; seller ID editabile.
- **Test:** fixture due seller, ex membro, supporto senza accesso globale, autorizzazioni per ogni operazione admin.
- **Deliverable:** contratti, threat model commerce, proof-of-concept non monetario e ADR aggiornati.
- **Accettazione:** contributor non può vendere nello scope altrui; order/customer isolation verificata; nessun pagamento reale.
- **Rollback:** conservare preview mock e feature flag off.

## Fase 7 · Marketplace

- **Obiettivo:** integrare backend commerce senza ampliare privilegi collaborativi.
- **Repository:** futuro adapter/Medusa, gui/client, zenflows, dpp.
- **Dipendenze:** fase 6 e pilot con dataset limitato.
- **Task:** seller-scoped API, checkout server-authoritative, PSP verificato, idempotenza, stock reservations, fulfillment→VF/DPP, resi e riconciliazione.
- **Rischi:** doppi ordini/addebiti, leakage multi-seller, emissioni DPP errate.
- **Test:** sandbox PSP, webhook duplicati/fuori ordine, crash retry, stesso seriale, cross-seller SQL/API, importi manipolati.
- **Deliverable:** pilot commerce e runbook reconciliation/incident.
- **Accettazione:** audit dal pagamento al passport; no doppio effetto; approval business/security prima dell'attivazione.
- **Rollback:** fermare nuovi checkout, continuare gestione ordini esistenti/rimborsi in canale controllato; non cancellare ledger.

## Fase 8 · Hardening e rollout

- **Obiettivo:** rendere sostenibile il sistema protetto.
- **Repository:** tutti e infrastruttura.
- **Dipendenze:** enforcement e pilot; hardening di base comincia già in fase 0.
- **Task:** threat review indipendente, dependency scan, limiti GraphQL/query complexity, load/chaos, key rotation drill, restore backup, audit retention, dashboard revoca; canary e runbook break-glass.
- **Rischi:** cache introdotte per performance senza freshness; bypass emergenziale permanente.
- **Test:** carico realistico, autorità/DB indisponibili, permessi revocati in volo, restore con permission epoch coerenti.
- **Deliverable:** SLO, monitoraggio, procedure e criteri release security.
- **Accettazione:** nessuna regressione matrice, deadline/revoca misurate, recupero documentato e provato.
- **Rollback:** canary per tenant/azione e read-only selettivo, non downgrade globale della policy.

## Coordinamento e lavori indipendenti

Indipendenti: inventario, audit redaction, fixture/test matrix, adapter SDK su mock, proiezioni public read, sandbox OSH, revisione credenziali. Coordinati: registration→GUI→rotazione; schema permission→Zenflows enforcement; decision API→DPP/feedback; private file storage→URL/cache GUI; envelope v2→verificatori server/client; seller mapping→Medusa/worker.

Ordine expand/contract: aggiungere nuovi contratti, distribuire consumer, misurare assenza vecchi client, poi dismettere. Non mantenere «legacy allow» indefinito per scritture critiche.

## Record storici ambigui

Classificare ogni record: controller provato; candidato con prove da verificare; conteso; nessuna evidenza. Conservare creator/eventi/import/email/primaryAccountable/custodian come **indizi distinti**, mai intercambiabili. Per oggetti contesi/ignoti: edit amministrativi bloccati, lettura secondo policy approvata, claim con prove, verifica umana a due persone per trasferimenti di alto impatto, notifica e periodo contestazione; audit reversibile del grant, non riscrittura della storia economica. Nessuno può auto-assegnarsi il primo record reclamato. Anche organizzazioni e DPP `createdBy` misto richiedono migrazione di provenance.
