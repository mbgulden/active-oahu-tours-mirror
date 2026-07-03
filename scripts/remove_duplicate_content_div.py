#!/usr/bin/env python3
"""
remove_duplicate_content_div.py — Remove the inner redundant <div id="content" class="site-content">
that exists inside the newly-wrapped <main id="content"> in 23 files.

The pre-existing markup on those 23 files was:
    <div id="content" class="site-content">
        <div id="content" class="site-content">    ← redundant inner div
            ... actual content ...
        </div>
    </div>

The lighthouse cycle 001 wrapped the outer div as <main>, leaving the inner one as
a duplicate ID. This script removes the inner one (and its matching close tag),
keeping the content intact under <main>.

Idempotent: if the inner <div id="content"> is already gone, no-op.
Safe: HTMLParser-based, never uses regex on HTML structure.
"""

import argparse
import sys
from pathlib import Path
from html.parser import HTMLParser


class InnerContentDivRemover(HTMLParser):
    """Detect the pattern <main id="content"> ... <div id="content"> ... </div> ... </main>
    and remove the inner <div id="content" class="site-content"> ... </div> wrapper.

    Strategy: walk the HTML, find the inner div's tag boundaries, splice them out.
    """

    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.text = text
        self.lines = text.splitlines(keepends=True)
        self.line_offsets = []
        running = 0
        for line in self.lines:
            self.line_offsets.append(running)
            running += len(line)

        # Track states
        self.depth_in_main_with_id_content = 0
        self.outer_is_main = False
        self.inner_div_depth = 0
        self.inner_div_open_pos = None  # (line, col) where <div id="content"> opens
        self.inner_div_close_pos = None  # (line, col) where matching </div> closes
        self.has_duplicate = False

        self.feed(text)
        self.close()

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        is_content_id = attr_dict.get("id") == "content" and "site-content" in (attr_dict.get("class") or "")

        if tag == "main" and is_content_id and not self.outer_is_main:
            self.outer_is_main = True
            self.depth_in_main_with_id_content = 1
        elif self.outer_is_main and tag == "div" and is_content_id and self.inner_div_open_pos is None:
            # Found the inner duplicate
            self.inner_div_open_pos = self.getpos()
            self.inner_div_depth = 1
            self.has_duplicate = True
        elif self.outer_is_main and self.inner_div_open_pos is not None and tag == "div":
            self.inner_div_depth += 1

    def handle_endtag(self, tag):
        if self.outer_is_main and tag == "main" and self.inner_div_open_pos is None:
            self.outer_is_main = False
        elif self.outer_is_main and self.inner_div_open_pos is not None and tag == "div":
            self.inner_div_depth -= 1
            if self.inner_div_depth == 0:
                self.inner_div_close_pos = self.getpos()

    def compute_removal(self) -> tuple[int, int] | None:
        """Returns (start_offset, end_offset) to remove (the inner div tags only), or None."""
        if not self.has_duplicate or self.inner_div_open_pos is None or self.inner_div_close_pos is None:
            return None

        def offset_from_pos(pos):
            line, col = pos
            line_idx = line - 1
            if line_idx < 0 or line_idx >= len(self.line_offsets):
                return -1
            return self.line_offsets[line_idx] + (col - 1)

        # Inner open: <div id="content" class="site-content"> — start at '<', end at '>'
        open_offset = offset_from_pos(self.inner_div_open_pos)
        open_end = self.text.find(">", open_offset) + 1

        # Inner close: </div> — find the matching tag
        close_offset = offset_from_pos(self.inner_div_close_pos)
        # close_pos may be at col 0 of next line
        search_end = min(close_offset + 20, len(self.text))
        close_start = self.text.find("</div>", close_offset, search_end)
        if close_start < 0:
            close_start = self.text.rfind("</div>", 0, close_offset + 1)
        close_end = close_start + len("</div>")

        if open_offset < 0 or close_start < 0:
            return None

        return (open_offset, close_end)


def process_file(filepath: Path, dry_run: bool) -> str:
    """Returns 'changed', 'skipped', or 'error'."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}", file=sys.stderr)
        return "error"

    remover = InnerContentDivRemover(text)
    removal = remover.compute_removal()

    if removal is None:
        return "skipped"

    start, end = removal
    updated = text[:start] + text[end:]

    # Verify HTML is still well-formed
    try:
        from html.parser import HTMLParser
        class V(HTMLParser):
            def __init__(self):
                super().__init__()
                self.stack = []
                self.errors = []
            def handle_starttag(self, tag, attrs):
                if tag in ('div', 'main', 'section', 'article', 'header', 'footer', 'nav', 'aside'):
                    self.stack.append((tag, self.getpos()))
            def handle_endtag(self, tag):
                if tag in ('div', 'main', 'section', 'article', 'header', 'footer', 'nav', 'aside'):
                    if self.stack and self.stack[-1][0] == tag:
                        self.stack.pop()
                    else:
                        self.errors.append(f'mismatched </{tag}> at {self.getpos()}')

        v = V()
        v.feed(updated)
        if v.errors or v.stack:
            print(f"  SKIP (would break HTML structure): {filepath}", file=sys.stderr)
            print(f"    errors={v.errors[:3]}, unclosed={v.stack[:3]}", file=sys.stderr)
            return "skipped"
    except Exception as e:
        print(f"  SKIP (validation error): {filepath}: {e}", file=sys.stderr)
        return "skipped"

    if not dry_run:
        filepath.write_text(updated, encoding="utf-8")
    return "changed"


def main():
    parser = argparse.ArgumentParser(description="Remove redundant inner <div id=\"content\"> wrappers")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--site-dir", default="site")
    parser.add_argument("--file", help="Process single file")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.file:
        files = [Path(args.file)]
    else:
        root = Path(args.site_dir)
        files = [p for p in root.rglob("*.html") if "_templates" not in p.parts and "_seo" not in p.parts]

    print(f"Scanning {len(files)} HTML files (dry_run={args.dry_run})...")
    counts = {"changed": 0, "skipped": 0, "error": 0}
    for f in files:
        result = process_file(f, args.dry_run)
        counts[result] += 1
        if args.verbose and result == "changed":
            print(f"  [+] {f.relative_to(Path(args.site_dir))}")

    print(f"\nResults: changed={counts['changed']}  skipped={counts['skipped']}  error={counts['error']}")
    if args.dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    main()