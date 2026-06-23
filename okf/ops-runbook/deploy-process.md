# Deploy Process for AOT

## What gets deployed

The `site/` directory in this repo is the deploy artifact. Cloudflare Pages
uses `destination_dir: site` (configured in the Pages project), so files
under `site/` are what get served.

**This means:**
- `site/index.html` → served at `https://activeoahutours.com/`
- `site/_redirects` → served as the canonical `_redirects` file (CF looks here)
- `site/_headers` → served as the canonical `_headers` file
- Everything else under `site/` is mirrored as-is at the corresponding URL

**Note:** The repo-root `_redirects` and `site/_redirects` BOTH end up
active in production. CF Pages reads `site/_redirects` as the canonical
entry, and the root `_redirects` is also evaluated (possibly via build-time
concat). Test BOTH paths when adding redirects. See `cloudflare-config.md`
for verification commands.

## Branch flow

```
┌─────────────────────────────────────────────────────────────┐
│ main (production)                                           │
│                                                             │
│ * Michael merges PRs here manually                          │
│ * Cloudflare Pages auto-deploys on push                     │
│ * Live at https://activeoahutours.com                       │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │  manual PR merge
                              │
┌─────────────────────────────────────────────────────────────┐
│ feat/<author>-GRO-XXXX-desc (your feature branch)          │
│                                                             │
│ * Anyone can push here                                      │
│ * Cloudflare Pages auto-builds preview                      │
│ * Preview at https://<hash>.active-oahu-tours-mirror.pages.dev │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │  git checkout -b feat/...
                              │
┌─────────────────────────────────────────────────────────────┐
│ staging (Michael's in-progress fixes)                       │
│                                                             │
│ * NOT a pre-production env                                  │
│ * Schema/SEO/JA work in flight                              │
│ * Michael merges to main when ready                         │
└─────────────────────────────────────────────────────────────┘
```

**Do NOT:**
- Push directly to `main` (pre-push hook blocks; if it doesn't, that's a bug)
- Push to `staging` unless you're Michael
- Cherry-pick from `staging` to your branch (those commits get reorganized)

## CF Pages build behavior

- **Build command**: empty (no build step, site/ is the static output)
- **Root directory**: repo root
- **Destination directory**: `site/`
- **Production branch**: `main`
- **Preview branches**: any other branch gets a preview URL automatically

Each push to a feature branch triggers:
1. GitHub webhook → CF Pages
2. CF clones the repo at the pushed commit
3. CF serves files from `site/`
4. CF returns a preview URL like `https://<hash>.active-oahu-tours-mirror.pages.dev`
5. CF runs any cloudflare-config (page rules, WAF, etc.) which already apply

**Edge changes** (WAF rules, transform rules, page rules) take effect
**immediately** when applied via API or dashboard — no deploy needed.

**Source changes** (HTML, JS, CSS, files in `site/`) take effect after a
deploy — typically 30-60 seconds for a new commit to `main`.

## Typical workflows

### "Edit a single page"
1. Branch off main: `git checkout -b feat/kai-GRO-XXXX-desc`
2. Edit `site/<page>/index.html`
3. `git diff` to verify
4. Commit, push
5. Open PR (`.github/pull_request_template.md`)
6. Wait for preview deploy
7. Test on preview URL
8. Post PR link in Linear, wait for Michael to merge

### "Add a Cloudflare WAF rule"
1. Capture current ruleset state via API (save to `/tmp/before.json`)
2. Add rule via `PUT /zones/{id}/rulesets/{ruleset_id}` with new rules array
3. Verify via live curl
4. Update Linear issue with: rule ID, expression, expected behavior
5. No PR needed (CF state is in dashboard, not git)
6. Rollback: capture before/after diff, know how to revert

### "Bulk edit via script"
1. Write the script under `scripts/` with a `--dry-run` flag
2. Test on a single sample file
3. Run `--dry-run` on the full site, inspect the output
4. Run for real
5. Commit the script AND the bulk diff in ONE commit
6. Branch name: `feat/kai-GRO-XXXX-bulk-edit-name`
7. PR with the bulk stats in the description

### "Rollback a bad merge"
```bash
# Option 1: Revert the merge commit
git checkout main
git pull origin main
git revert <merge-commit-sha>
git push origin main   # CF auto-deploys the revert

# Option 2: For CF changes, revert via API
# See cloudflare-config.md for rollback commands
```

## Deploy timing

| Action | Time to live |
|---|---|
| Git push to `main` | 30-60 seconds |
| Git push to feature branch (preview) | 30-60 seconds |
| CF edge rule change | Immediate (next request) |
| DNS record change | Propagation-dependent (usually <60s with proxy) |
| Page rule change | ~30 seconds |
| Transform rule change | ~30 seconds |

## Monitoring post-deploy

```bash
# Real-time CF events
curl -sS -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "X-Auth-Email: $CLOUDFLARE_AOT_EMAIL" -H "X-Auth-Key: $CLOUDFLARE_AOT_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"query":"{ viewer { accounts(filter: {accountTag: \"'$CLOUDFLARE_AOT_ACCOUNT_ID'\"}) { firewallEventsAdaptive(filter: {datetime_gt: \"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'\"}, limit: 50, orderBy: [datetime_DESC]) { action clientIP datetime clientRequestPath ruleId } } } }"}'

# Lighthouse after deploy
npx --yes lighthouse https://activeoahutours.com/ --preset=desktop ...
```