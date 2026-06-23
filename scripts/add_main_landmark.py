#!/usr/bin/env python3
"""
A11y: Add role="main" to all <div id="content" class="site-content"> elements.

Resolves Lighthouse 'landmark-one-main' audit failure (a11y weight 3).

Before: <div class="site-content" id="content">
After:  <div class="site-content" id="content" role="main">

Idempotent: skips files that already have role="main" on the content div.

Uses stdlib HTMLParser for safe attribute manipulation — never regex on HTML.

Usage:
    python3 scripts/add_main_landmark.py
    python3 scripts/add_main_landmark.py --dry-run    # Report only, don't write
"""
from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent.parent / 'site'


class MainLandmarkAdder(HTMLParser):
    """Stateful HTML parser that adds role="main" to <div id="content"> open tags.

    Tracks raw text offsets so we can rewrite the source file safely.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.rewrites: list[tuple[int, int, str]] = []  # (start, end, replacement)
        self._pos = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != 'div':
            return
        attr_dict = dict(attrs)
        if attr_dict.get('id') != 'content':
            return
        if attr_dict.get('role') == 'main':
            return  # Already done — idempotent

        # Reconstruct the open tag exactly as it appeared in the source.
        # We rely on get_starttag_text() which returns the full <tag ...> string.
        # Find the position of this start tag in the source via raw offset tracking.
        start_text = self.get_starttag_text()  # e.g., '<div class="site-content" id="content">'
        if start_text is None:
            return

        # Locate in remaining source from current position
        # HTMLParser guarantees strict order of callbacks during a single parse
        start_offset = self._find_in_remaining(start_text)
        if start_offset is None:
            return

        end_offset = start_offset + len(start_text)
        # Insert role="main" right before the closing '>'
        new_text = start_text[:-1].rstrip() + ' role="main">'
        self.rewrites.append((start_offset, end_offset, new_text))

    def _find_in_remaining(self, needle: str) -> int | None:
        """Find needle in self.rawdata starting from self._pos. Returns absolute offset."""
        haystack = self.rawdata
        idx = haystack.find(needle, self._pos)
        if idx == -1:
            return None
        self._pos = idx + 1
        return idx

    def error(self, message: str) -> None:
        # Don't crash on minor parse issues — log and continue.
        print(f"  parser warning: {message}", file=sys.stderr)


def process_file(path: Path, dry_run: bool = False) -> bool:
    """Returns True if file was modified (or would be, in dry-run)."""
    text = path.read_text(encoding='utf-8', errors='ignore')
    if 'id="content"' not in text:
        return False

    parser = MainLandmarkAdder()
    try:
        parser.feed(text)
        parser.close()
    except Exception as e:
        print(f"  parse error in {path}: {e}", file=sys.stderr)
        return False

    if not parser.rewrites:
        return False

    # Apply rewrites in reverse order so offsets remain valid
    new_text = text
    for start, end, replacement in sorted(parser.rewrites, key=lambda r: -r[0]):
        new_text = new_text[:start] + replacement + new_text[end:]

    if not dry_run:
        path.write_text(new_text, encoding='utf-8')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Add role="main" to #content divs site-wide.')
    parser.add_argument('--dry-run', action='store_true', help='Report changes without writing.')
    args = parser.parse_args()

    files = sorted(ROOT.rglob('*.html'))
    modified = 0
    skipped = 0

    for f in files:
        if process_file(f, dry_run=args.dry_run):
            modified += 1
        else:
            skipped += 1

    action = 'would modify' if args.dry_run else 'modified'
    print(f"Processed {len(files)} files: {modified} {action}, {skipped} skipped")
    return 0


if __name__ == '__main__':
    sys.exit(main())