#!/usr/bin/env bash
# Lighthouse audit runner for AOT.
# Usage:
#   ./scripts/lighthouse.sh production           # audit https://activeoahutours.com
#   ./scripts/lighthouse.sh preview <hash>       # audit https://<hash>.active-oahu-tours-mirror.pages.dev
#   ./scripts/lighthouse.sh compare <url1> <url2> # audit both, diff results
#
# Requires: lighthouse (npm install -g lighthouse), google-chrome or chromium

set -euo pipefail

REPORTS_DIR="${LIGHTHOUSE_REPORTS_DIR:-/tmp/lh_reports}"
mkdir -p "$REPORTS_DIR"

run_audit() {
    local name="$1"
    local url="$2"
    echo "  Auditing $name: $url"
    npx --yes lighthouse "$url" \
        --preset=desktop \
        --only-categories=performance,accessibility,best-practices,seo \
        --output=json --output=html \
        --output-path="$REPORTS_DIR/$name-desktop" \
        --quiet \
        --chrome-flags="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage" \
        > /dev/null 2>&1

    python3 - <<PYEOF
import json
d = json.load(open('$REPORTS_DIR/$name-desktop.report.json'))
print(f"  {'':15} {'Score':>6}")
for k, v in d['categories'].items():
    score = int(v['score'] * 100) if v['score'] is not None else 0
    print(f"  {k:15} {score:>6}")
print()
print("  Failing audits:")
for cat_name in ['best-practices', 'seo', 'accessibility']:
    for ref in d['categories'][cat_name]['auditRefs']:
        aud = d['audits'].get(ref['id'], {})
        if aud.get('score') is not None and aud['score'] < 1:
            print(f"    [{ref['id']:35}] {aud.get('title','')[:60]}")
PYEOF
}

case "${1:-}" in
    production)
        run_audit "prod-$(date +%Y%m%d-%H%M)" "https://activeoahutours.com/"
        ;;
    preview)
        if [ -z "${2:-}" ]; then
            echo "Usage: $0 preview <preview-hash>"
            exit 1
        fi
        run_audit "preview-${2}" "https://${2}.active-oahu-tours-mirror.pages.dev/"
        ;;
    compare)
        if [ -z "${2:-}" ] || [ -z "${3:-}" ]; then
            echo "Usage: $0 compare <url1> <url2>"
            exit 1
        fi
        name1="compare-a-$(date +%Y%m%d-%H%M)"
        name2="compare-b-$(date +%Y%m%d-%H%M)"
        run_audit "$name1" "$2"
        echo
        run_audit "$name2" "$3"
        echo
        echo "=== DIFF ==="
        python3 - <<PYEOF
import json
a = json.load(open('$REPORTS_DIR/$name1-desktop.report.json'))
b = json.load(open('$REPORTS_DIR/$name2-desktop.report.json'))
print(f"  {'':20} {'Before':>8} {'After':>8} {'Delta':>8}")
for k in a['categories'].keys():
    sa = int(a['categories'][k]['score'] * 100) if a['categories'][k]['score'] else 0
    sb = int(b['categories'][k]['score'] * 100) if b['categories'][k]['score'] else 0
    delta = sb - sa
    sign = '+' if delta > 0 else ''
    print(f"  {k:20} {sa:>8} {sb:>8} {sign}{delta:>7}")
PYEOF
        ;;
    *)
        echo "Usage: $0 {production|preview <hash>|compare <url1> <url2>}"
        exit 1
        ;;
esac