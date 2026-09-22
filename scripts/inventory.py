#!/usr/bin/env python3
"""Inventario statico riproducibile: legge solo sorgenti Git, non env o DB.
Eseguire dalla root del sito con i checkout descritti in repositories.json.
Non sostituisce introspezione runtime né audit manuale dei side effect.
"""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
MANIFEST = json.loads((ROOT / 'repositories.json').read_text())
REPOS = {r['name']: r for r in MANIFEST['repositories']}

def source(repo, path):
    r = REPOS[repo]
    return subprocess.check_output(['git', '-C', str(BASE / r['local_path']), 'show',
                                    f"{r['commit']}:{path}"], text=True)

def link(repo, path, first, last=None, label=None):
    last = last or first
    return f"[{label or path + ':' + str(first)}](https://github.com/interfacerproject/{repo}/blob/{REPOS[repo]['commit']}/{path}#L{first}-L{last})"

def camel(name):
    head, *rest = name.split('_')
    return head + ''.join(x.title() for x in rest)

def inventory():
    schema = source('zenflows', 'src/zenflows/gql/schema.ex')
    imports = set(re.findall(r'^\s*import_fields :(\w+)', schema, re.M))
    paths = subprocess.check_output(['git', '-C', str(BASE / REPOS['zenflows']['local_path']),
                                      'ls-tree', '-r', '--name-only', REPOS['zenflows']['commit']], text=True).splitlines()
    result = []
    for path in sorted(p for p in paths if p.endswith('/type.ex')):
        lines = source('zenflows', path).splitlines()
        obj = None
        current = None
        for i, line in enumerate(lines, 1):
            m = re.match(r'^object :(\w+) do', line)
            if m:
                obj = m[1] if m[1] in imports else None
                current = None
            if line == 'end':
                obj = None
                current = None
            f = re.match(r'^\tfield :(\w+)', line)
            if obj and f:
                current = {'kind': obj.split('_')[0], 'group': obj, 'name': camel(f[1]),
                           'symbol': f[1], 'path': path, 'line': i, 'auth': 'S', 'resolver': None}
                result.append(current)
            if obj and current:
                if 'only_guest?: true' in line: current['auth'] = 'G'
                if 'only_admin?: true' in line: current['auth'] = 'A'
                rm = re.search(r'&Resolv\.(\w+)/', line)
                if rm: current['resolver'] = rm[1]
    for kind in ['query', 'mutation']:
        block = re.search(r'^' + kind + r' do\n(.*?)^end', schema, re.M | re.S)
        start = schema[:block.start(1)].count('\n') + 1
        for i, line in enumerate(block[1].splitlines(), start):
            if re.match(r'^\tfield :echo,', line):
                result.append({'kind': kind, 'group': kind, 'name': 'echo', 'symbol': 'echo',
                               'path': 'src/zenflows/gql/schema.ex', 'line': i, 'auth': 'S', 'resolver': None})
    return sorted(result, key=lambda r: (r['kind'], r['group'], r['line']))

def evidence(row):
    refs = [link('zenflows', row['path'], row['line'], label='schema')]
    if row['resolver']:
        p = row['path'].replace('/type.ex', '/resolv.ex')
        text = source('zenflows', p)
        m = re.search(r'^def ' + row['resolver'] + r'\(', text, re.M)
        if m:
            n = text[:m.start()].count('\n') + 1
            refs.append(link('zenflows', p, n, min(n + 8, len(text.splitlines())), 'resolver'))
        dp = row['path'].replace('/type.ex', '/domain.ex')
        method = {'propose_intent': 'create', 'claim_person': 'claim'}.get(row['resolver'], row['resolver'].split('_')[0])
        if row['kind'] == 'mutation' and method in ['create', 'update', 'delete', 'claim']:
            dt = source('zenflows', dp)
            dm = re.search(r'^def ' + method + r'\(', dt, re.M)
            if dm:
                n = dt[:dm.start()].count('\n') + 1
                refs.append(link('zenflows', dp, n, min(n + 16, len(dt.splitlines())), 'dominio'))
    return ' · '.join(refs)

def build():
    rows = inventory()
    (ROOT / 'inventory.json').write_text(json.dumps(rows, indent=2) + '\n')
    for kind, filename, title in [('mutation', 'mutation-matrix.md', 'Mutation matrix Zenflows'),
                                   ('query', 'query-matrix.md', 'Query matrix Zenflows')]:
        selected = [r for r in rows if r['kind'] == kind]
        out = (f'> **Edizione italiana.** [English version](../../en/appendix/{filename}) · '
               'Le evidenze fissate a commit e i termini tecnici sono condivisi tra le due edizioni.\n\n'
               f'# {title}\n\n**{len(selected)} campi root** importati dal sorgente al commit del [manifest](repository-map.md). Tutte le righe riguardano Zenflows GraphQL `/api` e lo stesso schema su `/play`. Nomi camelCase derivati dai simboli Absinthe.\n\n')
        out += ('**Auth:** S = MW.Sign; A = MW.Admin; G = nessuna credenziale richiesta (meta only_guest non vieta utenti autenticati). '
                'Con `GQL_AUTH_CALLS=false`, S e A non verificano: non si presume questo setting in produzione. '
                'La colonna controlli distingue autenticazione da autorizzazione. FK/changeset possono rifiutare dati ma non provano ownership. '
                'Inventario statico completo dei campi importati, non test dinamico esaustivo.\n\n'
                '[Regole middleware](https://github.com/interfacerproject/zenflows/blob/' + REPOS['zenflows']['commit'] + '/src/zenflows/gql/schema.ex#L169-L193) · '
                '[Rilievi e condizioni](../04-authorization-audit.md) · [Test](../13-testing-strategy.md)\n\n')
        out += '| Operazione | Auth | Oggetto / effetti | Controlli esistenti e impatto | Remediation | Evidenza |\n|---|---|---|---|---|---|\n'
        for r in selected:
            obj = r['group'].replace(kind + '_', '')
            op = r['symbol'].split('_')[0]
            checks = 'Resolver senza principal; validazioni dati, non ACL. Modifica non scoped (F01/F09).'
            fix = 'Contesto nel dominio e grant scoped su oggetto/riferimenti; audit.'
            effect = obj
            if kind == 'query':
                checks = 'Nessun filtro per actor nei resolver esaminati; read non scoped. Policy dati da definire.'
                fix = 'Visibilità server, nested fields, liste/count e minimizzazione.'
            elif op == 'create' or r['symbol'] == 'propose_intent':
                checks = 'Dati validati; creator/parent e diritto di rappresentanza non legati al principal.'
                fix = 'Autorizzare creazione e parent; assegnare controller verificato e audit.'
            elif op == 'delete':
                checks = 'Delete per ID senza principal; FK possono impedire alcuni casi, non sono ACL.'
                fix = 'Permesso delete/retention, scope e relazioni; audit.'
            if r['auth'] == 'A':
                checks = 'Gate funzione con chiave admin; dominio non richiede actor. Non è self/tenant policy.'
                fix = 'Identità admin server-side scoped, audit e separazione signup/delete/import.'
            if obj in ['unit','role_behavior','agent_relationship_role','resource_specification','process_specification'] and kind == 'mutation':
                fix = 'Catalog manager o scope esplicito; impedire escalation tramite ruoli/spec globali.'
            if r['symbol'] == 'create_economic_event':
                effect = 'Evento, quantità, custodia, accountability, lineage, risorse nuove/contenute'
                checks = 'Invarianti VF su provider/receiver input, non su firmatario (F02).'
                fix = 'Autorizzare action, acting_for, origine/destinazione/processo e tutti gli effetti.'
            if r['symbol'] == 'update_economic_event':
                checks = 'Nessun actor; update limitato a note/agreedIn/realizationOf/triggeredBy, non action/provider.'
            if r['symbol'] == 'update_economic_resource':
                checks = 'Nessun actor; solo name/note/images/classifiedAs/repo in input GraphQL. F01.'
            if r['symbol'] == 'claim_person':
                checks = 'ID input, nessun self check; DID claim usa keyring server se configurato.'
                fix = 'Self/delega esplicita e proof chiave; audit di issuance.'
            if r['symbol'].startswith('person_') and 'verification' in r['symbol']:
                checks = 'Resolver lega azione a req_user; verifica token nel percorso verify. Controllo positivo.'
                fix = 'Preservare self-binding, test token/expiry, rate limit e audit.'
            if r['symbol'] == 'keypairoom_server':
                checks = 'Email validata ed esistenza coerente con firstRegistration; non prova possesso email.'
                fix = 'Rate limit/enumeration policy, key lifecycle e recupero documentati.'
            if r['symbol'] == 'my_agent':
                checks = 'Restituisce req_user autenticato (self-bound).'
                fix = 'Preservare; minimizzare campi e verificare stato account.'
            if r['symbol'] == 'person_check':
                checks = 'Lookup email+public key; non prova possesso privata. Restituisce Person.'
                fix = 'Challenge/sessione per login reale; limitare proiezione guest.'
            if r['symbol'] in ['person_exists','person_pubkey','instance_variables']:
                checks = 'Lookup guest intenzionale; non permission API.'
                fix = 'Contratto pubblico minimo e rate limits; evitare dati riservati.'
            if r['symbol'] in ['offers','requests']:
                checks = 'Resolver restituisce connessione vuota (stub), non marketplace.'
                fix = 'Definire scope prima di implementare dati reali.'
            if r['symbol'] == 'echo':
                checks = 'Echo senza persistenza; autenticazione root standard.'
                fix = 'Valutare rimozione diagnostica in produzione.'
                effect = 'Stringa input'
            out += f"| `{r['name']}` | {r['auth']} | {effect} | {checks} | {fix} | {evidence(r)} |\n"
        out += '\n## Copertura e limiti\n\n'
        if kind == 'mutation':
            out += ('Non esistono nel root importato `createEconomicResource` o `deleteEconomicEvent`: '
                    'le risorse sono create tramite eventi; esiste invece una primitiva interna `multi_delete` evento. '
                    'Commitment, Fulfillment, Claim, Settlement e altri import commentati non sono API attive nello schema analizzato. '
                    'Le funzioni raw e import richiedono inventario separato; il controllo di copertura non prova correttezza dei permessi.\n')
        else:
            out += ('Il gate è root-level: una query guest può risolvere relazioni annidate senza passare dal gate di una query root firmata dello stesso tipo. '
                    'I resolver di immagini, agent, trace e DPP trace vanno protetti per dati, non solo per nome del root field.\n')
        (ROOT / 'docs/it/appendix' / filename).write_text(out)
    print('Inventario:', len([r for r in rows if r['kind'] == 'mutation']), 'mutation,', len([r for r in rows if r['kind'] == 'query']), 'query')

if __name__ == '__main__':
    build()
