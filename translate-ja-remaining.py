#!/usr/bin/env python3
"""Translate remaining /ja/ pages — skips already-translated pages."""
from pathlib import Path
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time, sys, re

JA_DIR = Path("/home/ubuntu/work/active-oahu-static/site/ja")
translator = GoogleTranslator(source='en', target='ja')
JAPANESE_RE = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')

def is_already_japanese(text):
    jp_chars = len(JAPANESE_RE.findall(text))
    total_alpha = len(re.findall(r'[a-zA-Z]', text))
    return jp_chars > total_alpha and jp_chars > 5

def translate_page(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    translated = 0

    for selector, attr in [
        ('meta[name="description"]', 'content'),
        ('meta[property="og:description"]', 'content'),
        ('meta[property="og:title"]', 'content'),
        ('meta[name="twitter:description"]', 'content'),
    ]:
        for tag in soup.select(selector):
            val = tag.get(attr, '').strip()
            if val and len(val) > 10 and not is_already_japanese(val):
                try:
                    result = translator.translate(val)
                    if result: tag[attr] = result; translated += 1
                    time.sleep(0.1)
                except: pass

    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        val = title_tag.string.strip()
        if val and len(val) > 3 and not is_already_japanese(val):
            try:
                result = translator.translate(val)
                if result: title_tag.string.replace_with(result); translated += 1
                time.sleep(0.1)
            except: pass

    for tag_name in ['h1','h2','h3','h4','h5','h6','p','li','td','th','figcaption','blockquote','span','strong','em','b','i','label','dd','dt','cite','small','a']:
        for tag in soup.find_all(tag_name):
            if tag.string and tag.string.strip():
                val = tag.string.strip()
                if len(val) > 3 and not is_already_japanese(val):
                    try:
                        result = translator.translate(val)
                        if result: tag.string.replace_with(result); translated += 1
                        time.sleep(0.08)
                    except: pass

    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    return translated

# Find pages that need translation
all_files = sorted(JA_DIR.rglob("*.html"))
needed = []
for f in all_files:
    text = f.read_text()
    if len(JAPANESE_RE.findall(text)) < 200:
        needed.append(f)

print(f"Translating {len(needed)} pages (skipping {len(all_files)-len(needed)} already done)...", flush=True)

total_translated = 0
for i, path in enumerate(needed):
    rel = path.relative_to(JA_DIR)
    try:
        n = translate_page(path)
        total_translated += n
        print(f"[{i+1:3d}/{len(needed)}] {n:4d} texts  {rel}", flush=True)
    except Exception as e:
        print(f"[{i+1:3d}/{len(needed)}] ERROR {rel}: {e}", flush=True)
    time.sleep(0.1)

print(f"\nDone: {total_translated} texts across {len(needed)} pages", flush=True)
