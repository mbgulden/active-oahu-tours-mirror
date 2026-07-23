#!/usr/bin/env python3
"""GRO-513: targeted alt-text pass using HTMLParser discovery.

Adds source-map-approved alt text only to matching image start tags whose alt is
missing or empty. The parser identifies image attributes; replacements preserve
all non-alt attributes and avoid regex-based HTML discovery.
"""
from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
from pathlib import Path

ALT_BY_SRC = {
    "/wp-content/uploads/2025/03/TC_transparent_BF-Logo_L_2024_RGB.png": "Tripadvisor Travelers' Choice Best of the Best award logo",
    "/wp-content/uploads/2022/07/TC_2022_L_TRANSPARENT_BG_RGB.svg": "Tripadvisor Travelers' Choice 2022 award logo",
    "/wp-content/uploads/2022/07/Tripadvisor-awards_Website.jpg": "Active Oahu Tours Tripadvisor award certificates",
    "/wp-content/uploads/2022/07/travelers-Choice-2020.png": "Tripadvisor Travelers' Choice 2020 award badge",
    "/wp-content/uploads/2022/07/2019-certificate-of-excellence-1024x434.png": "Tripadvisor Certificate of Excellence 2019 award",
    "/wp-content/uploads/2022/07/2018-certificate-of-excellence-1024x440.png": "Tripadvisor Certificate of Excellence 2018 award",
    "/wp-content/uploads/2023/03/Kayak-Rental-on-mokolua-island1x2-480x240.jpg": "Kayaks pulled onto the sand during a Mokulua Islands kayaking trip",
    "/wp-content/uploads/2023/03/Kayaking-to-the-mokes1x3-480x160.jpg": "Kayakers paddling toward the Mokulua Islands off Kailua",
    "/wp-content/uploads/2023/03/Kayaking-at-Popoia-Island-Flat-Island-480x192.jpg": "Kayaking near Popoia Island off Kailua Beach",
    "/wp-content/uploads/2022/07/sharks-cove-snorkel-turtle-2x1_2000-480x240.jpg": "Sea turtle swimming at Sharks Cove on Oʻahu's North Shore",
    "/wp-content/uploads/2016/12/North-Shore-SUP_thumb-480x240.jpg": "Stand-up paddleboarding on Oʻahu's North Shore",
    "/wp-content/uploads/2018/11/active-oahu-cooler-e1648828214743-480x240.jpg": "Active Oahu cooler rental for beach days",
    "/wp-content/uploads/2025/04/Active-Oahu-487-2-480x320.jpg": "Active Oahu e-bike adventure riders on Oʻahu",
    "/wp-content/uploads/2025/04/Active-Oahu-E-Bikes-1.jpg": "Active Oahu electric bikes ready for an Oʻahu ride",
    "/wp-content/uploads/2018/11/DSC5470_2000_2000_1x2-480x240.jpg": "Beach umbrella rental set up on the sand",
    "/wp-content/uploads/2018/11/DSC5322_2000_2000_1x2-480x240.jpg": "Beach chairs set up for an Oʻahu beach day",
    "/wp-content/uploads/2016/11/Laie-Surf-Lessons-e1479168095187-1.jpg": "Surf lesson on Oʻahu's North Shore",
    "/wp-content/uploads/2016/11/logo-large-01-01.png": "Active Oahu Tours logo",
    "/wp-content/uploads/2018/11/DJI_0988_2000_1x2-115x115.jpg": "Aerial Active Oahu photo gallery thumbnail",
    "wp-content/uploads/2018/11/DJI_0988_2000_1x2-115x115.jpg": "Aerial Active Oahu photo gallery thumbnail",
}
SOURCE_ATTRS = ("src", "data-src", "data-lazy-src")


def render_img(attrs: list[tuple[str, str | None]], closing: str, alt_text: str) -> str:
    rendered = []
    has_alt = False
    for name, value in attrs:
        if name.lower() == "alt":
            has_alt = True
            rendered.append(f' {name}="{html.escape(alt_text, quote=True)}"')
            continue
        if value is None:
            rendered.append(f" {name}")
        else:
            rendered.append(f' {name}="{html.escape(value, quote=True)}"')
    if not has_alt:
        rendered.append(f' alt="{html.escape(alt_text, quote=True)}"')
    return "<img" + "".join(rendered) + closing


class ImageCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.replacements: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        values = {name.lower(): value or "" for name, value in attrs}
        source = next((values[name] for name in SOURCE_ATTRS if values.get(name) in ALT_BY_SRC), None)
        if source is None or values.get("alt", "").strip():
            return
        original = self.get_starttag_text()
        if not original:
            return
        closing = " />" if original.rstrip().endswith("/>") else ">"
        updated = render_img(attrs, closing, ALT_BY_SRC[source])
        self.replacements.append((original, updated, source))


def apply_replacements(source: str, replacements: list[tuple[str, str, str]]) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    updated = source
    for old, new, image_source in replacements:
        if old not in updated:
            raise RuntimeError(f"image start tag not found for replacement: {old[:120]}")
        updated = updated.replace(old, new, 1)
        counts[image_source] = counts.get(image_source, 0) + 1
    return updated, counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="report changes without writing")
    args = parser.parse_args()
    changed_files = 0
    total = 0
    by_source: dict[str, int] = {}
    for path in sorted(Path("site").rglob("*.html")):
        original = path.read_text(encoding="utf-8", errors="ignore")
        collector = ImageCollector()
        collector.feed(original)
        collector.close()
        if not collector.replacements:
            continue
        updated, counts = apply_replacements(original, collector.replacements)
        changed_files += 1
        total += sum(counts.values())
        for src, count in counts.items():
            by_source[src] = by_source.get(src, 0) + count
        if not args.check:
            path.write_text(updated, encoding="utf-8")
    action = "would_change" if args.check else "changed"
    print(f"SUMMARY action={action} files={changed_files} alt_attributes={total}")
    for src, count in sorted(by_source.items()):
        print(f"{count}\t{src}\t{ALT_BY_SRC[src]}")
    return 1 if args.check and total else 0


if __name__ == "__main__":
    raise SystemExit(main())
