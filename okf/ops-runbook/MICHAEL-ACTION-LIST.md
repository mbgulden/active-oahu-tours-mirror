# What Michael Needs to Do — AOT Workflow Setup

**Date:** 2026-06-23
**Kai:** This is your action list. Each item has a difficulty rating, time estimate, and step-by-step instructions. I did everything I could autonomously. The remaining items need you (or someone with repo admin access on github.com/mbgulden).

---

## TL;DR — What's waiting on you

| # | Action | Difficulty | Time | Why you |
|---|---|---|---|---|
| 1 | Merge 6 open PRs | Easy | 10 min | Manual-only policy |
| 2 | Enable GitHub Actions | Easy | 5 min | Repo admin only |
| 3 | Install npm tooling locally | Easy | 2 min | Needs `npm install` approval |
| 4 | Decide on staging → main promotion | Strategic | Decision | Deployment decision |
| 5 | Set up branch protection rules | Medium | 15 min | Repo admin only |
| 6 | Choose AI bot protection stance | Strategic | Decision | Already policy (off), confirm |

---

## 1. Merge the 6 open PRs (Easy — 10 minutes)

All these have been reviewed, tested on preview, and have Lighthouse data.

| PR | Title | What it does | Why merge |
|---|---|---|---|
| [**PR #8**](https://github.com/mbgulden/active-oahu-tours-mirror/pull/8) | llms.txt for AI | Adds curated tour catalog for ChatGPT/Claude/Perplexity citations | Gets AOT cited in AI search |
| [**PR #10**](https://github.com/mbgulden/active-oahu-tours-mirror/pull/10) | 404 rebuild | 72KB → 5KB, branded helpful page | Better UX for bad links |
| [**PR #11**](https://github.com/mbgulden/active-oahu-tours-mirror/pull/11) | Lanikai redirect | 301 to Sharks Cove (duplicate content fix) | SEO cleanup |
| [**PR #12**](https://github.com/mbgulden/active-oahu-tours-mirror/pull/12) | role=main fix | 247 pages get ARIA landmark | +2 a11y points in Lighthouse |
| [**PR #13**](https://github.com/mbgulden/active-oahu-tours-mirror/pull/13) | Workflow docs | Ops runbook, PR template | Sets up the system |
| [**PR #14**](https://github.com/mbgulden/active-oahu-tours-mirror/pull/14) | Pre-commit tooling | html-validate, stylelint, eslint, husky | Catches bugs before commit |

**Steps:**
1. Open each PR in the GitHub web UI
2. Read the description + check the Cloudflare Pages preview deploy link
3. Click "Merge Pull Request" → "Confirm merge"
4. Wait ~60 seconds for CF Pages to deploy
5. Spot-check `https://activeoahutours.com/` to verify

**Recommended merge order:** #12 → #10 → #11 → #8 → #13 → #14
(do the data changes first, then docs/tooling)

---

## 2. Enable GitHub Actions (Easy — 5 minutes)

Required for: GRO-2242 (Lighthouse CI, link check, lint workflow)

**Steps:**
1. Open https://github.com/mbgulden/active-oahu-tours-mirror/settings/actions
2. Under "Actions permissions", select "Allow all actions and reusable workflows"
3. Click "Save"

**That's it.** AGY can then create the workflow YAMLs in `.github/workflows/`.

**Why it matters:** Without this, the linters I just installed only run locally. With Actions, every PR gets automatic Lighthouse + link checks before merge.

---

## 3. Install npm tooling locally (Easy — 2 minutes)

Required for: GRO-2242 testing the CI, plus pre-commit hooks work after PR #14 merges.

**Steps:**
```bash
cd /home/ubuntu/work/active-oahu-tours-mirror
npm install
```

That's it. The `package.json` from PR #14 already specifies the deps. Husky auto-installs the pre-commit hook on `npm install`.

**Verify:**
```bash
bash scripts/lighthouse.sh production
# Should output Lighthouse scores: 98/81/50/77
```

---

## 4. Promote staging to main (Strategic decision)

**Current state:** `staging` is **16 commits ahead of main**, including:
- Schema injection on 148 pages (GRO-697)
- SEO meta repair on 26 broken pages (GRO-945)
- Japanese page path corrections
- JS audit (jQuery, CF CDN paths, FareHarbor entity fixes)
- 6 new SEO content pages
- Canonical fix on homepage (currently broken on production!)

**Why this matters:**
- The **homepage canonical is broken in production right now** (`href="/"` instead of absolute). Google's been seeing the bad version since June 7.
- Lighthouse SEO is at 77/100 (below our 90 threshold) partly because of this
- Other staging fixes would improve production Lighthouse scores

**What I recommend:** Promote staging to main as soon as you can. The risks:
- Some staging changes might conflict with each other
- Any staging commit that's still in flight should land in a separate feat branch first

**Steps to promote staging safely:**
```bash
# In your local clone of the repo
git checkout main
git pull origin main
git merge --no-ff origin/staging -m "Promote staging fixes to production"
git push origin main
# CF Pages auto-deploys in ~60s
# Run lighthouse on prod to compare to baseline
bash scripts/lighthouse.sh production
```

**Or, safer (more isolated):**
1. Cherry-pick specific commits from staging into individual feat branches
2. Test each via PR preview
3. Merge each as a separate PR

I can do the cherry-pick work if you want — just tell me which staging commits are stable.

---

## 5. Branch protection rules (Medium — 15 minutes, GitHub UI)

Recommended settings for `main` and `staging`:

**For `main`:**
- ☑ Require pull request reviews before merging (1 approval minimum)
- ☑ Require status checks to pass before merging (will need GH Actions enabled first)
- ☑ Require branches to be up to date before merging
- ☑ Do not allow force pushes
- ☑ Do not allow deletions
- ☑ Allow squash merging (keeps history clean)

**For `staging`:**
- ☑ Require pull request reviews (can be looser — 0 approvals)
- ☑ Do not allow force pushes
- ☑ Allow squash merging

**Steps:**
1. https://github.com/mbgulden/active-oahu-tours-mirror/settings/branches
2. Click "Add rule" for `main`
3. Configure as above
4. Repeat for `staging`

---

## 6. AI bot protection — confirm stance (Already done, just verify)

Per your earlier direction: **Bot Fight Mode is OFF permanently.** AI bot protection is **disabled**. Currently:

- `ai_bots_protection`: disabled
- `crawler_protection`: disabled
- `sbfm_definitely_automated`: allow
- `sbfm_verified_bots`: allow

This is intentional and aligned with the AI-as-opportunity strategy we discussed. **No action needed** — just confirming we don't accidentally turn these back on.

If you ever want to revisit: the Linear issue GRO-2215 follow-up is to add `llms.txt` (PR #8) which is the proactive play for AI visibility.

---

## What you DON'T need to do (Kai is handling)

- ✅ Pre-commit tooling setup (PR #14)
- ✅ Ops runbook documentation (PR #13)
- ✅ PR template (in PR #13)
- ✅ Linear task tracking for follow-ups
- ✅ CF edge security hardening (already shipped)
- ✅ Lighthouse baseline + per-PR scores
- ✅ Script bug fix + unit tests

---

## If you only have 5 minutes

Do this minimum:
1. Merge PR #12 (role=main fix) — easy win, real a11y improvement
2. Merge PR #8 (llms.txt) — gets AI citations started

If you have 30 minutes:
3. Merge the rest of the PRs in order
4. Decide on staging promotion (item #4 above)

If you have 2 hours:
5. Enable GH Actions + branch protection
6. Promote staging safely (cherry-pick the canonical fix first)
7. Run lighthouse on prod to measure the combined improvement

---

## Questions / clarifications needed

If anything above is unclear, ping me with the question. I have context on all of this.

**Things I made decisions on that you might want to override:**

| Decision | What I chose | Alternative |
|---|---|---|
| Branch name format | `feat/kai-GRO-XXXX-desc` | `feature/kai/...` (Git Flow style) |
| PR template sections | 7 mandatory sections | Minimal (just summary + test plan) |
| Linter permissiveness | Tuned to legacy HTML | Strict (would fail on 245 existing files) |
| Pre-commit hook scope | Only staged files (via lint-staged) | Site-wide (would block all commits) |
| Lighthouse baseline | Desktop only | Mobile + desktop |

Tell me if any of these are wrong for your taste.