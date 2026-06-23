#!/usr/bin/env python3
"""
GRO-585/A11y: Add role="main" to all <div id="content" class="site-content"> elements.

Resolves Lighthouse 'landmark-one-main' audit failure (a11y weight 3).

Before: <div class="site-content" id="content">
After:  <div class="site-content" id="content" role="main">

Idempotent: skips files that already have role="main" on the content div.
"""
from pathlib import Path
import re

ROOT = Path(__file__).parent.parent / 'site'

# Match the opening div tag with id="content"
# Pattern: <div [class="site-content"] id="content"> optionally with other attrs
PATTERN = re.compile(
    r'<div(\s+[^>]*?)?(\sid="content")([^>]*?)>',
    re.IGNORECASE
)

def has_role_main(s):
    """Check if the tag already has role='main' or role=main."""
    return bool(re.search(r'role\s*=\s*["\']main["\']', s, re.IGNORECASE))

def process_file(path: Path) -> bool:
    """Returns True if file was modified."""
    text = path.read_text(encoding='utf-8', errors='ignore')
    
    # Quick check: does this file even have id="content"?
    if 'id="content"' not in text:
        return False
    
    # Find all opening div tags with id="content"
    new_text = text
    modified = False
    
    for m in PATTERN.finditer(text):
        full_tag = m.group(0)
        if has_role_main(full_tag):
            continue
        # Insert role="main" before the closing >
        old_tag = full_tag
        new_tag = full_tag[:-1] + ' role="main">'
        new_text = new_text.replace(old_tag, new_tag, 1)
        modified = True
        # Only process first match per file (there's typically only one #content)
        break
    
    if modified:
        path.write_text(new_text, encoding='utf-8')
        return True
    return False

def main():
    files = list(ROOT.rglob('*.html'))
    modified = 0
    skipped = 0
    
    for f in files:
        if process_file(f):
            modified += 1
        else:
            skipped += 1
    
    print(f"Processed {len(files)} files: {modified} modified, {skipped} skipped (already had role=main or no #content)")

if __name__ == '__main__':
    main()
