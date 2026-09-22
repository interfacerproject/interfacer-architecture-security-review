#!/usr/bin/env python3
"""Valida documenti/artifact senza rete e senza leggere credenziali.
--sources controlla i riferimenti contro i commit nei checkout del manifest.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import argparse
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'): self.ids.add(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs: self.links.append(attrs[attr])


def validate(site=False, sources=False):
    errors = []
    pages = list(DOCS.rglob('*.md'))
    refs = set()
    diagrams = 0
    for path in pages:
        text = path.read_text()
        diagrams += len(re.findall(r'^```mermaid\s*$', text, re.M))
        if re.search(r'\{\{[a-z_]+\}\}', text): errors.append(f'Macro non risolta: {path.relative_to(ROOT)}')
        if text.count('```') % 2: errors.append(f'Fence sbilanciata: {path.relative_to(ROOT)}')
        for dest in re.findall(r'\]\(([^\s)]+)\)', text):
            url = urlsplit(dest)
            if url.scheme:
                if dest.startswith('https://github.com/interfacerproject/') and '/blob/' in dest: refs.add(dest)
                continue
            if not url.path: continue
            target = (path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(DOCS.resolve()): errors.append(f'Link fuori docs: {path.name}: {dest}')
            elif not target.exists(): errors.append(f'Link assente: {path.name}: {dest}')
        if 'README-RISERVATO.md' in text or 'interfacer-gui/.env:3' in text:
            errors.append(f'Dettaglio privato nel sito: {path.relative_to(ROOT)}')
    if sources:
        manifest = json.loads((ROOT / 'repositories.json').read_text())
        repos = {r['name']: r for r in manifest['repositories']}
        cache = {}
        for dest in sorted(refs):
            url = urlsplit(dest)
            parts = unquote(url.path).split('/')
            repo, sha, path = parts[2], parts[4], '/'.join(parts[5:])
            if repo not in repos or repos[repo]['commit'] != sha:
                errors.append(f'Commit fuori manifest: {repo}/{path}'); continue
            key = (repo, sha, path)
            if key not in cache:
                try:
                    content = subprocess.check_output(['git', '-C', str(ROOT.parent / repos[repo]['local_path']),
                                                       'show', f'{sha}:{path}'], text=True, stderr=subprocess.DEVNULL)
                    cache[key] = len(content.splitlines())
                except subprocess.CalledProcessError:
                    errors.append(f'Sorgente assente: {repo}/{path}'); continue
            lines = re.findall(r'L(\d+)', url.fragment)
            if any(int(n) > cache[key] or int(n) < 1 for n in lines):
                errors.append(f'Range non valido: {repo}/{path} {url.fragment}')
    html_count = 0
    if site:
        root = ROOT / 'site'
        parsed = {}
        for path in root.rglob('*.html'):
            page = Page(); page.feed(path.read_text()); parsed[path.resolve()] = page
        html_count = len(parsed)
        if not html_count: errors.append('Artifact HTML assente')
        for path, page in parsed.items():
            for dest in page.links:
                url = urlsplit(dest)
                if url.scheme or url.netloc: continue
                if url.path.startswith('/'):
                    errors.append(f'Link root-absolute non subpath-safe: {path.name}: {dest}'); continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                if target.is_dir(): target = target / 'index.html'
                if not target.exists():
                    errors.append(f'Asset/link HTML assente: {path.relative_to(root)}: {dest}'); continue
                if url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:
                    errors.append(f'Anchor assente: {path.relative_to(root)}: {dest}')
        for path in root.rglob('*'):
            if path.is_file() and ('RISERVATO' in path.name or path.name.startswith('.env')):
                errors.append('File riservato nel build')
    summary = {'markdown_pages': len(pages), 'mermaid_diagrams': diagrams, 'source_links': len(refs),
               'source_ranges_checked': sources, 'html_pages': html_count, 'errors': errors}
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if errors: raise SystemExit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', action='store_true')
    parser.add_argument('--sources', action='store_true')
    args = parser.parse_args()
    validate(args.site, args.sources)
