> **Edizione italiana.** [English version](../../en/appendix/validation.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# Metodo, validazione e limiti

## Metodo

Inventario locale read-only; acquisizione di repository pubblici mancanti; commit e gitlink registrati; tracing frontend/SDK→middleware→resolver→dominio→persistenza; inventario statico completo dei root field importati; lettura di router/handler DPP, proxy, feedback e servizi connessi. I rilievi distinguono comportamento confermato, rischio, limite, ipotesi da verificare e proposte.

Le configurazioni potenzialmente sensibili sono state ispezionate con output sanitizzato per posizione/nome, mai stampando valori. I dettagli operativi più sensibili sono nel rapporto locale privato esterno al sito. Nessun exploit, push, modifica remote, database o deploy applicativo è stato eseguito.

## Test applicativi eseguiti

| Verifica | Risultato | Limite |
|---|---|---|
| SDK `vitest run src/__tests__/unit.test.ts` | 31/31 pass, Vitest 2.1.9 | Storage/tagging/types; non authz backend |
| Espressione temporale Elixir per email token | Predicato attuale accetta timestamp sintetico vecchio; quello atteso lo nega | Solo espressione, non token reale/end-to-end |
| Inventario schema sorgente | 81 mutation e 62 query root | Estrazione statica, non introspezione runtime |

Il confronto temporale è stato eseguito con clock fisso, emissione dieci giorni prima e expiry quattro giorni, senza avviare Zenflows. [F11](../04-authorization-audit.md#f11-predicato-di-scadenza-email-invertito-confermato-p1).

## Validazione documentale

La root include strumenti ripetibili: `scripts/validate_docs.py` controlla link locali, fence, macro non risolte e confini del sito; con `--sources` verifica file e range contro commit Git, con `--site` verifica link/asset/anchor nell'HTML. `scripts/browser_check.mjs` verifica il build via HTTP sotto `/review/`, Mermaid, ricerca e viewport mobile senza rete esterna.

### Esiti locali · 22 settembre 2026

| Comando / controllo | Esito osservato |
|---|---|
| `python scripts/validate_docs.py --sources` | 55 pagine Markdown (27 per lingua + selettore); 450 link commit-pinned univoci con file/range verificati; zero errori |
| `mkdocs build --strict` | Build riuscito, nessun warning bloccante |
| `python scripts/validate_docs.py --site` | 56 HTML (55 documenti + 404), link/asset/anchor locali validi |
| `node scripts/browser_check.mjs` | 55 pagine visitate sotto `/review/`; 16 diagrammi Mermaid renderizzati; ricerca locale con risultati |
| Browser mobile | Viewport 390 px, contenuto 390 px, menu laterale funzionante |
| Rete del sito durante smoke test | Zero richieste esterne; Mermaid e ricerca funzionano con blocco egress |
| Stato Git dei 13 repository acquisiti | Uguale allo snapshot iniziale; nessuna modifica applicativa introdotta |

La verifica browser usa Chromium Playwright locale, non l'applicazione Interfacer. Il template 404 autonomo evita riferimenti root-absolute del tema quando non è ancora definito il repository subpath. Python locale 3.14; workflow predisposto con 3.12, compatibile con i requisiti Python dichiarati dalle dipendenze installate. Il workflow GitHub Actions non è stato eseguito né il sito pubblicato da questa sessione.

## Non eseguito

- Nessuna mutazione/API test su produzione o staging condiviso; nessuna scansione dell'applicazione pubblica.
- Suite SDK real-backend e Playwright GUI non eseguite: possono contattare servizi configurati.
- ExUnit Zenflows non eseguito con DB/Restroom; SQL Sandbox da sola non assicura un ambiente separato.
- Test Go DPP/feedback/inbox/wallet non eseguiti: toolchain Go non disponibile nel PATH e nessun backend effimero allestito.
- Nessun audit crittografico interno Zenroom, CVE audit completo o penetration test infrastrutturale.
- Nessun test Medusa: backend non implementato nel perimetro; la preview è mock.

## Limiti di riproducibilità

Il parent locale non è un repository Git. Commit dei singoli repository e dirty state iniziale sono nel manifest. La modifica GUI preesistente è preservata e non usata come codice commit-pinned. Checkout SDK locale e release GUI installata differiscono nelle versioni dichiarate; il mapping artifact→commit è da stabilire.

Le URL di codice sono commit-pinned; non è stato richiesto a GitHub di validare ogni link esterno individualmente. La validazione locale controlla gli stessi oggetti Git. Template compose e env non attestano deployment live. Le relazioni di rete disegnate sono implementate/configurabili, non una scansione dei servizi attivi.

La revisione approfondisce i percorsi prioritari, non tutte le possibili combinazioni dati o ogni repository dell'organizzazione. [Copertura per repository](repository-map.md), [matrice API](endpoint-matrix.md), [specifiche dei test da implementare](../13-testing-strategy.md).
