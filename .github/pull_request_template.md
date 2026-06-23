## Pull Request: [TYPE]/[AUTHOR-INITIALS]-[LINEAR-ID]-[SHORT-DESC]

**Linear Issue**: [GRO-XXXX](https://linear.app/growthwebdev/issue/GRO-XXXX)

<!--
Replace this block with the PR title in the format: type/author-GRO-XXXX-desc
  Types: feat | fix | chore | docs | refactor
  Example: feat/kai-GRO-2215-add-llms-txt

Fill in the sections below. Delete any section that's not applicable.
For trivial fixes (typo, single-line), condensed sections are OK.
-->

### Summary

[1-3 sentence description of what this PR does and why. Reference the Linear issue if one exists.]

### Scope (Files Changed)

[List significant files or directories changed. For bulk edits, group them:
- `site/247 HTML files` (bulk edit via `scripts/add_main_landmark.py`)
- `scripts/add_main_landmark.py` (new helper)
- `site/_headers` (cache-control update)]

### Risk Assessment

- **Blast Radius**: [e.g., "Isolated to 404 page", "Site-wide template change", "Affects SEO-critical pages", "Cloudflare edge rule (live instantly)"]
- **Worst Case Scenario**: [e.g., "Broken 404 page = 5xx on missing URLs", "CSS regression across site", "SEO degradation", "Blocks legitimate users via WAF rule"]
- **Rollback Plan**: [e.g., "`git revert <commit>` + auto-deploy", "Delete CF rule via API", "Toggle feature flag"]

### Test Plan

1. **Preview URL**: [Link to Cloudflare Pages PR deploy, e.g., `https://abc123.active-oahu-tours-mirror.pages.dev`]
2. **Verify Functionality**: [e.g., "Navigate to /activities/kailua-kayak-twin-islands-guided-tour/ and confirm CTA still works"]
3. **Visual Check**: [e.g., "Check 404 page renders cleanly on mobile (375px)"]
4. **Accessibility Check**: [if applicable: "Lighthouse a11y score >= 85 on preview"]
5. **Link Check**: [if applicable: "No new 404s in CF logs"]

### Lighthouse Impact (if applicable)

| Category | Before | Expected after |
|---|---|---|
| Performance | XX | XX |
| Accessibility | XX | XX |
| Best Practices | XX | XX |
| SEO | XX | XX |

[Skip this section if change doesn't affect rendered output]

### Cloudflare Edge Changes (if applicable)

- [ ] WAF rule added/modified
- [ ] Transform rule added/modified
- [ ] Page rule added/modified
- [ ] Zone setting changed
- [ ] DNS record changed

[For edge changes, run `scripts/cf_audit.sh` (TODO) to capture before/after, and verify the rule fires as expected via Security Events.]

### Linear Update

<!--
When this PR merges to main, Linear will auto-transition the issue to Done.
If you need to transition immediately or to a different state, do it manually:
  - Done (after merge verified in production)
  - Canceled (if you decided not to ship)
  - Blocked (waiting on something)
-->

Closes [GRO-XXXX]

---

### Pre-merge Checklist

- [ ] Branch rebased on latest `main` (or has clean merge base)
- [ ] Preview deploy tested manually
- [ ] No `git push --force` was used (this PR must be a normal push)
- [ ] If this is a bulk edit, the script used has been tested on a few sample files
- [ ] Files outside `site/` and `scripts/` only changed intentionally
- [ ] No secrets, API keys, or tokens in the diff
- [ ] Commit message follows `<Agent> [GRO-XXXX]: Brief description` format