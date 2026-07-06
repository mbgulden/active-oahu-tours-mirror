# Prismatic Web Plugin — Governance Guard

This package turns the Active Oahu Tours recovery into a reusable governance layer for any Prismatic-managed website.

It is designed for long-lived static/marketing/tourism sites where multiple agents touch content, CSS, redirects, SEO, deployment, and OKF documentation.

## What it installs

| Artifact | Target path | Purpose |
|---|---|---|
| Config | `.prismatic-web-governance.json` | Site-specific branches, URLs, protected paths, live markers, agent lanes |
| Guard | `scripts/prismatic_web_governance.py` | Stdlib-only local/CI/cron checker |
| Workflow | `.github/workflows/prismatic-web-governance.yml` | Scheduled/manual/PR governance report |
| Standards section | human docs | Require the guard before staging/production/PR safety claims |

## Guard checks

1. Local workspace cleanliness.
2. Production/staging ahead-behind counts.
3. `git cherry -v` patch-equivalence for staging-only commits.
4. Production/staging tree-SHA equality for history-only drift.
5. Open PR hygiene: age, mergeability, protected paths, overlap.
6. Live production homepage markers.
7. Stale remote branches.
8. Markdown + JSON reports for CI, Linear, OKF, or Hermes cron.

## Install into another site repo

From a repo that already contains this package:

```bash
python3 prismatic-web-plugin/governance/scripts/install_prismatic_web_governance.py \
  --target /path/to/site-repo \
  --site-name "Example Site" \
  --repo owner/example-site \
  --production-url https://example.com/ \
  --staging-url https://example.pages.dev/ \
  --homepage-path site/index.html \
  --required-marker "Example Site" \
  --forbidden-marker "old-broken-block"
```

Then in the target repo:

```bash
git fetch origin --prune
python3 scripts/prismatic_web_governance.py \
  --config .prismatic-web-governance.json \
  --report /tmp/prismatic-web-governance.md \
  --json /tmp/prismatic-web-governance.json \
  --report-only
```

Use `--report-only` during initial installation so existing site debt is reported but does not block adoption. Once the backlog is clean, run without `--report-only` for normal fail-on-FAIL behavior or with `--strict` for fail-on-WARN.

## Required human operating rule

No agent should claim any of the following without running the guard and citing the report:

- “staging has the fix”
- “production is stale”
- “this PR is safe”
- “homepage/nav is fixed”
- “branches are in sync”

## Staging reconciliation rule

Never merge stale staging into production merely to catch up history.

Decision tree:

1. `staging` behind `main` > policy → bring staging forward from main through a normal PR, or reset/rebuild only after approval.
2. `git cherry -v main staging` shows only `-` lines → staging-only commits are patch-equivalent upstream; they are cleanup debt, not unreleased work.
3. `git cherry -v main staging` shows `+` lines → review unique staging work before any reset/rebuild.
4. Production/staging tree SHAs are identical → deployable site is reconciled; remaining ahead/behind is history-only drift. Do not merge staging into production to chase history shape.

## Active Oahu proof point

This package was extracted after the Active Oahu Tours homepage/nav recovery:

- production nav restored to `nav-fix.css?v=10`
- integrated homepage About copy verified live
- `aot-quick-answer` regression removed
- open PR queue cleared
- staging brought forward from main through PRs, no force-push
- daily Hermes watchdog installed
- private/public OKF boundaries documented

## Distribution checklist

Before calling a site “governed,” verify:

- [ ] Config exists and parses.
- [ ] Guard compiles.
- [ ] Workflow invokes guard with `--report-only` while debt exists.
- [ ] Required and forbidden live markers are site-specific, not copied blindly.
- [ ] Production/staging branches are configured correctly.
- [ ] Protected paths include redirects, robots/sitemap, config, and deployment-critical files.
- [ ] Site standards require guard output before staging/production claims.
- [ ] Optional Hermes watchdog runs from a dedicated clean worktree.
- [ ] OKF records define public/private repo boundaries.
