#!/usr/bin/env python3
"""Fix Kadence CSS links on all HTML pages - dedup, fix hrefs, ensure all 5 present + strip/extract inline Kadence CSS."""
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

# Pattern to match inline Kadence CSS style tag
inline_css_re = re.compile(r"<style[^>]*id=['\"]kadence_blocks_css-inline-css['\"][^>]*>(.*?)</style>", re.DOTALL)
default_sig = "id2389"

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
        
        # Step 6: Handle inline Kadence CSS block
        match = inline_css_re.search(content)
        if match:
            css_text = match.group(1).strip()
            
            # Check if homepage
            if fname == 'index.html' and root == SITE:
                # Extract homepage styles to kadence-homepage.css
                css_dir = os.path.join(SITE, 'wp-content', 'themes', 'activeoahu', 'css')
                os.makedirs(css_dir, exist_ok=True)
                css_fpath = os.path.join(css_dir, 'kadence-homepage.css')
                with open(css_fpath, 'w', encoding='utf-8') as css_file:
                    css_file.write(css_text)
                
                # Replace inline style with link to the file
                link_tag = "<link rel='stylesheet' id='kadence-homepage-css' href='/wp-content/themes/activeoahu/css/kadence-homepage.css' type='text/css' media='all' />\n"
                content = inline_css_re.sub(link_tag, content)
                print("Extracted homepage CSS to kadence-homepage.css")
            else:
                # Check if it has the default homepage signature (which means it's unused template bloat on other pages)
                if default_sig in css_text:
                    # Strip entirely
                    content = inline_css_re.sub('', content)
                else:
                    # Extract page-specific unique styles to inline-{slug}.css
                    rel_path = os.path.relpath(fpath, SITE)
                    slug = rel_path.replace('/index.html', '').replace('.html', '').replace('/', '-')
                    
                    css_dir = os.path.join(SITE, 'wp-content', 'themes', 'activeoahu', 'css')
                    os.makedirs(css_dir, exist_ok=True)
                    css_fpath = os.path.join(css_dir, f"inline-{slug}.css")
                    with open(css_fpath, 'w', encoding='utf-8') as css_file:
                        css_file.write(css_text)
                    
                    link_tag = f"<link rel='stylesheet' id='kadence-inline-{slug}-css' href='/wp-content/themes/activeoahu/css/inline-{slug}.css' type='text/css' media='all' />\n"
                    content = inline_css_re.sub(link_tag, content)
                    print(f"Extracted unique page CSS for {rel_path} to inline-{slug}.css")
                    
        # Step 7: Clean up spacing that might be left over from removing style tag
        content = re.sub(r'\n{4,}', '\n\n', content)
        
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
