#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import json, sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('site')
scan_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('/tmp/aot-gro585-hreflang-before.json')
write = '--write' in sys.argv
SITE='https://activeoahutours.com'

class SpanParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source=source
        self.offsets=[0]
        for i,ch in enumerate(source):
            if ch=='\n': self.offsets.append(i+1)
        self.spans=[]
    def abs_pos(self,line,col): return self.offsets[line-1]+col
    def maybe_link(self, tag, attrs):
        if tag.lower() != 'link': return
        attrs_dict=dict(attrs)
        rel=(attrs_dict.get('rel') or '').lower()
        if rel == 'alternate' and 'hreflang' in attrs_dict:
            line,col=self.getpos(); start=self.abs_pos(line,col); raw=self.get_starttag_text() or ''
            self.spans.append((start,start+len(raw),attrs_dict))
    def handle_starttag(self, tag, attrs): self.maybe_link(tag, attrs)
    def handle_startendtag(self, tag, attrs): self.maybe_link(tag, attrs)

def canonical_lines(expected_en, expected_ja):
    return (f'<link rel="alternate" hreflang="en" href="{SITE}{expected_en}" />\n'
            f'<link rel="alternate" hreflang="ja" href="{SITE}{expected_ja}" />')

scan=json.load(open(scan_path))
safe={row['file']:row for row in scan['rows'] if row['counterpart_exists']}
changed=[]
for rel,row in safe.items():
    p=root/rel
    source=p.read_text()
    parser=SpanParser(source); parser.feed(source)
    spans=parser.spans
    if not spans: continue
    repl=canonical_lines(row['expected_en'], row['expected_ja'])
    pieces=[]; cursor=0; inserted=False
    for start,end,attrs in spans:
        pieces.append(source[cursor:start])
        if not inserted:
            pieces.append(repl); inserted=True
        # skip duplicate/old alternate tag
        cursor=end
        # if duplicate tags are on separate lines, remove following immediate blank/indent? preserve rest
    pieces.append(source[cursor:])
    out=''.join(pieces)
    if out != source:
        changed.append({'file':rel,'route':row['route'],'expected_en':row['expected_en'],'expected_ja':row['expected_ja'],'old_links':row['links']})
        if write: p.write_text(out)
print(json.dumps({'write':write,'safe_files':len(safe),'changed_files':len(changed),'changed':changed}, ensure_ascii=False, indent=2))
