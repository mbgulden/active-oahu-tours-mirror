#!/usr/bin/env python3
"""Fix all relative asset paths on HTML pages to use absolute /wp-content/ paths.
This fixes broken images, srcset URLs, and other asset references from deep pages."""
import os, re, json

SITE = os.path.join(os.path.dirname(__file__), 'site')

# Collect all duplicate image paths to report
total_fixes = 0
fixed_files = 0

for root, dirs, files in os.walk(SITE):
    if '_templates' in root:
        continue
    for fname in files:
        if not fname.endswith('.html') or fname == 'head.html':
            continue
        
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        changes = 0
        
        # Fix 1: src="../../wp-content/..." -> src="/wp-content/..."
        # Matches any depth of relative path like ../, ../../, ../../../ etc.
        content, count1 = re.subn(
            r'(src|href|srcset)="(?:\.\./)+(wp-content/[^"]*)"',
            r'\1="/\2"',
            content
        )
        changes += count1
        
        # Fix 2: src='../../wp-content/...' -> src='/wp-content/...'
        content, count2 = re.subn(
            r"(src|href|srcset)='(?:\.\./)+(wp-content/[^']*)'",
            r"\1='/wp-content/\2'",
            content
        )
        # Wait, the capture group will capture "wp-content/..." but the path might 
        # have extra ../ at the start that need stripping. Let me be more careful.
        # Actually the regex above captures (wp-content/...) which is correct - 
        # the (?:\.\./)+ matches the leading ../ and discards them.
        # Then \1='/wp-content/\2' inserts the absolute path.
        changes += count2
        
        # Fix 3: srcset URLs with relative paths (multiple URLs separated by comma)
        # e.g., srcset="../../wp-content/uploads/img.jpg 1024w, ../../wp-content/..."
        def fix_srcset(m):
            urls = m.group(1)
            fixed = re.sub(r'(?:\.\./)+(wp-content/)', r'/\1', urls)
            return f'srcset="{fixed}"'
        
        content, count3 = re.subn(
            r'srcset="((?:[^"]*\.\./)+[^"]*)"',
            fix_srcset,
            content
        )
        changes += count3
        
        # Fix 4: Same for single-quoted srcset
        def fix_srcset_single(m):
            urls = m.group(1)
            fixed = re.sub(r'(?:\.\./)+(wp-content/)', r'/\1', urls)
            return f"srcset='{fixed}'"
        
        content, count4 = re.subn(
            r"srcset='((?:[^']*\.\./)+[^']*)'",
            fix_srcset_single,
            content
        )
        changes += count4
        
        # Fix 5: Data attributes like data-full-image, data-light-image with relative paths
        content, count5 = re.subn(
            r'(data-(?:full-image|light-image))="(?:\.\./)+(wp-content/[^"]*)"',
            r'\1="/\2"',
            content
        )
        changes += count5
        
        if changes > 0:
            fixed_files += 1
            total_fixes += changes
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

print(f"Fixed {total_fixes} asset paths across {fixed_files} files")

# Verify sample pages
test_pages = [
    'oahu-kayaking-and-beach-adventures/ultimate-guide-to-lanikai-beach/index.html',
    'activities/kailua-kayak-twin-islands-guided-tour/index.html',
    'index.html',
]
print("\n=== Verification samples ===")
for page in test_pages:
    fpath = os.path.join(SITE, page)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        # Count remaining relative paths
        remaining = len(re.findall(r'(?:\.\./)+(wp-content/)', content))
        abs_count = content.count('/wp-content/')
        print(f"  {page}: {abs_count} absolute, {remaining} relative")
