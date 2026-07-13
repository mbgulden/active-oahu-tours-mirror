#!/usr/bin/env python3
"""Targeted alt-text pass for GRO-513.

Adds descriptive alt text to recurring AOT media assets that were exported with
missing/empty alt attributes. This is intentionally src-map driven so the pass is
idempotent and avoids guessing from surrounding HTML.
"""
from __future__ import annotations

import re
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
    "/wp-content/uploads/2018/11/DSC5322_2000_2000_1x2-480x240.jpg": "Beach chairs set up for an Oahu beach day",
    "/wp-content/uploads/2016/11/Laie-Surf-Lessons-e1479168095187-1.jpg": "Surf lesson on Oahu's North Shore",
    "/wp-content/uploads/2016/11/logo-large-01-01.png": "Active Oahu Tours logo",
    "/wp-content/uploads/2018/11/DJI_0988_2000_1x2-115x115.jpg": "Aerial Active Oahu photo gallery thumbnail",
    "wp-content/uploads/2018/11/DJI_0988_2000_1x2-115x115.jpg": "Aerial Active Oahu photo gallery thumbnail",
}

IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
SRC_RE = re.compile(r'''\s(?:src|data-src|data-lazy-src)=(['"])(.*?)\1''', re.IGNORECASE | re.DOTALL)
ALT_RE = re.compile(r'''\salt=(['"])(.*?)\1''', re.IGNORECASE | re.DOTALL)


def patch_img_tag(tag: str) -> tuple[str, bool, str | None]:
    src_match = SRC_RE.search(tag)
    if not src_match:
        return tag, False, None
    src = src_match.group(2)
    alt = ALT_BY_SRC.get(src)
    if alt is None:
        return tag, False, None
    alt_attr = f' alt="{alt}"'
    alt_match = ALT_RE.search(tag)
    if alt_match:
        if alt_match.group(2).strip():
            return tag, False, None
        return tag[: alt_match.start()] + alt_attr + tag[alt_match.end() :], True, src
    insert_at = tag.rfind("/>")
    if insert_at == -1:
        insert_at = tag.rfind(">")
    return tag[:insert_at] + alt_attr + tag[insert_at:], True, src


def main() -> None:
    total = 0
    files_changed = 0
    by_src: dict[str, int] = {k: 0 for k in ALT_BY_SRC}
    for path in sorted(Path("site").rglob("*.html")):
        original = path.read_text(encoding="utf-8", errors="ignore")
        changed = False

        def repl(match: re.Match[str]) -> str:
            nonlocal changed, total
            new_tag, did, src = patch_img_tag(match.group(0))
            if did:
                changed = True
                total += 1
                by_src[src or ""] = by_src.get(src or "", 0) + 1
            return new_tag

        updated = IMG_RE.sub(repl, original)
        if changed:
            path.write_text(updated, encoding="utf-8")
            files_changed += 1
    print(f"SUMMARY files_changed={files_changed} alt_attributes_updated={total}")
    for src, count in sorted(by_src.items(), key=lambda item: (-item[1], item[0])):
        if count:
            print(f"{count}\t{src}\t{ALT_BY_SRC[src]}")


if __name__ == "__main__":
    main()
