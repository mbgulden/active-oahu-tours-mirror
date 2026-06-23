#!/usr/bin/env python3
import os
import re
import urllib.request
import base64

SITE_DIR = os.path.join(os.path.dirname(__file__), 'site')
TEMPLATES_DIR = os.path.join(SITE_DIR, '_templates')

def fetch_live_token():
    url = "https://activeoahutours.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching live token: {e}")
        return None

    # Find all occurrences of window.__CF$cv$params={r:'...',t:'...'}
    # Support single or double quotes
    matches = re.findall(r"window\.__CF\$cv\$params\s*=\s*\{\s*r\s*:\s*['\"]([^'\"]+)['\"]\s*,\s*t\s*:\s*['\"]([^'\"]+)['\"]\s*\}", html)
    if not matches:
        print("No CF tokens found in the live page HTML.")
        return None

    best_r = None
    best_t = None
    best_ts = -1

    for r, t in matches:
        try:
            # Decode the base64 timestamp (e.g. MTc4MDI0NjI3NQ==)
            decoded = base64.b64decode(t).decode('utf-8')
            ts = int(decoded)
            print(f"Found token: r='{r}', t='{t}' (Timestamp: {ts})")
            if ts > best_ts:
                best_ts = ts
                best_r = r
                best_t = t
        except Exception as e:
            print(f"Error parsing token timestamp for r={r}, t={t}: {e}")
            # If base64 decode fails, we can still fallback to the last one
            if best_ts == -1:
                best_r = r
                best_t = t

    if best_r and best_t:
        print(f"Selected newest token: r='{best_r}', t='{best_t}' (Timestamp: {best_ts})")
        return best_r, best_t
    return None

def update_files(new_r, new_t):
    new_token_str = f"window.__CF$cv$params={{r:'{new_r}',t:'{new_t}'}}"
    token_pattern = re.compile(r"window\.__CF\$cv\$params\s*=\s*\{\s*r\s*:\s*['\"][^'\"]+['\"]\s*,\s*t\s*:\s*['\"][^'\"]+['\"]\s*\}")
    
    updated_count = 0
    
    # 1. Update templates and pages
    for root, dirs, files in os.walk(SITE_DIR):
        for fname in files:
            if not fname.endswith('.html'):
                continue
            
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            if token_pattern.search(content):
                new_content = token_pattern.sub(new_token_str, content)
                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_count += 1

    print(f"Updated CF token in {updated_count} files.")

def main():
    token_info = fetch_live_token()
    if not token_info:
        print("Failed to retrieve live token. Exiting.")
        return
    
    new_r, new_t = token_info
    update_files(new_r, new_t)

if __name__ == "__main__":
    main()
