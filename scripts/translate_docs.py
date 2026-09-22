#!/usr/bin/env python3
"""Rigenera la copia inglese dei documenti pubblici italiani.

Usa l'endpoint Google Translate pubblico via HTTPS: eseguire solo intenzionalmente,
mai in CI e mai su report riservati. Il risultato versionato deve essere revisionato
tecnicamente e validato con validate_docs.py. Blocchi di codice, inline code e
destinazioni dei link non vengono inviati come testo traducibile. I blocchi Mermaid
già revisionati nella copia inglese vengono preservati durante la rigenerazione.
"""
from pathlib import Path
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs' / 'it'
TARGET = ROOT / 'docs' / 'en'
CACHE_PATH = ROOT / '.translation-cache.json'
SEP = 'ZXQSEPARATORZXQ'
TOKEN = re.compile(r'`[^`]+`|(?<=\]\()[^)]+(?=\))|https?://\S+|\b[0-9a-f]{40}\b')

try:
    CACHE = json.loads(CACHE_PATH.read_text())
except FileNotFoundError:
    CACHE = {}


def protect(text):
    values = []
    def sub(match):
        values.append(match.group(0))
        return f'ZXQPROTECTED{len(values)-1}ZXQ'
    return TOKEN.sub(sub, text), values


def restore(text, values):
    for i, value in enumerate(values):
        text = text.replace(f'ZXQPROTECTED{i}ZXQ', value)
    return text


def request(text):
    if text in CACHE:
        return CACHE[text]
    data = urllib.parse.urlencode({'client': 'dict-chrome-ex', 'sl': 'it', 'tl': 'en', 'dt': 't', 'q': text}).encode()
    req = urllib.request.Request('https://translate.googleapis.com/translate_a/single', data=data,
                                 headers={'User-Agent': 'Mozilla/5.0 Interfacer documentation translation'})
    for attempt in range(7):
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.load(response)
            value = ''.join(part[0] for part in result[0])
            CACHE[text] = value
            return value
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt == 6: raise
            time.sleep(2 ** attempt)


def translate_lines(lines):
    output = list(lines)
    candidates = []
    fenced = False
    for i, line in enumerate(lines):
        if line.startswith('```'):
            fenced = not fenced
            continue
        stripped = line.strip()
        if fenced or not stripped or set(stripped) <= set('|:- '):
            continue
        candidates.append(i)
    pos = 0
    while pos < len(candidates):
        indexes, protected, originals, length = [], [], [], 0
        while pos < len(candidates):
            i = candidates[pos]
            value, tokens = protect(lines[i])
            addition = len(value) + len(SEP) + 2
            if indexes and length + addition > 3500: break
            indexes.append(i); protected.append(value); originals.append(tokens); length += addition; pos += 1
        translated = request(('\n' + SEP + '\n').join(protected))
        pieces = translated.split(SEP)
        if len(pieces) != len(indexes):
            raise RuntimeError(f'Separatore alterato: attesi {len(indexes)}, ricevuti {len(pieces)}')
        for i, piece, tokens in zip(indexes, pieces, originals):
            output[i] = restore(piece.strip('\n'), tokens)
        print(f'{pos}/{len(candidates)} righe', end='\r', flush=True)
    return output


def counterpart(path):
    rel = path.relative_to(SOURCE)
    prefix = '../it/' if rel.parent == Path('.') else '../../it/appendix/'
    return prefix + rel.name


def without_language_banner(lines):
    """La barra lingua è specifica dell'edizione e non deve essere tradotta."""
    if lines and lines[0].startswith('> **Edizione italiana.**'):
        return lines[2:] if len(lines) > 1 and not lines[1].strip() else lines[1:]
    return lines


def mermaid_blocks(text):
    return re.findall(r'```mermaid\n.*?\n```', text, flags=re.S)


def preserve_reviewed_mermaid(text, target):
    """Conserva le etichette inglesi dei diagrammi già revisionati e versionati."""
    if not target.exists():
        return text
    reviewed = iter(mermaid_blocks(target.read_text()))
    return re.sub(r'```mermaid\n.*?\n```', lambda _match: next(reviewed), text, flags=re.S)


def main():
    for source in sorted(SOURCE.rglob('*.md')):
        rel = source.relative_to(SOURCE)
        target = TARGET / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        source_lines = without_language_banner(source.read_text().splitlines())
        translated = translate_lines(source_lines)
        translated = [re.sub(r'^(#{1,6})(?=\S)', r'\1 ', line) for line in translated]
        banner = [f'> **English edition.** [Versione italiana]({counterpart(source)}) · '
                  f'Technical terms and commit-pinned evidence are shared across both editions.', '']
        output = '\n'.join(banner + translated) + '\n'
        output = preserve_reviewed_mermaid(output, target)
        target.write_text(output)
        print(f'\n{rel}')
        CACHE_PATH.write_text(json.dumps(CACHE, ensure_ascii=False, indent=2) + '\n')
    print(f'Tradotti {len(list(SOURCE.rglob("*.md")))} documenti.')

if __name__ == '__main__':
    main()
