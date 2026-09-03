#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import json, sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('site')
scan_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('/tmp/aot-gro585-hreflang-after.json')
write = '--write' in sys.argv

class SpanParser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source=source; self.offsets=[0]; self.spans=[]
        for i,ch in enumerate(source):
            if ch=='\n': self.offsets.append(i+1)
    def abs_pos(self,line,col): return self.offsets[line-1]+col
    def maybe_link(self, tag, attrs):
        if tag.lower() != 'link': return
        attrs_dict=dict(attrs)
        if (attrs_dict.get('rel') or '').lower() == 'alternate' and 'hreflang' in attrs_dict:
            line,col=self.getpos(); start=self.abs_pos(line,col); raw=self.get_starttag_text() or ''
            self.spans.append((start,start+len(raw)))
    def handle_starttag(self, tag, attrs): self.maybe_link(tag, attrs)
    def handle_startendtag(self, tag, attrs): self.maybe_link(tag, attrs)

scan=json.load(open(scan_path))
rows=[row for row in scan['rows'] if not row['counterpart_exists']]
changed=[]
for row in rows:
    p=root/row['file']
    source=p.read_text()
    parser=SpanParser(source); parser.feed(source)
    if not parser.spans: continue
    pieces=[]; cursor=0
    for start,end in parser.spans:
        pieces.append(source[cursor:start])
        # Remove the tag and a single following newline if the tag is on its own line.
        cursor=end
        if cursor < len(source) and source[cursor] == '\n':
            cursor += 1
    pieces.append(source[cursor:])
    out=''.join(pieces)
    if out != source:
        changed.append({'file':row['file'],'route':row['route'],'removed_links':row['links'],'counterpart':row['counterpart']})
        if write: p.write_text(out)
print(json.dumps({'write':write,'no_counterpart_rows':len(rows),'changed_files':len(changed),'changed':changed}, ensure_ascii=False, indent=2))
