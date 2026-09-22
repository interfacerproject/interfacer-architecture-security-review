> **Edizione italiana.** [English version](../en/17-team-discussion.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 17 · Discussione tecnica con il team

## Obiettivo della riunione

Non ottenere adesione a una soluzione predefinita, ma concordare **quali garanzie offrire, chi possiede i dati autorevoli e quale rischio contenere per primo**. Leggere prima sintesi, F01–F05 e il rapporto riservato in canale controllato.

## Agenda proposta · 90 minuti

| Minuti | Tema | Esito richiesto |
|---|---|---|
| 0–15 | Commit realmente deployed, ingress e consumer | Correzioni alla mappa, owner DevOps |
| 15–30 | Tracce risorsa/evento/DPP/feedback | Accordo sui fatti e condizioni, non sulle preferenze |
| 30–45 | Controller, membership, storico ambiguo | Regola provvisoria e responsabile migrazione |
| 45–60 | Autorità/PEP/revoca/guasti | Scegliere trade-off Q01/Q06/Q11/Q12 |
| 60–75 | DPP sezioni e Medusa seller | Confini tra edit, repair, publish, sell |
| 75–90 | Milestone e test | Primo scope, acceptance gate e coordinamento release |

## Casi da discutere concretamente

**Fablab e macchina:** Alice crea una macchina per un fablab, Bob la custodisce, Carla deve usarla. Chi può correggere specifiche, autorizzare un comando ON, trasferire custodia e vendere un kit derivato? Non usare un unico campo «owner» per quattro domande.

**Design aperto e seller indipendente:** Bob contribuisce al design Alice, poi vende un prodotto costruito legalmente. Può creare il proprio listing, ma non modificare payout o DPP manufacturer di Alice. Quali claim sul produttore può fare?

**Riparazione:** un operatore esterno appende un repair event a un esemplare. Deve vedere il recapito del customer? Può ritirare un certificato? Come rettifica un proprio evento errato senza riscrivere la storia?

**Revoca simultanea:** Alice revoca Bob mentre DPP sta completando una modifica già autorizzata. La UI dice «revocato» al commit del grant o dopo drain? Quanto downtime accettiamo se Zenflows è indisponibile?

**Storico ambiguo:** primaryAccountable è una persona creata da import/email, il custode è un'altra e il contributor rivendica controllo. Chi decide e quali dati restano editabili durante la disputa?

## Ruoli da coinvolgere

Maintainer Zenflows (modello e transazioni), DPP (workflow/documenti/storage), GUI/SDK (compatibilità e onboarding), DevOps (deployment/secrets/HA), responsabile prodotto/legale (privacy, seller, certificazione), QA/security (negativi e fault injection). Assegnare persone reali durante la riunione, non presumere disponibilità.

## Decision log da produrre dopo la discussione

Per ogni ADR: esito accepted/rejected/deferred, motivazione, alternative considerate, owner, scadenza revisione, evidenze aggiuntive e test di accettazione. Questo documento non aggiorna automaticamente gli ADR a ACCEPTED. Pianificare il lavoro nel tracker dei repository scelti dal team; questa roadmap non crea issue né modifica i repository applicativi.

## Obiezioni ragionevoli e risposte provvisorie

- «Un servizio authz esterno è più pulito»: può esserlo; dimostrare dati, consistency e costi operativi prima di imporlo.
- «Tutto è pubblico»: pubblico non autorizza scrittura e non include automaticamente email, bozze o ordini.
- «La firma è sufficiente»: prova la chiave, non il diritto sull'oggetto; confrontare F02/F04.
- «Basta primaryAccountable»: non copre delega, org, repair, seller e import storico.
- «Bloccare DPP interrompe il lavoro»: mantenere lettura e un canale controllato; non chiamare remediation il solo nascondere l'editor.
- «Revoca immediata è scontata»: tra DB diversi serve una definizione precisa e un test di concorrenza.

## Informazioni da richiedere senza segreti

Digest immagini/commit, topologia ingress e firewall, inventario delle variabili **per nome e consumer**, volumi/latency/SLO, esempi sintetici dei record storici, policy attuale di pubblicazione, flussi organizzativi, pianificazione Medusa/PSP, significato dei punti wallet e servizi fisici attivi. Nessuno deve incollare credenziali, seed o dump di produzione in chat/issue.
