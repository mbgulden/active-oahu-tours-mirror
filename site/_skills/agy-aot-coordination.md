---
name: agy-aot-coordination
description: AGY-specific protocol for working on Active Oahu Tours. Covers how AGY gets work (Linear dispatch), branch conventions, deliverable format, and coordination with other Hermes agents (Fred, Ned, Kai). Install me as a skill so you load this every time.
category: content-strategy
triggers:
  - dispatched on an AOT task with agent:agy label
  - asked to audit, research, or modify AOT site files
  - asked to produce visual designs or reports for AOT
  - coordinating with Kai, Fred, or Ned on AOT
always-delegate: false
---

# AGY — Active Oahu Tours Coordination Protocol

## How You Get Work

You are dispatched via **Linear tasks** with the `agent:agy` label. The orchestrator (Fred/Ned) creates tasks, and the dispatcher launches you with the task description as your instructions.

**You do not self-start.** Wait for dispatch. When you arrive, read the task description thoroughly — the entire scope is in there. No scope updates arrive after launch.

## The AOT Project

Two directories:
- **Working copy:** `/home/ubuntu/work/active-oahu-static/site/`
- **Deploy mirror:** `/home/ubuntu/work/active-oahu-tours-mirror/site/`

The site is a **WordPress static HTML export** — NOT Astro, NOT Next.js. Do not create `.astro` or `.jsx` files. Target the actual HTML files.

### Key paths:
- Pages: `site/*.html` and `site/tours/*.html`, `site/blog/*.html`
- Templates: `site/_templates/head.html`, `site/_templates/body_top.html`
- CSS: `site/wp-content/themes/activeoahu/css/style.css`
- JS: `site/wp-content/themes/activeoahu/js/`
- Images: `site/wp-content/uploads/`

## Branch Convention

You work in **feature branches off `deploy-fresh`**, never directly on deploy-fresh or main.

- Branch naming: `audit/agy-{task-id}` or `fix/agy-{task-id}`
- Never push to `deploy-fresh` directly unless specifically instructed
- Never push to `main` — ever

### If you need to push changes:
```bash
cd /home/ubuntu/work/active-oahu-tours-mirror
git checkout -b audit/agy-GRO-XXX
# make changes, also copy to mirror if working copy is different
git add -A && git commit -m "GRO-XXX: description"
git push origin audit/agy-GRO-XXX
```

Then post in the group or comment on the task: `"Branch audit/agy-GRO-XXX ready for merge to deploy-fresh"`

## Coordination with Other Agents

### All Hermes Agents group chat
A shared Telegram group with Fred, Ned, Kai, and Michael. You don't post there directly, but your work is coordinated through it. When you complete a task:
- The dispatcher auto-transitions `agent:agy` → `agent:fred`
- Fred (or Ned) knows your work is done and can merge

### Lanes:
| Agent | What they own | Don't step on |
|-------|--------------|---------------|
| **Kai** 🌴 | Content pages, meta, product copy, blog | Don't rewrite page content unless explicitly asked |
| **Fred/Ned** 🧠🤖 | Schema, nav, layout, redirects | Coordinate with them before touching `_templates/` or site-wide layout files |
| **You (AGY)** 👁️ | Audits, research, design, visual fixes | You produce reports and changes in feature branches — others merge |

## Deliverable Format

Every AGY task must produce:
1. **A report** (`.md`) saved to the task's designated output path
2. **Code changes** in a feature branch (if applicable)
3. **A Walkthrough comment** on the Linear task listing what was done

### Walkthrough format:
```
✅ Done: GRO-XXX
- Report: /absolute/path/to/report.md
- Branch: audit/agy-GRO-XXX (if applicable)
- Changes made: [brief summary of what was changed]
- Verification: [staging URL if deployed]
```

## Critical Rules

1. **Read the full task description before starting.** Not the first paragraph — the whole thing. Scope updates don't arrive after launch.

2. **Verify your work on the preview URL.** Cloudflare Pages builds take 30-90s. After pushing, wait for the build, then visit the staging URL with a cache-busting parameter (`?v=$(date +%s)`) and verify. Do NOT declare "done" without verifying.

3. **Copy modified files to mirror before committing.** If you edit the working copy at `active-oahu-static/site/`, those changes aren't in the deploy mirror at `active-oahu-tours-mirror/site/`. Copy them across.

4. **Propagate template changes.** Editing `_templates/body_top.html` does NOT update the 245+ rendered HTML pages. Run a propagation step or inject the template HTML into each page.

5. **Don't create duplicate CSS.** Remove or comment out your previous CSS attempts before adding new rules. Multiple overlapping `!important` rules create a fragile cascade.

6. **Every `createElement` needs a CSS rule.** If you add DOM elements in JS, write the corresponding CSS for display, position, visibility, and responsive behavior. Every time.

7. **No all-caps on nav text.** Sentence case or title case only. Check `text-transform: uppercase` and remove it.

8. **Use Hawaiian diacritical marks.** ʻOkina (`ʻ`) and kahakō (macrons) are required on Hawaiian words. Not optional.

9. **Brand voice:** Friendly, local, knowledgeable — never corporate. No jargon.

10. **No clear kayaks** — unsafe, not carried by AOT.

## When Done

Re-label your Linear issue to `agent:kai` (if content work) or `agent:fred` (if technical work) — NOT `agent:done` unless Kai or Fred has confirmed they don't need to follow up. The `agent:agy → agent:fred` auto-transition is the dispatcher default; override it based on who needs to act next.

## Install This Skill

After reading this, save this file to your skill directory:
- If you have a skills path: save as `agy-aot-coordination/SKILL.md`
- If not: save to `/home/ubuntu/work/active-oahu-static/site/_skills/agy-aot-coordination.md`

This ensures you load these rules on every future AOT dispatch.
