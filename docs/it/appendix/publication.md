> **Edizione italiana.** [English version](../../en/appendix/publication.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# Anteprima e pubblicazione

Il deliverable è un sito **MkDocs + Material**, autonomo rispetto ai repository applicativi. Il sito Docsify preesistente non è stato toccato. I comandi seguenti si eseguono dalla root `architecture-review/`; il README della root contiene le istruzioni complete.

## Ambiente locale

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python scripts/validate_docs.py
mkdocs serve -a 127.0.0.1:8008
```

Aprire `http://127.0.0.1:8008/`. Per il build statico:

```bash
mkdocs build --strict
python scripts/validate_docs.py --site
```

Output in `site/`. La documentazione usa link relativi e Mermaid vendorizzato con licenza; non è configurato un dominio o `site_url` di produzione. La ricerca è locale al sito e indicizza solo `docs/`.

## GitHub Pages

La destinazione standalone è [`interfacerproject/interfacer-architecture-security-review`](https://github.com/interfacerproject/interfacer-architecture-security-review). Il repository può restare privato durante la revisione dell’ambito di disclosure; creazione e push del repository **non** eseguono il deploy del sito. Ambienti virtuali, cache, build generati e rapporti riservati sono esclusi.

Dopo approvazione, abilitare **Settings → Pages → GitHub Actions** ed eseguire manualmente **Interfacer documentation · GitHub Pages**. Non è presente un trigger push automatico. Il workflow `.github/workflows/pages.yml` installa le dipendenze bloccate, valida Markdown e HTML, costruisce in modalità strict, esegue i controlli browser e carica solo `site/` tramite `upload-pages-artifact`/`deploy-pages`. Il deploy usa l’environment `github-pages`, eventualmente protetto da reviewer.

Non pubblicare il workspace parent: contiene checkout applicativi e materiale riservato che non fanno parte di questo repository.

## Riservatezza

Il rapporto operativo sensibile è deliberatamente esterno alla directory del sito. Non basta escludere una pagina dalla sidebar: MkDocs può comunque copiarla e indicizzarla. Non copiarlo in `docs/`, nel repository pubblico o negli artifact. Il livello di visibilità Pages può differire da quello del repository: verificarlo prima della pubblicazione.

## Validazioni facoltative

```bash
# Richiede i checkout Git al layout registrato nel manifest:
python scripts/inventory.py
python scripts/validate_docs.py --sources

# Richiede Node.js e Chromium Playwright:
npm ci
npx playwright install chromium
node scripts/browser_check.mjs
```

Il controllo browser serve il build sotto `/review/` per simulare un repository subpath, senza contattare le applicazioni Interfacer. [Esiti e limiti](validation.md).
