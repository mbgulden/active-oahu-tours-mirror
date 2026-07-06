#!/usr/bin/env python3
"""
add_main_landmark.py — Wrap the primary content area of each AOT HTML page
with a <main> landmark, satisfying Lighthouse's landmark-one-main audit.

Two page patterns are supported (detected automatically):
  1. Standard WP theme pages: <div id="content" class="site-content"> ... </div>
     → wrap with <main id="content" class="site-content"> ... </main>
  2. Custom guide pages (no site-content wrapper): <body> ... </body>
     → wrap the inner body content with <main> ... </main>

Idempotent: re-running on an already-wrapped page is a no-op (skipped).
Safe: HTMLParser-based, never uses regex on HTML (per AGY audit lessons).
Usage:
  python3 scripts/add_main_landmark.py --dry-run              # show what would change
  python3 scripts/add_main_landmark.py --site-dir site        # apply changes
  python3 scripts/add_main_landmark.py --file path/to/x.html  # single file
"""

import argparse
import sys
from pathlib import Path
from html.parser import HTMLParser


class MainLandmarkWrapper(HTMLParser):
    """
    Walks the HTML and identifies where to insert <main> / </main>.
    Strategy:
      - If page has <div id="content" class="site-content">, mark that as wrap start.
      - Else if page has <body> with no <main> already, wrap the body inner content.
    Tracks open/close tag positions so we know where to insert.
    """

    def __init__(self, filepath: str):
        super().__init__(convert_charrefs=True)
        self.filepath = filepath
        self.lines = Path(filepath).read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        # Pre-compute char offset for each line so we can splice
        self.line_offsets = []
        running = 0
        for line in self.lines:
            self.line_offsets.append(running)
            running += len(line)
        self.text = "".join(self.lines)

        # State
        self.has_main = False
        self.has_site_content = False
        self.site_content_open_pos = None  # (start, end) of the opening div tag
        self.site_content_div_depth = 0
        self.site_content_close_pos = None  # (start, end) of the matching close
        self.body_open_pos = None
        self.body_close_pos = None
        self.in_body = False
        self.body_depth_inside_main = 0
        self.in_main = False
        self.main_open_pos = None
        self.main_close_pos = None

        # Drive the parser: feed() + close() are HTMLParser's parse methods
        self.feed(self.text)
        self.close()

    def _tag_pos(self, tag: str, attrs, self_closing: bool):
        """Reconstruct the tag string with original attrs to find its position."""
        attr_str = ""
        for k, v in attrs:
            if v is None:
                attr_str += f" {k}"
            else:
                attr_str += f' {k}="{v}"'
        sl = " /" if self_closing else ""
        return f"<{tag}{attr_str}{sl}>"

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.has_main = True
            self.in_main = True
            self.main_open_pos = self.getpos()
        elif tag == "body":
            self.in_body = True
            self.body_open_pos = self.getpos()
        elif tag == "div" and not self.in_main:
            attr_dict = dict(attrs)
            if attr_dict.get("id") == "content" and "site-content" in (attr_dict.get("class") or ""):
                if not self.has_site_content:
                    self.has_site_content = True
                    self.site_content_open_pos = self.getpos()
                    self.site_content_div_depth = 1
        elif self.has_site_content and tag == "div":
            self.site_content_div_depth += 1

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
            self.main_close_pos = self.getpos()
        elif tag == "body":
            self.in_body = False
            self.body_close_pos = self.getpos()
        elif self.has_site_content and tag == "div":
            self.site_content_div_depth -= 1
            if self.site_content_div_depth == 0:
                self.site_content_close_pos = self.getpos()

    def has_comment_marker_after_close(self) -> bool:
        """Returns True if the closing </div> is followed by '<!-- #content -->'
        marker (WordPress convention). Used to disambiguate which </div>
        corresponds to the outer site-content div when there are nested
        <div id="content"> inside (23 affected files)."""
        if self.site_content_close_pos is None:
            return False
        def offset_from_pos(pos):
            if pos is None:
                return -1
            line, col = pos
            line_idx = line - 1
            if line_idx < 0 or line_idx >= len(self.line_offsets):
                return -1
            return self.line_offsets[line_idx] + (col - 1)
        close_offset = offset_from_pos(self.site_content_close_pos)
        if close_offset < 0:
            return False
        search_end = min(close_offset + 80, len(self.text))
        chunk = self.text[close_offset:search_end]
        return '<!-- #content -->' in chunk

    def has_landmark_issue(self) -> bool:
        """Returns True if the page is missing <main>."""
        return not self.has_main

    def compute_edit(self) -> tuple[list[tuple[int, int, str]], str]:
        """
        Returns (edits, mode) where edits is a list of (offset, length, replacement)
        and mode is 'standard' (wrap site-content) or 'body' (wrap entire body inner).
        Offsets are byte offsets into self.text.
        """
        if not self.has_landmark_issue():
            return [], "skip"

        # Compute byte offsets from line/column
        def offset_from_pos(pos):
            if pos is None:
                return -1
            line, col = pos
            # HTMLParser columns are 1-indexed char positions on the line
            line_idx = line - 1
            if line_idx < 0 or line_idx >= len(self.line_offsets):
                return -1
            return self.line_offsets[line_idx] + (col - 1)

        if self.has_site_content:
            # Mode: standard — wrap the site-content div as <main>
            # We replace ONLY the opening tag and the matching closing tag's `</div>` -> `</main>`.
            # The opening <div id="content" class="site-content"> becomes <main id="content" class="site-content">.
            open_line, open_col = self.site_content_open_pos
            # The tag itself extends from the '<' to the '>'. We need to find those bounds in self.text.
            open_offset = offset_from_pos(self.site_content_open_pos)
            open_end = self.text.find(">", open_offset) + 1
            close_line, close_col = self.site_content_close_pos
            close_offset = offset_from_pos(self.site_content_close_pos)
            # Same edge case: parser reports post-tag position which may be col 0 of next line.
            search_end = min(close_offset + 20, len(self.text))
            close_start = self.text.find("</div>", close_offset, search_end)
            if close_start < 0:
                close_start = self.text.rfind("</div>", 0, close_offset + 1)
            close_end = close_start + len("</div>")

            original_open = self.text[open_offset:open_end]
            original_close = self.text[close_start:close_end]
            new_open = original_open.replace("<div", "<main", 1).replace("</div>", "</main>", 0)
            # Ensure the new opening has no slash for self-closing (it shouldn't — site-content is a container)
            new_open = new_open.replace(" />", ">")
            new_close = "</main>"

            return [
                (open_offset, open_end - open_offset, new_open),
                (close_start, close_end - close_start, new_close),
            ], "standard"
        else:
            # Mode: body — wrap everything inside <body>...</body> with <main>...</main>
            body_open_offset = offset_from_pos(self.body_open_pos)
            body_open_end = self.text.find(">", body_open_offset) + 1
            body_close_offset = offset_from_pos(self.body_close_pos)
            # body_close_pos may be at col 0 of the next line (parser reports post-tag position).
            # Search for </body> within a small lookahead window after that offset.
            search_end = min(body_close_offset + 20, len(self.text))
            body_close_start = self.text.find("</body>", body_close_offset, search_end)
            if body_close_start < 0:
                body_close_start = self.text.rfind("</body>", 0, body_close_offset + 1)
            body_close_end = body_close_start + len("</body>")

            return [
                (body_open_end, 0, "\n<main>\n"),
                (body_close_start, 0, "\n</main>\n"),
            ], "body"


def apply_edits(text: str, edits: list[tuple[int, int, str]]) -> str:
    """Apply edits right-to-left so earlier offsets stay valid."""
    out = text
    for offset, length, replacement in sorted(edits, key=lambda e: -e[0]):
        out = out[:offset] + replacement + out[offset + length:]
    return out


def process_file(filepath: Path, dry_run: bool) -> str:
    """Returns 'changed', 'skipped', or 'error'."""
    try:
        wrapper = MainLandmarkWrapper(str(filepath))
    except Exception as e:
        print(f"  ERROR parsing {filepath}: {e}", file=sys.stderr)
        return "error"

    if not wrapper.has_landmark_issue():
        return "skipped"

    edits, mode = wrapper.compute_edit()
    if mode == "skip" or not edits:
        return "skipped"

    # Validate: all edit offsets must be non-negative
    for off, ln, _ in edits:
        if off < 0 or ln < 0:
            print(f"  SKIP (invalid offsets) {filepath}", file=sys.stderr)
            return "skipped"

    original = wrapper.text
    updated = apply_edits(original, edits)

    if not dry_run:
        filepath.write_text(updated, encoding="utf-8")
    return "changed"


def main():
    parser = argparse.ArgumentParser(description="Add <main> landmark to AOT HTML pages")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--site-dir", default="site", help="Site root (default: site)")
    parser.add_argument("--file", help="Process a single file instead of a directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show per-file status")
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
            rel = f.relative_to(Path(args.site_dir)) if not args.file else f
            print(f"  [+] {rel}")

    print(f"\nResults: changed={counts['changed']}  skipped={counts['skipped']}  error={counts['error']}")
    if args.dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    main()