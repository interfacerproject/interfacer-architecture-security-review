# Interfacer · Architecture and security review

Bilingual, code-based review of the Interfacer ecosystem: authentication, authorization, ownership, Digital Product Passports, cross-service trust, marketplace implications, migration, tests and **PROPOSED** ADRs.

Revisione bilingue e basata sul codice dell’ecosistema Interfacer: autenticazione, autorizzazione, ownership, Digital Product Passport, trust cross-service, implicazioni marketplace, migrazione, test e ADR **PROPOSED**.

- [Documentation home · Homepage](docs/index.md)
- [English edition](docs/en/index.md)
- [Edizione italiana](docs/it/index.md)
- [Analyzed repositories and commits](docs/en/appendix/repository-map.md)
- [Repository e commit analizzati](docs/it/appendix/repository-map.md)

> [!WARNING]
> The private operational security report is intentionally outside this repository and must not be copied into GitHub Pages, CI logs or public artifacts. Source findings should be disclosed only after maintainer review.
>
> Il rapporto operativo di sicurezza riservato è intenzionalmente esterno a questo repository e non deve essere copiato in GitHub Pages, log CI o artifact pubblici. La disclosure dei rilievi sorgente richiede la revisione dei maintainer.

## Local preview · Anteprima locale

Requires Python 3.12+:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python scripts/validate_docs.py
mkdocs serve -a 127.0.0.1:8008
```

Open `http://127.0.0.1:8008/`. Build and validate the static artifact with:

```bash
mkdocs build --strict
python scripts/validate_docs.py --site
```

The generated `site/` directory is ignored. Links and assets are relative and have been tested under a repository subpath.

La directory generata `site/` è ignorata. Link e asset sono relativi e testati anche sotto il subpath di un repository.

## Reproducibility · Riproducibilità

`repositories.json` records commits and gitlinks; `discovery.json` records repository discovery; `inventory.json` contains the static API inventory. With source checkouts arranged as recorded in the manifest:

```bash
python scripts/inventory.py
python scripts/validate_docs.py --sources
```

These commands only read Git data. They do not access databases, environment files or application services. `--sources` validates source files and line ranges at the pinned commits; it does not replace semantic review.

I comandi leggono soltanto dati Git: non accedono a database, file environment o servizi applicativi. `--sources` valida file e intervalli ai commit fissati, ma non sostituisce la revisione semantica.

The Italian edition is the technical baseline. `scripts/translate_docs.py` can intentionally regenerate the English edition through a public translation endpoint; it is never run in CI, never processes private reports, preserves reviewed Mermaid blocks, and its output requires human review. The local translation cache is ignored.

L’edizione italiana è la baseline tecnica. `scripts/translate_docs.py` può rigenerare intenzionalmente l’edizione inglese tramite un endpoint di traduzione pubblico; non viene mai eseguito in CI, non tratta rapporti riservati, preserva i diagrammi Mermaid revisionati e richiede revisione umana. La cache locale è ignorata.

## Browser smoke test · Test browser

```bash
npm ci
npx playwright install chromium
npm run test:site
```

The test serves the build under `/review/`, blocks external requests, visits every page and checks Mermaid, search, responsive navigation and horizontal overflow.

Il test serve il build sotto `/review/`, blocca richieste esterne, visita ogni pagina e controlla Mermaid, ricerca, navigazione responsive e overflow orizzontale.

## GitHub Pages

The workflow `.github/workflows/pages.yml` is deliberately manual (`workflow_dispatch`). Before running it:

1. review disclosure scope;
2. configure **Settings → Pages → GitHub Actions**;
3. optionally protect the `github-pages` environment with reviewers;
4. manually run **Interfacer documentation · GitHub Pages**.

The build job has read-only repository access; only the deploy job receives `pages: write` and `id-token: write`. Only `site/` is uploaded. Depending on the GitHub plan and settings, Pages visibility can differ from repository visibility.

Il workflow è deliberatamente manuale. Prima dell’esecuzione, approvare l’ambito di disclosure, configurare Pages tramite GitHub Actions ed eventualmente proteggere l’environment `github-pages`. Solo `site/` viene pubblicato.

## Scope and limits · Ambito e limiti

This is primarily a static source review, not an attestation of the live deployment. No production/staging mutations or destructive tests were run. Local SDK tests passed 31/31; Go backend suites were not run because Go was unavailable. See [validation and limits](docs/en/appendix/validation.md) / [validazione e limiti](docs/it/appendix/validation.md).

Questa è principalmente una revisione statica del codice, non un’attestazione del deployment live. Non sono state eseguite mutation su produzione/staging né prove distruttive. I test SDK locali sono passati 31/31; le suite backend Go non sono state eseguite perché Go non era disponibile.

## License

Documentation and supporting scripts are licensed under [AGPL-3.0-or-later](LICENSE), unless a vendored asset states otherwise. Mermaid 11.4.1 is vendored under its MIT license in `docs/assets/vendor/` and is used without runtime CDN or remote fonts.
