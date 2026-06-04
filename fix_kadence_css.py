#!/usr/bin/env python3
"""Fix Kadence CSS links on all HTML pages - dedup, fix hrefs, ensure all 5 present."""
import os, re, sys

SITE = os.path.join(os.path.dirname(__file__), 'site')
KADENCE_ORDER = ['rowlayout', 'column', 'image', 'advancedbtn', 'advancedgallery']
KADENCE_LINKS = {
    name: f"<link rel='stylesheet' id='kadence-blocks-{name}-css' href='/wp-content/plugins/kadence-blocks/dist/style-blocks-{name}.css' type='text/css' media='all' />"
    for name in KADENCE_ORDER
}

# Pattern to match any Kadence block <link> tag
kadence_link_re = re.compile(
    r"<link[^>]*id=['\"]kadence-blocks-(?:%s)-css['\"][^>]*>" % '|'.join(KADENCE_ORDER)
)

fixed_count = 0

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
        
        # Step 1: Fix wrong hrefs (advancedgallery pointing to image.css)
        content = re.sub(
            r"<link[^>]*id=['\"]kadence-blocks-advancedgallery-css['\"][^>]*style-blocks-image\.css[^>]*>",
            KADENCE_LINKS['advancedgallery'],
            content
        )
        
        # Step 2: Remove all existing Kadence block link tags
        content = kadence_link_re.sub('', content)
        
        # Step 3: Clean up excessive blank lines
        content = re.sub(r'\n{4,}', '\n\n', content)
        
        # Step 4: Build clean Kadence block
        kadence_block = '\n'.join(KADENCE_LINKS[name] for name in KADENCE_ORDER) + '\n'
        
        # Step 5: Insert Kadence block before style-style-css
        content = re.sub(
            r"(<link[^>]*style-style-css[^>]*>)",
            kadence_block + r'\1',
            content,
            count=1
        )
        
        if content != original:
            fixed_count += 1
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)

print(f"Fixed {fixed_count} pages")

# Verification
print("\n=== Presence by Kadence file ===")
for name in KADENCE_ORDER:
    count = 0
    for root, dirs, files in os.walk(SITE):
        if '_templates' in root:
            continue
        for fname in files:
            if fname.endswith('.html'):
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if f'style-blocks-{name}.css' in content:
                    count += 1
    print(f"  {name}: {count} pages")

print("\n=== Duplicate check ===")
dup_found = False
for root, dirs, files in os.walk(SITE):
    if '_templates' in root:
        continue
    for fname in files:
        if fname.endswith('.html'):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            for name in KADENCE_ORDER:
                count = content.count(f'style-blocks-{name}.css')
                if count > 1:
                    print(f"  DUPLICATE {name}: {fpath}")
                    dup_found = True
                    break
if not dup_found:
    print("  No duplicates found!")

print("\n=== Wrong href check ===")
wrong_count = 0
for root, dirs, files in os.walk(SITE):
    if '_templates' in root:
        continue
    for fname in files:
        if fname.endswith('.html'):
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if re.search(r'advancedgallery-css[^>]*style-blocks-image\.css', content):
                print(f"  WRONG: {fpath}")
                wrong_count += 1
print(f"  Wrong hrefs: {wrong_count}")
