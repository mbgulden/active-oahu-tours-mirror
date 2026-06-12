# Japanese Schema Injection Plan (GRO-1180)

**Date:** 2026-06-12  
**Target:** 83 Japanese Mirror Pages (`ja/`)  
**Strategy:** Align schema markup types with English counterparts while optimizing all content values (names, descriptions, target audiences, FAQs) into natural, high-quality Japanese.

---

## 1. Schema Optimization Strategy

Although the staging branch has some basic schema blocks injected, they are machine-translated and contain serious errors. For example:
* **"Three Tables" (スリー・テーブルズ - a geographic location)** was translated as **"テーブル 3 つ"** (three dining tables).
* **"Dry bag"** was repeated as **"ドライバッグ、ドライバッグ"**.
* **Target audiences (touristType)** like `"Adventure Travelers"` and `"Families"` were left in English.
* **Product names** were keyword-stuffed and read like spam (e.g., `"オアフ ビーチ チェア レンタル、ノース ショア オアフ、ライエ近く..."`).

### Natural Japanese Best Practices:
1. **Name Field:** Clean, readable titles that indicate the product or tour clearly without keyword stuffing.
2. **Description Field:** Smooth, polite, and persuasive Japanese prose using standard honorifics (です/ます調).
3. **Tourist Type Mapping:**
   - `"Adventure Travelers"` → `"アドベンチャー旅行者"`
   - `"Families"` → `"ファミリー"`
   - `"Couples"` → `"カップル"`
   - `"Groups"` → `"グループ・団体"`
4. **Geo & Feature Corrections:** Use standard katakana terms for local Hawaiian attractions (e.g., "シャークス・コーブ" for Sharks Cove, "チャイナマンズ・ハット" for Chinaman's Hat, "ワイメア湾" for Waimea Bay).

---

## 2. Priority Injection List (Based on GSC Impressions)

| Priority | Page Path | Schema Type | GSC Impressions | Primary Focus |
| --- | --- | --- | --- | --- |
| **1 (P0)** | `ja/activities/sharks-cove-self-guided-snorkel/` | `TouristTrip` + `LocalBusiness` | 1,334 | Fix Three Tables translation and tourist types. |
| **2 (P0)** | `ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/` | `TouristTrip` | 653 | Refine self-guided instructions description. |
| **3 (P0)** | `ja/rentals/oahu-beach-chair-rentals/` | `Product` | 319 | Fix keyword-stuffed product names. |
| **4 (P0)** | `ja/index.html` | `TravelAgency` | 271 | Localize travel agency services description. |
| **5 (P1)** | `ja/rentals/oahu-beach-umbrella-rentals/` | `Product` | 270 | Localize parasol rental description. |
| **6 (P1)** | `ja/rentals/oahu-snorkel-mask-and-fin-rentals/` | `Product` | 235 | local business offers. |
| **7 (P1)** | `ja/rentals/oahu-boogie-board-rentals/` | `Product` | 235 | Bodyboarding gear description. |
| **8 (P1)** | `ja/activities/haleiwa-paddleboarding/` | `TouristTrip` | 187 | Haleiwa historic town context. |
| **9 (P1)** | `ja/rentals/oahu-stand-up-paddle-board-rentals-sup-hire/` | `Product` | 149 | SUP hire description. |
| **10 (P2)** | `ja/activities/oahu-surf-lessons/` | `TouristTrip` | 144 | Surf lessons. |

---

## 3. Localized Japanese Schema Templates

### Template 1: TouristTrip (Tour/Activity Pages)
For pages like `/ja/activities/sharks-cove-self-guided-snorkel/`.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TouristTrip",
  "name": "シャークスコーブ セルフガイド・シュノーkelツアー（オアフ島ノースショア）",
  "description": "オアフ島ノースショアの名所ププケア・ビーチ・パーク内にあるシャークス・コーブ（Sharks Cove）とスリー・テーブルズ（Three Tables）で、2時間または4時間のガイドなしシュノーケリング体験をお楽しみください。曇り止めスプレー、ドライバッグ、高品質なシュノーケルギア一式が含まれています。",
  "url": "https://activeoahutours.com/ja/activities/sharks-cove-self-guided-snorkel/",
  "tourOperator": {
    "@type": "TravelAgency",
    "name": "Active Oahu Tours",
    "url": "https://activeoahutours.com",
    "telephone": "+1-808-123-4567"
  },
  "touristType": [
    "アドベンチャー旅行者",
    "ファミリー",
    "カップル",
    "グループ"
  ],
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "39.00",
    "availability": "https://schema.org/InStock",
    "url": "https://activeoahutours.com/ja/activities/sharks-cove-self-guided-snorkel/"
  }
}
</script>
```

### Template 2: Product (Equipment Rental Pages)
For pages like `/ja/rentals/oahu-beach-chair-rentals/`.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "オアフ島ビーチチェア・レンタル",
  "description": "ハワイ・オアフ島ノースショアやカイルア周辺で快適にリラックスできる高品質なビーチチェアのレンタルです。ご指定のビーチやご宿泊先への配達オプションもご用意しています。",
  "url": "https://activeoahutours.com/ja/rentals/oahu-beach-chair-rentals/",
  "brand": {
    "@type": "Brand",
    "name": "Active Oahu Tours"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "price": "10.00",
    "availability": "https://schema.org/InStock",
    "url": "https://activeoahutours.com/ja/rentals/oahu-beach-chair-rentals/"
  }
}
</script>
```

### Template 3: FAQPage (Frequently Asked Questions)
For pages like `/ja/faq/index.html`.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "カヤックやSUPのレンタルに車のキャリアは含まれていますか？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "はい、すべてのカヤックおよびSUPのレンタル料金には、お車の上に乗せるためのルーフラックソフトパッドとストラップのレンタルが無料で含まれています。当店のスタッフが固定方法を丁寧にご案内いたします。"
      }
    },
    {
      "@type": "Question",
      "name": "シャークスコーブには駐車場がありますか？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "はい、ププケア・ビーチ・パークには無料の公共駐車場がございます。ただし、特に夏期や週末の午前中は混雑しやすいため、早い時間帯（午前9時前）の到着をお勧めいたします。"
      }
    }
  ]
}
</script>
```

### Template 4: HowTo (Tutorial/Guide Pages)
For guides like `/ja/oahu-equipment-rentals/how-to-transport-kayaks-and-sups-from-our-shop-in-kailua-to-the-beach/`.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "カイルアの店舗からビーチまでカヤック・SUPを安全に運搬する方法",
  "description": "お車のルーフ（屋根）を傷つけることなく、カヤックやSUPをしっかりと固定してビーチまで運搬する手順をステップ・バイ・ステップで解説します。",
  "step": [
    {
      "@type": "HowToStep",
      "name": "ソフトルーフパッドの設置",
      "text": "車のルーフの埃を軽く拭き取り、均等な幅でフロントとリアのルーフ上にソフトパッドを設置します。ドアを開け、ストラップを車内で締めて固定します。"
    },
    {
      "@type": "HowToStep",
      "name": "カヤック・SUPの積載",
      "text": "カヤックまたはSUPをソフトパッドの上に静かにスライドさせます。前後が車の中心線と平行になるように位置を調整します。"
    },
    {
      "@type": "HowToStep",
      "name": "ストラップでの緊締",
      "text": "パッドの上部からストラップを通し、カヤック・SUPを巻き込むようにしてカムバックルにしっかりと締め付けます。余ったストラップはバタつかないように結び留めてください。"
    }
  ]
}
</script>
```

---

## 4. Implementation Steps

1. **Staged Cleanup:** Run a script to remove outdated, machine-translated `application/ld+json` script blocks from all 83 Japanese pages.
2. **Corrective Re-Injection:** Inject the newly localized templates above, pulling variables (URLs, prices) dynamically for matching pages.
3. **Google Rich Result Testing:** Validate the updated markup using Schema Markup Validator.
