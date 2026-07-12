# GRO-578 Hawaiian diacritical pass — high-traffic visible text

Generated: 2026-07-12
Branch: kai/gro-578-diacritical-pass

## Scope
HTMLParser-based visible text pass across 12 high-traffic AOT pages: homepage, activities/rentals hubs, kayak rental/product pages, Kāneʻohe/Mokoliʻi guide pages, Lanikai, Sharks Cove, and launch guide. The script intentionally preserved `Active Oahu` as the brand/legal phrase and skipped URLs, scripts, styles, and code/pre blocks.

## Results by file
| File | Hawaii→Hawaiʻi | Oahu→Oʻahu | Kaneohe→Kāneʻohe | Mokolii/Mokoli'i→Mokoliʻi |
|---|---:|---:|---:|---:|
| `site/index.html` | +1 | +24 | +2 | +6 |
| `site/activities.html` | +3 | +64 | +1 | +6 |
| `site/rentals/index.html` | +0 | +15 | +10 | +4 |
| `site/kayak-rentals/index.html` | +1 | +29 | +4 | +6 |
| `site/rentals/oahu-tandem-kayak-rentals/index.html` | +0 | +21 | +3 | +8 |
| `site/oahu-launch-guide/index.html` | +0 | +22 | +4 | +5 |
| `site/kaneohe-bay-sandbar-tide-guide/index.html` | +0 | +5 | +12 | +1 |
| `site/oahu-equipment-rentals/chinamans-hat-kayak-rentals/index.html` | +0 | +16 | +1 | +18 |
| `site/mokolii/index.html` | +0 | +21 | +0 | +5 |
| `site/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/index.html` | +1 | +16 | +0 | +3 |
| `site/oahu-kayaking-and-beach-adventures/ultimate-guide-to-lanikai-beach/index.html` | +0 | +5 | +0 | +1 |
| `site/sharks-cove-snorkeling-guide/index.html` | +3 | +21 | +0 | +5 |

## Verification
- `python3 scripts/gro578_diacritical_text_pass.py --write` changed 12 files / 318 text nodes on first run.
- Follow-up correction preserved the English adjective `Hawaiian`, fixed accidental `Hawaiʻian` outputs, and preserved compact/domain brand text such as `ActiveOahu.com`.
- Idempotence check: `python3 scripts/gro578_diacritical_text_pass.py` returned `SUMMARY changed_files=0 changed_text_nodes=0`.
- HTML smoke parse: Python `HTMLParser` parsed all 12 changed HTML files successfully.
- Guard search for malformed place-name suffixes found only two pre-existing `Active OʻahuReady` JSON text blobs outside this pass target set; no new `Hawaiʻi[a-zA-Z]` issues remain in changed files.

## Fact-check gates
- `Hawaiʻi`, `Oʻahu`, and source references for Hawaiian place names checked against the University of Hawaiʻi at Mānoa Library Hawaiʻi Place Names research guide / Ulukau Hawaiian Place Names resources.
- `Kāneʻohe` and `Heʻeia` context checked against NOAA/University of Hawaiʻi Heʻeia National Estuarine Research Reserve and Hawaiʻi DLNR DOBOR Heʻeia Kea Small Boat Harbor references.
- `Mokoliʻi` spelling and common alternate `Chinaman’s Hat` checked against Hawaiian Place Names/Ulukau-style source references and public geography references returned for Mokoliʻi.
- Operational claims, prices, durations, route safety, and imagery were not edited in this pass; existing safety/route claims remain for separate editorial review.

## Image/GPS verification
No imagery was selected, moved, generated, or retagged in this pass.
