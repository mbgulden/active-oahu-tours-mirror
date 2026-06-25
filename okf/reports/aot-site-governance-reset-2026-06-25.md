---
type: Report
title: AOT Site Governance Reset — Branch Drift, Page Restoration, and Style Standards
description: OKF record for the Active Oahu Tours branch-drift incident, missing all-day snorkel pages, style inconsistency concerns, and the new site-management operating standard.
resource: https://github.com/mbgulden/active-oahu-tours-mirror/blob/main/okf/reports/aot-site-governance-reset-2026-06-25.md
tags: [active-oahu, site-governance, branch-drift, style-normalization, okf, linear-dispatch]
timestamp: 2026-06-25T22:00:00Z
linear_issue: GRO-2473
git_repo: mbgulden/active-oahu-tours-mirror
git_path: okf/reports/aot-site-governance-reset-2026-06-25.md
status: active
verified_by: fred
---

# AOT Site Governance Reset — Branch Drift, Page Restoration, and Style Standards

## TL;DR

The missing “all-day Sharks Cove snorkel” pages were not deleted. They were stranded on `master` while the live production/root Pages behavior matched `main`. Michael correctly identified that this is a branch drift and site-governance failure, not a two-page recovery issue.

This OKF report captures the operating decision: **AOT site edits now require source-of-truth verification, drift auditing, safe page restoration, style normalization, and live URL verification. No blind `main`/`master` merges.**

## Current Outcome Table

| Outcome | Status | Evidence |
|---|---:|---|
| Identify root cause of missing snorkel/stops pages | ✅ Done | Pages exist on `origin/master`, absent from `origin/main`; production URLs 404 |
| First branch-drift audit | ✅ Done | 23 master-only pages, 300 modified shared files |
| Site editing standards doc | ✅ Merged | `docs/AOT_SITE_MANAGEMENT_STANDARDS.md` |
| Drift guard script | ✅ Merged | `scripts/aot_branch_drift_guard.py` |
| GitHub Actions drift workflow | ✅ Merged | `.github/workflows/aot-branch-drift.yml` |
| Content restoration task | 🟡 Active | GRO-2474 |
| Style normalization audit | 🟡 Active | GRO-2476 |
| Live snorkel URL watcher | 🟡 Active | Hermes cron `8a21c85c9170` |

## Trigger / Incident

Michael was looking for a page that described an **all-day snorkel experience** with “other stops along the way.” The relevant cluster was:

- `/rentals/snorkel-gear-rentals/`
- `/guides/eating-your-way-windward-to-north-shore/`
- `/ja/rentals/snorkel-gear-rentals/`
- `/ja/guides/eating-your-way-windward-to-north-shore/`

These existed in older/static/master content, but returned 404 on the production domain.

Michael then identified the real issue:

> “So, it sounds like there needs to be a branch drift audit of all the things that are incongruent and get it all back in sync and then prevent it from doing this again.”

Later, Michael expanded the scope:

> “I noticed inconsistent styles between old and new pages and there’s a lot of issues. We’ll need to establish a lot of standards for site editing and management.”

## Root Cause

The AOT mirror had diverged branches:

- `origin/master` contained content pages that did not exist on `origin/main`.
- Production/root Cloudflare Pages behavior matched `main` for the missing pages.
- Repo governance had inconsistent/aspirational production-branch claims.
- Page generations/styles came from multiple eras/templates, causing style drift and inconsistent UX.

This made page-level recovery fragile: a restored page could be live on a preview branch but still 404 on production, or it could restore content while bringing old styling/CTA behavior with it.

## Drift Evidence

First-pass audit from `origin/main` vs `origin/master`:

| Drift Type | Count |
|---|---:|
| `master`/candidate-only files | 134 |
| `main`/production-only files | 64 before guard merge; 67 after guard merge |
| Modified shared files | 300 |
| Master-only pages | 23 |
| Main-only pages | 1 |
| Critical changed files | 4 before guard merge; 5 after guard workflow added |

Known master-only page examples:

| Path | URL |
|---|---|
| `site/rentals/snorkel-gear-rentals/index.html` | `/rentals/snorkel-gear-rentals/` |
| `site/guides/eating-your-way-windward-to-north-shore/index.html` | `/guides/eating-your-way-windward-to-north-shore/` |
| `site/ja/rentals/snorkel-gear-rentals/index.html` | `/ja/rentals/snorkel-gear-rentals/` |
| `site/ja/guides/eating-your-way-windward-to-north-shore/index.html` | `/ja/guides/eating-your-way-windward-to-north-shore/` |
| `site/activities/kawela-bay-self-guided-kayak-tour/index.html` | `/activities/kawela-bay-self-guided-kayak-tour/` |
| `site/guides/kailua-vs-lanikai/index.html` | `/guides/kailua-vs-lanikai/` |
| `site/guides/lanikai-pillbox-hike/index.html` | `/guides/lanikai-pillbox-hike/` |
| `site/guides/oahu-kayak-safety-tide-guide/index.html` | `/guides/oahu-kayak-safety-tide-guide/` |
| `site/multi-activity-adventure-packages/index.html` | `/multi-activity-adventure-packages/` |
| `site/oahu-kayak-safety-tide-index-map/index.html` | `/oahu-kayak-safety-tide-index-map/` |

Generated report artifacts from Fred’s session:

- `/tmp/aot-branch-drift-audit.md`
- `/tmp/aot-branch-drift-guard-current.md`
- `/tmp/aot-branch-drift-post-merge.md`

## Decisions Locked

### D1 — Treat as governance failure, not page deletion

Pages were not “deleted.” They were stranded by branch divergence. Future incident language should say **branch drift** unless a deletion commit is proven.

### D2 — No blind merge between `main` and `master`

There are 300 modified shared files. A blind merge risks overwriting redirects, sitemap, JSON-LD, booking behavior, CSS/JS behavior, and page-era styling.

### D3 — Restore approved pages in small batches

Restore revenue/content pages from the source branch only after reviewing:

- title/meta/canonical
- JSON-LD/schema
- FareHarbor IDs / booking CTA behavior
- internal links
- sitemap and redirects
- mobile/style consistency

### D4 — Verbatim restore is allowed only with explicit style debt

For traffic/revenue recovery, a page may be restored verbatim first. But it must be flagged for style normalization if it uses older visual patterns.

### D5 — Standards and guardrails must live in repo and OKF

The repo contains executable standards/guardrails. OKF contains the operating memory and dispatch map.

## What Shipped

Merged on `main` via PR #16:

- PR: <https://github.com/mbgulden/active-oahu-tours-mirror/pull/16>
- Commit: `5a3e6288` — `[Fred] Add AOT site governance and branch drift guard (#GRO-2475)`

Files added/updated:

| File | Purpose |
|---|---|
| `docs/AOT_SITE_MANAGEMENT_STANDARDS.md` | Site editing, restoration, style, linking, booking, and done standards |
| `scripts/aot_branch_drift_guard.py` | Deterministic `main`/`master` drift report/guard |
| `.github/workflows/aot-branch-drift.yml` | CI/manual/scheduled drift report workflow |
| `PRISMATIC_ENGINE.yaml` | Requires live production-source verification and forbids blind merges |

## Verification Commands

Run from `/home/ubuntu/work/active-oahu-tours-mirror`:

```bash
git fetch origin --prune
python3 scripts/aot_branch_drift_guard.py \
  --prod origin/main \
  --candidate origin/master \
  --report /tmp/aot-branch-drift-current.md \
  --json /tmp/aot-branch-drift-current.json

python3 -m py_compile scripts/aot_branch_drift_guard.py

python3 - <<'PY'
import yaml
for p in ['PRISMATIC_ENGINE.yaml', '.github/workflows/aot-branch-drift.yml']:
    yaml.safe_load(open(p))
    print(p, 'OK')
PY
```

Strict mode should currently fail until drift is resolved:

```bash
python3 scripts/aot_branch_drift_guard.py \
  --prod origin/main \
  --candidate origin/master \
  --strict \
  --allow-candidate-only-pages 0 \
  --allow-critical-changed 0
```

Expected current failure shape:

```text
STRICT DRIFT GUARD FAILED: candidate_only_pages=23 > 0; critical_changed_files=N > 0
```

## Outstanding Work / Linear Map

| ID | Owner/Lane | Purpose | Status |
|---|---|---|---|
| GRO-2473 | Fred | Parent branch-drift audit + production sync plan | Active |
| GRO-2474 | Kai Content | Restore approved master-only content pages to production branch | Active |
| GRO-2475 | Fred | Add branch-drift prevention guard | Done |
| GRO-2476 | Kai CSS | Style normalization audit for old/new page inconsistency | Active |

## Future-Agent Runbook

1. Read this OKF report.
2. Read `docs/AOT_SITE_MANAGEMENT_STANDARDS.md`.
3. Run the drift guard from the repo root.
4. Confirm production branch/source-of-truth with live `curl` checks; do not trust stale branch labels.
5. For content restoration, start with GRO-2474 and prioritize snorkel/revenue pages.
6. For style normalization, start with GRO-2476 and classify old/new templates before rewriting CSS.
7. Do not blind merge `master` into `main`.
8. After every restored page batch, verify production HTTP 200 and affected internal links/CTAs.
9. Update this OKF report or add a dated follow-up report with results.

## Page Restoration Acceptance Criteria

A restored page is not complete until:

- Production or preview URL returns 200.
- `<title>`, meta description, canonical, OG/Twitter tags are page-specific.
- JSON-LD is valid and not copied from an unrelated template.
- Relevant FareHarbor item IDs are preserved.
- Internal links do not point to 404s.
- Mobile header/sticky CTA/footer are visually consistent.
- If style is legacy, a linked style-normalization follow-up exists.

## Style Normalization Acceptance Criteria

Style audit should classify pages into:

1. Current acceptable template/style
2. Verbatim-restored pages needing normalization
3. Legacy WordPress/Kadence artifact pages
4. Booking/sticky CTA mismatch pages
5. Mobile/header/footer inconsistency pages

Priority order:

1. Revenue pages and booking funnels
2. Pages with active internal links from live pages
3. Japanese mirrors of revenue pages
4. Informational guide pages
5. Redirect placeholder pages

## Revenue Funnel Priority

The first content recovery funnel is:

```text
/sharks-cove-snorkeling/
/sharks-cove-snorkeling-guide/
→ /rentals/snorkel-gear-rentals/
→ /guides/eating-your-way-windward-to-north-shore/
```

Known commercial details for `/rentals/snorkel-gear-rentals/`:

- FareHarbor item: `7872`
- Price: `$18`
- Promise: full-day snorkel rental + after-hours return
- Route: Kailua pickup → Windward Coast → North Shore / Sharks Cove
- Linked guide: Eating Your Way from Windward Oahu to the North Shore

## Risk Register

| Risk | Severity | Mitigation |
|---|---:|---|
| Blind merge overwrites production behavior | High | Guardrails + no-blind-merge standard |
| Restored pages bring legacy style drift | High | GRO-2476 style audit + verbatim/normalized classification |
| Production branch assumption remains wrong | High | Live curl verification before edit/merge |
| Sitemap/redirect drift sends users to 404s | High | Drift guard + post-restore sitemap/redirect verification |
| FareHarbor item IDs lost during copy | High | Booking standard + page acceptance criteria |
| Agents continue page whack-a-mole | Medium | OKF report + repo standards + skill update |

## Related Artifacts

- Repo standards: `docs/AOT_SITE_MANAGEMENT_STANDARDS.md`
- Drift guard: `scripts/aot_branch_drift_guard.py`
- Workflow: `.github/workflows/aot-branch-drift.yml`
- Governance config: `PRISMATIC_ENGINE.yaml`
- PR: <https://github.com/mbgulden/active-oahu-tours-mirror/pull/16>
- Linear parent: <https://linear.app/growthwebdev/issue/GRO-2473/aot-branch-drift-audit-production-sync-plan-main-vs-master>
- Content restore: <https://linear.app/growthwebdev/issue/GRO-2474/aot-restore-approved-master-only-content-pages-to-production-branch>
- Prevention guard: <https://linear.app/growthwebdev/issue/GRO-2475/aot-add-branch-drift-prevention-guard-for-production-deploy-branch>
- Style audit: <https://linear.app/growthwebdev/issue/GRO-2476/aot-style-normalization-audit-for-oldnew-page-inconsistency>

## Next Action

Kai Content should execute GRO-2474 using this OKF report plus the repo standards as context. Kai CSS should execute GRO-2476 before broad style changes. Fred should verify restored URLs and keep the live-link watcher active until the snorkel funnel is live.
