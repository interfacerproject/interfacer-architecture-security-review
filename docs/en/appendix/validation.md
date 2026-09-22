> **English edition.** [Italian version](../../it/appendix/validation.md) · Technical terms and commit-pinned evidence are shared across both editions.

# Method, validation and limits

## Method

Read-only local inventory; acquisition of missing public repositories; commits and gitlinks recorded; tracing frontend/SDK→middleware→resolver→domain→persistence; complete static inventory of imported root fields; reading DPP router/handler, proxy, feedback and connected services. The findings distinguish confirmed behavior, risk, limit, hypotheses to be verified and proposals.

Potentially sensitive configurations were inspected with output sanitized by location/name, never printing values. The most sensitive operational details are in the off-site private local report. No exploits, pushes, remote modifications, database or application deployments were performed.

## Application tests performed

| Check | Result | Limit |
|---|---|---|
| SDK `vitest run src/__tests__/unit.test.ts` | 31/31 pass, Vitest 2.1.9 | Storage/tagging/types; no authz backend |
| Elixir time expression for email token | Current predicate accepts old synthetic timestamp; the expected one denies it | Expression only, not real/end-to-end token |
| Source schema inventory | 81 mutations and 62 root queries | Static extraction, not runtime introspection |

The time comparison was performed with a fixed clock, emission ten days earlier and expiry four days, without starting Zenflows. [F11](../04-authorization-audit.md#f11-inverted-email-expiration-predicate-confirmed-p1).

## Document validation

The root includes repeatable tools: `scripts/validate_docs.py` checks local links, fences, unresolved macros and site boundaries; with `--sources` checks files and ranges against Git commits, with `--site` checks links/assets/anchors in HTML. `scripts/browser_check.mjs` verifies build via HTTP under `/review/`, Mermaid, search and mobile viewport without external network.

### Local results · September 22, 2026

| Command/check | Observed outcome |
|---|---|
| `python scripts/validate_docs.py --sources` | 55 Markdown pages (27 per language + language chooser); 450 unique commit-pinned links with verified files/ranges; zero errors |
| `mkdocs build --strict` | Build successful, no blocking warnings |
| `python scripts/validate_docs.py --site` | 56 HTML files (55 documents + 404), valid local links/assets/anchors |
| `node scripts/browser_check.mjs` | 55 pages visited under `/review/`; 16 rendered Mermaid diagrams; local search returned results |
| Mobile browser | Viewport 390 px, content 390 px, working side menu |
| Site network during smoke test | Zero external requests; Mermaid and search work with egress block |
| Git status of the 13 repositories acquired | Same as initial snapshot; no application changes introduced |

Browser testing uses local Chromium Playwright, not the Interfacer application. The standalone 404 template avoids theme root-absolute references when the repository subpath is not yet defined. Local Python 3.14; workflow set up with 3.12, compatible with the Python requirements declared by the installed dependencies. The GitHub Actions workflow was not executed nor the site published from this session.

## Not executed

- No mutation/API testing on shared production or staging; no public application scanning.
- Real-backend SDK and Playwright GUI suites not running: can contact configured services.
- ExUnit Zenflows not running with DB/Restroom; SQL Sandbox alone does not ensure a separate environment.
- Go DPP/feedback/inbox/wallet tests not run: Go toolchain not available in PATH and no ephemeral backend set up.
- No internal Zenroom crypto audits, full CVE audits or infrastructure penetration tests.
- No Medusa tests: backend not implemented in the perimeter; the preview is mock.

## Limits of reproducibility

The local parent is not a Git repository. Individual repository commits and initial dirty states are in the manifest. The pre-existing GUI change is preserved and not used as commit-pinned code. Local SDK checkout and installed GUI release differ in declared versions; the artifact→commit mapping is to be established.

Code URLs are commit-pinned; GitHub was not required to validate each external link individually. Local validation checks the Git objects themselves. Compose and env templates do not attest to live deployment. The network relationships drawn are implemented/configurable, not a scan of active services.

The review delves into priority paths, not every possible data combination or every repository in the organization. [Coverage per repository](repository-map.md), [API matrix](endpoint-matrix.md), [test specifications to implement](../13-testing-strategy.md).
