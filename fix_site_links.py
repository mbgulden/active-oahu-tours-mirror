#!/usr/bin/env python3
"""
Fix relative and root-relative links to the guided and self-guided Mokulua Islands kayak tours.
Corrects any trailing spaces, entity encodings (&#32;), or incorrect/missing parent relative prefixes (../).
"""
import os
import re

SITE_DIRS = [
    "/home/ubuntu/work/active-oahu-static/site",
    "/home/ubuntu/work/active-oahu-tours-mirror/site"
]

fixed_count = 0

for site_dir in SITE_DIRS:
    print(f"Processing directory: {site_dir}")
    if not os.path.exists(site_dir):
        print(f"  ⚠️ Skip: Directory not found")
        continue
    
    for root, dirs, files in os.walk(site_dir):
        if '_templates' in root.split(os.sep):
            continue
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            
            # Calculate depth relative to site_dir
            rel_path = os.path.relpath(fpath, site_dir)
            dir_name = os.path.dirname(rel_path)
            if dir_name:
                depth = len(dir_name.split(os.sep))
            else:
                depth = 0
            
            rel_prefix = "../" * depth
            
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            original = content
            
            def repl(m):
                full = m.group(0)
                # Determine prefix (preserve leading / if present)
                if 'href="/' in full or "href='/" in full:
                    prefix = "/"
                else:
                    prefix = rel_prefix
                
                # Determine which quote was used
                quote = "'" if "href='" in full else '"'
                
                # Determine which tour slug
                if 'kailua-kayak-twin-islands-guided-tour' in full:
                    slug = "activities/kailua-kayak-twin-islands-guided-tour/"
                else:
                    slug = "activities/kailua-bay-mokulua-island-self-guided-kayak-tour/"
                
                return f"href={quote}{prefix}{slug}{quote}"
            
            # Match href="activities/..." or href="/activities/..." or href="../../activities/..."
            # including optional space or &#32; and optional .html extension
            pattern = r'href=["\'](?:/|(?:\.\./)+)?activities/(?:kailua-kayak-twin-islands-guided-tour|kailua-bay-mokulua-island-self-guided-kayak-tour)/(?:\s+|&#32;)?(?:\.html)?["\']'
            
            content = re.sub(pattern, repl, content)
            
            if content != original:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"  Fixed: {rel_path} (depth {depth}, prefix: {rel_prefix if 'href="/' not in content else '/'})")

print(f"Done! Fixed links in {fixed_count} files.")
