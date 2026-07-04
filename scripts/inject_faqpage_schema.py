#!/usr/bin/env python3
"""Inject FAQPage JSON-LD into selected Active Oahu service pages.

GRO-323: add FAQPage structured data to five high-priority service pages.
The edit is intentionally idempotent and uses HTMLParser to locate </head>
instead of regex-based HTML surgery.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MARKER_START = "<!-- GRO-323 FAQPage JSON-LD -->"
MARKER_END = "<!-- /GRO-323 FAQPage JSON-LD -->"


@dataclass(frozen=True)
class FAQEntry:
    question: str
    answer: str


PAGES: dict[str, list[FAQEntry]] = {
    "site/sharks-cove-snorkeling/index.html": [
        FAQEntry(
            "Is Sharks Cove good for beginner snorkelers?",
            "Sharks Cove is best for confident swimmers when North Shore surf is calm, usually in summer. If waves are up, choose a protected Windward Oʻahu option instead and always check current ocean conditions before entering.",
        ),
        FAQEntry(
            "Do I need to book gear ahead for Sharks Cove snorkeling?",
            "Booking ahead is recommended so your mask, fins, snorkel, and safety gear are ready before you drive to the North Shore. Active Oahu can help you match gear to your group and itinerary.",
        ),
        FAQEntry(
            "When is the best time to snorkel Sharks Cove?",
            "Go early in the day during calm summer conditions for easier parking, clearer water, and fewer crowds. Avoid Sharks Cove during high surf, strong surge, or poor visibility.",
        ),
    ],
    "site/chinamans-hat/index.html": [
        FAQEntry(
            "How long does it take to kayak to Chinaman's Hat?",
            "The paddle to Mokoliʻi, commonly called Chinaman's Hat, is one of Oʻahu's shorter kayak routes and can be quick in calm conditions. Allow extra time for wind, setup, landing safely, and returning before conditions build.",
        ),
        FAQEntry(
            "Can beginners kayak to Mokoliʻi?",
            "Beginners can enjoy this route on calm days with the right gear, tide timing, and safety guidance. Wind, current, and reef conditions matter, so check conditions and follow Active Oahu's route briefing before launching.",
        ),
        FAQEntry(
            "Where do Chinaman's Hat kayak trips launch?",
            "Most self-guided paddlers launch from the Kualoa area on Windward Oʻahu. Active Oahu provides route guidance and rental support so guests know where to go and how to paddle respectfully around Mokoliʻi.",
        ),
    ],
    "site/kaneohe-sandbar/index.html": [
        FAQEntry(
            "Can you kayak to the Kaneohe Sandbar?",
            "Yes, the Kaneohe Sandbar can be reached by kayak in suitable weather and tide conditions. The experience is best planned around wind, tide, and route guidance because the bay is exposed and conditions can change.",
        ),
        FAQEntry(
            "What tide is best for the Kaneohe Sandbar?",
            "Lower tides reveal more of the sandbar, while higher tides may leave it underwater. Check the tide table for your date and plan enough time to paddle back before wind or weather makes the return harder.",
        ),
        FAQEntry(
            "Is the Kaneohe Sandbar kayak trip self-guided?",
            "Active Oahu supports self-guided Kaneohe Sandbar kayak adventures with the gear and local route information guests need to plan a safer day on the bay.",
        ),
    ],
    "site/kayak-kailua/index.html": [
        FAQEntry(
            "Can I kayak from Kailua Beach to the Mokulua Islands?",
            "Yes, experienced paddlers can kayak from Kailua Beach toward the Mokulua Islands when conditions allow. The route is exposed, so guests should check wind, surf, permits, landing rules, and safety guidance before heading out.",
        ),
        FAQEntry(
            "Do Kailua kayak rentals include safety gear?",
            "Active Oahu rental setups include the core paddling gear needed for a self-guided day, with route and safety guidance provided before you launch.",
        ),
        FAQEntry(
            "How early should I start a Kailua kayak trip?",
            "Start early for calmer winds, easier parking, and more time on the water. Windward Oʻahu trade winds often build later in the day, which can make the return paddle harder.",
        ),
    ],
    "site/rentals/oahu-tandem-kayak-rentals/kailua-kayak-rentals/index.html": [
        FAQEntry(
            "Do I need a reservation for Kailua kayak rentals?",
            "Reservations are recommended so the right kayak, paddles, life jackets, and accessories are available for your group. Booking ahead also helps the team prepare route and safety guidance.",
        ),
        FAQEntry(
            "Can tandem kayaks be used by first-time paddlers?",
            "Tandem kayaks are a popular choice for first-time paddlers because two people can share the work. Conditions still matter, so choose a route that matches your group's comfort and follow the pre-launch briefing.",
        ),
        FAQEntry(
            "Where can I paddle with a Kailua kayak rental?",
            "Popular Kailua routes include Kailua Bay, Popoia Island, and, for stronger paddlers in good conditions, the Mokulua Islands. Active Oahu helps guests choose a route based on weather, ability, and timing.",
        ),
    ],
}


class HeadEndFinder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.end_head_pos: tuple[int, int] | None = None

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "head" and self.end_head_pos is None:
            self.end_head_pos = self.getpos()


def absolute_index_from_line_col(text: str, line: int, col: int) -> int:
    # HTMLParser positions are 1-based line, 0-based column.
    lines = text.splitlines(keepends=True)
    return sum(len(part) for part in lines[: line - 1]) + col


def schema_block(faqs: Iterable[FAQEntry]) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq.question,
                "acceptedAnswer": {"@type": "Answer", "text": faq.answer},
            }
            for faq in faqs
        ],
    }
    payload = json.dumps(schema, ensure_ascii=False, indent=2)
    return f"{MARKER_START}\n<script type=\"application/ld+json\">\n{payload}\n</script>\n{MARKER_END}\n"


def strip_existing_block(text: str) -> tuple[str, bool]:
    start = text.find(MARKER_START)
    if start == -1:
        return text, False
    end = text.find(MARKER_END, start)
    if end == -1:
        raise ValueError("Found GRO-323 start marker without end marker")
    end += len(MARKER_END)
    if end < len(text) and text[end : end + 1] == "\n":
        end += 1
    return text[:start] + text[end:], True


def inject(path: Path, faqs: list[FAQEntry], *, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    stripped, replaced = strip_existing_block(text)

    parser = HeadEndFinder()
    parser.feed(stripped)
    if parser.end_head_pos is None:
        raise ValueError(f"No </head> found in {path}")

    insert_at = absolute_index_from_line_col(stripped, *parser.end_head_pos)
    new_text = stripped[:insert_at] + schema_block(faqs) + stripped[insert_at:]

    if new_text == text:
        return "unchanged"
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return "updated" if replaced else "inserted"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    for rel, faqs in PAGES.items():
        path = ROOT / rel
        if not path.exists():
            raise FileNotFoundError(path)
        result = inject(path, faqs, dry_run=args.dry_run)
        prefix = "DRY " if args.dry_run else ""
        print(f"{prefix}{result}: {rel} ({len(faqs)} FAQs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
