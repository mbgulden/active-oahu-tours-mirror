import os
import re
import json
from bs4 import BeautifulSoup

SITE_ROOT = "/home/ubuntu/work/active-oahu-static/site"
GSC_FILE = "/home/ubuntu/work/active-oahu-static/site/_seo/raw/gsc_ja_search_analytics.json"

# Load GSC data
gsc_data = {}
if os.path.exists(GSC_FILE):
    with open(GSC_FILE, "r", encoding="utf-8") as f:
        raw_gsc = json.load(f)
    rows = raw_gsc.get("rows", [])
    
    # Aggregate by page URL
    for row in rows:
        keys = row.get("keys", [])
        if len(keys) < 2:
            continue
        page_url = keys[1]
        clicks = row.get("clicks", 0)
        impressions = row.get("impressions", 0)
        position = row.get("position", 0.0)
        
        if page_url not in gsc_data:
            gsc_data[page_url] = {"clicks": 0, "impressions": 0, "pos_sum": 0.0, "count": 0}
        
        gsc_data[page_url]["clicks"] += clicks
        gsc_data[page_url]["impressions"] += impressions
        gsc_data[page_url]["pos_sum"] += position
        gsc_data[page_url]["count"] += 1

def get_word_count(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    # remove scripts and styles
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    # clean up whitespace and split
    words = re.findall(r'\w+', text)
    return len(words)

def get_ja_pages():
    ja_pages = []
    ja_dir = os.path.join(SITE_ROOT, "ja")
    for root, dirs, files in os.walk(ja_dir):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, SITE_ROOT)
                ja_pages.append(rel_path)
    return sorted(ja_pages)

def audit_pages():
    ja_files = get_ja_pages()
    audit_results = []
    
    for ja_rel in ja_files:
        ja_full = os.path.join(SITE_ROOT, ja_rel)
        
        # Determine EN counterpart relative path
        en_rel = ja_rel[3:] # strip 'ja/'
        en_full = os.path.join(SITE_ROOT, en_rel)
        
        # Read JA file
        with open(ja_full, "r", encoding="utf-8", errors="replace") as f:
            ja_content = f.read()
            
        # Read EN file if exists
        en_exists = os.path.exists(en_full)
        en_word_count = 0
        if en_exists:
            with open(en_full, "r", encoding="utf-8", errors="replace") as f:
                en_content = f.read()
                en_word_count = get_word_count(en_content)
        
        ja_word_count = get_word_count(ja_content)
        
        # Determine GSC Page URL
        # e.g. ja/activities/sharks-cove-self-guided-snorkel/index.html -> https://activeoahutours.com/ja/activities/sharks-cove-self-guided-snorkel/
        url_part = ja_rel.replace("index.html", "")
        if not url_part.endswith("/"):
            url_part += "/"
        gsc_url = f"https://activeoahutours.com/{url_part}"
        
        # If url_part is just ja/
        if url_part == "ja/":
            gsc_url = "https://activeoahutours.com/ja/"
            
        # Get GSC stats
        stats = gsc_data.get(gsc_url, {"clicks": 0, "impressions": 0, "pos_sum": 0.0, "count": 0})
        clicks = stats["clicks"]
        impressions = stats["impressions"]
        avg_pos = stats["pos_sum"] / stats["count"] if stats["count"] > 0 else 0.0
        
        # Hreflang check
        # Look for <link rel="alternate" hreflang="ja" ...> and hreflang="en" ...>
        has_ja_hreflang = 'hreflang="ja"' in ja_content or "hreflang='ja'" in ja_content
        has_en_hreflang = 'hreflang="en"' in ja_content or "hreflang='en'" in ja_content
        hreflang_correct = "✅" if (has_ja_hreflang and has_en_hreflang) else "❌"
        
        # Schema check
        # Check for ld+json schema
        schema_present = "application/ld+json" in ja_content
        schema_status = "✅" if schema_present else "❌"
        
        # Content quality rating
        # If EN counterpart does not exist, check JA word count
        if not en_exists:
            content_quality = "✅" if ja_word_count > 200 else "⚠️"
        else:
            ratio = ja_word_count / en_word_count if en_word_count > 0 else 1.0
            if ratio < 0.25:
                content_quality = "❌" # Very thin
            elif ratio < 0.5:
                content_quality = "⚠️" # Thin compared to EN
            else:
                content_quality = "✅" # Good translation depth
        
        # Estimate traffic potential: impressions * 0.1 / (avg_pos if avg_pos > 0 else 10)
        # Sort key should prioritize impressions
        traffic_potential = impressions
        
        audit_results.append({
            "ja_path": ja_rel,
            "en_path": en_rel if en_exists else "N/A",
            "hreflang": hreflang_correct,
            "schema": schema_status,
            "quality": content_quality,
            "ja_words": ja_word_count,
            "en_words": en_word_count,
            "clicks": clicks,
            "impressions": impressions,
            "avg_pos": avg_pos,
            "potential": traffic_potential
        })
        
    return audit_results

def generate_report(results):
    # Sort by impressions desc, then clicks desc
    sorted_results = sorted(results, key=lambda x: (x["impressions"], x["clicks"]), reverse=True)
    
    report_path = "/home/ubuntu/work/active-oahu-static/site/_seo/reports/03-japanese-market/ja-page-inventory-2026-06-11.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Japanese Page Inventory Audit (GRO-1180)\n\n")
        f.write("**Date:** 2026-06-11  \n")
        f.write(f"**Total JA pages audited:** {len(results)}  \n")
        f.write(f"**Pages with Schema:** {sum(1 for x in results if x['schema'] == '✅')} ({sum(1 for x in results if x['schema'] == '✅')/len(results)*100:.1f}%)  \n")
        f.write(f"**Hreflang Coverage:** {sum(1 for x in results if x['hreflang'] == '✅')/len(results)*100:.1f}%  \n\n")
        
        f.write("## Detailed Audit Table\n\n")
        f.write("This table lists all audited Japanese mirror pages sorted by traffic potential (GSC impressions).\n\n")
        f.write("| URL Path | EN Counterpart | Hreflang? | Schema? | Content Quality | JA Words / EN Words | GSC Impressions | GSC Clicks | Avg Position |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        
        for r in sorted_results:
            url_link = f"[{r['ja_path']}](file://{SITE_ROOT}/{r['ja_path']})"
            en_link = f"[{r['en_path']}](file://{SITE_ROOT}/{r['en_path']})" if r['en_path'] != "N/A" else "N/A"
            f.write(f"| {url_link} | {en_link} | {r['hreflang']} | {r['schema']} | {r['quality']} | {r['ja_words']} / {r['en_words']} | {r['impressions']} | {r['clicks']} | {r['avg_pos']:.1f} |\n")
            
    print(f"Generated page inventory report at {report_path}")

if __name__ == "__main__":
    results = audit_pages()
    generate_report(results)
