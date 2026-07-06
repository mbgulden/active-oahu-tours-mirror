# Active Oahu Tours Site Editing & Management Standards

**Status:** Initial governance standard  
**Owner:** Fred / Staging Governor  
**Reason:** Branch drift and inconsistent page styling caused revenue/content pages to exist on one branch but 404 on production.

## 1. Source of Truth

The AOT static mirror must have one clearly verified production source of truth.

Until the Cloudflare Pages deploy configuration is formally verified and updated in this repo, agents must treat the production branch as **unknown-at-start** and verify it before making site changes.

Required production-source verification before content or style changes:

```bash
git fetch origin --prune
python3 scripts/aot_branch_drift_guard.py --prod origin/main --candidate origin/master --report /tmp/aot-branch-drift.md
curl -sSI https://activeoahutours.com/<changed-path>/ | sed -n '1,8p'
```

Do not rely on branch names alone. The live custom domain and Cloudflare Pages root preview are authoritative.

## 2. No Blind Merges Between `main` and `master`

`main` and `master` have diverged. A blind merge can overwrite styles, redirects, sitemap entries, schema, or booking behavior.

Required approach:

1. Run a drift audit.
2. Classify drift into:
   - production-critical route/SEO files: `_redirects`, `site/_redirects`, `sitemap.xml`, `robots.txt`
   - content pages present on only one branch
   - shared pages modified differently
   - generated/static artifacts that should not be hand-edited
3. Restore approved pages in small batches.
4. Verify every restored URL on production with HTTP 200.
5. Only then update sitemap, redirects, and internal links.

## 3. Page Restoration Standard

When a page exists on a non-production branch and is missing from production:

- Prefer copying the already-built page from the source branch over rewriting from scratch.
- Preserve:
  - `<title>`
  - meta description
  - canonical URL
  - OpenGraph/Twitter tags
  - JSON-LD schema
  - FareHarbor item IDs / `data-fh-item`
  - internal links
  - Japanese mirror page if present
- After copy, verify:

```bash
python3 - <<'PY'
from pathlib import Path
for p in [Path('site/path/index.html')]:
    s = p.read_text(errors='ignore')
    assert '<title>' in s
    assert 'canonical' in s
    assert 'application/ld+json' in s
print('basic page checks passed')
PY
```

Then verify live:

```bash
curl -sSI https://activeoahutours.com/path/ | sed -n '1,8p'
```

## 4. Style Consistency Standard

Inconsistent old/new page styles are treated as a governance issue, not a one-off CSS issue.

Every page edit must preserve or move toward a consistent style system:

- Use existing shared templates/components where possible.
- Do not introduce page-local visual patterns unless documented.
- Do not copy old WordPress/Kadence inline style blobs into new pages unless the page is being restored verbatim and scheduled for style normalization.
- Prefer shared CSS classes and shared body/footer/header templates.
- Any page restored from an older branch must be flagged for one of:
  - **verbatim restore**: restore quickly to recover traffic/revenue, then normalize later
  - **normalized restore**: restore and style-normalize in the same PR

Minimum visual consistency checks for restored pages:

- Header/menu present and functional
- Mobile sticky CTA present and uses the correct FareHarbor item when relevant
- Typography and spacing match nearby current pages
- Footer links work from subdirectory paths
- No obvious legacy progress overlay, booking overlay, or stale WordPress artifact

## 5. Booking / FareHarbor Standard

Revenue pages must preserve booking behavior.

For rentals and tours:

- Preserve page-level `data-fh-item` where present.
- Sticky CTA must deep-link to the correct item, not just generic catalog.
- Rental pages must keep pricing, duration, included gear, pickup/delivery details, and return policy visible above or near booking CTA.

Known priority example:

- `/rentals/snorkel-gear-rentals/`
  - FareHarbor item: `7872`
  - Price: `$18`
  - Promise: full-day rental + after-hours return
  - Funnel: Kailua pickup → Windward/North Shore stops → Sharks Cove snorkel

## 6. Internal Linking Standard

Route clusters must be linked as funnels, not isolated pages.

For the all-day Sharks Cove snorkel funnel:

```text
/sharks-cove-snorkeling/
/sharks-cove-snorkeling-guide/
→ /rentals/snorkel-gear-rentals/
→ /guides/eating-your-way-windward-to-north-shore/
```

Any restored route guide must have inbound links from relevant commercial pages and outbound links back to booking pages.

## 7. Sitemap / Redirect Standard

After restoring or moving pages:

- Ensure canonical URLs match final production paths.
- Ensure `sitemap.xml` contains production-intended live pages.
- Ensure `_redirects` does not point live traffic at 404s.
- If a path is intentionally retired, redirect to the closest relevant page.

## 8. Branch Drift Guard

Run before and after site-management work:

```bash
python3 scripts/aot_branch_drift_guard.py --prod origin/main --candidate origin/master --report /tmp/aot-branch-drift.md
```

Use `--strict` only after the current drift backlog is resolved or a baseline is committed.

## 8.5. Prismatic Web Governance Guard

Before claiming any of these statements, run the portable governance guard:

- “staging has the fix”
- “production is stale”
- “this PR can safely merge”
- “the homepage/nav is fixed”
- “all Active Oahu project branches are in sync”

Required command:

```bash
git fetch origin --prune
python3 scripts/prismatic_web_governance.py \
  --config .prismatic-web-governance.json \
  --report /tmp/aot-prismatic-web-governance.md \
  --json /tmp/aot-prismatic-web-governance.json
```

The guard checks branch divergence, open/stale/conflicting PRs, protected-path overlap, dirty workspaces, remote stale branches, and live production homepage markers. WARN/FAIL sections are the cleanup backlog unless explicitly waived in a PR or Linear thread.

See `docs/PRISMATIC_WEB_GOVERNANCE_SYSTEM.md` for the Prismatic Web Plugin distribution contract.

## 8.6. Branch Reconciliation Guidance

When `staging` or another preview branch is ahead of production, do **not** assume it contains unreleased work. The governance guard uses both `git cherry -v <production> <staging>` and production/staging tree SHA equality:

- `- <sha> ...` means the staging-only commit is patch-equivalent to production and is cleanup debt.
- `+ <sha> ...` means staging may contain unique work that needs review before any reset/rebuild.
- Identical production/staging tree SHAs mean the deployable site content is already reconciled; remaining ahead/behind is history-only drift.

If all staging-only commits are patch-equivalent, the preferred fix is to rebuild/reset staging from production after human/governor approval or use a normal non-force PR to bring staging forward from `main`. Do not merge stale staging into production just to “catch up”; that can reintroduce old files and erase newer homepage/nav fixes.

## 9. Agent Responsibilities

- **Fred:** governance, deploy source verification, drift guard, staging/production merge decisions.
- **Kai Content:** page copy, SEO, schema/content preservation, guide/rental funnel restoration.
- **Kai CSS:** style normalization, legacy artifact cleanup, mobile visual consistency.
- **Kai JS:** booking CTA behavior, FareHarbor embed behavior, interaction checks.
- **AGY:** review/audit of restoration batches before broad production merge.
- **Jules/Ned:** deterministic scripts, CI, validation tooling, implementation review.

## 10. Definition of Done for Site Changes

A site change is not done until all are true:

- Branch/source of truth was verified.
- Files were changed on the intended branch via a feature branch/PR.
- Drift guard was run and report reviewed.
- Page-level checks passed.
- Production or preview URL returned expected status.
- Internal links/booking CTAs were checked for affected pages.
- Linear issue includes evidence: command output, URLs, and any intentional deferred style debt.
