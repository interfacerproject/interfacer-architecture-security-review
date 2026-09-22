> **Edizione italiana.** [English version](../../en/appendix/repository-map.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# Mappa dei repository e riproducibilità

Data di acquisizione (UTC): `2026-09-21T15:30:50.340931+00:00`. Il parent locale non è un repository Git; il sito è un deliverable autonomo. Nessun remote modificato o push effettuato.

## Snapshot analizzati

| Repository | Commit | Copertura | Stack / note |
|---|---|---|---|
| [interfacer-client](https://github.com/interfacerproject/interfacer-client) | [`dfb1baabf16516a845957d5587ccb933c1874221`](https://github.com/interfacerproject/interfacer-client/tree/dfb1baabf16516a845957d5587ccb933c1874221) | Locale; auth/crypto/GraphQL/resources/DPP e unit test | SDK TypeScript; package locale dichiara 0.1.0, non equivalenza automatica con release GUI |
| [interfacer-docs](https://github.com/interfacerproject/interfacer-docs) | [`da1e1e840f738c5362ae2e7028df9481903590ae`](https://github.com/interfacerproject/interfacer-docs/tree/da1e1e840f738c5362ae2e7028df9481903590ae) | Clone aggiuntivo; verifica sito preesistente | Docsify in docs/index.html, non modificato |
| [interfacer-dpp](https://github.com/interfacerproject/interfacer-dpp) | [`5f6ae20380ae80716ac6a8742b69bdc82e141296`](https://github.com/interfacerproject/interfacer-dpp/tree/5f6ae20380ae80716ac6a8742b69bdc82e141296) | Locale; router, tutti gli handler, auth, modello e storage | Go/Gin, MongoDB/MinIO, Zenroom eseguibile |
| [interfacer-feedback-service](https://github.com/interfacerproject/interfacer-feedback-service) | [`d905a82a02d4115b13c87557591b7ddca6eb39b1`](https://github.com/interfacerproject/interfacer-feedback-service/tree/d905a82a02d4115b13c87557591b7ddca6eb39b1) | Locale; router/auth/handler/persistenza | Go/Gin, SQLite, publisher log |
| [interfacer-gui](https://github.com/interfacerproject/interfacer-gui) | [`9afe601d4d28dd6ccc0b4db2092da65f8055823e`](https://github.com/interfacerproject/interfacer-gui/tree/9afe601d4d28dd6ccc0b4db2092da65f8055823e) | Locale; approfondita sui flussi auth/DPP/commerce/API | Next.js 12/React; SDK installato 0.6.1; modifica locale hook esclusa dalle evidenze commit-pinned |
| [interfacer-proxy](https://github.com/interfacerproject/interfacer-proxy) | [`10d07344e2bcf7e3673f906e51aeb52cd6abf0cb`](https://github.com/interfacerproject/interfacer-proxy/tree/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb) | Locale; router/forwarding/config approfonditi | Go net/http, nessun DB |
| [zenflows](https://github.com/interfacerproject/zenflows) | [`893489d81fddf07e470094e72863958de402cca7`](https://github.com/interfacerproject/zenflows/tree/893489d81fddf07e470094e72863958de402cca7) | Locale; inventario root completo e domini rappresentativi approfonditi | Elixir, Absinthe, Ecto/PostgreSQL; authn e ValueFlows |
| [zenflows-bank](https://github.com/interfacerproject/zenflows-bank) | [`e5c2d2e6bd1ad072d1575de0a2be983854429b35`](https://github.com/interfacerproject/zenflows-bank/tree/e5c2d2e6bd1ad072d1575de0a2be983854429b35) | Clone aggiuntivo; CLI/airdrop e relazioni dati | Copertura mirata, non audit completo smart contract/RPC |
| [zenflows-crypto](https://github.com/interfacerproject/zenflows-crypto) | [`0ffcce9b90799c9cb61f11fc594aeb513a01326f`](https://github.com/interfacerproject/zenflows-crypto/tree/0ffcce9b90799c9cb61f11fc594aeb513a01326f) | Clone aggiuntivo; contratti firma/verify e integrazione | Non audit matematico della libreria Zenroom |
| [zenflows-fabaccess](https://github.com/interfacerproject/zenflows-fabaccess) | [`8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc`](https://github.com/interfacerproject/zenflows-fabaccess/tree/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc) | Clone aggiuntivo; main/API e controlli | FastAPI/pyfabapi; server Fabaccess esterno non auditato |
| [zenflows-inbox](https://github.com/interfacerproject/zenflows-inbox) | [`963ae1d38116fb17ed35d6524ca7cfb8f16c0efd`](https://github.com/interfacerproject/zenflows-inbox/tree/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd) | Clone aggiuntivo; auth, messaggi/social/router/storage | Go/Gin e Tarantool; diverse superfici auth |
| [zenflows-osh](https://github.com/interfacerproject/zenflows-osh) | [`56855d426ffd884d91dd72373a2292f1ae5695ed`](https://github.com/interfacerproject/zenflows-osh/tree/56855d426ffd884d91dd72373a2292f1ae5695ed) | Clone aggiuntivo; router e clone/analisi | Git/osh CLI e filesystem temporaneo |
| [zenflows-wallet](https://github.com/interfacerproject/zenflows-wallet) | [`f5cf1668afe371329ed827d0bb56557e0bedcda6`](https://github.com/interfacerproject/zenflows-wallet/tree/f5cf1668afe371329ed827d0bb56557e0bedcda6) | Clone aggiuntivo; handler DID/auth e token | Go/Gin e Tarantool; non PSP |

## Working tree e SDK

La GUI aveva già `hooks/useProjectCRUD.ts` modificato e file non tracciati (skill locale e immagine). Non sono stati cambiati, archiviati nel sito o usati come evidenza pubblica. Per l'hook si è letto `git show HEAD:hooks/useProjectCRUD.ts`; per gli altri riferimenti si usa il commit manifest. I checkout applicativi restano invariati salvo eventuale cache del test runner.

GUI `package.json` richiede `@dyne/interfacer-client ^0.6.1` e l'installazione locale è 0.6.1; checkout separato dichiara 0.1.0. Sono analizzati come snapshot distinti: la catena delle responsabilità è verificata ma la corrispondenza source/dist della release installata non è certificata. La fase 1 deve associare artifact effettivi a commit.

## Submodule fissati dai repository

Non confondere HEAD del clone crypto con ogni submodule storico. Di seguito i gitlink registrati, indipendentemente dall'inizializzazione locale. Non sono stati inizializzati tutti i submodule/test framework. Per DPP il gitlink crypto corrisponde al clone analizzato.

| Repository | Path submodule | Commit registrato |
|---|---|---|
| interfacer-docs | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| interfacer-dpp | `internal/auth/zenflows-crypto` | `0ffcce9b90799c9cb61f11fc594aeb513a01326f` |
| interfacer-feedback-service | `internal/auth/zenflows-crypto` | `0ffcce9b90799c9cb61f11fc594aeb513a01326f` |
| interfacer-gui | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| interfacer-gui | `components/interfacer-dpp` | `76b17cc479a0fba9c014d624bc3ad14823c1ac78` |
| interfacer-gui | `zenflows-crypto` | `53dbe70a61cb016fb196b9f9d4687cd3d26febcb` |
| interfacer-proxy | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| zenflows | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| zenflows | `zencode` | `53dbe70a61cb016fb196b9f9d4687cd3d26febcb` |
| zenflows-crypto | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| zenflows-crypto | `test/bats` | `e222fc64047493adcb3151e60c13bb19b350b97b` |
| zenflows-crypto | `test/test_helper/bats-assert` | `ffe84ea5dd43b568851549b3e241db150c12929c` |
| zenflows-crypto | `test/test_helper/bats-file` | `c7df56ce2ffbd08d3e85c9d91f67981b7f317bf8` |
| zenflows-crypto | `test/test_helper/bats-support` | `3c8fadc5097c9acfc96d836dced2bb598e48b009` |
| zenflows-fabaccess | `pyfabapi` | `2383a6cc0dd3c49a677e05e5cedd6854d89f4237` |
| zenflows-fabaccess | `zenflows-crypto` | `49c4f42c667d53101efaec52617b19b0abc96089` |
| zenflows-inbox | `zenflows-crypto` | `b28ddcf14532aa8950d95af63c0e2b2cf2cd8b34` |
| zenflows-osh | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| zenflows-wallet | `.reuse` | `2f4dc7dca0e04bf8f9eb8e6feb49ff6bcde9f795` |
| zenflows-wallet | `zenflows-crypto` | `6b780619fbbb6fc5d148016dcc05968db67b1a20` |

## Discovery aggiuntiva

Elenco pubblico dell'organizzazione ottenuto via GitHub API, senza scritture remote. La presenza di un repo non prova il suo uso nel deployment. Oltre ai componenti analizzati sono stati scoperti i seguenti repository, **non sottoposti a code audit in questa revisione**:

- [zenswarm-storage](https://github.com/interfacerproject/zenswarm-storage): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [planetmint-interfacer](https://github.com/interfacerproject/planetmint-interfacer): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [loshifacer](https://github.com/interfacerproject/loshifacer): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [Node-RED_Interfacer](https://github.com/interfacerproject/Node-RED_Interfacer): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [Interfacer-notebook](https://github.com/interfacerproject/Interfacer-notebook): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [.github](https://github.com/interfacerproject/.github): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [workflows](https://github.com/interfacerproject/workflows): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [Interfacer_DPP-visualisations](https://github.com/interfacerproject/Interfacer_DPP-visualisations): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [README](https://github.com/interfacerproject/README): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [reuse](https://github.com/interfacerproject/reuse): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [EconSim](https://github.com/interfacerproject/EconSim): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [DTECH_HSU_2025_OPS](https://github.com/interfacerproject/DTECH_HSU_2025_OPS): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [dtech-example-data-injection](https://github.com/interfacerproject/dtech-example-data-injection): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [interfacer-client-sdk-docs](https://github.com/interfacerproject/interfacer-client-sdk-docs): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.
- [interfacer-3d-demo-models](https://github.com/interfacerproject/interfacer-3d-demo-models): da classificare con maintainer; nessuna garanzia di sicurezza o integrazione dedotta dal nome.

## Documentazione/deployment esistenti

`interfacer-docs/docs/index.html` contiene Docsify e file sidebar/.nojekyll. GUI ha workflow di publish/test-deploy; gli altri componenti hanno workflow immagini, non sostituiti. Il sito di questa revisione non assume un dominio o un repository Pages già assegnato: [istruzioni locali](publication.md). Non modificati i siti esistenti.

## Limiti della copertura

Non analizzati integralmente DID controller/Restroom runtime, Zenroom internals, LOSH/planetmint/Node-RED, infrastruttura reale, smart contract, Fabaccess server o servizi federati. Medusa è un requisito futuro. Non enumerati endpoint di applicazioni non clonate né infrastrutture che non compaiono nel sorgente. L'inventario è completo per i root GraphQL importati e le rotte dei servizi esplicitamente elencate, non una certificazione dell'intera organizzazione GitHub.
