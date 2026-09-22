> **Edizione italiana.** [English version](../en/01-executive-summary.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 01 · Sintesi esecutiva

## Conclusione

La premessa è **confermata per percorsi concreti**, ma va precisata: Zenflows non è privo di controlli. Verifica firme, distingue alcune operazioni amministrative e valida invarianti ValueFlows. Manca il collegamento sistematico tra **persona autenticata, azione richiesta e oggetti coinvolti**. Inoltre DPP e feedback non condividono una nozione affidabile di principal e permesso.

Questo è un problema di modello e di enforcement, non risolvibile nascondendo pulsanti nella GUI o aggiungendo solo un controllo a `updateEconomicResource`.

## Cinque risultati prioritari

| ID | Risultato confermato | Conseguenza | Priorità tecnica |
|---|---|---|---|
| F01 | `req_user` creato dal middleware non usato nei CRUD risorsa, organizzazione e altri resolver | Firma valida di un'altra persona non impedisce modifiche per ID, se i vincoli dati sono soddisfatti | P0 |
| F02 | Eventi controllano provider/custodia/responsabilità dichiarati, senza legarli al firmatario | Le mutazioni indirette possono aggirare una futura protezione del solo CRUD | P0 |
| F03 | Router DPP senza middleware auth generale; più handler di scrittura senza auth | Integrità e pubblicazione del passaporto non sono subordinate ai diritti Zenflows | P0 |
| F04 | Feedback verifica la chiave ma prende il principal da `x-user-id` | Un controllo SQL di ownership può essere corretto ma basato su identità non autenticata | P0 |
| F05 | DPP GET/list non filtrano per policy; risorse guest espongono relazioni annidate | Bozza non significa privato; nuove informazioni riservate non possono essere aggiunte in sicurezza | P1 |

[Dettagli, evidenze, condizioni e incertezza per ciascun rilievo](04-authorization-audit.md). P0 indica urgenza di triage, **non un punteggio CVSS né prova di sfruttamento live**. Esposizione di rete, configurazione e dati reali non sono stati verificati contro produzione.

## Primo milestone raccomandato: confine minimo verificabile

Timebox indicativo: **1–2 sprint**, da stimare con i maintainer. Due backend developer più supporto frontend/DevOps e revisione security, non una promessa di calendario.

- Triage privato di credenziali/configurazioni e superfici amministrative.
- Chiudere temporaneamente le scritture DPP non protette finché non esiste enforcement server-side, anche sull'origine diretta.
- Definire principal verificato e prima policy `resource.update`, con fixture Alice/Bob; inventariare **anche eventi e scritture interne** prima di dichiarare protetta una risorsa.
- Risolvere binding chiave→persona nel feedback; non fidarsi di header di identità forniti dal client.
- Approvare una regola conservativa per record senza amministratore certo: revisione manuale, non assegnazione automatica.

**Accettazione:** nessun percorso noto di scrittura DPP rimane aperto senza un gate verificabile; un test API negativo e uno di dominio per Alice/Bob sono riproducibili in ambiente isolato; inventario versionato e owner tecnico assegnato. Questo milestone è contenimento, non completamento del sistema permessi.

## Cosa mantenere

Preservare ValueFlows, PostgreSQL/Ecto, firme esistenti durante la migrazione, API e GUI dove possibile. Aggiungere un contesto esplicito di esecuzione e un modulo policy, non riscrivere tutti i servizi. Il modello economico resta distinto dal controllo amministrativo.

## Cosa non decidere implicitamente

`primaryAccountable` non è un ACL, `custodian` non è un amministratore, un contributo non è una delega, un DID risolvibile non è un'autorizzazione, una risorsa open hardware non è automaticamente vendibile da ogni editor. [Domande decisionali](14-open-questions.md).

## Limiti essenziali

Revisione statica e test unitari locali sicuri; nessun test di mutazione su sistemi remoti. Medusa non è un backend implementato nei repository analizzati. Non si certifica la sicurezza di dipendenze crittografiche, DID controller o servizi federati esterni. La GUI dipende da SDK 0.6.1 installato, mentre il checkout SDK dichiara 0.1.0: il percorso concettuale è verificato, l'equivalenza binaria va attestata in release.
