# Testing Guidelines for AOT

## Pre-PR checks

Before opening any PR, run these checks. If any fail, fix them first.

### 1. Diff sanity
```bash
git diff --stat                    # is the scope what you expected?
git diff --name-only               # are the files you intended?
git diff | grep -iE "(api_key|token|secret|password|bearer)" && echo "STOP: secret in diff"
```

### 2. Local Python syntax check (for .py changes)
```bash
python3 -m py_compile scripts/your_script.py
```

### 3. HTML spot-check (for .html changes)
```bash
# Pick 3 random files you touched
git diff --name-only -- '*.html' | shuf | head -3 | xargs -I {} sh -c 'echo "--- {} ---" && head -c 500 {}'
```

### 4. Lighthouse (for any rendered-output change)
```bash
# Wait for Cloudflare Pages preview deploy, then:
npx --yes lighthouse https://<preview-id>.active-oahu-tours-mirror.pages.dev/ \
  --preset=desktop \
  --only-categories=performance,accessibility,best-practices,seo \
  --output=json --output=html \
  --output-path=/tmp/lh_reports/<change-name>-desktop \
  --quiet \
  --chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"

# Quick summary
python3 -c "
import json
d = json.load(open('/tmp/lh_reports/<change-name>-desktop.report.json'))
for k, v in d['categories'].items():
    print(f'  {k:20} {int(v[\"score\"]*100)}/100')
"
```

Compare to the baseline in `lighthouse-baseline.md`. **If any category drops
more than 5 points, investigate before opening the PR.**

### 5. Link check (for new internal links)
```bash
# Manual approach: hit each new link
curl -sSI "https://activeoahutours.com/new-link/" -m 10 | head -3
# Expected: 200 or 301 (not 404)
```

For automated checking, install lychee later (TODO).

### 6. CF edge change verification
For WAF rules / transform rules / page rules:

```bash
# Test the targeted path
curl -sS -o /dev/null -w "%{http_code}\n" -m 10 "https://activeoahutours.com/target/path"

# Verify legit paths still work
curl -sS -o /dev/null -w "%{http_code}\n" -m 10 "https://activeoahutours.com/"
curl -sS -o /dev/null -w "%{http_code}\n" -m 10 "https://activeoahutours.com/tours/"
```

**For WAF rule changes:** also check Security Events to confirm the rule
fires as expected (see `cloudflare-config.md` for query).

## Lighthouse baseline

**Last measured:** 2026-06-23, desktop, against production `activeoahutours.com/`

| Category | Score |
|---|---|
| Performance | 93 |
| Accessibility | 81 |
| Best Practices | 50 |
| SEO | 77 |

**Known issues (deferred to separate work):**
- Best Practices 50: third-party cookies (FareHarbor), deprecations (jQuery)
- Accessibility 81: color-contrast, heading-order, link-name, missing form labels
- SEO 77: hreflang audit (GRO-585), canonical (some pages relative, see PR #11), link-text

**Capture baseline before/after every PR** that affects rendered output.
See `scripts/lighthouse.sh` (TODO) for automation.

## Post-merge verification

After Michael merges to main, wait ~60 seconds for Cloudflare Pages to deploy,
then:

1. **Lighthouse on production** (compare to baseline)
2. **Spot-check 3 key pages** (homepage, top tour, /404.html)
3. **Check Cloudflare Security Events** if the PR was a CF change
4. **Update Linear** to Done state with merge confirmation

## Test environments

| Environment | URL | Source |
|---|---|---|
| Production | https://activeoahutours.com | `main` branch, manual merge only |
| Preview (per PR) | `https://<hash>.active-oahu-tours-mirror.pages.dev` | Auto-built from feature branch |
| Staging (NOT for testing) | (internal) | `staging` branch, Michael's in-progress work |

**Use the PR preview URL for testing, not staging.**

## Common mistakes to avoid

- ❌ Trusting the live site as the "source of truth" for canonical/hreflang
  (production deploys from `main` which may be behind staging)
- ❌ Skipping Lighthouse because the change "looks small"
- ❌ Opening a PR before the Pages preview deploy succeeds
- ❌ Not testing the actual user-facing paths (vs just the file content)
- ❌ Forgetting to purge CF cache after edge changes (sometimes required)