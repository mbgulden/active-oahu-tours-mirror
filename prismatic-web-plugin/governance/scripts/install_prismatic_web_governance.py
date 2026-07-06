#!/usr/bin/env python3
"""Install the Prismatic Web Governance Guard into a site repository.

This script is intentionally stdlib-only so it can run in fresh repos and CI.
It copies the proven guard, renders site-specific config/workflow templates, and
prints the next verification commands.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]
TEMPLATES = PACKAGE_ROOT / "templates"
GUARD_SOURCE = REPO_ROOT / "scripts" / "prismatic_web_governance.py"


def marker_list(values: list[str]) -> str:
    return json.dumps(values, indent=4, ensure_ascii=False)


def render_template(path: Path, replacements: dict[str, str]) -> str:
    text = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = sorted(set(part.split("}}", 1)[0] for part in text.split("{{")[1:]))
    if unresolved:
        raise SystemExit(f"Unresolved template tokens in {path}: {', '.join(unresolved)}")
    return text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install Prismatic Web Governance Guard into a target site repo.")
    parser.add_argument("--target", required=True, help="Target repository root")
    parser.add_argument("--site-name", required=True, help="Human-friendly site name")
    parser.add_argument("--repo", required=True, help="GitHub repository, e.g. owner/name")
    parser.add_argument("--production-url", required=True, help="Canonical production homepage URL")
    parser.add_argument("--staging-url", default="", help="Preview/staging homepage URL")
    parser.add_argument("--homepage-path", default="site/index.html", help="Homepage file path in the repo")
    parser.add_argument("--production-branch", default="main", help="Production branch name without origin/")
    parser.add_argument("--staging-branch", default="staging", help="Staging branch name without origin/")
    parser.add_argument("--legacy-branch", default="", help="Optional legacy/older branch name without origin/ (for example master)")
    parser.add_argument("--required-marker", action="append", default=[], help="Required live production marker; repeatable")
    parser.add_argument("--forbidden-marker", action="append", default=[], help="Forbidden live production marker; repeatable")
    parser.add_argument("--force", action="store_true", help="Overwrite existing governance artifacts")
    return parser.parse_args()


def write_text(path: Path, content: str, *, force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_file(src: Path, dest: Path, *, force: bool) -> None:
    if not src.exists():
        raise SystemExit(f"Missing source file: {src}")
    if dest.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def main() -> int:
    args = parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        raise SystemExit(f"Target repo does not exist: {target}")
    if not (target / ".git").exists():
        raise SystemExit(f"Target is not a git repository root: {target}")
    if not args.required_marker:
        raise SystemExit("At least one --required-marker is required so live production can be checked.")

    legacy_ref = f"origin/{args.legacy_branch}" if args.legacy_branch else None
    allowed_branches = []
    for branch in [args.production_branch, args.staging_branch, args.legacy_branch, "deploy-fresh"]:
        if branch and branch not in allowed_branches:
            allowed_branches.append(branch)

    replacements = {
        "SITE_NAME": args.site_name,
        "REPO": args.repo,
        "PRODUCTION_URL": args.production_url,
        "STAGING_URL": args.staging_url,
        "HOMEPAGE_PATH": args.homepage_path,
        "PRODUCTION_BRANCH": args.production_branch,
        "STAGING_BRANCH": args.staging_branch,
        "LEGACY_BRANCH": args.legacy_branch,
        "LEGACY_BRANCH_JSON": json.dumps(legacy_ref),
        "ALLOWED_LONG_LIVED_BRANCHES_JSON": json.dumps(allowed_branches, ensure_ascii=False),
        "REQUIRED_MARKERS_JSON": marker_list(args.required_marker),
        "FORBIDDEN_MARKERS_JSON": marker_list(args.forbidden_marker),
        "GITHUB_TOKEN_EXPRESSION": "${{ github.token }}",
    }

    config = render_template(TEMPLATES / "prismatic-web-governance.json.tmpl", replacements)
    workflow = render_template(TEMPLATES / "prismatic-web-governance.yml.tmpl", replacements)
    workflow = workflow.replace("__GITHUB_TOKEN_EXPRESSION__", "${{ github.token }}")

    # Validate rendered JSON before writing.
    json.loads(config)

    write_text(target / ".prismatic-web-governance.json", config + ("" if config.endswith("\n") else "\n"), force=args.force)
    write_text(target / ".github" / "workflows" / "prismatic-web-governance.yml", workflow, force=args.force)
    copy_file(GUARD_SOURCE, target / "scripts" / "prismatic_web_governance.py", force=args.force)

    print("Installed Prismatic Web Governance Guard")
    print(f"target={target}")
    print("wrote=.prismatic-web-governance.json")
    print("wrote=.github/workflows/prismatic-web-governance.yml")
    print("wrote=scripts/prismatic_web_governance.py")
    print("\nNext verification command:")
    print("python3 scripts/prismatic_web_governance.py --config .prismatic-web-governance.json --report /tmp/prismatic-web-governance.md --json /tmp/prismatic-web-governance.json --report-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
