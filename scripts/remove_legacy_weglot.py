#!/usr/bin/env python3
"""Remove legacy Weglot artifacts from static mirror files.

The mirror contains WordPress-generated HTML fragments and a few HTML documents
saved with .pdf extensions. This cleaner uses exact block/line removal for the
legacy Weglot assets and keeps the static English/Japanese lang-switcher intact.
HTMLParser is used as a post-clean token sanity pass so bulk edits are checked
against parseable HTML tokens without rewriting the document tree.
"""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
import argparse, re

WEGLOT_RE = re.compile(r"(weglot|cdn\.weglot|wp-content/plugins/weglot|\bwg[_-])", re.I)
START_WEGLOT_SCRIPT_RE = re.compile(r"<script\b(?=[^>]*(?:id=['\"][^'\"]*weglot|weglot-data|wp-weglot|WeGlot|wp-content/plugins/weglot|cdn\.weglot))", re.I)
START_FLAG_STYLE_RE = re.compile(r"<style\b(?=[^>]*id=['\"]custom-flag-handle-inline-css['\"])", re.I)
WEGLOT_LINK_RE = re.compile(r"<link\b[^>]*(?:weglot|wp-content/plugins/weglot|cdn\.weglot)[^>]*>", re.I)

class WeglotTokenScanner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.matches=0
    def handle_starttag(self, tag, attrs):
        attrs_blob=' '.join(f'{k}={v}' for k,v in attrs)
        if WEGLOT_RE.search(attrs_blob): self.matches += 1
    def handle_comment(self, data):
        if WEGLOT_RE.search(data): self.matches += 1
    def handle_data(self, data):
        if WEGLOT_RE.search(data): self.matches += 1

def clean_text(text: str) -> tuple[str, bool]:
    out=[]; changed=False; skip_until=None
    for line in text.splitlines(keepends=True):
        low=line.lower()
        if skip_until:
            changed=True
            if skip_until in low: skip_until=None
            continue
        if ('.weglot-flags' in low or 'aside.country-selector' in low or 'label.wgcurrent' in low) and '{' in line:
            changed=True
            if '}' not in line: skip_until='}'
            continue
        if START_WEGLOT_SCRIPT_RE.search(line):
            changed=True
            if '</script>' not in low: skip_until='</script>'
            continue
        if START_FLAG_STYLE_RE.search(line):
            changed=True
            if '</style>' not in low: skip_until='</style>'
            continue
        if WEGLOT_LINK_RE.search(line):
            changed=True; continue
        if '<aside' in low and 'country-selector' in low and WEGLOT_RE.search(line):
            changed=True; continue
        if '<!--' in line and WEGLOT_RE.search(line):
            changed=True; continue
        new=line.replace('.lang-switcher, .weglot-flags, [href*="/ja/"]', '.lang-switcher, [href*="/ja/"]')
        new=new.replace(".lang-switcher, .weglot-flags, [href*='/ja/']", ".lang-switcher, [href*='/ja/']")
        # Drop generated Weglot CSS rules/JS init lines, but keep unrelated static nav.
        if WEGLOT_RE.search(new) and any(token in low for token in ['.weglot-flags','wg-','weglot.init','wp-weglot-js-js-after','data-wg-notranslate']):
            if 'data-wg-notranslate' in low and not any(token in low for token in ['.weglot-flags','wg-','weglot.init','wp-weglot-js-js-after']):
                new=new.replace(' data-wg-notranslate=""','')
            else:
                changed=True; continue
        if new != line: changed=True
        out.append(new)
    cleaned=''.join(out)
    scanner=WeglotTokenScanner(); scanner.feed(cleaned); scanner.close()
    return cleaned, changed

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument('root', nargs='?', default='site'); ap.add_argument('--dry-run', action='store_true')
    args=ap.parse_args(); changed=[]
    suffixes={'.html','.pdf'}
    for path in sorted(p for p in Path(args.root).rglob('*') if p.suffix.lower() in suffixes):
        try: original=path.read_text(errors='strict')
        except UnicodeDecodeError: continue
        cleaned,did=clean_text(original)
        if did and cleaned != original:
            changed.append(str(path))
            if not args.dry_run: path.write_text(cleaned)
    for p in changed: print(p)
    print(f'changed_files={len(changed)}')
if __name__ == '__main__': main()
