# GRO-579 targeted alt-text pass — 2026-07-13T20:49Z

## Scope

Bounded Kai cron implementation slice for GRO-579 on branch `content/gro-513-alt-text-audit-pass` / PR #99. This pass only filled empty `alt` attributes for five recurring, filename/page-context-verifiable image assets across English and Japanese activity pages.

## Files changed

- `site/activities/lanikai-beach-self-guided-snorkel/index.html`
- `site/activities/sharks-cove-self-guided-snorkel/index.html`
- `site/activities/popoia-island-and-kailua-bay-guided-kayak-tour/index.html`
- `site/activities/kailua-kayak-twin-islands-guided-tour/index.html`
- `site/ja/activities/lanikai-beach-self-guided-snorkel/index.html`
- `site/ja/activities/sharks-cove-self-guided-snorkel/index.html`
- `site/ja/activities/popoia-island-and-kailua-bay-guided-kayak-tour/index.html`
- `site/ja/activities/kailua-kayak-twin-islands-guided-tour/index.html`

## Alt text added

English:

- `/wp-content/uploads/2022/07/Oahu-Snorkeling_Header2-3x1-1.jpg` → `Snorkeler over a shallow Oʻahu reef`
- `/wp-content/uploads/2022/07/sharks-cove-snorkel-self-guided-cropped_2000_15-115x115.jpg` → `Snorkeler exploring clear water at Sharks Cove`
- `/wp-content/uploads/2022/07/sharks-cove-snorkel-self-guided-cropped_2000_2-115x115.jpg` → `Rocky Sharks Cove shoreline for self-guided snorkeling`
- `/wp-content/uploads/2023/03/Kailua_Bay_Kayaking_Cloudy_background_drone-115x115.png` → `Kayakers paddling on Kailua Bay under cloudy skies`
- `/wp-content/uploads/2023/03/Kailua_Beach_In_backround_Kayak_drone-115x115.png` → `Kayaks near Kailua Beach seen from above`

Japanese mirror pages:

- `/wp-content/uploads/2022/07/Oahu-Snorkeling_Header2-3x1-1.jpg` → `オアフ島の浅いリーフでシュノーケリングする人`
- `/wp-content/uploads/2022/07/sharks-cove-snorkel-self-guided-cropped_2000_15-115x115.jpg` → `シャークスコーブの透明な海でシュノーケリングする人`
- `/wp-content/uploads/2022/07/sharks-cove-snorkel-self-guided-cropped_2000_2-115x115.jpg` → `セルフガイドのシュノーケリングに使われるシャークスコーブの岩場の海岸`
- `/wp-content/uploads/2023/03/Kailua_Bay_Kayaking_Cloudy_background_drone-115x115.png` → `曇り空のカイルア湾を進むカヤック`
- `/wp-content/uploads/2023/03/Kailua_Beach_In_backround_Kayak_drone-115x115.png` → `上空から見たカイルア・ビーチ近くのカヤック`

## Verification output

```text
html_files_parsed=310
total_images=6263
missing_or_empty_alt=386
files_with_missing_or_empty_alt=78
selected_target_empty_alt_remaining=0
htmlparser_reparse_ok=8 files
```

Previous post-PR #99 inventory was `missing_or_empty_alt=406`, so this bounded pass removed 20 empty alt attributes.

`git diff --stat` for this slice:

```text
8 files changed, 20 insertions(+), 20 deletions(-)
```

## Fact-check gates

Named facts touched: Oʻahu, Kailua Bay, Kailua Beach, Sharks Cove, snorkeling, kayaking, reef/rocky shoreline, cloudy conditions.

Verification method:

- Existing AOT canonical activity pages in this repo confirmed the relevant products/context: `site/activities/sharks-cove-self-guided-snorkel/index.html`, `site/activities/lanikai-beach-self-guided-snorkel/index.html`, `site/activities/popoia-island-and-kailua-bay-guided-kayak-tour/index.html`, and `site/activities/kailua-kayak-twin-islands-guided-tour/index.html` contain the matching Sharks Cove, Kailua Bay, Kailua Beach, snorkel, and kayak context.
- Asset filenames provide direct subject/location support for the targeted image claims: `Kailua_Bay_Kayaking_Cloudy_background_drone`, `Kailua_Beach_In_backround_Kayak_drone`, `Oahu-Snorkeling_Header2`, and `sharks-cove-snorkel-self-guided-cropped`.
- External spot-check search results found AOT's live Sharks Cove page and public Kailua Beach/Kailua Bay references matching the place-name context.
- No prices, durations, route-safety claims, availability claims, or permit claims were added or changed.

## Image/GPS verification

- No images were selected, copied, generated, optimized, resized, renamed, or metadata-edited in this pass.
- Existing repo image assets were treated as read-only; only HTML `alt` attributes changed.
- Workspace image paths verified present under `site/wp-content/uploads/...`.
- EXIF/GPS check with Pillow: all five targeted assets had `gps_present=False`, so exact GPS was not available from the checked repo copies.
- Because GPS was unavailable, alt text stayed conservative and tied to filename + page context rather than adding coordinates, routes, safety promises, or overly specific landmark claims.
