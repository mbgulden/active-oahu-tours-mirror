#!/usr/bin/env python3
"""Batch translate all /ja/ pages from English to Japanese using deep-translator."""
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator
from pathlib import Path
import time, sys, re

JA_DIR = Path("/home/ubuntu/work/active-oahu-static/site/ja")
translator = GoogleTranslator(source='en', target='ja')
JAPANESE_RE = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')

def is_already_japanese(text):
    """Return True if text is predominantly Japanese already."""
    jp_chars = len(JAPANESE_RE.findall(text))
    total_alpha = len(re.findall(r'[a-zA-Z]', text))
    return jp_chars > total_alpha and jp_chars > 5

def translate_tag_text(tag):
    """Replace all NavigableString children with translations."""
    for child in list(tag.children):
        if isinstance(child, NavigableString):
            text = child.strip()
            if text and len(text) > 3 and not is_already_japanese(text):
                try:
                    result = translator.translate(text)
                    if result:
                        child.replace_with(result)
                    time.sleep(0.12)
                except Exception:
                    pass

def translate_page(path):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'lxml')
    translated = 0

    # Meta tags
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
                    if result:
                        tag[attr] = result
                        translated += 1
                    time.sleep(0.12)
                except Exception as e:
                    pass

    # Title
    title_tag = soup.find('title')
    if title_tag and title_tag.string:
        val = title_tag.string.strip()
        if val and len(val) > 3 and not is_already_japanese(val):
            try:
                result = translator.translate(val)
                if result:
                    title_tag.string.replace_with(result)
                    translated += 1
                time.sleep(0.12)
            except Exception:
                pass

    # Body text tags — translate direct string content
    text_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'td', 'th',
                 'figcaption', 'blockquote', 'span', 'strong', 'em', 'b', 'i',
                 'label', 'dd', 'dt', 'cite', 'small', 'a'}
    for tag in soup.find_all(text_tags):
        if tag.string and tag.string.strip():
            val = tag.string.strip()
            if len(val) > 3 and not is_already_japanese(val):
                try:
                    result = translator.translate(val)
                    if result:
                        tag.string.replace_with(result)
                        translated += 1
                    time.sleep(0.12)
                except Exception:
                    pass
        elif not is_already_japanese(tag.get_text(strip=True)):
            translate_tag_text(tag)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    return translated

def main():
    html_files = sorted(JA_DIR.rglob("*.html"))
    total = len(html_files)
    print(f"Translating {total} pages...", flush=True)

    total_translated = 0
    for i, path in enumerate(html_files):
        rel = path.relative_to(JA_DIR)
        try:
            n = translate_page(path)
            total_translated += n
            print(f"[{i+1:3d}/{total}] {n:4d} texts  {rel}", flush=True)
        except Exception as e:
            print(f"[{i+1:3d}/{total}] ERROR {rel}: {e}", flush=True)
        time.sleep(0.15)

    print(f"\nDone: {total_translated} texts translated across {total} pages", flush=True)

if __name__ == '__main__':
    main()
