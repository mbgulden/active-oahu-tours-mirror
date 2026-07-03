#!/usr/bin/env python3
"""
fix_main_landmark_close.py — Recovery script for 23 files where add_main_landmark.py
incorrectly closed the <main> tag at the wrong </div>.

The bug: add_main_landmark.py tracked div depth from the FIRST <div id="content" class="site-content">
open, then closed <main> at the FIRST </div> after. But 23 files have a SECOND nested
<div id="content" class="site-content"> inside, so the tracker closed <main> too early.

This script:
  1. Finds the broken </main> in the wrong place
  2. Removes it
  3. Finds the real outer </div><!-- #content --> close
  4. Replaces it with </main><!-- #content -->

Uses the <!-- #content --> marker to uniquely identify the correct close (all 23 files
have this WordPress convention marker).

Idempotent: if the </main> is already in the right place, no-op.

Usage:
  python3 scripts/fix_main_landmark_close.py --dry-run
  python3 scripts/fix_main_landmark_close.py
"""

import argparse
import re
import sys
from pathlib import Path


CONTENT_MARKER_PATTERN = re.compile(r'</div>\s*<!--\s*#content\s*-->')
BROKEN_MAIN_CLOSE = re.compile(r'</main>\s*<!--\s*\.entry-content\s*-->\s*</div>')
# Pattern: redundant inner <div id="content" class="site-content"> wrapping <div class="entry-content">
# The inner div has the same id as the outer <main>, so it must be removed entirely,
# with its content (the entry-content div) moving up to be a direct child of <main>.
REDUNDANT_INNER_DIV_PATTERN = re.compile(
    r'<div\s+id="content"\s+class="site-content">\s*\n\s*<div\s+class="entry-content">(.*?)</div>\s*<!--\s*\.entry-content\s*-->\s*\n\s*</div>',
    re.DOTALL,
)


def fix_file(text: str) -> tuple[str, bool]:
    """Returns (new_text, changed)."""
    changed = False

    # Step 1: Detect if </main> is in the wrong place. The correct place is
    # immediately before the <!-- #content --> marker. If </main> appears
    # BEFORE that marker, it's misplaced.
    content_marker_match = CONTENT_MARKER_PATTERN.search(text)
    if content_marker_match:
        marker_pos = content_marker_match.start()
        # Find ALL </main> occurrences
        main_close_positions = [m.start() for m in re.finditer(r'</main>', text)]

        # If any </main> appears before the marker, it's misplaced.
        misplaced_closes = [pos for pos in main_close_positions if pos < marker_pos]

        if misplaced_closes:
            # Remove all misplaced </main> tags (replace with empty string)
            for pos in reversed(misplaced_closes):
                # Find the full tag including any whitespace
                end_pos = text.find('>', pos) + 1
                text = text[:pos] + text[end_pos:]
            # Now replace the </div><!-- #content --> marker with </main><!-- #content -->
            text, n = CONTENT_MARKER_PATTERN.subn('</main><!-- #content -->', text, count=1)
            if n > 0:
                changed = True

    # Step 2: Remove redundant inner <div id="content" class="site-content"> wrapper.
    # The inner div has the same id as the outer <main>, so it must be removed.
    # Its content (the entry-content div) moves up to be a direct child of <main>.
    # Runs independently of step 1 — applies whenever the duplicate exists.
    if 'id="content" class="site-content"' in text and '<main id="content"' in text:
        def strip_inner_div(m):
            inner = m.group(1)
            return f'<div class="entry-content">{inner}</div>'

        new_text, n = REDUNDANT_INNER_DIV_PATTERN.subn(strip_inner_div, text, count=1)
        if n > 0:
            text = new_text
            changed = True

    return text, changed


def validate_structure(text: str, filepath: Path) -> tuple[bool, list[str]]:
    """Validates that the <main> landmark is properly placed AFTER fixes.

    We don't do deep HTML structure validation — WordPress output is messy and
    has many non-LIFO patterns that would cause false positives. Instead, we just
    check that:
      - Exactly one <main> opens and one </main> closes
      - id="content" appears exactly once (no duplicate IDs)
      - The <main> close happens AFTER the <!-- #content --> marker (or there's
        no marker, in which case we don't check)

    If any of these fail, validation fails.
    """
    import re
    errors = []

    # Count main tags
    main_opens = len(re.findall(r'<main\b', text))
    main_closes = len(re.findall(r'</main>', text))
    if main_opens != 1 or main_closes != 1:
        errors.append(f'<main> count: opens={main_opens} closes={main_closes}')

    # Count duplicate id="content"
    id_content_count = len(re.findall(r'id="content"', text))
    if id_content_count != 1:
        errors.append(f'id="content" appears {id_content_count} times (expected 1)')

    # If we have the <!-- #content --> marker, the </main> should appear before it
    if '<!-- #content -->' in text:
        main_pos = text.find('</main>')
        marker_pos = text.find('<!-- #content -->')
        if main_pos > marker_pos:
            errors.append(f'</main> appears AFTER <!-- #content --> marker')

    if errors:
        return False, errors
    return True, []


def process_file(filepath: Path, dry_run: bool, verbose: bool) -> str:
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}", file=sys.stderr)
        return "error"

    new_text, changed = fix_file(text)
    if not changed:
        return "skipped"

    # Validate the AFTER state (focus on <main> integrity only)
    valid, errors = validate_structure(new_text, filepath)
    if not valid:
        print(f"  SKIP (validation failed): {filepath}", file=sys.stderr)
        for e in errors[:5]:
            print(f"    {e}", file=sys.stderr)
        return "skipped"

    if verbose:
        print(f"  [+] {filepath.name}")
    if not dry_run:
        filepath.write_text(new_text, encoding="utf-8")
    return "changed"


def main():
    parser = argparse.ArgumentParser(description="Fix broken <main> closing in 23 affected files")
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
        result = process_file(f, args.dry_run, args.verbose)
        counts[result] += 1

    print(f"\nResults: changed={counts['changed']}  skipped={counts['skipped']}  error={counts['error']}")
    if args.dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    main()