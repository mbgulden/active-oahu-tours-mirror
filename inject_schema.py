#!/usr/bin/env python3
"""
Inject JSON-LD schema markup into 15 Japanese-language pages on the Active Oahu Tours mirror site.
Each page gets a schema block inserted just before </head>.
"""

import os
import re
import json

SITE_ROOT = "/home/ubuntu/work/active-oahu-tours-mirror/site/ja"

# Each entry: (relative_path, english_title, url, schema_type, extra_json)
# extra_json is optional additional fields for the schema object
pages = [
    (
        "active-oahu-photo-gallery/index.html",
        "Gallery – Active Oahu",
        "https://activeoahutours.com/ja/active-oahu-photo-gallery/",
        "WebPage",
        None,
    ),
    (
        "activities/page/2/index.html",
        "Oahu Kayak Tours & Adventures, Kayak in Kailua, Oahu",
        "https://activeoahutours.com/ja/activities/page/2/",
        "WebPage",
        None,
    ),
    (
        "activities/page/3/index.html",
        "Oahu Kayak Tours & Adventures, Kayak in Kailua, Oahu",
        "https://activeoahutours.com/ja/activities/page/3/",
        "WebPage",
        None,
    ),
    (
        "become-a-partner/index.html",
        "Become a Partner – Active Oahu",
        "https://activeoahutours.com/multi-day-kayak-and-beach-gear-rentals/kayak-beach-gear-rental-partners/become-a-partner/",
        "WebPage",
        None,
    ),
    (
        "cancellation-policy/index.html",
        "Cancellation Policy – Active Oahu",
        "https://activeoahutours.com/ja/cancellation-policy/",
        "WebPage",
        None,
    ),
    (
        "job-dashboard/index.html",
        "Job Dashboard – Active Oahu",
        "https://activeoahutours.com/ja/job-dashboard/",
        "WebPage",
        None,
    ),
    (
        "join-the-team/index.html",
        "Join the Team – Active Oahu",
        "https://activeoahutours.com/ja/join-the-team/",
        "WebPage",
        None,
    ),
    (
        "kailua-oahu-storefront/index.html",
        "Kayak and Beach Gear Rentals Near Kailua, Oahu",
        "https://activeoahutours.com/ja/kailua-oahu-storefront/",
        "LocalBusiness",
        {
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "134B Hamakua Drive",
                "addressLocality": "Kailua",
                "addressRegion": "HI",
                "postalCode": "96734",
                "addressCountry": "US",
            }
        },
    ),
    (
        "oahu-kayaking-and-beach-adventures/chinamans-hat-kayak-adventure/index.html",
        "Chinaman's Hat Kayak Adventure – Active Oahu",
        "https://activeoahutours.com/ja/oahu-kayaking-and-beach-adventures/chinamans-hat-kayak-adventure/",
        "WebPage",
        None,
    ),
    (
        "oahu-kayaking-and-beach-adventures/index.html",
        "Oahu Kayaking and Beach Experiences - Kaneohe Sandbar and More",
        "https://activeoahutours.com/ja/oahu-kayaking-and-beach-adventures/",
        "CollectionPage",
        None,
    ),
    (
        "oahu-kayaking-and-beach-adventures/kahana-river-kayak-adventure/index.html",
        "Kahana River Kayak Adventure – Active Oahu",
        "https://activeoahutours.com/ja/oahu-kayaking-and-beach-adventures/kahana-river-kayak-adventure/",
        "WebPage",
        None,
    ),
    (
        "oahu-kayaking-and-beach-adventures/kalama-beach-bodyboarding-adventure/index.html",
        "Kalama Beach Bodyboarding Adventure – Active Oahu",
        "https://activeoahutours.com/ja/oahu-kayaking-and-beach-adventures/kalama-beach-bodyboarding-adventure/",
        "WebPage",
        None,
    ),
    (
        "oahu-kayaking-and-beach-adventures/popoia-island-kayaking-adventure/index.html",
        "Popoia Island Kayaking Adventure – Active Oahu",
        "https://activeoahutours.com/ja/oahu-kayaking-and-beach-adventures/popoia-island-kayaking-adventure/",
        "WebPage",
        None,
    ),
    (
        "privacy-policy/index.html",
        "Privacy Policy – Active Oahu",
        "https://activeoahutours.com/ja/privacy-policy/",
        "WebPage",
        None,
    ),
    (
        "trip-cancellation-insurance-terms-and-conditions/index.html",
        "Trip Cancellation Insurance Terms and Conditions – Active Oahu",
        "https://activeoahutours.com/ja/trip-cancellation-insurance-terms-and-conditions/",
        "WebPage",
        None,
    ),
]


def build_schema_block(name, url, schema_type, extra=None):
    """Build a JSON-LD script block for the given schema."""
    schema = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": name,
        "url": url,
    }
    if extra:
        schema.update(extra)
    json_str = json.dumps(schema, ensure_ascii=False, indent=2)
    block = f'<script type="application/ld+json">\n{json_str}\n</script>'
    return block


def verify_file(filepath):
    """Verify a file has exactly 1 </head> and at least 1 schema.org reference."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    head_close_count = content.count("</head>")
    schema_count = content.count("schema.org")

    issues = []
    if head_close_count != 1:
        issues.append(f"Expected 1 </head>, found {head_close_count}")
    if schema_count < 1:
        issues.append("No schema.org reference found")

    return issues, head_close_count, schema_count


def main():
    success_count = 0
    fail_count = 0

    for rel_path, name, url, schema_type, extra in pages:
        filepath = os.path.join(SITE_ROOT, rel_path)

        if not os.path.isfile(filepath):
            print(f"❌ FILE NOT FOUND: {filepath}")
            fail_count += 1
            continue

        # Read the file
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if schema already exists
        if "schema.org" in content:
            print(f"⚠️  SKIPPING (already has schema): {rel_path}")
            success_count += 1
            continue

        # Build the schema block
        schema_block = build_schema_block(name, url, schema_type, extra)

        # Inject before </head>
        if "</head>" not in content:
            print(f"❌ NO </head> FOUND: {rel_path}")
            fail_count += 1
            continue

        new_content = content.replace("</head>", f"{schema_block}\n</head>", 1)

        # Write back
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        # Verify
        issues, hc, sc = verify_file(filepath)
        if issues:
            print(f"❌ VERIFY FAILED ({rel_path}): {'; '.join(issues)}")
            fail_count += 1
        else:
            print(f"✅ OK ({rel_path}): </head>={hc}, schema.org={sc}")
            success_count += 1

    print(f"\n{'='*60}")
    print(f"Done. {success_count} succeeded, {fail_count} failed.")


if __name__ == "__main__":
    main()
