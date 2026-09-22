> **Edizione italiana.** [English version](../en/14-open-questions.md) · Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.

# 14 · Questioni aperte e decisioni del team

Ogni raccomandazione è provvisoria. Le domande non bloccano la consegna; guidano le fasi e gli ADR.

## Q01 · Centralizzare le decisioni o solo i dati?

**Perché conta / evidenza:** F01/F03: risorse e DPP hanno PEP incoerenti; [zenflows/src/zenflows/vf/economic_resource/resolv.ex:28–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/resolv.ex#L28-L64); [interfacer-dpp/cmd/main/main.go:30–54](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/cmd/main/main.go#L30-L54).

**Possibili risposte, vantaggi e svantaggi:** Policy locale in ogni servizio: autonomia e latenza bassa, ma divergenza/revoca difficile. Tutto centrale: coerenza, ma coupling e single failure domain. Ibrido: coerenza comune con workflow locale, ma contratto più rigoroso.

**Raccomandazione provvisoria e conseguenze:** Modulo Zenflows per diritti comuni, regole DPP locali più restrittive. Conseguenza: chiamata online nelle write DPP e failure closed.

**Informazioni ancora necessarie:** Volumi, latenza consentita, disponibilità richiesta e capacità operativa del team.

## Q02 · Permission store in Zenflows o servizio dedicato?

**Perché conta / evidenza:** L’autorità delle risorse è PostgreSQL; DPP non ha lookup risorsa: [zenflows/src/zenflows/vf/economic_resource/domain.ex:246–332](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/domain.ex#L246-L332); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Possibili risposte, vantaggi e svantaggi:** Zenflows: transazioni con risorse e meno deploy, ma maggiore responsabilità del servizio. Servizio dedicato: separazione/evoluzione indipendente, ma sync e consistenza di un altro DB.

**Raccomandazione provvisoria e conseguenze:** Tenere in Zenflows all’inizio con API interna stabile, estraibile se si dimostra necessario. Non iniziare con un nuovo container obbligatorio.

**Informazioni ancora necessarie:** Roadmap federazione, proprietario del modulo e requisiti HA.

## Q03 · Quale eredità Organization→Project→Resource?

**Perché conta / evidenza:** AgentRelationship non implementa scope amministrativo: [zenflows/src/zenflows/vf/agent_relationship.ex:34–64](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/agent_relationship.ex#L34-L64).

**Possibili risposte, vantaggi e svantaggi:** Nessuna eredità: semplice revoca locale ma molti grant. Eredità unica esplicita: UX utile, rischio blast radius. Grafo multiparent: flessibile, difficile spiegare deny e revoca.

**Raccomandazione provvisoria e conseguenze:** Un parent amministrativo, opt-in e grant di origine tracciata; non ereditare da citazioni/containedIn. Permessi commerciali esclusi.

**Informazioni ancora necessarie:** Esistono risorse personali in progetti aziendali? Servono eccezioni o consorzi multi-org?

## Q04 · Il creator deve diventare controller?

**Perché conta / evidenza:** Produzione assegna accountability al receiver input, import usa prima email: [zenflows/src/zenflows/vf/economic_event/domain.ex:124–285](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L124-L285); [zenflows/src/zenflows/sw_pass/domain.ex:108–197](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/sw_pass/domain.ex#L108-L197).

**Possibili risposte, vantaggi e svantaggi:** Sempre creator: semplice ma sottrae controllo all’organizzazione. Sempre primaryAccountable: compatibile con UI ma dato economico non affidabile. Creator self o org delegante: più esplicito, richiede acting_for.

**Raccomandazione provvisoria e conseguenze:** Nuovi record self→creator verificato; per-org→org con delega. Per lo storico mai automatismo senza prove.

**Informazioni ancora necessarie:** Definizione legale/operativa di ownership e qualità dei record importati.

## Q05 · Come delegare e invitare persone?

**Perché conta / evidenza:** Contributor GUI è evento/notifica, non accettazione: [interfacer-gui/hooks/useProjectCRUD.ts:67–119](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/hooks/useProjectCRUD.ts#L67-L119).

**Possibili risposte, vantaggi e svantaggi:** Grant immediato: rapido, attribuzione non consenziente. Invito accettato: consenso e binding, più stati. Gruppi/org role: meno gestione, diritti più larghi.

**Raccomandazione provvisoria e conseguenze:** Invito scoped con expiry e accettazione autenticata; delega non transitiva per default. Mai concedere più di quanto delegabile.

**Informazioni ancora necessarie:** Si possono invitare esterni senza account? Quali ruoli possono delegare?

## Q06 · Il DPP deve consultare Zenflows o duplicare ACL?

**Perché conta / evidenza:** DPP ha solo productId stringa e createdBy misto: [interfacer-dpp/internal/model/model.go:25–51](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/model/model.go#L25-L51); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Possibili risposte, vantaggi e svantaggi:** Online: revoca rapida e autorità unica, dipendenza runtime. ACL replicate: autonomia, stale policy e sync. Capability breve: meno chiamate, finestra di revoca e gestione token.

**Raccomandazione provvisoria e conseguenze:** Decisioni online per write, binding parent stabile; non replicare membership libera. Valutare cache solo dopo misure.

**Informazioni ancora necessarie:** Disponibilità DPP offline e tolleranza massima alla revoca.

## Q07 · Permessi DPP indipendenti dalla risorsa?

**Perché conta / evidenza:** Riparazioni sono sezione singola; nessuna ACL sezioni: [interfacer-dpp/internal/model/model.go:127–147](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/model/model.go#L127-L147).

**Possibili risposte, vantaggi e svantaggi:** Identici al resource editor: facile, troppi diritti. Indipendenti: flessibile ma bypass. Derivati per azione e sezione: least privilege, più comandi API.

**Raccomandazione provvisoria e conseguenze:** Diritto base scoped sulla stessa risorsa + ruolo/sezione DPP; repair append separato da spec edit. Generic PUT ristretto.

**Informazioni ancora necessarie:** Chi certifica, chi ripara e quali dati devono essere immutabili per normativa?

## Q08 · Come autenticare e limitare i service account?

**Perché conta / evidenza:** Account condiviso Fabaccess e keyring DID: [zenflows-fabaccess/main.py:55–123](https://github.com/interfacerproject/zenflows-fabaccess/blob/8294b50a9e97f2ef85ad72fc0bc0cff66af33cfc/main.py#L55-L123); [zenflows/src/zenflows/did.ex:63–112](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/did.ex#L63-L112).

**Possibili risposte, vantaggi e svantaggi:** Chiave unica globale: semplice ma grande blast radius. Credenziali distinte TLS: gestibili, rotazione da implementare. mTLS/workload identity: forte binding, maggiore infrastruttura.

**Raccomandazione provvisoria e conseguenze:** Identity distinta per servizio/ambiente, scopi e audience, separazione actor/service; TLS e credenziali rotabili come minimo.

**Informazioni ancora necessarie:** Secret manager/PKI disponibili, scheduler/container platform, responsabili rotazione.

## Q09 · Collaboratore e seller sono ruoli separati?

**Perché conta / evidenza:** La preview usa seller mock senza ID o backend: [interfacer-gui/lib/previewCommerce/mockData.ts:17–183](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/lib/previewCommerce/mockData.ts#L17-L183).

**Possibili risposte, vantaggi e svantaggi:** Unificare owner/editor/seller: UX semplice ma mandato commerciale improprio. Separare: onboarding più lungo ma dati finanziari isolati. Seller indipendente sul design pubblico: favorisce ecosistema, richiede licenza/compliance.

**Raccomandazione provvisoria e conseguenze:** Separare grants commerciali; edit non dà sell. Consenso del design owner non è automaticamente necessario per ogni uso della licenza.

**Informazioni ancora necessarie:** Marketplace policy, licenze supportate, responsabilità legale produttore/rivenditore.

## Q10 · Seller deve essere Organization e cosa succede all’offboarding?

**Perché conta / evidenza:** Organization è Agent economico; seller ancora stringa mock: [zenflows/src/zenflows/vf/organization/resolv.ex:25–51](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/organization/resolv.ex#L25-L51); [interfacer-gui/lib/previewCommerce/mockData.ts:207–365](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/lib/previewCommerce/mockData.ts#L207-L365).

**Possibili risposte, vantaggi e svantaggi:** Solo org: governance chiara, esclude individui. Persona o org con legal profile: inclusivo, più verifiche. Account seller separato: flessibile, ulteriore mapping.

**Raccomandazione provvisoria e conseguenze:** Seller entity distinta legata a legal subject person/org; membership gestisce accesso. Uscita membro revoca deleghe, non riscrive ordini/seller storico.

**Informazioni ancora necessarie:** Paesi, KYC/payout provider, venditori individuali e trasferibilità account.

## Q11 · Quale garanzia tra allow, revoca e commit remoto?

**Perché conta / evidenza:** Zenflows e DPP hanno DB separati; status DPP read-then-write: [interfacer-dpp/internal/handler/handler.go:480–551](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L480-L551).

**Possibili risposte, vantaggi e svantaggi:** Check una volta: economico, ammette write in volo. Epoch/CAS locale: protegge versioni ma non atomizza authority. Permit e drain/coordinatore: revoca completata più forte, complessità e gestione crash.

**Raccomandazione provvisoria e conseguenze:** Documentare semantica bounded in-flight per edit ordinario, online no cache; azioni critiche solo dopo protocollo di serializzazione/drain provato.

**Informazioni ancora necessarie:** È accettabile qualche secondo? Quando UI può dire revoca completata? Requisiti normativi/commerciali.

## Q12 · Cosa fare se Zenflows/authz non risponde?

**Perché conta / evidenza:** DPP oggi non dipende da una decisione resource; introdurla cambia disponibilità: [interfacer-dpp/internal/auth/auth.go:98–151](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/auth/auth.go#L98-L151).

**Possibili risposte, vantaggi e svantaggi:** Fail-open: disponibilità alta ma bypass proprio nel guasto. Fail-closed: sicuro, scritture bloccate. Snapshot pubblico/capability limitata: continuità selettiva, complessità freshness.

**Raccomandazione provvisoria e conseguenze:** Fail-closed per write/private read, snapshot solo pubblico; retry idempotente e SLO espliciti.

**Informazioni ancora necessarie:** Budget downtime e priorità tra repair offline, pubblicazione e checkout.

## Q13 · Come convivono pubblico e privato?

**Perché conta / evidenza:** Guest resource e DPP draft leggibili senza policy: [zenflows/src/zenflows/vf/economic_resource/type.ex:224–353](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_resource/type.ex#L224-L353); [interfacer-dpp/internal/handler/handler.go:226–329](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L226-L329).

**Possibili risposte, vantaggi e svantaggi:** Tutto pubblico: semplice, incompatibile con PII/commerciale. Tutto autenticato: più protetto, limita open data. Proiezioni e sezioni: bilanciato, richiede manutenzione schema/cache.

**Raccomandazione provvisoria e conseguenze:** Proiezione pubblica versionata e internal model separato; applicare policy anche a nested/count/file/cache.

**Informazioni ancora necessarie:** Quali dati già pubblicati devono restare tali? Consensi, retention e requisiti DPP.

## Q14 · Chi può trasferire controllo amministrativo?

**Perché conta / evidenza:** transferAllRights è transizione economica, non consensus admin: [zenflows/src/zenflows/vf/economic_event/domain.ex:782–909](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L782-L909).

**Possibili risposte, vantaggi e svantaggi:** Seguire automaticamente VF: semplice, equivoco e escalation. Comando separato unilaterale: chiaro ma rischio errori. Proposta/accettazione e step-up: sicuro, più workflow.

**Raccomandazione provvisoria e conseguenze:** Comando separato con accettazione target, policy grants dopo transfer e audit; doppia approvazione per contesi/alto impatto.

**Informazioni ancora necessarie:** Poteri supporto, controversie, ultimo amministratore e soggetti non registrati.

## Q15 · Come migrare record senza controller certo?

**Perché conta / evidenza:** Import usa email come surrogate e DPP createdBy può essere header: [zenflows/src/zenflows/sw_pass/domain.ex:108–197](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/sw_pass/domain.ex#L108-L197); [interfacer-dpp/internal/handler/handler.go:41–116](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/handler/handler.go#L41-L116).

**Possibili risposte, vantaggi e svantaggi:** Backfill primaryAccountable: veloce, rischia assegnazioni illegittime. Claim first-come: economico, favorisce appropriazione. Review con prove: costosa, conserva fiducia.

**Raccomandazione provvisoria e conseguenze:** Classi confidence e disputed, read-only per edit rischiosi, processo claim revisionato e tracciato; nessuna equivalenza automatica tra custodia/creazione/contributo.

**Informazioni ancora necessarie:** Dimensione dataset, prove disponibili, persone responsabili della revisione.

## Q16 · Che valore e authority hanno wallet e punti?

**Perché conta / evidenza:** Wallet AddDiff è accessibile dopo DID/firma; bank ha airdrop: [zenflows-wallet/wallet.go:83–136](https://github.com/interfacerproject/zenflows-wallet/blob/f5cf1668afe371329ed827d0bb56557e0bedcda6/wallet.go#L83-L136); [zenflows-bank/cmd/airdrop.go:31–125](https://github.com/interfacerproject/zenflows-bank/blob/e5c2d2e6bd1ad072d1575de0a2be983854429b35/cmd/airdrop.go#L31-L125).

**Possibili risposte, vantaggi e svantaggi:** Punti auto-dichiarati: semplici, nessuna fiducia economica. Premi emessi server: più credibili, richiedono eventi/idempotenza. Ledger commerciale: ulteriore compliance e controllo.

**Raccomandazione provvisoria e conseguenze:** Non collegare punti a pagamenti/premi di valore prima di issuer policy e audit; decidere se mantenerli reputazionali.

**Informazioni ancora necessarie:** Uso reale bank/airdrop, valore attribuito ai punti, gestione rettifiche.

## Q17 · Come gestire identità federate e DID revocati?

**Perché conta / evidenza:** DPP/wallet verificano HTTP 200; inbox usa Person lookup: [interfacer-dpp/internal/auth/auth.go:98–151](https://github.com/interfacerproject/interfacer-dpp/blob/5f6ae20380ae80716ac6a8742b69bdc82e141296/internal/auth/auth.go#L98-L151); [zenflows-inbox/zenflows-auth.go:11–36](https://github.com/interfacerproject/zenflows-inbox/blob/963ae1d38116fb17ed35d6524ca7cfb8f16c0efd/zenflows-auth.go#L11-L36).

**Possibili risposte, vantaggi e svantaggi:** Solo Person locali: semplice, riduce federazione. DID universale: aperto, trust/issuer/revoca poco definiti. Federation allowlist con mapping: controllabile, governance necessaria.

**Raccomandazione provvisoria e conseguenze:** Principal locale o federato ammesso esplicitamente; risolvere binding e stato della chiave, non fidarsi del solo explorer HTTP.

**Informazioni ancora necessarie:** Controller authoritative, semantica deactivation, issuer trusted e utenti cross-instance.

## Q18 · Medusa o Zenflows è authority delle quantità?

**Perché conta / evidenza:** VF modifica quantità con eventi; preview stock è statico: [zenflows/src/zenflows/vf/economic_event/domain.ex:124–285](https://github.com/interfacerproject/zenflows/blob/893489d81fddf07e470094e72863958de402cca7/src/zenflows/vf/economic_event/domain.ex#L124-L285); [interfacer-gui/lib/previewCommerce/mockData.ts:207–365](https://github.com/interfacerproject/interfacer-gui/blob/9afe601d4d28dd6ccc0b4db2092da65f8055823e/lib/previewCommerce/mockData.ts#L207-L365).

**Possibili risposte, vantaggi e svantaggi:** Zenflows master: un ledger economico, integrazione reservations complessa. Medusa stock master: commerce naturale, proiezione VF eventuale. Due master: autonomia ma conflitti/doppio decremento.

**Raccomandazione provvisoria e conseguenze:** Medusa master stock commerciale iniziale; VF proiezione idempotente e distinta dalle altre quantità. Validare per fablab e produzione.

**Informazioni ancora necessarie:** Requisiti produzione/inventario non commerciale, unità serializzate e gestione fulfillment.
