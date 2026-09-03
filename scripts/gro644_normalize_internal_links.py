#!/usr/bin/env python3
"""Normalize AOT static-site anchor links for GRO-644.

Uses HTMLParser to identify anchor tags, then performs exact start-tag
replacements only where a local href needs correction. This avoids regex-based
HTML discovery and avoids rewriting entire documents.
"""
from __future__ import annotations

import argparse
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit, urlunsplit

SITE_ROOT = Path("site")
SKIP_PREFIXES = ("#", "mailto:", "tel:", "javascript:", "data:")


def is_ja_page(path: Path) -> bool:
    try:
        return path.relative_to(SITE_ROOT).parts[0] == "ja"
    except Exception:
        return False


def existing_target(candidate: Path) -> Path | None:
    if candidate.is_file():
        return candidate
    if candidate.is_dir() and (candidate / "index.html").is_file():
        return candidate / "index.html"
    if candidate.suffix == "" and candidate.with_suffix(".html").is_file():
        return candidate.with_suffix(".html")
    return None


def root_relative_for(target: Path) -> str:
    rel = target.relative_to(SITE_ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def normalize_href(value: str, page: Path, is_home_anchor: bool) -> str:
    stripped = value.strip()
    lower = stripped.lower()
    if not stripped or lower.startswith(SKIP_PREFIXES) or lower.startswith(("http://", "https://", "//")):
        return value

    if is_home_anchor:
        return "/ja/" if is_ja_page(page) else "/"

    parsed = urlsplit(stripped)
    path = parsed.path
    if not path:
        return value

    # Common footer links appear relative inside generated pages and templates;
    # normalize by known site-root slugs even when resolving from _templates/.
    if path in {"cancellation-policy/index.html", "cancellation-policy/"}:
        return urlunsplit(("", "", "/cancellation-policy/", parsed.query, parsed.fragment))
    if path in {"privacy-policy/index.html", "privacy-policy/"}:
        return urlunsplit(("", "", "/privacy-policy/", parsed.query, parsed.fragment))
    if path in {"join-the-team/index.html", "join-the-team/"}:
        return urlunsplit(("", "", "/join-the-team/", parsed.query, parsed.fragment))

    if path.startswith("/"):
        new_path = path
        if path in ("/index.html", "/ja/index.html"):
            new_path = "/ja/" if path.startswith("/ja/") else "/"
        elif path.endswith("/index.html"):
            new_path = path[: -len("index.html")]
        if new_path != path:
            return urlunsplit(("", "", new_path, parsed.query, parsed.fragment))
        return value

    try:
        candidate = (page.parent / path).resolve().relative_to(Path.cwd())
    except ValueError:
        return value
    target = existing_target(candidate)
    if target is None:
        return value
    new_path = root_relative_for(target)
    return urlunsplit(("", "", new_path, parsed.query, parsed.fragment))


_HREF_RE = re.compile(r"(?i)(\bhref\s*=\s*)(['\"])(.*?)(\2)", re.DOTALL)


def replace_href_in_starttag(starttag: str, old: str, new: str) -> str:
    def repl(match: re.Match[str]) -> str:
        if html.unescape(match.group(3)) != old:
            return match.group(0)
        return f"{match.group(1)}{match.group(2)}{html.escape(new, quote=True)}{match.group(4)}"

    updated, count = _HREF_RE.subn(repl, starttag, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace href in tag: {starttag[:120]}")
    return updated


TARGET_CONTEXT_TOKENS = {
    "aot-logo", "site-title", "breadcrumb", "footer", "site-footer", "content-info",
}
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
}


class AnchorCollector(HTMLParser):
    def __init__(self, page: Path):
        super().__init__(convert_charrefs=False)
        self.page = page
        self.replacements: list[tuple[str, str]] = []
        self.context_stack: list[tuple[str, set[str]]] = []

    @staticmethod
    def context_tokens(tag: str, attrs: list[tuple[str, str | None]]) -> set[str]:
        tokens = {tag.lower()}
        for name, value in attrs:
            if value is None:
                continue
            if name.lower() in {"class", "id", "role"}:
                tokens.update(value.lower().replace("_", "-").split())
        return tokens

    def in_target_context(self) -> bool:
        return any(tokens & TARGET_CONTEXT_TOKENS for _, tokens in self.context_stack)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag_l = tag.lower()
        if tag_l != "a":
            if tag_l not in VOID_TAGS:
                self.context_stack.append((tag_l, self.context_tokens(tag, attrs)))
            return
        href = next((v for k, v in attrs if k.lower() == "href" and v is not None), None)
        if href is None:
            return
        rel_values = " ".join(v or "" for k, v in attrs if k.lower() == "rel").lower().split()
        is_home = "home" in rel_values
        if not is_home and not self.in_target_context():
            return
        new_href = normalize_href(href, self.page, is_home)
        if new_href == href:
            return
        starttag = self.get_starttag_text()
        if not starttag:
            return
        self.replacements.append((starttag, replace_href_in_starttag(starttag, href, new_href)))

    def handle_endtag(self, tag: str):
        tag_l = tag.lower()
        if tag_l == "a":
            return
        for idx in range(len(self.context_stack) - 1, -1, -1):
            if self.context_stack[idx][0] == tag_l:
                del self.context_stack[idx:]
                break


def iter_html(paths: Iterable[str]) -> list[Path]:
    if paths:
        return [Path(p) for p in paths]
    return sorted(SITE_ROOT.rglob("*.html"))


def apply_replacements(original: str, replacements: list[tuple[str, str]]) -> str:
    updated = original
    for old, new in replacements:
        if old == new:
            continue
        count = updated.count(old)
        if count < 1:
            raise RuntimeError(f"Start tag not found for replacement: {old[:120]}")
        updated = updated.replace(old, new, 1)
    return updated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--check", action="store_true", help="report files that would change without writing")
    args = parser.parse_args()

    changed: list[Path] = []
    total_replacements = 0
    for path in iter_html(args.paths):
        original = path.read_text(encoding="utf-8")
        collector = AnchorCollector(path)
        collector.feed(original)
        collector.close()
        if not collector.replacements:
            continue
        updated = apply_replacements(original, collector.replacements)
        changed.append(path)
        total_replacements += len(collector.replacements)
        if not args.check:
            path.write_text(updated, encoding="utf-8")

    action = "would change" if args.check else "changed"
    print(f"{action}: {len(changed)} file(s), {total_replacements} href replacement(s)")
    for path in changed[:200]:
        print(path)
    if len(changed) > 200:
        print(f"... {len(changed)-200} more")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
