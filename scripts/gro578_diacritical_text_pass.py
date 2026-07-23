#!/usr/bin/env python3
"""GRO-578: HTMLParser-based visible-text Hawaiian diacritical pass.

This intentionally edits only visible text nodes in a curated set of high-traffic
AOT pages. It skips tags/attributes, script/style/textarea/title internals are
handled as parser text data, and preserves the legal/brand phrase "Active Oahu".
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

TARGETS = [
    "site/beach-gear-rentals/index.html",
    "site/kayak-safety-guide/index.html",
    "site/kaneohe-sandbar/index.html",
    "site/chinamans-hat/index.html",
    "site/guides/kailua-beach-park/index.html",
    "site/guides/best-beaches-windward-oahu/index.html",
]

RAW_TERMS = ["Hawaii", "Oahu", "Kaneohe", "Mokolii", "Mokoli'i", "Laie"]

PLACEHOLDER = "__ACTIVE_OAHU_BRAND__"
COMPACT_PLACEHOLDER = "__ACTIVE_OAHU_COMPACT_BRAND__"
REPLACEMENTS = [
    ("Active Oahu", PLACEHOLDER),
    ("ActiveOahu", COMPACT_PLACEHOLDER),
    ("ActiveOʻahu", COMPACT_PLACEHOLDER),
    # Preserve the English adjective; the audit target is Hawaiian place names.
    ("Hawaiian", "__HAWAIIAN_ADJECTIVE__"),
    ("Hawaiʻian", "__HAWAIIAN_ADJECTIVE__"),
    ("Hawaii", "Hawaiʻi"),
    ("Oahu", "Oʻahu"),
    ("Kaneohe", "Kāneʻohe"),
    ("Kane'ohe", "Kāneʻohe"),
    ("Mokolii", "Mokoliʻi"),
    ("Mokoli'i", "Mokoliʻi"),
    ("Laie", "Lāʻie"),
    ("__HAWAIIAN_ADJECTIVE__", "Hawaiian"),
    (COMPACT_PLACEHOLDER, "ActiveOahu"),
    (PLACEHOLDER, "Active Oahu"),
]

SKIP_TAGS = {"script", "style", "code", "pre", "textarea"}


def line_offsets(text: str) -> list[int]:
    offsets = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            offsets.append(idx + 1)
    return offsets


class DataSpanParser(HTMLParser):
    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=False)
        self.source = source
        self.offsets = line_offsets(source)
        self.skip_stack: list[str] = []
        self.spans: list[tuple[int, int]] = []

    def abs_pos(self, line: int, col: int) -> int:
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag: str, attrs):
        if tag.lower() in SKIP_TAGS:
            self.skip_stack.append(tag.lower())

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            for i in range(len(self.skip_stack) - 1, -1, -1):
                if self.skip_stack[i] == tag:
                    del self.skip_stack[i]
                    break

    def handle_data(self, data: str):
        if self.skip_stack or not data:
            return
        line, col = self.getpos()
        start = self.abs_pos(line, col)
        self.spans.append((start, start + len(data)))


def apply_replacements(chunk: str) -> str:
    out = chunk
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    return out


def count_terms(text: str) -> dict[str, int]:
    return {term: text.count(term) for term in RAW_TERMS}


def process_file(path: Path, write: bool) -> dict:
    source = path.read_text(encoding="utf-8")
    parser = DataSpanParser(source)
    parser.feed(source)
    pieces = []
    cursor = 0
    changed_spans = 0
    for start, end in parser.spans:
        pieces.append(source[cursor:start])
        old = source[start:end]
        new = apply_replacements(old)
        if old != new:
            changed_spans += 1
        pieces.append(new)
        cursor = end
    pieces.append(source[cursor:])
    output = "".join(pieces)
    if write and output != source:
        path.write_text(output, encoding="utf-8")
    return {
        "file": str(path),
        "changed": output != source,
        "changed_text_nodes": changed_spans,
        "before": count_terms(source),
        "after": count_terms(output),
    }


def main() -> int:
    import argparse, json
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    results = [process_file(Path(p), args.write) for p in TARGETS]
    print(json.dumps(results, indent=2, ensure_ascii=False))
    changed = sum(1 for r in results if r["changed"])
    nodes = sum(r["changed_text_nodes"] for r in results)
    print(f"SUMMARY changed_files={changed} changed_text_nodes={nodes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
