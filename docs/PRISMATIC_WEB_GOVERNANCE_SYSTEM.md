# Prismatic Web Governance System

**Status:** Active Oahu implementation + portable Prismatic Web Plugin pattern  
**Owner:** Kai / Prismatic web-site operators  
**Primary guard:** [`scripts/prismatic_web_governance.py`](../scripts/prismatic_web_governance.py)

## Why this exists

A long-lived revenue website cannot depend on agent memory, branch folklore, or a single “staging looks okay” check. Active Oahu already hit the bad version of that pattern:

- staging/main/master drift
- open PRs holding real fixes while production stayed rough
- Cloudflare cache making live state look older than source
- agents checking different workspaces and drawing different conclusions
- homepage/nav regressions left in PR limbo

This system turns that into a repeatable governance layer that can ship with the **Prismatic Web Plugin** for every managed site.

## What the system enforces

| Governance surface | Guardrail |
|---|---|
| Branch source-of-truth | Compares production/staging branches and fails when staging is behind production beyond policy |
| PR hygiene | Lists open PRs, mergeability, age, protected-path touches, and file overlap between PRs |
| Workspace safety | Warns if the local worktree is dirty so agents do not `git add .` someone else’s WIP |
| Live production freshness | Fetches production with `Cache-Control: no-cache`, checks HTTP status and required/forbidden markers |
| Stale branches | Flags old remote branches outside the allowed long-lived branch set |
| CI reporting | Writes Markdown + optional JSON for GitHub Actions, Linear comments, or Hermes cron |

## Files

| File | Purpose |
|---|---|
| [`.prismatic-web-governance.json`](../.prismatic-web-governance.json) | Site-specific policy/config |
| [`scripts/prismatic_web_governance.py`](../scripts/prismatic_web_governance.py) | Portable stdlib-only checker |
| [`.github/workflows/prismatic-web-governance.yml`](../.github/workflows/prismatic-web-governance.yml) | Daily/manual/PR governance report |
| [`docs/PRISMATIC_WEB_GOVERNANCE_SYSTEM.md`](PRISMATIC_WEB_GOVERNANCE_SYSTEM.md) | This operating spec |

## Running locally

```bash
git fetch origin --prune
python3 scripts/prismatic_web_governance.py \
  --config .prismatic-web-governance.json \
  --report /tmp/prismatic-web-governance.md \
  --json /tmp/prismatic-web-governance.json
```

Strict mode is for CI gates after the current backlog is clean:

```bash
python3 scripts/prismatic_web_governance.py --strict
```

Default exit behavior:

- `PASS` → exit `0`
- `WARN` → exit `0` unless `--strict`
- `FAIL` → exit `1`
- `--report-only` → always exit `0` after writing reports; use while installing the guard or during known-cleanup periods

## AOT policy encoded today

The current Active Oahu config deliberately encodes the homepage/nav fixes that just shipped:

Required production markers:

- `nav-fix.css?v=10`
- `Active Oahu is a Kailua-based outfitter`

Forbidden production markers:

- `aot-quick-answer`

That means the checker will catch a rollback to the cramped nav or the ugly homepage quick-answer block.

## How agents should use it

Before saying “staging has the fix,” “production is stale,” “this PR is safe,” or “homepage is fixed,” run the guard and include the report path/output in the Linear or PR comment.

Minimum agent loop:

1. `git fetch origin --prune`
2. Run `python3 scripts/prismatic_web_governance.py --report /tmp/<site>-governance.md`
3. Read the WARN/FAIL sections.
4. If touching site files, fix the relevant issue or explicitly document the waiver.
5. Never promote or merge around a FAIL unless Michael explicitly accepts the risk.

## Plugin distribution contract

For a new Prismatic-managed website, the plugin should install:

1. `.prismatic-web-governance.json` with site URLs, branch names, protected paths, required markers, and agent lanes.
2. `scripts/prismatic_web_governance.py` unchanged.
3. A GitHub Action equivalent to `.github/workflows/prismatic-web-governance.yml`.
4. A project-specific doc that explains the site’s promotion policy and live verification markers.

Required config fields:

```json
{
  "site": {
    "name": "Example Site",
    "repo": "owner/repo",
    "production_branch": "origin/main",
    "staging_branch": "origin/staging",
    "production_url": "https://example.com/",
    "staging_url": "https://example.pages.dev/",
    "homepage_path": "site/index.html"
  },
  "policy": {
    "max_open_pr_age_days": 7,
    "max_staging_behind_production_commits": 0,
    "required_production_markers": [],
    "forbidden_production_markers": [],
    "protected_paths": []
  }
}
```

## Definition of done for this governance layer

- The guard runs locally.
- The guard writes a Markdown report.
- The guard catches the real AOT branch/PR/live-marker state.
- GitHub Actions can run it on PRs, schedule, and manual dispatch.
- Future sites can copy the script and only change JSON config.

## Current known caveat

The first AOT run may report existing branch/PR hygiene warnings because it is doing its job: surfacing stale or divergent work instead of letting it rot quietly. Treat those as the cleanup backlog, not as a script failure.
