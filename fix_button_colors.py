#!/usr/bin/env python3
"""Change Beach Gear Rental Booking Options buttons to #669900 green with hover."""
import os, re

SITE = os.path.join(os.path.dirname(__file__), 'site')

BTN_IDS = ['4341_19d39b-95', '4338_925179-dd', '4314_29a840-cc']

for root, dirs, files in os.walk(SITE):
    if '_templates' in root:
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        for btn_id in BTN_IDS:
            if btn_id not in content:
                continue
            
            escaped = re.escape(btn_id)
            
            # Add background:#669900 before width:initial
            content = re.sub(
                r'(ul\.menu[^}]*kb-btn' + escaped + r'\.kb-button\{)width:initial;(\})',
                r'\1background:#669900;width:initial;\2',
                content
            )
            
            # Add hover rule after the width rule
            hover_css = ".wp-block-kadence-advancedbtn .kb-btn" + btn_id + ".kb-button:hover, .wp-block-kadence-advancedbtn .kb-btn" + btn_id + ".kb-button:focus{background:#557a00;}"
            
            # Find the closing brace of the width rule and insert hover after it
            pattern = re.compile(
                r'(kb-btn' + escaped + r'\.kb-button\{[^}]*\})'
            )
            def add_hover(m):
                return m.group(1) + "\n" + hover_css
            
            content = pattern.sub(add_hover, content)
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated: {os.path.relpath(fpath, SITE)}")

print("\nDone!")
