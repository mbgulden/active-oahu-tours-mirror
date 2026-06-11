#!/usr/bin/env python3
"""Fast bulk download of missing images using concurrent requests."""
import os, re, sys, concurrent.futures, requests
from urllib.parse import unquote

SITE = os.path.join(os.path.dirname(__file__), 'site')
LIVE_BASE = 'https://activeoahutours.com'
MAX_WORKERS = 10

# Quick scan - just find all /wp-content/uploads/ paths
PATTERN = re.compile(r'(?:src|href|srcset)="[^"]*/wp-content/uploads/([^"]+)"', re.IGNORECASE)

def find_all():
    refs = set()
    for root, dirs, files in os.walk(SITE):
        if '_templates' in root: continue
        for fn in files:
            if not fn.endswith('.html'): continue
            with open(os.path.join(root, fn), 'r', encoding='utf-8', errors='replace') as f:
                c = f.read()
            for m in PATTERN.finditer(c):
                refs.add(unquote(m.group(1).split('?')[0]))
    return refs

def download(path):
    local = os.path.join(SITE, 'wp-content', 'uploads', path)
    if os.path.exists(local): return ('exists', path)
    try:
        r = requests.get(f"{LIVE_BASE}/wp-content/uploads/{path}", timeout=15,
                         headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200 and len(r.content) > 200:
            os.makedirs(os.path.dirname(local), exist_ok=True)
            with open(local, 'wb') as f:
                f.write(r.content)
            return ('ok', path)
        return (f'HTTP-{r.status_code}', path)
    except Exception as e:
        return (f'error', path)

print("Scanning...")
refs = find_all()
print(f"Found {len(refs)} references")

missing = [r for r in refs if not os.path.exists(os.path.join(SITE, 'wp-content', 'uploads', r))]
print(f"Missing: {len(missing)}")

if not missing:
    print("Nothing to download!")
    sys.exit(0)

ok, fail = 0, 0
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    for i, (status, path) in enumerate(ex.map(download, missing)):
        if status == 'ok': ok += 1
        elif status == 'exists': pass
        else: fail += 1
        if (i+1) % 50 == 0 or i == len(missing)-1:
            print(f"  [{i+1}/{len(missing)}] OK: {ok}, Fail: {fail}")

print(f"\nDone! Downloaded: {ok}, Failed: {fail}")

if fail:
    with open('still_missing.txt', 'w') as f:
        for r in missing:
            if not os.path.exists(os.path.join(SITE, 'wp-content', 'uploads', r)):
                f.write(f"{r}\n")
    print(f"Still-missing list: still_missing.txt")
