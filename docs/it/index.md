> **Edizione italiana.** [English version](../en/index.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# Interfacer · Revisione architetturale e sicurezza

**Analisi del codice, non attestazione del deployment. Decisioni proposte, non approvate.**

Questa indagine nasce per rendere Interfacer utilizzabile da più persone, organizzazioni e futuri venditori senza confondere una firma valida con il diritto di modificare un oggetto.

## Cosa è stato analizzato

Sei repository locali, sei componenti applicativi aggiuntivi recuperati dall'organizzazione GitHub e il sito documentale esistente. Ricostruzione di GraphQL, REST, Keypairoom/Zenroom, ValueFlows, DPP, feedback, inbox, wallet, fabaccess e preview commerce. [Versioni e profondità della copertura](appendix/repository-map.md).

## I problemi confermati nel sorgente

1. **Identità non utilizzata nel dominio Zenflows:** i percorsi CRUD analizzati ignorano il richiedente autenticato.
2. **Controlli economici non equivalenti a permessi:** gli eventi confrontano il `provider` fornito dal client con responsabilità/custodia della risorsa.
3. **DPP con enforcement incompleto:** diverse scritture non verificano il chiamante; creazione e allegati non verificano il diritto sul prodotto.
4. **Identità incoerente tra servizi:** il feedback usa un identificatore dichiarato separatamente dalla chiave verificata; il proxy non corregge questa separazione.
5. **Lettura pubblica non separata dai dati riservati:** risorse con relazioni annidate, DPP in bozza e file richiedono una policy esplicita prima di introdurre dati privati.

I percorsi, le condizioni e i limiti sono nel [registro dei rilievi](04-authorization-audit.md). Le questioni operative particolarmente sensibili sono in un rapporto locale separato, non incluso nel sito. Nessuna credenziale è riprodotta.

## Direzione proposta

Un modulo di autorizzazione **dentro Zenflows**, con dati autorevoli in PostgreSQL; enforcement nel dominio e in ogni servizio. DPP conserva dati e regole documentali, ma consulta l'autorità per i diritti sulla risorsa. Contratto condiviso e client sottili, non un nuovo microservizio obbligatorio. Permessi commerciali separati da quelli collaborativi.

## Decisioni richieste

- Chi può amministrare una risorsa e con quali prove si migrano i record storici?
- Quali diritti si ereditano da organizzazione/progetto?
- Quale consistenza serve per revoca e scritture cross-service?
- Quali sezioni DPP sono pubbliche, modificabili o append-only?
- Chi è il venditore legale, distinto da autore, collaboratore e custode?

## Percorsi di lettura

| Destinatario | Percorso |
|---|---|
| Maintainer e tech lead | [Sintesi](01-executive-summary.md) → [Roadmap](12-migration-roadmap.md) → [Discussione](17-team-discussion.md) |
| Backend | [Architettura attuale](02-current-architecture.md) → [Audit](04-authorization-audit.md) → [Modello permessi](08-permission-model.md) |
| Frontend e SDK | [Autenticazione](03-authentication-analysis.md) → [DPP](06-dpp-analysis.md) → [Medusa](10-medusa-implications.md) |
| DevOps e security | [Trust cross-service](07-cross-service-authorization.md) → [Threat model](11-threat-model.md) → [Test](13-testing-strategy.md) |
| Revisori delle proposte | [Alternative](15-alternative-solutions.md) → [ADR PROPOSED](16-decision-records.md) → [Questioni aperte](14-open-questions.md) |

[Metodo, limiti e validazione](appendix/validation.md) · [Riferimenti al codice](appendix/code-references.md) · [Glossario](appendix/glossary.md)
