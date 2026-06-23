# Active Oahu Tours — Ops Runbook

This is the canonical reference for everything operational about the AOT site.
**If you're an agent (Kai, Fred, AGY, Jules) or Michael touching the site,
start here.**

## Contents

| Doc | What's in it |
|---|---|
| [git-workflow.md](git-workflow.md) | Branch naming, commit messages, force-push rules, PR flow |
| [cloudflare-config.md](cloudflare-config.md) | CF account + zone setup, WAF rules, transform rules, page rules |
| [deploy-process.md](deploy-process.md) | How staging → main → production actually works, rollback |
| [testing-guidelines.md](testing-guidelines.md) | Pre-PR checks, post-merge verification, Lighthouse baseline |
| [linear-integration.md](linear-integration.md) | How PRs interact with Linear, issue state transitions |
| [scripts/](scripts/) | Helper Python scripts (all idempotent) |

## TL;DR for new agents

```bash
# 1. Check your assigned Linear issues
#    https://linear.app/growthwebdev/project/active-oahu-tours-static-mirror-migration

# 2. Create a feature branch (see git-workflow.md)
cd /home/ubuntu/work/active-oahu-tours-mirror
git checkout main
git pull origin main
git checkout -b feat/<your-initials>-GRO-XXXX-<short-desc>

# 3. Make changes, run script helpers in scripts/ as needed
python3 scripts/add_main_landmark.py --dry-run   # example

# 4. Commit with conventional format
git add <specific-files>
git commit -m "[Kai] GRO-1234: Add llms.txt for AI discovery"

# 5. Push (NEVER --force on shared branches)
git push -u origin feat/your-branch

# 6. Open PR via GitHub API or UI
# 7. Verify Cloudflare Pages preview deploy
# 8. Update Linear with PR link + status comment
# 9. Wait for Michael's manual merge to main
```

## Hard rules (NEVER violate)

1. **Never `git push --force` to `main`, `staging`, or `deploy-fresh`.**
   - Force-push is only acceptable on your own private feature branch.
   - If you force-pushed and lost work, use `git reflog` to recover.
2. **Never push directly to `main`.** Always go through a PR.
3. **Never edit files in `okf/` unless you're updating ops docs.** It's the
   canonical knowledge base.
4. **Never commit `.env`, API tokens, or PATs.** Check `git diff` before commit.
5. **Never delete `site/_redirects` or root `_redirects` without checking
   both are empty.** Both are read by CF Pages (the canonical one is whichever
   Pages reads as the entry redirect file at deploy time).
6. **Never skip the preview-deploy verification step.** Even for "obvious"
   fixes.
7. **Never merge staging into main without explicit Michael approval.**

## When in doubt

- Read [git-workflow.md](git-workflow.md) for git operations.
- Read [cloudflare-config.md](cloudflare-config.md) before touching CF.
- Read [testing-guidelines.md](testing-guidelines.md) before opening a PR.
- If you're an agent and something's ambiguous: file a Linear comment with
  options, ask Michael via Telegram, don't guess.