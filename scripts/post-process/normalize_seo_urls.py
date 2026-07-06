#!/usr/bin/env python3
"""
normalize_seo_urls.py — POST-PROCESSOR: Normalize canonical/hreflang to absolute URLs across all AOT HTML files.

Runs as part of the deploy pipeline (after generators, before CF Pages deploy).
Idempotent — safe to re-run on every deploy.

Why this exists:
- The template (site/_templates/head.html) is the source of truth for new pages
- Six Python generators consume the template and write absolute canonical URLs
- But ~130 legacy WordPress-export files bypass the template entirely
- WordPress Yoast SEO plugin emits relative paths (e.g. href="/")
- This post-processor normalizes everything to absolute URLs so Lighthouse audits pass

Patterns fixed:
  - <link rel="canonical" href="/path" />     → href="https://activeoahutours.com/path"
  - <link rel="alternate" href="/path" hreflang="x" /> → href="https://activeoahutours.com/path"

Idempotent: re-running on already-fixed pages is a no-op.

Usage:
  python3 scripts/fix_seo_urls.py --dry-run   # show what would change
  python3 scripts/fix_seo_urls.py             # apply changes
"""

import argparse
import re
import sys
from pathlib import Path

CANONICAL_RE = re.compile(
    # Match canonical links in either attribute order: rel-then-href OR href-then-rel
    r'<link\s+(?:rel="canonical"\s+href="([^"]*)"|href="([^"]*)"\s+rel="canonical")',
    re.IGNORECASE,
)
HREFLANG_RE = re.compile(
    # Match hreflang links in any of the common attribute orderings
    r'<link\s+(?:'
    r'rel="alternate"\s+href="([^"]*)"\s+hreflang="([^"]*)"'  # rel, href, hreflang
    r'|href="([^"]*)"\s+hreflang="([^"]*)"\s+rel="alternate"'  # href, hreflang, rel
    r'|rel="alternate"\s+hreflang="([^"]*)"\s+href="([^"]*)"'  # rel, hreflang, href (rare)
    r')',
    re.IGNORECASE,
)

BASE_URL = "https://activeoahutours.com"


def absolutize_href(href: str) -> str:
    """Convert relative path to absolute URL. Pass-through for already-absolute URLs."""
    if href.startswith(("http://", "https://")):
        return href
    if not href.startswith("/"):
        href = "/" + href
    return BASE_URL + href


def _join_url(href: str) -> str:
    # Pass through absolute URLs unchanged
    if href.startswith(("http://", "https://")):
        return href
    if not href.startswith("/"):
        href = "/" + href
    return BASE_URL + href


def process_text(text: str, filepath: str) -> tuple[str, int, int]:
    """Returns (new_text, canonical_changes, hreflang_changes)."""
    canon_count = 0
    hreflang_count = 0

    def canon_repl(m):
        nonlocal canon_count
        # group(1) populated when rel comes first; group(2) when href comes first
        if m.group(1) is not None:
            old_href = m.group(1)
            new_href = _join_url(old_href)
            if old_href == new_href:
                return m.group(0)
            canon_count += 1
            return f'<link rel="canonical" href="{new_href}"'
        else:
            old_href = m.group(2)
            new_href = _join_url(old_href)
            if old_href == new_href:
                return m.group(0)
            canon_count += 1
            return f'<link href="{new_href}" rel="canonical"'

    def hreflang_repl(m):
        nonlocal hreflang_count
        # 3 possible orderings → 3 (href, lang) pair possibilities
        if m.group(1) is not None:  # rel, href, lang
            href, lang = m.group(1), m.group(2)
            prefix_template = '<link rel="alternate" href="{href}" hreflang="{lang}"'
        elif m.group(3) is not None:  # href, lang, rel
            href, lang = m.group(3), m.group(4)
            prefix_template = '<link href="{href}" hreflang="{lang}" rel="alternate"'
        else:  # rel, lang, href
            href, lang = m.group(6), m.group(5)
            prefix_template = '<link rel="alternate" hreflang="{lang}" href="{href}"'

        new_href = _join_url(href)
        if href == new_href:
            return m.group(0)
        hreflang_count += 1
        return prefix_template.format(href=new_href, lang=lang)

    new_text = CANONICAL_RE.sub(canon_repl, text)
    new_text = HREFLANG_RE.sub(hreflang_repl, new_text)

    return new_text, canon_count, hreflang_count


def process_file(filepath: Path, dry_run: bool, verbose: bool) -> tuple[str, int, int]:
    """Returns ('changed'|'skipped', canonical_changes, hreflang_changes)."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ERROR reading {filepath}: {e}", file=sys.stderr)
        return "error", 0, 0

    new_text, canon_count, hreflang_count = process_text(text, str(filepath))

    if canon_count == 0 and hreflang_count == 0:
        return "skipped", 0, 0

    if verbose:
        rel = filepath.name
        print(f"  [+] {rel}: canonical={canon_count} hreflang={hreflang_count}")

    if not dry_run:
        filepath.write_text(new_text, encoding="utf-8")

    return "changed", canon_count, hreflang_count


def main():
    parser = argparse.ArgumentParser(description="Fix canonical/hreflang URLs to absolute")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--site-dir", default="site", help="Site root")
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
    total_canon = 0
    total_hreflang = 0
    for f in files:
        result, c, h = process_file(f, args.dry_run, args.verbose)
        counts[result] += 1
        total_canon += c
        total_hreflang += h

    print(f"\nResults: changed={counts['changed']}  skipped={counts['skipped']}  error={counts['error']}")
    print(f"  Canonical fixes: {total_canon}")
    print(f"  Hreflang fixes:  {total_hreflang}")
    if args.dry_run:
        print("(dry run — no files written)")


if __name__ == "__main__":
    main()