# Git Workflow for AOT

## Branch naming

Pattern: `<type>/<author-initials>-<linear-id>-<short-desc>`

- **Type**: `feat` | `fix` | `chore` | `docs` | `refactor` | `audit`
- **Author**: 2-3 letter initials (Kai = `kai`, Fred = `fred`, AGY = `agy`, etc.)
- **Linear ID**: `GRO-XXXX` (the issue identifier, not the UUID)
- **Short desc**: kebab-case, ≤ 40 chars, no branch prefixes

**Examples:**
- `feat/kai-GRO-2215-add-llms-txt`
- `fix/agy-GRO-586-lanikai-redirect`
- `chore/kai-GRO-2003-bump-deps`
- `docs/kai-GRO-2050-runbook-update`

**Bad:**
- `feat/llms-txt` (missing author + Linear ID)
- `feature/kai/llms-txt` (wrong prefix style)
- `feat/kai-fix-bug` (missing Linear ID — if there's no issue, file one first)

## Commit messages

Format: `[<Author>] <Linear-ID>: <Imperative description>`

- **Author**: same as branch initials
- **Imperative**: "Add X", "Fix Y", "Refactor Z" (not "Added", "Fixed")
- **Description**: ≤ 72 chars on first line, optional body below

**Examples:**
```
[Kai] GRO-2215: Add llms.txt for AI crawler discovery
[Agy] GRO-586: Redirect Lanikai snorkel page to Sharks Cove
[Fred] GRO-2224: Add Prismatic Engine pre-push hook
```

**Multi-commit PRs:** Use `git rebase -i` to clean up commits before opening the
PR. Aim for atomic commits that could each be reverted independently.

## Branch lifecycle

```
main  (production — Michael merges manually only)
  │
  ├── feat/kai-GRO-XXXX-desc  (your feature branch, off main)
  │     │
  │     └── (your commits here)
  │
  └── (PR opened: feat/kai-GRO-XXXX-desc → main)
        │
        └── (Cloudflare Pages auto-builds preview URL)
              │
              └── (you verify on preview, iterate)
                    │
                    └── (Michael merges → production deploys)
```

**Branch off `main`, not `staging`.** Staging has fixes not yet approved for
production (see "Why staging exists" below).

## Why staging exists

`staging` is **not** a pre-production environment. It's Michael's working
branch for in-progress fixes that shouldn't go to main yet. Typical contents:

- Schema injection fixes (GRO-697)
- Japanese page path corrections
- SEO meta repair work
- 6 new SEO content pages in flight

When Michael says "merge staging into main" or "promote staging", he means
the staging branch is ready for production. **Do not auto-merge staging.**

If you need a fix that's already on staging, branch off main and re-implement
it (don't cherry-pick from staging — those commits may be reorganized).

## Force-push rules

- ✅ `git push --force-with-lease` to **your own private feature branch** is OK
- ❌ `git push --force` to ANY shared branch (main, staging, deploy-fresh, master)
- ❌ `git push --force-with-lease` to any branch other than your own

**Why:** The pre-push hook (`scripts/pre-push-hook.py`) already blocks force
pushes to protected branches. If the hook lets one through, that's a bug —
report it, don't bypass it.

**If you accidentally force-pushed and lost work:**
```bash
# Find the lost commit
git reflog

# Cherry-pick or reset to it
git reset --hard <commit-sha>   # only on your local feature branch
```

## Pre-commit checks (manual for now)

Before every commit:
```bash
# 1. Check what's about to be committed
git diff --stat

# 2. Verify no secrets in the diff
git diff | grep -iE "(api_key|secret|token|password|bearer)" | head -5

# 3. Verify only intended files
git diff --name-only
```

**Automated pre-commit hooks** (lychee, html-validate, etc.) are planned but
not yet installed. See `testing-guidelines.md` for the current manual process.

## Pull Request workflow

1. Branch off `main` (never staging)
2. Make atomic commits
3. Run pre-PR checks (see `testing-guidelines.md`)
4. Push to your feature branch
5. Open PR via GitHub API or web UI
6. Use the PR template at `.github/pull_request_template.md`
7. Wait for Cloudflare Pages auto-preview deploy
8. Manually verify on the preview URL
9. Post PR link in the Linear issue
10. Wait for Michael to manually merge to main

**PR title format** (matches branch name):
`feat/kai-GRO-2215-add-llms-txt → main`

## Common operations

### "I want to undo my last commit (not pushed yet)"
```bash
git reset --soft HEAD~1    # keeps changes staged
git reset --hard HEAD~1    # discards changes (CAREFUL)
```

### "I want to undo a commit that's already pushed"
```bash
git revert <commit-sha>    # creates new commit that undoes the old one
git push origin your-branch
```

### "I want to sync my branch with latest main"
```bash
git fetch origin main
git rebase origin/main      # rewrites your commit history on top of main
git push --force-with-lease origin your-branch
```

### "I made a mistake in the last commit's message"
```bash
git commit --amend -m "New message"
git push --force-with-lease origin your-branch
```

## See also

- [deploy-process.md](deploy-process.md) — what happens after merge
- [testing-guidelines.md](testing-guidelines.md) — what to verify before PR
- [linear-integration.md](linear-integration.md) — Linear ↔ PR workflow