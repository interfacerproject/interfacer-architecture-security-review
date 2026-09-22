> **English edition.** [Italian version](../../it/appendix/publication.md) · Technical terms and commit-pinned evidence are shared across both editions.

# Preview and publish

The deliverable is a **MkDocs + Material** site, independent from the application repositories. The pre-existing Docsify site was not touched. The following commands are run from the `architecture-review/` root; the root README contains complete instructions.

## Local environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock
python scripts/validate_docs.py
mkdocs serve -a 127.0.0.1:8008
```

Open `http://127.0.0.1:8008/`. For static build:

```bash
mkdocs build --strict
python scripts/validate_docs.py --site
```

Output is written to `site/`. The documentation uses relative links and a vendored, licensed Mermaid build; no production domain or `site_url` is configured. Search runs locally and indexes only `docs/`.

## GitHub Pages

The standalone destination is [`interfacerproject/interfacer-architecture-security-review`](https://github.com/interfacerproject/interfacer-architecture-security-review). The repository can remain private while maintainers review disclosure scope; creating or pushing the repository does **not** deploy the site. Virtual environments, caches, generated builds and confidential reports are excluded.

After approval, enable **Settings → Pages → GitHub Actions** and manually run **Interfacer documentation · GitHub Pages**. There is no automatic push trigger. The `.github/workflows/pages.yml` workflow installs locked dependencies, validates Markdown and HTML, builds in strict mode, runs browser checks, and uploads only `site/` through `upload-pages-artifact`/`deploy-pages`. The deployment uses the `github-pages` environment, which can be protected with reviewers.

Do not publish the parent workspace: it contains application checkouts and private material that are not part of this repository.

## Confidentiality

The sensitive operational report is deliberately external to the site directory. It's not enough to exclude a page from the sidebar: MkDocs can still copy and index it. Do not copy it to `docs/`, the public repository, or artifacts. The Pages visibility level may differ from that of the repository: check this before publishing.

## Optional validations

```bash
# Requires Git checkouts in the layout recorded by the manifest:
python scripts/inventory.py
python scripts/validate_docs.py --sources

# Requires Node.js and Playwright Chromium:
npm ci
npx playwright install chromium
node scripts/browser_check.mjs
```

The browser control serves the build under `/review/` to simulate a subpath repository, without contacting Interfacer applications. [Outcomes and limitations](validation.md).
