> **English edition.** [Italian version](../../it/appendix/repository-map.md) · Technical terms and commit-pinned evidence are shared across both editions.

# Repository map and reproducibility

Acquisition date (UTC): `2026-09-21T15:30:50.340931+00:00`. The local parent is not a Git repository; the site is an autonomous deliverable. No remotes modified or pushes performed.

## Snapshots analyzed

| Repositories | Commit | Coverage | Stacks / notes |
|---|---|---|---|
| [interfacer-client](https://github.com/interfacerproject/interfacer-client) | [`dfb1baabf16516a845957d5587ccb933c1874221`](https://github.com/interfacerproject/interfacer-client/tree/dfb1baabf16516a845957d5587ccb933c1874221) | Local; auth/crypto/GraphQL/resources/DPP and unit tests | TypeScript SDK; local package declares 0.1.0, not automatic equivalence with GUI release |
| [interfacer-docs](https://github.com/interfacerproject/interfacer-docs) | [`da1e1e840f738c5362ae2e7028df9481903590ae`](https://github.com/interfacerproject/interfacer-docs/tree/da1e1e840f738c5362ae2e7028df9481903590ae) | Additional clone; check pre-existing site | Docsify in docs/index.html, unmodified |
| [interfacer-dpp](https://github.com/interfacerproject/interfacer-dpp) | [`5f6ae20380ae80716ac6a8742b69bdc82e141296`](https://github.com/interfacerproject/interfacer-dpp/tree/5f6ae20380ae80716ac6a8742b69bdc82e141296) | Local; router, all handlers, auth, model and storage | Go/Gin, MongoDB/MinIO, Zenroom executable |
| [interfacer-feedback-service](https://github.com/interfacerproject/interfacer-feedback-service) | [`d905a82a02d4115b13c87557591b7ddca6eb39b1`](https://github.com/interfacerproject/interfacer-feedback-service/tree/d905a82a02d4115b13c87557591b7ddca6eb39b1) | Local; router/auth/handler/persistence | Go/Gin, SQLite, publisher log |
| [interfacer-gui](https://github.com/interfacerproject/interfacer-gui) | [`9afe601d4d28dd6ccc0b4db2092da65f8055823e`](https://github.com/interfacerproject/interfacer-gui/tree/9afe601d4d28dd6ccc0b4db2092da65f8055823e) | Local; in-depth analysis of auth/DPP/commerce/API flows | Next.js 12/React; Installed SDK 0.6.1; hook local modification excluded from commit-pinned evidence |
| [interfacer-proxy](https://github.com/interfacerproject/interfacer-proxy) | [`10d07344e2bcf7e3673f906e51aeb52cd6abf0cb`](https://github.com/interfacerproject/interfacer-proxy/tree/10d07344e2bcf7e3673f906e51aeb52cd6abf0cb) | Local; router/forwarding/config in depth | Go net/http, no DB |
| [zenflows](https://github.com/interfacerproject/zenflows) | [`893489d81fddf07e470094e72863958de402cca7`](https://github.com/interfacerproject/zenflows/tree/893489d81fddf07e470094e72863958de402cca7) | Local; comprehensive root inventory and in-depth representative domains | Elixir, Absinthe, Ecto/PostgreSQL; authn and ValueFlows |
| [zenflows-bank](https://github.com/interfacerproject/zenflows-bank) | [`e5c2d2e6bd1ad072d1575de0a2be983854429b35`](https://github.com/interfacerproject/zenflows-bank/tree/e5c2d2e6bd1ad072d1575de0a2be983854429b35) | Additional clone; CLI/airdrop and data relations | Targeted coverage, not full smart contract/RPC audit |
| [zenflows-crypto](https://github.com/interfacerproject/zenflows-crypto) | [`0ffcce9b90799c9cb61f11fc594aeb513a01326f`](https://github.com/interfacerproject/zenflows-crypto/tree/0ffcce9b90799c9cb61f11fc594aeb513a01326f) | Additional clone; signature/verify and integration contracts | Non-mathematical audit of the Zenroom library |
| [zenflows-fabaccess](https://github.com/interfacerproject/zenflows-fabaccess) | [`8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc`](https://github.com/interfacerproject/zenflows-fabaccess/tree/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc) | Additional clone; main/API and controls | FastAPI/pyfabapi; external Fabaccess server not audited |
| [zenflows-inbox](https://github.com/interfacerproject/zenflows-inbox) | [`963ae1d38116fb17ed35d6524ca7cfb8f16c0efd`](https://github.com/interfacerproject/zenflows-inbox/tree/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd) | Additional clone; auth, messages/social/router/storage | Go/Gin and Tarantool; different surfaces auth |
| [zenflows-osh](https://github.com/interfacerproject/zenflows-osh) | [`56855d426ffd884d91dd72373a2292f1ae5695ed`](https://github.com/interfacerproject/zenflows-osh/tree/56855d426ffd884d91dd72373a2292f1ae5695ed) | Additional clone; router and clone/analysis | Git/osh CLI and temporary filesystem |
| [zenflows-wallet](https://github.com/interfacerproject/zenflows-wallet) | [`f5cf1668afe371329ed827d0bb56557e0bedcda6`](https://github.com/interfacerproject/zenflows-wallet/tree/f5cf1668afe371329ed827d0bb56557e0bedcda6) | Additional clone; DID/auth and token handler | Go/Gin and Tarantool; not PSP |

## Working tree and SDK

The GUI already had modified `hooks/useProjectCRUD.ts` and untracked files (local skill and image). They have not been changed, archived on the site or used as public evidence. For the hook it was read `git show HEAD:hooks/useProjectCRUD.ts`; for other references the commit manifest is used. Application checkouts remain unchanged except for any test runner cache.

GUI `package.json` requires `@dyne/interfacer-client ^0.6.1` and local installation is 0.6.1; separate checkout states 0.1.0. They are analyzed as distinct snapshots: the chain of responsibility is verified but the source/dist correspondence of the installed release is not certified. Phase 1 must associate actual artifacts with commits.

## Submodules set by repositories

Don't confuse the HEAD of the crypto clone with any historical submodule. Below are the registered gitlinks, regardless of local initialization. Not all submodules/test frameworks have been initialized. For DPP the crypto gitlink corresponds to the analyzed clone.

| Repositories | Path submodule | Commit logged |
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

## Additional Discovery

Public organization list obtained via GitHub API, without remote writes. The presence of a repo does not prove its use in deployment. In addition to the analyzed components, the following repositories were discovered, **not code audited in this review**:

- [zenswarm-storage](https://github.com/interfacerproject/zenswarm-storage): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [planetmint-interfacer](https://github.com/interfacerproject/planetmint-interfacer): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [loshifacer](https://github.com/interfacerproject/loshifacer): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [Node-RED_Interfacer](https://github.com/interfacerproject/Node-RED_Interfacer): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [Interfacer-notebook](https://github.com/interfacerproject/Interfacer-notebook): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [.github](https://github.com/interfacerproject/.github): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [workflows](https://github.com/interfacerproject/workflows): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [Interfacer_DPP-visualisations](https://github.com/interfacerproject/Interfacer_DPP-visualisations): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [README](https://github.com/interfacerproject/README): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [reuse](https://github.com/interfacerproject/reuse): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [EconSim](https://github.com/interfacerproject/EconSim): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [DTECH_HSU_2025_OPS](https://github.com/interfacerproject/DTECH_HSU_2025_OPS): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [dtech-example-data-injection](https://github.com/interfacerproject/dtech-example-data-injection): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [interfacer-client-sdk-docs](https://github.com/interfacerproject/interfacer-client-sdk-docs): to be classified with maintainer; no security or integration guarantees deduced from the name.
- [interfacer-3d-demo-models](https://github.com/interfacerproject/interfacer-3d-demo-models): to be classified with maintainer; no security or integration guarantees deduced from the name.

## Existing documentation/deployment

`interfacer-docs/docs/index.html` contains Docsify and sidebar/.nojekyll files. GUI has publish/test-deploy workflow; the other components have image workflows, not replaced. The site for this review does not assume an already assigned domain or Pages repository: [local instructions](publication.md). Existing sites have not been modified.

## Coverage limits

Not fully analyzed DID controller/Restroom runtime, Zenroom internals, LOSH/planetmint/Node-RED, real infrastructure, smart contracts, Fabaccess server or federated services. Medusa is a future requirement. Endpoints of non-cloned applications nor infrastructures that do not appear in the source are not enumerated. The inventory is comprehensive for imported GraphQL roots and explicitly listed service routes, not a certification of the entire GitHub organization.
