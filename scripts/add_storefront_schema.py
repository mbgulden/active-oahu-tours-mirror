#!/usr/bin/env python3
"""Add/refresh Active Oahu TravelAgency JSON-LD on homepage and contact page.

Idempotent helper for GRO-324. Uses HTMLParser to locate JSON-LD script blocks
without regexing HTML structure, then performs targeted span replacement.
"""
from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
from typing import Any

SITE = Path(__file__).resolve().parents[1] / "site"
TARGETS = [SITE / "index.html", SITE / "contact-us" / "index.html"]

TRAVEL_AGENCY: dict[str, Any] = {
    "@context": "https://schema.org",
    "@type": "TravelAgency",
    "@id": "https://activeoahutours.com/#storefront",
    "name": "Active Oahu Tours",
    "legalName": "Active Oahu, LLC",
    "url": "https://activeoahutours.com/",
    "logo": "https://activeoahutours.com/wp-content/uploads/2019/06/Active-Oahu-Logo.jpg",
    "image": "https://activeoahutours.com/wp-content/uploads/2025/03/Active-Oahu-373-e1743021729980.jpg",
    "description": "Kayak tours, e-bike adventures, paddleboarding, snorkeling, and beach gear rentals from Kailua on Oʻahu's Windward Coast.",
    "telephone": "+1-808-498-1894",
    "email": "info@activeoahutours.com",
    "priceRange": "$$",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "134B Hamakua Dr",
        "addressLocality": "Kailua",
        "addressRegion": "HI",
        "postalCode": "96734",
        "addressCountry": "US",
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 21.3949,
        "longitude": -157.7437,
    },
    "areaServed": [
        {"@type": "AdministrativeArea", "name": "Oʻahu"},
        {"@type": "Place", "name": "Kailua"},
        {"@type": "Place", "name": "Lanikai"},
        {"@type": "Place", "name": "Kāneʻohe Bay"},
        {"@type": "Place", "name": "Mokoliʻi"},
        {"@type": "Place", "name": "North Shore Oʻahu"},
    ],
    "sameAs": [
        "https://www.facebook.com/activeoahutours/",
        "https://www.instagram.com/activeoahu/",
        "https://twitter.com/activeoahutours",
    ],
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Oʻahu kayak rentals"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Guided kayak tours"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Electric bike rentals"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Snorkel and beach gear rentals"}},
    ],
}

CONTACT_PAGE: dict[str, Any] = {
    "@context": "https://schema.org",
    "@type": "ContactPage",
    "@id": "https://activeoahutours.com/contact-us/#contact",
    "name": "Contact Active Oahu Tours",
    "description": "Contact Active Oahu Tours for kayak rentals, guided tours, e-bike adventures, snorkeling, and beach gear on Oʻahu.",
    "url": "https://activeoahutours.com/contact-us/",
    "mainEntity": {"@id": "https://activeoahutours.com/#storefront"},
}

@dataclass
class ScriptBlock:
    start: int
    end: int
    data: str

class JsonLdParser(HTMLParser):
    def __init__(self, html: str) -> None:
        super().__init__(convert_charrefs=False)
        self.html = html
        self.line_starts = [0]
        for i, ch in enumerate(html):
            if ch == "\n":
                self.line_starts.append(i + 1)
        self._in_jsonld = False
        self._start_offset = 0
        self._data: list[str] = []
        self.blocks: list[ScriptBlock] = []

    def current_offset(self) -> int:
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "script":
            return
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if attr_map.get("type", "").lower() == "application/ld+json":
            self._start_offset = self.current_offset()
            self._data = []
            self._in_jsonld = True

    def handle_data(self, data: str) -> None:
        if self._in_jsonld:
            self._data.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_jsonld:
            end = self.current_offset() + len("</script>")
            self.blocks.append(ScriptBlock(self._start_offset, end, "".join(self._data)))
            self._in_jsonld = False

def compact_script(obj: dict[str, Any]) -> str:
    return "<script type=\"application/ld+json\">" + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"

def parse_type(data: str) -> tuple[Any, str | None]:
    try:
        obj = json.loads(data)
    except json.JSONDecodeError:
        return None, None
    return obj.get("@type"), obj.get("@id")

def upsert_jsonld(html: str, schema: dict[str, Any]) -> tuple[str, str]:
    parser = JsonLdParser(html)
    parser.feed(html)
    desired_type = schema.get("@type")
    desired_id = schema.get("@id")
    replacement = compact_script(schema)

    for block in parser.blocks:
        schema_type, schema_id = parse_type(block.data)
        if schema_id == desired_id or schema_type == desired_type:
            if html[block.start:block.end] == replacement:
                return html, "unchanged"
            return html[:block.start] + replacement + html[block.end:], "updated"

    head_idx = html.lower().find("</head>")
    if head_idx < 0:
        raise RuntimeError("No </head> found")
    return html[:head_idx] + replacement + "\n" + html[head_idx:], "inserted"

def main() -> int:
    results: list[str] = []
    homepage = TARGETS[0]
    contact = TARGETS[1]

    html = homepage.read_text(encoding="utf-8")
    html, status = upsert_jsonld(html, TRAVEL_AGENCY)
    homepage.write_text(html, encoding="utf-8")
    results.append(f"{homepage.relative_to(SITE.parent)}: TravelAgency {status}")

    html = contact.read_text(encoding="utf-8")
    html, status_contact = upsert_jsonld(html, CONTACT_PAGE)
    html, status_agency = upsert_jsonld(html, TRAVEL_AGENCY)
    contact.write_text(html, encoding="utf-8")
    results.append(f"{contact.relative_to(SITE.parent)}: ContactPage {status_contact}; TravelAgency {status_agency}")

    print("\n".join(results))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
