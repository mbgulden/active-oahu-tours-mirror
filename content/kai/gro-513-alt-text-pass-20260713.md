# GRO-513 alt text pass — 2026-07-13

## Scope

Targeted, src-map-driven alt text remediation for recurring Active Oahu Tours media assets with empty or missing `alt` attributes.

## Artifact

- Script: `scripts/gro513_alt_text_pass.py`
- Changed HTML files: 278 tracked `site/**/*.html` files
- Alt attributes updated by the scripted pass: 438
- Additional diacritical cleanup in touched text/alt strings: `Oahu` possessive/location references corrected to `Oʻahu` where encountered in this pass.

## Verification output

```text
$ python3 scripts/gro513_alt_text_pass.py
SUMMARY files_changed=0 alt_attributes_updated=0

$ python3 - <<'PY'
... HTMLParser alt audit over site/**/*.html ...
PY
ALT_AUDIT files_with_missing_or_empty_alt=79 missing_or_empty_alt=406 total_images=6263

$ python3 -m py_compile scripts/gro513_alt_text_pass.py
# exit 0
```

Baseline from the same parser before this pass:

```text
SUMMARY files_with_bad 277 bad 843 total 6263
```

Net result: missing/empty image alt attributes reduced from 843 to 406 (-437 by final audit; scripted run reported 438 tag updates, with one source variant normalized during diacritical cleanup).

## Fact-check gates

Named facts touched in alt text and verification method:

- `Oʻahu`: spelling/diacritical style corrected to match AOT's current polished-copy convention and prior diacritical pass.
- `Kailua`, `Mokulua Islands`, `Popoia Island`, `Sharks Cove`, `North Shore`: verified against existing AOT page context where each image appears and against media filenames (`Kayaking-to-the-mokes`, `Kayak-Rental-on-mokolua-island`, `Kayaking-at-Popoia-Island`, `sharks-cove-snorkel-turtle`, `North-Shore-SUP_thumb`).
- Product/activity claims (`e-bike`, `cooler rental`, `beach umbrella rental`, `beach chairs`, `stand-up paddleboarding`, `surf lesson`, `kayaking`): verified against the AOT page sections where the images are embedded and the source media filenames.
- Tripadvisor award claims: verified against existing AOT award pages and source filenames for `TC_2022`, `travelers-Choice-2020`, `2019-certificate-of-excellence`, `2018-certificate-of-excellence`, and `TC_transparent_BF-Logo_L_2024_RGB`.

No prices, durations, permits, weather/tide/safety claims, or new operational promises were added.

## Image/GPS verification

- Source files are existing repo/WP-export media under `site/wp-content/uploads/...`; no NAS originals were edited, renamed, resized, optimized, or direct-linked.
- EXIF/GPS check was run with Pillow for the mapped raster images. Result: dimensions readable, no GPS tags present in these exported site derivatives.
- Because GPS was absent, location/subject confidence came from the strongest available in-repo evidence: source filenames, existing AOT page placement, surrounding headings/copy, and award/logo filenames.
- Alt text was kept descriptive but not over-specific where GPS was unavailable (example: `Aerial Active Oahu photo gallery thumbnail` rather than asserting an exact beach or route for `DJI_0988_2000_1x2-115x115.jpg`).

Mapped source examples:

- `site/wp-content/uploads/2023/03/Kayaking-to-the-mokes1x3-480x160.jpg` → `Kayakers paddling toward the Mokulua Islands off Kailua`
- `site/wp-content/uploads/2023/03/Kayaking-at-Popoia-Island-Flat-Island-480x192.jpg` → `Kayaking near Popoia Island off Kailua Beach`
- `site/wp-content/uploads/2022/07/sharks-cove-snorkel-turtle-2x1_2000-480x240.jpg` → `Sea turtle swimming at Sharks Cove on Oʻahu's North Shore`
- `site/wp-content/uploads/2018/11/DJI_0988_2000_1x2-115x115.jpg` → `Aerial Active Oahu photo gallery thumbnail`

## Remaining work

406 missing/empty alt attributes remain, mostly one-off media assets that need a separate verification pass rather than filename guessing.
