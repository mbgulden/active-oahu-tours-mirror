#!/usr/bin/env python3
"""Remove stale Cloudflare challenge snippets and defer TripAdvisor widgets.

This is intentionally HTMLParser-assisted: the parser identifies script tag
boundaries in the original byte-for-byte document, then we apply targeted span
replacements without reserializing the full static export.
"""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LAZY_SRC = "/assets/js/aot-lazy-tripadvisor.js"
TRIPADVISOR_MARKER = "https://www.jscache.com/wejs"
CF_MARKERS = ("/cdn-cgi/challenge-platform/scripts/jsd/main.js", "window.__CF$cv")


@dataclass(frozen=True)
class Replacement:
    start: int
    end: int
    text: str


class ScriptTransformParser(HTMLParser):
    def __init__(self, html: str) -> None:
        super().__init__(convert_charrefs=False)
        self.html = html
        self.line_offsets = self._line_offsets(html)
        self.replacements: list[Replacement] = []
        self._script_start: int | None = None
        self._script_tag_end: int | None = None
        self._script_attrs: dict[str, str | None] = {}
        self._script_contains_cf = False

    @staticmethod
    def _line_offsets(text: str) -> list[int]:
        offsets = [0]
        for idx, char in enumerate(text):
            if char == "\n":
                offsets.append(idx + 1)
        return offsets

    def _absolute_pos(self) -> int:
        line, col = self.getpos()
        return self.line_offsets[line - 1] + col

    def _tag_end(self, start: int) -> int:
        end = self.html.find(">", start)
        if end == -1:
            raise ValueError(f"unterminated tag at byte {start}")
        return end + 1

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "script":
            return
        start = self._absolute_pos()
        tag_end = self._tag_end(start)
        attr_map = {key.lower(): value for key, value in attrs}
        src = attr_map.get("src") or ""
        script_type = attr_map.get("type") or ""
        self._script_start = start
        self._script_tag_end = tag_end
        self._script_attrs = attr_map
        self._script_contains_cf = any(marker in src for marker in CF_MARKERS)
        if script_type.lower() == "speculationrules":
            close = self.html.lower().find("</script>", tag_end)
            end = close + len("</script>") if close != -1 else tag_end
            body = self.html[tag_end:close if close != -1 else tag_end]
            if not body.strip():
                self.replacements.append(Replacement(start, end, ""))
        if TRIPADVISOR_MARKER in src:
            close = self.html.lower().find("</script>", tag_end)
            end = close + len("</script>") if close != -1 else tag_end
            replacement = (
                f'<script type="text/plain" data-aot-lazy-tripadvisor '
                f'data-src="{src}"></script>'
            )
            self.replacements.append(Replacement(start, end, replacement))

    def handle_data(self, data: str) -> None:
        if self._script_start is not None and any(marker in data for marker in CF_MARKERS):
            self._script_contains_cf = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "script" or self._script_start is None:
            return
        end = self._tag_end(self._absolute_pos())
        if self._script_contains_cf:
            self.replacements.append(Replacement(self._script_start, end, ""))
        self._script_start = None
        self._script_tag_end = None
        self._script_attrs = {}
        self._script_contains_cf = False


def apply_replacements(html: str, replacements: Iterable[Replacement]) -> str:
    result = html
    for repl in sorted(replacements, key=lambda item: item.start, reverse=True):
        result = result[: repl.start] + repl.text + result[repl.end :]
    return result


def ensure_lazy_loader(html: str) -> str:
    if "data-aot-lazy-tripadvisor" not in html:
        return html
    loader = f'<script src="{LAZY_SRC}" defer></script>'
    if loader in html:
        html = html.replace(loader, "")
    body_idx = html.lower().rfind("</body>")
    if body_idx == -1:
        return html + "\n" + loader + "\n"
    return html[:body_idx] + loader + "\n" + html[body_idx:]


def normalize_duplicate_body_close(html: str) -> str:
    while "</body>\n</body>" in html:
        html = html.replace("</body>\n</body>", "</body>")
    while "</body>\n\n</body>" in html:
        html = html.replace("</body>\n\n</body>", "</body>")
    while "</body></body>" in html:
        html = html.replace("</body></body>", "</body>")
    html = html.replace(
        "</body>\n\n" + f'<script src="{LAZY_SRC}" defer></script>' + "\n</body>",
        f'<script src="{LAZY_SRC}" defer></script>' + "\n</body>",
    )
    html = html.replace(
        "</body>\n" + f'<script src="{LAZY_SRC}" defer></script>' + "\n</body>",
        f'<script src="{LAZY_SRC}" defer></script>' + "\n</body>",
    )
    return html


def remove_fareharbor_prewarm(html: str) -> str:
    """Remove hidden FareHarbor prewarm iframes while preserving click booking."""
    html = html.replace(
        "\n"
        "  // Pre-warm: preload the FareHarbor book page in hidden iframe\n"
        "  function prewarmFH() {\n"
        "    var pw = document.createElement('iframe');\n"
        "    pw.src = 'https://fareharbor.com/embeds/book/activeoahutours/?u=f9b48d18-715e-4919-9c8e-077c045cf4bf&from-ssl=yes';\n"
        "    pw.style.cssText = 'display:none!important;width:0!important;height:0!important';\n"
        "    pw.title = 'fareharbor-prewarm';\n"
        "    pw.setAttribute('aria-hidden', 'true');\n"
        "    pw.setAttribute('tabindex', '-1');\n"
        "    document.body.appendChild(pw);\n"
        "    setTimeout(function() {\n"
        "      if (pw.parentNode) pw.parentNode.removeChild(pw);\n"
        "    }, 4000);\n"
        "  }\n",
        "\n"
        "  // FareHarbor prewarm intentionally disabled: loading the hidden\n"
        "  // checkout iframe on every page view creates third-party-cookie\n"
        "  // Lighthouse noise before a visitor asks to book.\n",
    )
    html = html.replace(
        "document.addEventListener('DOMContentLoaded', function() {\n"
        "      prewarmFH();\n"
        "      wrapFH();\n"
        "    });",
        "document.addEventListener('DOMContentLoaded', function() {\n"
        "      wrapFH();\n"
        "    });",
    )
    html = html.replace(
        "  } else {\n"
        "    prewarmFH();\n"
        "    wrapFH();\n"
        "  }",
        "  } else {\n"
        "    wrapFH();\n"
        "  }",
    )
    return html


def transform_file(path: Path) -> tuple[int, int]:
    html = path.read_text(encoding="utf-8")
    parser = ScriptTransformParser(html)
    parser.feed(html)
    cf_count = sum(1 for repl in parser.replacements if repl.text == "")
    ta_count = sum(1 for repl in parser.replacements if "data-aot-lazy-tripadvisor" in repl.text)
    updated = apply_replacements(html, parser.replacements)
    updated = remove_fareharbor_prewarm(updated)
    updated = normalize_duplicate_body_close(updated)
    updated = ensure_lazy_loader(updated)
    updated = normalize_duplicate_body_close(updated)
    if updated != html:
        path.write_text(updated, encoding="utf-8")
    if updated == html and not parser.replacements:
        return (0, 0)
    return (cf_count, ta_count)


def main() -> None:
    cf_total = 0
    ta_total = 0
    changed = 0
    for path in sorted([*SITE.rglob("*.html"), *SITE.rglob("*.php")]):
        cf_count, ta_count = transform_file(path)
        if cf_count or ta_count:
            changed += 1
            cf_total += cf_count
            ta_total += ta_count
    print(f"changed_files={changed}")
    print(f"removed_cloudflare_challenge_snippets={cf_total}")
    print(f"deferred_tripadvisor_widgets={ta_total}")


if __name__ == "__main__":
    main()
