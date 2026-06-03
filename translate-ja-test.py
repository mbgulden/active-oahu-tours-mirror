#!/usr/bin/env python3
"""Translate 2 Japanese HTML pages as a test."""
import sys, time
from pathlib import Path
sys.path.insert(0, '/home/ubuntu/work')

# Import from the main script
import importlib.util
spec = importlib.util.spec_from_file_location("translate_ja", "/home/ubuntu/work/translate-ja.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

JA_DIR = Path("/home/ubuntu/work/active-oahu-static/site/ja")
files = [JA_DIR / 'index.html', JA_DIR / 'faq/index.html']

for path in files:
    rel = path.relative_to(JA_DIR.parent)
    print(f"\n{rel}")
    if mod.translate_page(path):
        print("  ✅ Translated")
    else:
        print("  ⏭️  Skipped")

# Verify
for path in files:
    with open(path) as f:
        html = f.read()
    # Check for Japanese characters
    import re
    jp = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', html))
    print(f"  {path.name}: {jp} Japanese chars")
