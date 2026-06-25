#!/usr/bin/env python3
"""AOT branch/page drift guard.

Compares a production branch against a candidate/source branch and reports:
- files present only on candidate
- files present only on production
- shared files modified differently
- route/SEO critical drift
- page-level drift with titles and URLs

Default is report-only. Use --strict to exit non-zero when drift exceeds thresholds.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
CRITICAL_SUFFIXES = (
    '_redirects',
    'site/_redirects',
    'sitemap.xml',
    'site/sitemap.xml',
    'robots.txt',
    'site/robots.txt',
    'PRISMATIC_ENGINE.yaml',
)


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ['git', '-C', str(ROOT), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout


def list_files(ref: str) -> set[str]:
    out = git('ls-tree', '-r', '--name-only', ref)
    return {line for line in out.splitlines() if line}


def blob(ref: str, path: str) -> bytes | None:
    proc = subprocess.run(
        ['git', '-C', str(ROOT), 'show', f'{ref}:{path}'],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def sha(ref: str, path: str) -> str:
    data = blob(ref, path)
    if data is None:
        return ''
    return hashlib.sha256(data).hexdigest()


def html_title(ref: str, path: str) -> str:
    if not path.endswith('.html'):
        return ''
    data = blob(ref, path)
    if not data:
        return ''
    text = data[:16000].decode('utf-8', errors='ignore')
    match = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    return ' '.join(match.group(1).split()) if match else ''


def page_url(path: str) -> str:
    if path.startswith('site/') and path.endswith('/index.html'):
        return '/' + path[len('site/'):-len('index.html')]
    if path == 'site/index.html':
        return '/'
    return ''


def category(path: str) -> str:
    if path.startswith('site/ja/'):
        return 'ja'
    if path.startswith('site/guides/'):
        return 'guides'
    if path.startswith('site/rentals/'):
        return 'rentals'
    if path.startswith('site/activities/'):
        return 'activities'
    if path.startswith('site/blog/'):
        return 'blog'
    if path.startswith('site/wp-content/'):
        return 'wp-content'
    if path.startswith('site/_templates/'):
        return 'templates'
    if path.startswith('site/') and path.endswith('/index.html'):
        return 'other-pages'
    if any(path.endswith(s) for s in CRITICAL_SUFFIXES):
        return 'routing/seo/governance'
    return path.split('/', 1)[0] if '/' in path else 'root'


def count_by_category(paths: Iterable[str]) -> dict[str, int]:
    return dict(Counter(category(p) for p in paths).most_common())


def rows_for_pages(paths: list[str], ref: str, limit: int = 80) -> list[dict[str, str]]:
    rows = []
    for path in paths[:limit]:
        rows.append({
            'path': path,
            'url': page_url(path),
            'title': html_title(ref, path),
            'category': category(path),
        })
    return rows


def build_report(prod: str, candidate: str, fetch: bool = True) -> dict:
    if fetch:
        git('fetch', 'origin', '--prune')
    prod_files = list_files(prod)
    cand_files = list_files(candidate)
    prod_only = sorted(prod_files - cand_files)
    cand_only = sorted(cand_files - prod_files)
    shared = sorted(prod_files & cand_files)
    modified = [p for p in shared if sha(prod, p) != sha(candidate, p)]

    candidate_only_pages = [p for p in cand_only if page_url(p)]
    prod_only_pages = [p for p in prod_only if page_url(p)]
    modified_pages = [p for p in modified if p.startswith('site/') and p.endswith(('.html', '.xml', '.txt'))]
    critical_changed = sorted(
        p for p in set(prod_only + cand_only + modified)
        if any(p.endswith(s) for s in CRITICAL_SUFFIXES) or p.startswith('.github/')
    )

    merge_base = git('merge-base', prod, candidate).strip()
    return {
        'prod': prod,
        'candidate': candidate,
        'merge_base': merge_base,
        'counts': {
            'prod_files': len(prod_files),
            'candidate_files': len(cand_files),
            'candidate_only_files': len(cand_only),
            'prod_only_files': len(prod_only),
            'modified_shared_files': len(modified),
            'candidate_only_pages': len(candidate_only_pages),
            'prod_only_pages': len(prod_only_pages),
            'modified_shared_page_or_text_files': len(modified_pages),
            'critical_changed_files': len(critical_changed),
        },
        'by_category': {
            'candidate_only': count_by_category(cand_only),
            'prod_only': count_by_category(prod_only),
            'modified': count_by_category(modified),
        },
        'critical_changed': critical_changed,
        'candidate_only_page_examples': rows_for_pages(candidate_only_pages, candidate, limit=200),
        'prod_only_page_examples': rows_for_pages(prod_only_pages, prod, limit=80),
    }


def markdown(report: dict) -> str:
    lines: list[str] = []
    prod = report['prod']
    candidate = report['candidate']
    lines.append(f'# AOT Branch Drift Guard — `{prod}` vs `{candidate}`')
    lines.append('')
    lines.append(f'- Merge base: `{report["merge_base"]}`')
    lines.append('')
    lines.append('## Counts')
    for key, value in report['counts'].items():
        lines.append(f'- {key}: **{value}**')
    lines.append('')
    for section, title in [
        ('candidate_only', 'Candidate-only categories'),
        ('prod_only', 'Production-only categories'),
        ('modified', 'Modified shared-file categories'),
    ]:
        lines.append(f'## {title}')
        for key, value in report['by_category'][section].items():
            lines.append(f'- {key}: {value}')
        if not report['by_category'][section]:
            lines.append('- none')
        lines.append('')
    lines.append('## Critical changed files')
    for path in report['critical_changed'][:200]:
        lines.append(f'- `{path}`')
    if not report['critical_changed']:
        lines.append('- none')
    lines.append('')
    lines.append('## Candidate-only page examples')
    lines.append('| Path | URL | Title |')
    lines.append('|---|---|---|')
    for row in report['candidate_only_page_examples'][:100]:
        title = row['title'].replace('|', '/')[:140]
        lines.append(f'| `{row["path"]}` | `{row["url"]}` | {title} |')
    if not report['candidate_only_page_examples']:
        lines.append('| — | — | — |')
    lines.append('')
    lines.append('## Production-only page examples')
    lines.append('| Path | URL | Title |')
    lines.append('|---|---|---|')
    for row in report['prod_only_page_examples'][:60]:
        title = row['title'].replace('|', '/')[:140]
        lines.append(f'| `{row["path"]}` | `{row["url"]}` | {title} |')
    if not report['prod_only_page_examples']:
        lines.append('| — | — | — |')
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prod', default='origin/main', help='Production/deploy source ref')
    parser.add_argument('--candidate', default='origin/master', help='Candidate/source ref to compare')
    parser.add_argument('--report', default='', help='Write Markdown report to path')
    parser.add_argument('--json', default='', help='Write JSON report to path')
    parser.add_argument('--strict', action='store_true', help='Exit non-zero when drift exceeds thresholds')
    parser.add_argument('--allow-candidate-only-pages', type=int, default=0)
    parser.add_argument('--allow-critical-changed', type=int, default=0)
    parser.add_argument('--no-fetch', action='store_true')
    args = parser.parse_args()

    report = build_report(args.prod, args.candidate, fetch=not args.no_fetch)
    md = markdown(report)
    print(md)
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(md)
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    if args.strict:
        counts = report['counts']
        failures = []
        if counts['candidate_only_pages'] > args.allow_candidate_only_pages:
            failures.append(
                f"candidate_only_pages={counts['candidate_only_pages']} > {args.allow_candidate_only_pages}"
            )
        if counts['critical_changed_files'] > args.allow_critical_changed:
            failures.append(
                f"critical_changed_files={counts['critical_changed_files']} > {args.allow_critical_changed}"
            )
        if failures:
            print('\nSTRICT DRIFT GUARD FAILED: ' + '; '.join(failures), file=sys.stderr)
            return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
