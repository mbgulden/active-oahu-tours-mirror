#!/usr/bin/env python3
"""Inject guarded FareHarbor booking analytics loader into static AOT pages.

Targets pages that expose FareHarbor booking links/FH.open calls but do not yet
emit the booking_click event. Idempotent: pages with booking_click or the loader
marker are skipped. The actual browser logic lives in
site/assets/js/aot-booking-analytics.js to keep bulk HTML edits small.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MARKER = "<!-- AOT booking analytics tracking -->"
LOADER = f'{MARKER}\n<script src="/assets/js/aot-booking-analytics.js" defer></script>\n'


def has_booking_surface(text: str) -> bool:
    return "fareharbor.com/embeds/book" in text or "FH.open" in text


def already_instrumented(text: str) -> bool:
    return "booking_click" in text or MARKER in text or "/assets/js/aot-booking-analytics.js" in text


def inject(text: str) -> str:
    needles = [
        "<!-- FareHarbor plugin activated -->",
        '<script src="https://fareharbor.com/embeds/api/v1/',
        "</body>",
    ]
    for needle in needles:
        idx = text.find(needle)
        if idx != -1:
            return text[:idx] + LOADER + text[idx:]
    return text + "\n" + LOADER


def main() -> int:
    changed = []
    for path in sorted(SITE.rglob("*.html")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not has_booking_surface(text) or already_instrumented(text):
            continue
        new_text = inject(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(path.relative_to(ROOT))
    print(f"Injected booking analytics loader into {len(changed)} pages")
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
