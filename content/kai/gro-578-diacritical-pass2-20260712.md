# GRO-578 Hawaiian Diacritical Pass 2 — High-Traffic AOT Pages

Timestamp: 2026-07-12T22:19:21Z

## Scope

Second bounded visible-text pass for six high-traffic Active Oahu Tours pages identified by the baseline audit:

- `site/beach-gear-rentals/index.html`
- `site/kayak-safety-guide/index.html`
- `site/kaneohe-sandbar/index.html`
- `site/chinamans-hat/index.html`
- `site/guides/kailua-beach-park/index.html`
- `site/guides/best-beaches-windward-oahu/index.html`

The pass uses the existing HTMLParser-based script and keeps URLs, scripts, styles, code/pre blocks, and the legal/brand phrase `Active Oahu` untouched. This pass intentionally edits visible text only; remaining bare terms are largely in URLs, attributes, schema/script blocks, brand/legal names, or other contexts that need a separate manual/attribute-aware pass.

## Verification output

- Dry run: `python3 scripts/gro578_diacritical_text_pass.py` → `SUMMARY changed_files=6 changed_text_nodes=170`
- Write run: `python3 scripts/gro578_diacritical_text_pass.py --write` → `SUMMARY changed_files=6 changed_text_nodes=170`
- Idempotence: `python3 scripts/gro578_diacritical_text_pass.py` → `SUMMARY changed_files=0 changed_text_nodes=0`
- HTML smoke parse: Python `HTMLParser` parsed all 6 changed HTML files successfully.
- Guard search for malformed terms/placeholders did not find new script placeholders or `Hawaiʻian`-style errors in the changed files. Repository-wide search still finds pre-existing `Active Oʻahu` instances outside this pass.

## Before/after counts from write run

| File | Changed text nodes | Hawaii before→after | Oahu before→after | Kaneohe before→after | Mokolii before→after | Mokoli'i before→after | Laie before→after |
|---|---:|---:|---:|---:|---:|---:|---:|
| `site/beach-gear-rentals/index.html` | 33 | 6→4 | 87→57 | 2→0 | 7→3 | 2→1 | 2→2 |
| `site/kayak-safety-guide/index.html` | 27 | 5→5 | 80→56 | 4→0 | 7→3 | 2→1 | 2→2 |
| `site/kaneohe-sandbar/index.html` | 27 | 6→4 | 75→54 | 20→12 | 7→3 | 2→1 | 2→2 |
| `site/chinamans-hat/index.html` | 21 | 4→4 | 72→50 | 0→0 | 7→3 | 2→1 | 2→2 |
| `site/guides/kailua-beach-park/index.html` | 26 | 10→8 | 87→62 | 0→0 | 7→3 | 2→1 | 2→2 |
| `site/guides/best-beaches-windward-oahu/index.html` | 36 | 7→5 | 95→58 | 3→3 | 7→3 | 2→1 | 2→2 |

## Fact-check gates

Named facts touched were Hawaiian place/state names only:

- `Hawaiʻi` / `Oʻahu`: verified against GoHawaii visitor pages/search results using official spellings, including `https://www.gohawaii.com/islands` and `https://www.gohawaii.com/islands/oahu`.
- Hawaiian geographic-name orthography process: verified against the Hawaiʻi Board on Geographic Names page (`https://planning.hawaii.gov/gis/hbgn`), which states the Board designates official names/spellings and adds ʻokina/kahakō as appropriate.
- `Kāneʻohe`, `Mokoliʻi`, `Lāʻie`: handled as Hawaiian place-name orthography corrections under the HBGN/GNIS source-of-truth process. This pass did not change routes, prices, durations, operational safety claims, access rules, or product availability.
- Brand/legal names: `Active Oahu` / `Active Oahu Tours` intentionally preserved unless Michael chooses to rebrand.

## Image/GPS verification

No imagery was selected, copied, placed, optimized, renamed, metadata-edited, or linked. NAS originals untouched.
