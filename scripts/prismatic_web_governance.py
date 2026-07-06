#!/usr/bin/env python3
"""Prismatic Web Governance Guard.

A portable governance checker for long-lived static/marketing websites managed by
multiple agents. It turns the lessons from Active Oahu Tours into a repeatable
control plane:

- branch/source-of-truth drift
- open/stale/conflicting PRs
- protected-path PR overlap
- dirty local workspaces
- live homepage marker verification
- markdown + JSON reports suitable for CI, Linear, or Hermes cron

The script is intentionally stdlib-only. It shells out to git and optionally gh.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / ".prismatic-web-governance.json"
CF_SCRIPT_RE = re.compile(r"<script>\(function\(\)\{function c\(\).*?/cdn-cgi/challenge-platform/scripts/jsd/main\.js.*?</script>", re.S)


@dataclass
class Check:
    name: str
    status: str
    summary: str
    details: list[str] = field(default_factory=list)

    def icon(self) -> str:
        return {"pass": "✅", "warn": "🟡", "fail": "❌", "info": "ℹ️"}.get(self.status, "•")


def run(cmd: list[str], *, check: bool = False, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=check)


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args], check=False)
    if check and proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return proc.stdout.strip()


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def parse_iso(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def branch_exists(ref: str) -> bool:
    return run(["git", "rev-parse", "--verify", "--quiet", ref]).returncode == 0


def rev_count(left: str, right: str) -> int:
    out = git("rev-list", "--count", f"{left}..{right}")
    return int(out or "0")


def exclusive_commits(base: str, head: str, limit: int = 10) -> list[str]:
    out = git("log", "--oneline", f"{base}..{head}", f"--max-count={limit}", check=False)
    return [line for line in out.splitlines() if line]


def cherry_equivalence(upstream: str, head: str) -> tuple[int, int, list[str]]:
    """Return (equivalent, unique, sample_lines) for commits in head not in upstream.

    `git cherry` prints '-' for patch-equivalent commits already present upstream
    and '+' for commits whose patch is unique. This is exactly what a website
    staging branch needs before anyone decides whether it can be reset/rebuilt.
    """
    out = git("cherry", "-v", upstream, head, check=False)
    equivalent = 0
    unique = 0
    sample: list[str] = []
    for line in out.splitlines():
        if not line:
            continue
        if line.startswith("-"):
            equivalent += 1
        elif line.startswith("+"):
            unique += 1
        if len(sample) < 10:
            sample.append(line)
    return equivalent, unique, sample


def file_at_ref(ref: str, path: str) -> str:
    proc = run(["git", "show", f"{ref}:{path}"], check=False)
    return proc.stdout if proc.returncode == 0 else ""


def normalize_html(html: str) -> str:
    html = CF_SCRIPT_RE.sub("", html)
    html = re.sub(r"window\.__CF\$cv\$params=.*?;</script>", "</script>", html, flags=re.S)
    return html.strip()


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def fetch_url(url: str, timeout: int = 25) -> tuple[int, dict[str, str], str]:
    req = urllib.request.Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "Prismatic-Web-Governance/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec - governance probes configured URLs
        body = resp.read().decode("utf-8", errors="replace")
        return resp.status, {k.lower(): v for k, v in resp.headers.items()}, body


def gh_json(args: list[str]) -> Any:
    proc = run(["gh", *args], check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout or "null")


def check_workspace() -> Check:
    status = git("status", "--short")
    if status:
        return Check("workspace", "warn", "Local worktree is dirty; do not stage blindly.", status.splitlines()[:40])
    return Check("workspace", "pass", "Local worktree is clean.")


def check_branches(cfg: dict[str, Any]) -> Check:
    site = cfg["site"]
    policy = cfg["policy"]
    prod = site["production_branch"]
    staging = site["staging_branch"]
    details: list[str] = []
    status = "pass"

    git("fetch", "origin", "--prune")
    for ref in [prod, staging, site.get("legacy_content_branch")]:
        if ref and not branch_exists(ref):
            status = "fail"
            details.append(f"Missing configured ref: `{ref}`")

    if branch_exists(prod) and branch_exists(staging):
        staging_behind = rev_count(staging, prod)
        prod_behind = rev_count(prod, staging)
        equiv, unique, cherry_sample = cherry_equivalence(prod, staging)
        details.append(f"`{staging}` is behind `{prod}` by **{staging_behind}** commits.")
        details.append(f"`{prod}` is behind `{staging}` by **{prod_behind}** commits.")
        details.append(f"Staging-only patch equivalence vs production: **{equiv}** equivalent, **{unique}** unique.")
        if staging_behind:
            details.append("Production-only commits not present on staging:")
            details.extend(f"- `{line}`" for line in exclusive_commits(staging, prod, limit=10))
        if prod_behind:
            details.append("Staging-only commits (`git cherry -v production staging`; `-` means patch-equivalent upstream):")
            details.extend(f"- `{line}`" for line in cherry_sample)
        if staging_behind > policy.get("max_staging_behind_production_commits", 0):
            status = "fail"
        # Do not fail merely because staging has patch-equivalent commits: that
        # is cleanup debt, not unreconciled work. Still fail on truly unique
        # staging-only patches unless policy allows them.
        if unique > policy.get("max_production_behind_staging_commits", 0):
            status = "fail"
        if prod_behind and unique == 0:
            details.append("Reconciliation guidance: staging-only commits are patch-equivalent to production. Prefer rebuilding/resetting staging from production after human/governor approval; do not merge stale staging into production.")

    return Check("branch-drift", status, "Production/staging branch topology checked.", details)


def check_open_prs(cfg: dict[str, Any]) -> Check:
    repo = cfg["site"].get("repo")
    policy = cfg["policy"]
    protected_paths = tuple(policy.get("protected_paths", []))
    max_age = int(policy.get("max_open_pr_age_days", 7))
    now = utcnow()

    try:
        prs = gh_json(["pr", "list", "--repo", repo, "--state", "open", "--limit", "100", "--json", "number,title,headRefName,baseRefName,mergeable,mergeStateStatus,updatedAt,url,files"])
    except Exception as exc:  # gh may be unavailable in forks
        return Check("open-prs", "warn", "Could not query GitHub PRs with gh.", [str(exc)])

    if not prs:
        return Check("open-prs", "pass", "No open PRs.")

    status = "pass"
    details: list[str] = []
    file_to_prs: dict[str, list[int]] = {}
    for pr in prs:
        # `gh pr list` can report UNKNOWN merge state until a PR is hydrated.
        # Re-query the individual PR so the governance report does not create
        # false red alarms from GitHub's lazy mergeability computation.
        if str(pr.get("mergeStateStatus") or pr.get("mergeable") or "UNKNOWN").upper() == "UNKNOWN":
            try:
                hydrated = gh_json([
                    "pr", "view", str(pr["number"]), "--repo", repo,
                    "--json", "number,title,headRefName,baseRefName,mergeable,mergeStateStatus,updatedAt,url,files",
                ])
                pr.update(hydrated)
            except Exception:
                pass
        updated = parse_iso(pr["updatedAt"])
        age_days = (now - updated).total_seconds() / 86400
        files = [f.get("path", "") for f in pr.get("files", [])]
        state = pr.get("mergeStateStatus") or pr.get("mergeable") or "UNKNOWN"
        line = f"#{pr['number']} `{pr['headRefName']}` → `{pr['baseRefName']}` `{state}` age={age_days:.1f}d — {pr['title']}"
        if age_days > max_age:
            status = "warn"
            line = "STALE " + line
        if str(state).upper() in {"DIRTY", "CONFLICTING", "BLOCKED", "UNKNOWN"}:
            status = "fail"
            line = "BLOCKED " + line
        if any(p in protected_paths for p in files):
            status = "warn" if status == "pass" else status
            line += " — touches protected path"
        details.append(line)
        for p in files:
            file_to_prs.setdefault(p, []).append(pr["number"])

    overlaps = {p: nums for p, nums in file_to_prs.items() if len(nums) > 1}
    if overlaps:
        status = "fail"
        details.append("PR file overlaps detected:")
        for p, nums in sorted(overlaps.items())[:30]:
            details.append(f"- `{p}` touched by PRs {nums}")

    return Check("open-prs", status, f"{len(prs)} open PR(s) checked for age, mergeability, protected paths, and overlap.", details)


def check_live(cfg: dict[str, Any]) -> Check:
    site = cfg["site"]
    policy = cfg["policy"]
    url = site["production_url"]
    source = normalize_html(file_at_ref(site["production_branch"], site["homepage_path"]))
    details: list[str] = []
    status = "pass"
    try:
        code, headers, body_raw = fetch_url(url)
    except Exception as exc:
        return Check("live-production", "fail", f"Production URL fetch failed: {url}", [str(exc)])
    body = normalize_html(body_raw)
    details.append(f"HTTP {code}; cf-cache-status={headers.get('cf-cache-status', 'n/a')}; bytes={len(body_raw)}")
    if code != 200:
        status = "fail"
    if source:
        details.append(f"live sha16={sha16(body)}; `{site['production_branch']}:{site['homepage_path']}` sha16={sha16(source)}")
    for marker in policy.get("required_production_markers", []):
        if marker not in body_raw:
            status = "fail"
            details.append(f"Missing required marker: `{marker}`")
    for marker in policy.get("forbidden_production_markers", []):
        if marker in body_raw:
            status = "fail"
            details.append(f"Forbidden marker present: `{marker}`")
    return Check("live-production", status, "Production homepage marker/freshness probe completed.", details)


def check_stale_branches(cfg: dict[str, Any]) -> Check:
    policy = cfg["policy"]
    allowed = set(policy.get("allowed_long_lived_branches", []))
    stale_days = int(policy.get("stale_branch_days", 14))
    now = utcnow()
    proc = run(["git", "for-each-ref", "refs/remotes/origin", "--format=%(refname:short)|%(committerdate:iso8601)|%(authorname)"])
    if proc.returncode != 0:
        return Check("stale-branches", "warn", "Could not list remote branches.", [proc.stderr.strip()])
    details: list[str] = []
    status = "pass"
    for line in proc.stdout.splitlines():
        if not line or line.startswith("origin/HEAD"):
            continue
        ref, date_s, author = line.split("|", 2)
        name = ref.removeprefix("origin/")
        if name in allowed:
            continue
        # Git iso8601 dates may include timezone like +0000; normalize for fromisoformat.
        normalized = re.sub(r" ([+-]\d{2})(\d{2})$", r"\1:\2", date_s)
        try:
            age = (now - dt.datetime.fromisoformat(normalized)).total_seconds() / 86400
        except ValueError:
            continue
        if age > stale_days:
            status = "warn"
            details.append(f"`{ref}` age={age:.1f}d author={author}")
    if not details:
        details.append(f"No non-allowed remote branches older than {stale_days}d found.")
    return Check("stale-branches", status, "Remote branch age sweep completed.", details[:60])


def run_all(cfg: dict[str, Any]) -> list[Check]:
    return [
        check_workspace(),
        check_branches(cfg),
        check_open_prs(cfg),
        check_live(cfg),
        check_stale_branches(cfg),
    ]


def markdown_report(cfg: dict[str, Any], checks: list[Check]) -> str:
    site = cfg["site"]
    now = utcnow().isoformat(timespec="seconds")
    overall = "fail" if any(c.status == "fail" for c in checks) else "warn" if any(c.status == "warn" for c in checks) else "pass"
    lines = [
        f"# Prismatic Web Governance Report — {site['name']}",
        "",
        f"- Generated: `{now}`",
        f"- Repo: `{site.get('repo', '')}`",
        f"- Overall: **{overall.upper()}**",
        "",
        "## Summary",
        "",
        "| Check | Status | Summary |",
        "|---|---:|---|",
    ]
    for check in checks:
        lines.append(f"| `{check.name}` | {check.icon()} {check.status} | {check.summary} |")
    lines.append("")
    for check in checks:
        lines.extend([f"## {check.icon()} {check.name}", "", check.summary, ""])
        if check.details:
            lines.extend(check.details)
            lines.append("")
    lines.extend([
        "## Operating Rule",
        "",
        "If this report is WARN/FAIL, no agent should claim a site branch is safe to promote until the failing section is either fixed or explicitly waived in the PR/Linear thread with evidence.",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--report", type=Path, default=Path("/tmp/prismatic-web-governance.md"))
    parser.add_argument("--json", dest="json_path", type=Path, default=None)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on WARN or FAIL. Default exits non-zero only on FAIL.")
    parser.add_argument("--report-only", action="store_true", help="Always exit zero after writing reports. Use while installing the guard or during known-cleanup periods.")
    args = parser.parse_args(argv)

    cfg = load_config(args.config)
    checks = run_all(cfg)
    report = markdown_report(cfg, checks)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report, encoding="utf-8")
    print(report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps({"checks": [c.__dict__ for c in checks]}, indent=2), encoding="utf-8")

    has_fail = any(c.status == "fail" for c in checks)
    has_warn = any(c.status == "warn" for c in checks)
    if args.report_only:
        return 0
    if has_fail or (args.strict and has_warn):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
