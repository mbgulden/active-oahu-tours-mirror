#!/usr/bin/env python3
"""Translate all Japanese HTML pages from English to Japanese using Google Translate."""
import os, sys, time, re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
from googletrans import Translator

JA_DIR = Path("/home/ubuntu/work/active-oahu-static/site/ja")
translator = Translator()

# HTML tags whose text content we want to translate
TRANSLATABLE_TAGS = {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a', 'span', 
                      'td', 'th', 'label', 'button', 'strong', 'em', 'b', 'i',
                      'figcaption', 'blockquote', 'cite', 'dd', 'dt', 'option',
                      'title', 'meta'}

# Attributes to translate
TRANSLATABLE_ATTRS = {'content': ['meta[name="description"]', 'meta[property="og:description"]'],
                       'alt': ['img'],
                       'title': ['a[title]'],
                       'aria-label': ['*']}

# Skip these: scripts, styles, code, pre, noscript
SKIP_TAGS = {'script', 'style', 'code', 'pre', 'noscript', 'svg', 'math'}

def should_translate_tag(tag):
    """Check if a tag's text should be translated."""
    if tag.name in SKIP_TAGS:
        return False
    # Skip if parent is in skip tags
    for parent in tag.parents:
        if parent.name in SKIP_TAGS:
            return False
    return True

def extract_text_chunks(soup):
    """Extract translatable text chunks from the soup, mapping them to their elements."""
    chunks = []
    
    for tag in soup.find_all(TRANSLATABLE_TAGS):
        if not should_translate_tag(tag):
            continue
        
        # For title tag, translate the whole thing
        if tag.name == 'title' and tag.string:
            text = tag.string.strip()
            if text and len(text) > 3:
                chunks.append((tag, 'string', text))
        
        # For meta description
        elif tag.name == 'meta' and tag.get('name') == 'description':
            content = tag.get('content', '').strip()
            if content and len(content) > 10:
                chunks.append((tag, 'content', content))
        
        # For regular text-bearing elements with direct string
        elif tag.string and tag.string.strip():
            text = tag.string.strip()
            if len(text) > 2 and not text.startswith('<!--'):
                chunks.append((tag, 'string', text))
        
        # For <a> tags - translate the visible text
        elif tag.name == 'a':
            texts = [s for s in tag.stripped_strings]
            if texts:
                full = ' '.join(texts)
                if len(full) > 2:
                    chunks.append((tag, 'strings', full))
    
    return chunks

def translate_chunks(chunks, batch_size=15):
    """Translate text chunks in batches to respect rate limits."""
    results = {}
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [c[2] for c in batch]
        
        try:
            translations = translator.translate(texts, dest='ja', src='en')
            for j, trans in enumerate(translations):
                elem, attr, orig = batch[j]
                results[(id(elem), attr)] = trans.text
            print(f"  Batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}: {len(batch)} texts translated")
        except Exception as e:
            print(f"  Batch {i//batch_size + 1} ERROR: {e}")
            # Try one by one as fallback
            for j, (elem, attr, orig) in enumerate(batch):
                try:
                    time.sleep(0.5)
                    trans = translator.translate(orig, dest='ja', src='en')
                    results[(id(elem), attr)] = trans.text
                except Exception as e2:
                    print(f"    Skipping: {orig[:50]}... ({e2})")
            time.sleep(1)
        
        time.sleep(0.5)  # Rate limiting
    
    return results

def apply_translations(chunks, translations):
    """Apply translations back to the DOM."""
    for elem, attr, orig in chunks:
        key = (id(elem), attr)
        if key in translations:
            trans = translations[key]
            if attr == 'string':
                elem.string.replace_with(trans)
            elif attr == 'content':
                elem['content'] = trans
            elif attr == 'strings':
                # For <a> tags, replace all child text nodes
                for child in elem.children:
                    if isinstance(child, NavigableString) and child.strip():
                        child.replace_with(trans)
                        break

def translate_page(html_path):
    """Translate a single HTML page."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    chunks = extract_text_chunks(soup)
    
    if not chunks:
        return False
    
    translations = translate_chunks(chunks)
    apply_translations(chunks, translations)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return True

def main():
    html_files = list(JA_DIR.rglob("*.html"))
    total = len(html_files)
    print(f"Found {total} HTML files in {JA_DIR}")
    
    done = 0
    failed = 0
    
    for i, path in enumerate(html_files):
        rel = path.relative_to(JA_DIR.parent)
        print(f"\n[{i+1}/{total}] {rel}")
        try:
            if translate_page(path):
                done += 1
            else:
                print("  No translatable content, skipping")
                failed += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1
        
        # Rate limit between pages
        time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"Done: {done} translated, {failed} skipped/failed")

if __name__ == '__main__':
    main()
