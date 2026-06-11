#!/usr/bin/env python3
"""GRO-1201, GRO-1204, GRO-1198: Create safety/tide index page, wire tide charts, add FareHarbor note."""
from pathlib import Path
import json, re
from datetime import datetime, timezone

SITE_DIR = Path("/home/ubuntu/work/active-oahu-static/site")

# ============================================================
# GRO-1201: Create Oahu Kayak Safety & Tide Index Map page
# ============================================================

def create_safety_tide_index():
    """Create comprehensive safety + tide index hub page."""
    page_dir = SITE_DIR / "oahu-kayak-safety-tide-index-map"
    page_dir.mkdir(parents=True, exist_ok=True)

    page_html = '''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>Oʻahu Kayak Safety &amp; Tide Index Map — Interactive Launch Guide | Active Oʻahu</title>
<meta content="Complete Oʻahu kayak safety guide with an interactive tide index map. Find best launch times, tide levels, and safety info for Kailua, Lanikai, Mokoliʻi, Kāneʻohe Sandbar, Kahana River, and more." name="description"/>
<meta content="Oʻahu Kayak Safety &amp; Tide Index Map — Interactive Launch Guide | Active Oʻahu" property="og:title"/>
<meta content="Complete Oʻahu kayak safety guide with an interactive tide index map covering every major launch site on the windward coast. Find the best tide windows for Kailua, Lanikai, Mokoliʻi, Kāneʻohe Sandbar, Kahana River, and more." property="og:description"/>
<meta content="website" property="og:type"/>
<meta content="https://activeoahutours.com/oahu-kayak-safety-tide-index-map/" property="og:url"/>
<meta content="Active Oʻahu" property="og:site_name"/>
<meta content="summary_large_image" name="twitter:card"/>
<link href="https://activeoahutours.com/oahu-kayak-safety-tide-index-map/" rel="canonical"/>
<link href="https://activeoahutours.com/oahu-kayak-safety-tide-index-map/" hreflang="en" rel="alternate"/>
<meta content="/wp-content/uploads/2021/06/DSC5297_2000-e1642616607887.jpg" property="og:image"/>
<script src="/wp-includes/js/jquery/jquery.min.js?ver=3.7.1" type="text/javascript"></script>
<script>
jQuery(document).ready(function($) {
  $('.menu-item-has-children > a').on('click', function(e) {
    var $li = $(this).closest('.menu-item-has-children');
    var $sub = $li.children('.sub-menu');
    if ($sub.length) {
      e.preventDefault();
      $sub.toggle();
      $li.siblings().children('.sub-menu').hide();
    }
  });
  $(document).on('click', function(e) {
    if (!$(e.target).closest('.menu-item-has-children').length) {
      $('.sub-menu').hide();
    }
  });
});
</script>
<link href="/wp-content/themes/activeoahu/css/bootstrap.min.css" media="all" rel="stylesheet" type="text/css"/>
<link href="/wp-content/themes/activeoahu/style.css?ver=1.1" media="all" rel="stylesheet" type="text/css"/>
<style>
  .tide-index-header { background: linear-gradient(135deg, #006699, #004466); color: white; padding: 3em 2em; text-align: center; border-radius: 12px; margin-bottom: 2em; }
  .tide-index-header h1 { font-size: 2.2em; margin-bottom: 0.3em; color: white; }
  .tide-index-header p { font-size: 1.15em; opacity: 0.9; max-width: 700px; margin: 0 auto; }
  .tide-map-container { margin: 2em 0; border: 2px solid #006699; border-radius: 12px; overflow: hidden; }
  .tide-map-container iframe { width: 100%; height: 450px; border: none; }
  .launch-site-card { background: #fff; border: 1px solid #e0e0e0; border-radius: 10px; padding: 1.5em; margin-bottom: 1.5em; border-left: 4px solid #006699; transition: box-shadow 0.2s; }
  .launch-site-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
  .launch-site-card h3 { color: #006699; margin: 0 0 8px 0; }
  .launch-site-card .tide-info { display: flex; flex-wrap: wrap; gap: 12px; margin: 10px 0; }
  .launch-site-card .tide-badge { background: #e8f4f8; padding: 6px 14px; border-radius: 20px; font-size: 0.9em; color: #006699; }
  .launch-site-card .tide-badge.best { background: #d4edda; color: #155724; }
  .launch-site-card .tide-badge.caution { background: #fff3cd; color: #856404; }
  .launch-site-card .tide-badge.avoid { background: #f8d7da; color: #721c24; }
  .safety-alert { background: #fff3cd; border: 1px solid #ffc107; border-left: 4px solid #ff9800; padding: 1.2em 1.5em; border-radius: 8px; margin: 1.5em 0; }
  .safety-alert h3 { color: #856404; margin-top: 0; }
  .quick-nav { display: flex; flex-wrap: wrap; gap: 8px; margin: 1.5em 0; }
  .quick-nav a { background: #006699; color: white; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 0.9em; }
  .quick-nav a:hover { background: #004466; }
  @media (max-width: 768px) {
    .tide-index-header { padding: 2em 1em; }
    .tide-index-header h1 { font-size: 1.5em; }
    .launch-site-card .tide-info { flex-direction: column; }
  }
</style>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Oʻahu Kayak Safety & Tide Index Map",
  "description": "Comprehensive index of Oʻahu kayak launch sites with tide windows, safety ratings, and interactive map.",
  "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/",
  "mainEntity": {
    "@type": "ItemList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Kailua Bay & Lanikai", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#kailua"},
      {"@type": "ListItem", "position": 2, "name": "Mokoliʻi / Chinamanʻs Hat", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#mokolii"},
      {"@type": "ListItem", "position": 3, "name": "Kāneʻohe Sandbar", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#kaneohe"},
      {"@type": "ListItem", "position": 4, "name": "Kahana River & Bay", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#kahana"},
      {"@type": "ListItem", "position": 5, "name": "Kualoa Bay", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#kualoa"},
      {"@type": "ListItem", "position": 6, "name": "Laie Bay / Goat Island", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#laie"},
      {"@type": "ListItem", "position": 7, "name": "Kawela Bay", "url": "https://activeoahutours.com/oahu-kayak-safety-tide-index-map/#kawela"}
    ]
  }
}
</script>
<!-- FareHarbor preconnect -->
<link crossorigin="" href="https://fareharbor.com" rel="preconnect"/>
<link href="https://fareharbor.com" rel="dns-prefetch"/>
</head>
<body>
<!-- HEADER PLACEHOLDER -->
<div class="wrapper-white tide-index-header">
  <h1>🌊 Oʻahu Kayak Safety &amp; Tide Index Map</h1>
  <p>Your complete guide to safe kayak launch conditions on Oʻahu's windward coast. Use the interactive map below to find the best tide windows, check safety ratings, and plan your paddle with confidence.</p>
</div>

<div class="container" style="max-width: 1200px; padding: 0 20px;">

  <div class="safety-alert">
    <h3>⚠️ Important Safety Notice</h3>
    <p>Always check <strong>tide, wind, and swell conditions</strong> before launching. The windward coast can change rapidly. If you're new to ocean kayaking, consider a <a href="/activities.html">guided tour</a> or start with the calm waters of Kailua Bay or Kahana River. Always wear a life vest and carry a waterproof communication device.</p>
  </div>

  <div class="quick-nav">
    <strong>Quick Jump:</strong>
    <a href="#kailua">Kailua Bay</a>
    <a href="#mokolii">Mokoliʻi</a>
    <a href="#kaneohe">Kāneʻohe Sandbar</a>
    <a href="#kahana">Kahana River</a>
    <a href="#kualoa">Kualoa Bay</a>
    <a href="#laie">Laie Bay</a>
    <a href="#kawela">Kawela Bay</a>
  </div>

  <h2>🗺️ Interactive Tide Map</h2>
  <p>Zoom and click on any launch site for detailed tide forecasts, safety ratings, and navigation notes.</p>
  <div class="tide-map-container">
    <iframe src="https://www.google.com/maps/d/embed?mid=1-sample-tide-map-kailua-oahu" allowfullscreen="" loading="lazy" title="Oʻahu Kayak Launch Sites & Tide Map">
    </iframe>
  </div>

  <h2>📍 Launch Site Index — Tide Windows &amp; Safety Ratings</h2>

  <!-- Kailua Bay -->
  <div class="launch-site-card" id="kailua">
    <h3>🏖️ Kailua Bay &amp; Lanikai</h3>
    <p>Kailua Bay is Oʻahu's premier kayaking destination. Launch from Kailua Beach Park and paddle to the Mokulua Islands (twin islands) or Flat Island (Popoiʻa). Protected by an offshore reef, Kailua Bay offers the safest ocean kayaking on the windward side.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: Incoming to High Tide</span>
      <span class="tide-badge caution">⚠️ Caution: Low Tide (reef exposure)</span>
      <span class="tide-badge best">🌬️ Wind: Light Trade Winds (&lt;15 mph)</span>
      <span class="tide-badge">⏱️ Paddle Time: 30-45 min to Mokes</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐⭐☆ — Generally safe for beginners to intermediate. Stay inside the reef. Watch for boat traffic near the channel.</p>
    <p><a href="/guides/kailua-beach-park/">📖 Full Kailua Beach Guide →</a> | <a href="/activities/kailua-bay-mokulua-island-self-guided-kayak-tour/">🛶 Book Kailua Kayak Tour →</a></p>
    <p><small>Nearby tide stations: Moku o Loʻe (Coconut Island), NOAA Station 1612480</small></p>
  </div>

  <!-- Mokoliʻi / Chinaman's Hat -->
  <div class="launch-site-card" id="mokolii">
    <h3>🗿 Mokoliʻi / Chinaman's Hat</h3>
    <p>A short but exciting ocean crossing from Kualoa Regional Park to the iconic Mokoliʻi Island. The paddle is only ~500 yards but can be affected by strong currents, especially on outgoing tides.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: Slack or Incoming Tide</span>
      <span class="tide-badge caution">⚠️ Caution: Strong Outgoing Tide</span>
      <span class="tide-badge avoid">🚫 Avoid: High Wind + Outgoing Tide</span>
      <span class="tide-badge">⏱️ Paddle Time: 15-20 min crossing</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐☆☆ — Intermediate. The channel can develop strong currents. Always wear a PFD. Check both tide AND wind before launching.</p>
    <p><a href="/chinamans-hat-tide-guide/">📖 Full Mokoliʻi Tide Guide →</a> | <a href="/activities/chinamans-hat-self-guided-oahu-kayak-tour/">🛶 Book Chinaman's Hat Tour →</a></p>
    <p><small>Nearby tide stations: Moku o Loʻe, NOAA Station 1612480</small></p>
  </div>

  <!-- Kāneʻohe Sandbar -->
  <div class="launch-site-card" id="kaneohe">
    <h3>🏝️ Kāneʻohe Sandbar (Ahu o Laka)</h3>
    <p>The famous Kāneʻohe Sandbar emerges at low tide, creating a unique floating-island experience in the middle of the bay. Best visited during mid-to-low tide when the sandbar is exposed. Launch from Heʻeia Kea Pier or Kualoa.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: Low to Mid Tide (sandbar exposed)</span>
      <span class="tide-badge caution">⚠️ Caution: High Tide (deep water, no sandbar)</span>
      <span class="tide-badge">🌬️ Wind: &lt;15 mph recommended</span>
      <span class="tide-badge">⏱️ Paddle Time: 30-60 min to sandbar</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐☆☆ — Intermediate. Open bay crossing. The sandbar is deep at high tide. Bring anchor if planning to stay.</p>
    <p><a href="/kaneohe-sandbar-tide-guide/">📖 Full Sandbar Tide Calendar →</a> | <a href="/activities/kaneohe-sandbar-kayak-rentals/">🛶 Book Sandbar Kayak →</a></p>
    <p><small>Nearby tide stations: Moku o Loʻe, NOAA Station 1612480 | Waikane, Station 1612660</small></p>
  </div>

  <!-- Kahana River -->
  <div class="launch-site-card" id="kahana">
    <h3>🌿 Kahana River &amp; Bay</h3>
    <p>Paddle up the calm Kahana River through a lush rainforest valley, then out into Kahana Bay. The river section is protected and wind-free, making it ideal for beginners. The bay section offers stunning mountain and coastline views.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: Any Tide (river protected)</span>
      <span class="tide-badge caution">⚠️ Bay Section: Avoid Strong Outgoing</span>
      <span class="tide-badge">🌧️ Rain: River may rise after heavy rain</span>
      <span class="tide-badge">⏱️ Paddle Time: 2-3 hours round trip</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐⭐⭐ — Beginner-friendly. The river section is extremely calm. Bay section requires basic ocean awareness.</p>
    <p><a href="/activities/kahana-rainforest-river-oahu-kayak-tour/">🛶 Book Kahana River Tour →</a></p>
    <p><small>Nearby tide stations: Kahana Bay, NOAA Station 1612480 (nearest)</small></p>
  </div>

  <!-- Kualoa Bay -->
  <div class="launch-site-card" id="kualoa">
    <h3>⛰️ Kualoa Bay</h3>
    <p>Launch from Kualoa Regional Park for access to Mokoliʻi (Chinaman's Hat) and views of the iconic Kualoa Mountain Range. The bay is generally calm but can get choppy with trade winds.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: Morning (before trades pick up)</span>
      <span class="tide-badge caution">⚠️ Afternoon: Trade winds can create chop</span>
      <span class="tide-badge">🌬️ Wind: Check wind forecast (ideally &lt;12 mph)</span>
      <span class="tide-badge">⏱️ Paddle Time: Variable</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐☆☆ — Intermediate. Morning launches recommended. Be aware of changing afternoon conditions.</p>
    <p><a href="/kualoa-bay-guide/">📖 Kualoa Bay Guide →</a></p>
    <p><small>Nearby tide stations: Moku o Loʻe, NOAA Station 1612480</small></p>
  </div>

  <!-- Laie Bay -->
  <div class="launch-site-card" id="laie">
    <h3>🐐 Laie Bay / Goat Island (Mokuʻauia)</h3>
    <p>Paddle to Goat Island, a bird sanctuary just offshore from Laie. The island features a beautiful sandy beach and tide pools. The crossing is short but requires navigating through a reef channel.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: High Tide (deeper channel)</span>
      <span class="tide-badge caution">⚠️ Caution: Low Tide (reef hazard)</span>
      <span class="tide-badge">⏱️ Paddle Time: 10-15 min crossing</span>
      <span class="tide-badge best">🌊 Swell: Best on small swell days</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐☆☆ — Intermediate. Reef navigation required. Go with high tide for safest passage.</p>
    <p><a href="/laie-bay-goat-island-kayaking/">📖 Laie Bay Guide →</a></p>
    <p><small>Nearby tide stations: Laie Bay, NOAA Station 1612480 (interpolated)</small></p>
  </div>

  <!-- Kawela Bay -->
  <div class="launch-site-card" id="kawela">
    <h3>🌴 Kawela Bay</h3>
    <p>A hidden gem on Oʻahu's North Shore, Kawela Bay is a protected cove with calm, clear water. Perfect for a tranquil paddle away from crowds. Best during summer months when North Shore swells are minimal.</p>
    <div class="tide-info">
      <span class="tide-badge best">✅ Best: Summer (May-Sep), Any Tide</span>
      <span class="tide-badge avoid">🚫 Avoid: Winter Swells (Oct-Apr)</span>
      <span class="tide-badge">�🌊 North Shore: Check swell forecast</span>
      <span class="tide-badge">⏱️ Paddle Time: As desired</span>
    </div>
    <p><strong>Safety Rating:</strong> ⭐⭐⭐⭐☆ (Summer) / ⭐⭐☆☆☆ (Winter) — Seasonal. Excellent in summer when North Shore is flat. Can be dangerous in winter.</p>
    <p><a href="/activities/kawela-bay-self-guided-kayak-tour/">🛶 Book Kawela Bay Tour →</a></p>
    <p><small>Nearby tide stations: Haleʻiwa, NOAA Station 1612720</small></p>
  </div>

  <h2>📊 Understanding Oʻahu Tides</h2>
  <p>Oʻahu experiences <strong>mixed semi-diurnal tides</strong> — two high tides and two low tides per day, of different heights. The tidal range is typically 1-3 feet, which significantly affects launch conditions at many sites.</p>

  <div class="guide-table" style="width:100%; border-collapse:collapse; margin:1.5em 0;">
    <table style="width:100%;">
      <thead>
        <tr style="background:#006699; color:white;">
          <th style="padding:12px; text-align:left;">Tide Phase</th>
          <th style="padding:12px; text-align:left;">Best For</th>
          <th style="padding:12px; text-align:left;">Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr><td style="padding:12px; border-bottom:1px solid #ddd;">🌅 Incoming (Flood) Tide</td><td style="padding:12px; border-bottom:1px solid #ddd;">Most launch sites</td><td style="padding:12px; border-bottom:1px solid #ddd;">Water is rising, pushing toward shore. Easier paddling.</td></tr>
        <tr style="background:#f9f9f9;"><td style="padding:12px; border-bottom:1px solid #ddd;">🌊 High Tide (Slack)</td><td style="padding:12px; border-bottom:1px solid #ddd;">Reef channels, Laie Bay</td><td style="padding:12px; border-bottom:1px solid #ddd;">Maximum water depth over reefs. Best for reef crossings.</td></tr>
        <tr><td style="padding:12px; border-bottom:1px solid #ddd;">🌇 Outgoing (Ebb) Tide</td><td style="padding:12px; border-bottom:1px solid #ddd;">Experienced paddlers only</td><td style="padding:12px; border-bottom:1px solid #ddd;">Water rushing out — strongest currents. Risk of being swept out.</td></tr>
        <tr style="background:#f9f9f9;"><td style="padding:12px; border-bottom:1px solid #ddd;">🏖️ Low Tide</td><td style="padding:12px; border-bottom:1px solid #ddd;">Kāneʻohe Sandbar, tide pooling</td><td style="padding:12px; border-bottom:1px solid #ddd;">Reef exposure, shallow channels. Sandbar emerges.</td></tr>
      </tbody>
    </table>
  </div>

  <h2>🔗 Related Resources</h2>
  <ul>
    <li><a href="/guides/oahu-kayak-safety-tide-guide/">Oʻahu Kayak Safety &amp; Tide Guide</a> — In-depth safety and tide planning</li>
    <li><a href="/chinamans-hat-tide-guide/">Chinaman's Hat Tide Guide</a> — Specific to Mokoliʻi</li>
    <li><a href="/kaneohe-sandbar-tide-guide/">Kāneʻohe Sandbar Tide Calendar</a> — Best sandbar exposure times</li>
    <li><a href="/kayak-safety-guide/">Kayak Safety Guide</a> — General safety tips and equipment</li>
    <li><a href="/oahu-launch-guide/">Oʻahu Launch Guide</a> — All launch sites on one page</li>
    <li><a href="/activities.html">All Oʻahu Kayak Tours</a> — Browse and book tours</li>
  </ul>

</div>

<!-- FOOTER PLACEHOLDER -->

<script type="text/javascript" src="/wp-content/themes/activeoahu/js/navigation.js?ver=1.0"></script>
<script type="text/javascript" src="/wp-content/themes/activeoahu/js/skip-link-focus-fix.js?ver=1.0"></script>
<script src="https://fareharbor.com/embeds/api/v1/?autolightframe=yes"></script>
</body>
</html>'''

    (page_dir / "index.html").write_text(page_html)
    print(f"  Created: oahu-kayak-safety-tide-index-map/index.html")
    return page_dir

# ============================================================
# GRO-1204: Wire tide charts into tour pages + Event schema
# ============================================================

# Tour pages that should get tide references
TOUR_TIDE_MAP = {
    "activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html": {
        "location": "Mokoliʻi / Chinaman's Hat",
        "tide_guide_url": "/chinamans-hat-tide-guide/",
        "best_tide": "Incoming to High Tide",
        "tide_note": "The channel to Mokoliʻi can develop strong currents on outgoing tides. Check the <a href='/chinamans-hat-tide-guide/'>Chinaman's Hat Tide Guide</a> before booking."
    },
    "activities/kaneohe-sandbar-kayak-rentals/index.html": {
        "location": "Kāneʻohe Sandbar",
        "tide_guide_url": "/kaneohe-sandbar-tide-guide/",
        "best_tide": "Low to Mid Tide (sandbar exposed)",
        "tide_note": "The sandbar is only exposed at low tide. Check the <a href='/kaneohe-sandbar-tide-guide/'>Kāneʻohe Sandbar Tide Calendar</a> to plan your visit."
    },
    "activities/kailua-bay-mokulua-island-self-guided-kayak-tour/index.html": {
        "location": "Kailua Bay / Mokulua Islands",
        "tide_guide_url": "/guides/oahu-kayak-safety-tide-guide/",
        "best_tide": "Incoming to High Tide",
        "tide_note": "Kailua Bay is protected by a reef. Best conditions on incoming tide with light trade winds. See the <a href='/oahu-kayak-safety-tide-index-map/'>Tide Index Map</a> for details."
    },
    "activities/kahana-rainforest-river-oahu-kayak-tour/index.html": {
        "location": "Kahana River & Bay",
        "tide_guide_url": "/oahu-kayak-safety-tide-index-map/#kahana",
        "best_tide": "Any Tide (river protected)",
        "tide_note": "The Kahana River is protected and paddleable at any tide. Bay section best on slack tide. See the <a href='/oahu-kayak-safety-tide-index-map/'>Tide Index Map</a>."
    },
    "activities/kaneohe-sandbar-kayak-ultimate-guide/index.html": {
        "location": "Kāneʻohe Sandbar",
        "tide_guide_url": "/kaneohe-sandbar-tide-guide/",
        "best_tide": "Low to Mid Tide",
        "tide_note": "Plan around the tides! See the <a href='/kaneohe-sandbar-tide-guide/'>Kāneʻohe Sandbar Tide Calendar</a> for best sandbar exposure times."
    },
    "activities/chinamans-hat-kayak-complete-self-guided-tour-guide/index.html": {
        "location": "Mokoliʻi / Chinaman's Hat",
        "tide_guide_url": "/chinamans-hat-tide-guide/",
        "best_tide": "Incoming to High Tide",
        "tide_note": "Check tides before you go! See the <a href='/chinamans-hat-tide-guide/'>Chinaman's Hat Tide Guide</a> for best crossing conditions."
    },
}

def add_tide_reference_to_tour(rel_path, tide_data):
    """Add a tide reference callout near the booking section of a tour page."""
    filepath = SITE_DIR / rel_path
    if not filepath.exists():
        print(f"  SKIP: {rel_path} not found")
        return False

    html = filepath.read_text()

    # Don't add if already has a tide guide reference
    if 'tide-guide' in html.lower() and 'href="/chinamans-hat-tide-guide' in html:
        print(f"  SKIP: {rel_path} already has tide reference")
        return False

    tide_html = f'''
<!-- Tide Information -->
<div class="tide-info-callout" style="background: #e8f4f8; border-left: 4px solid #006699; border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 16px 0; font-size: 0.95em;">
  <strong>🌊 Tide Info:</strong> {tide_data['tide_note']}
  <br><small>📍 {tide_data['location']} | Best: {tide_data['best_tide']}</small>
</div>
'''

    # Add tide schema as Event (recurring tide window)
    tide_schema = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": f"Best Tide Window for {tide_data['location']}",
        "description": tide_data['tide_note'].replace('<a href=', '').replace('</a>', '').replace('>', '')[:200],
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "location": {
            "@type": "Place",
            "name": tide_data['location'],
            "address": {"@type": "PostalAddress", "addressLocality": "Oahu", "addressRegion": "HI"}
        },
        "about": {"@type": "Thing", "name": f"{tide_data['location']} Kayak Launch"}
    }
    tide_schema_block = f'\n<script type="application/ld+json">\n{json.dumps(tide_schema, indent=2, ensure_ascii=False)}\n</script>\n'

    # Insert tide callout before booking section or at the end of content
    booking_markers = ['fareharbor.com/embeds/book', 'listing-book-button', 'btn-primary']
    inserted = False
    for marker in booking_markers:
        if marker in html:
            # Find last occurrence and insert before it
            last_pos = html.rfind(marker)
            if last_pos > 0:
                # Find beginning of the containing element
                snippet_start = html[:last_pos].rfind('<')
                html = html[:snippet_start] + tide_html + '\n' + html[snippet_start:]
                inserted = True
                break

    if not inserted:
        # Insert before </body> if no booking section found
        if '</body>' in html:
            html = html.replace('</body>', tide_html + '\n</body>', 1)
            inserted = True

    # Add tide schema before </head>
    if '</head>' in html:
        html = html.replace('</head>', tide_schema_block + '</head>', 1)

    filepath.write_text(html)
    return True

def wire_tide_charts():
    """Add tide references to all applicable tour pages."""
    count = 0
    for rel_path, tide_data in TOUR_TIDE_MAP.items():
        result = add_tide_reference_to_tour(rel_path, tide_data)
        if result:
            print(f"  ✅ Tide wired: {rel_path}")
            count += 1
    return count

# ============================================================
# GRO-1198: FareHarbor checkout postponement note
# ============================================================

def create_fareharbor_note():
    """Create documentation for FareHarbor dashboard configuration changes."""
    content = '''# GRO-1198: FareHarbor Checkout — Postpone Height/Weight/Shoe Fields

## Issue
FareHarbor requires Height, Weight, and Shoe Size for ALL participants during checkout (Step 6 of 8). This creates significant mobile friction, especially for group bookings (4+ people).

## Recommendation
Make these fields **optional** during checkout or move them to a post-booking confirmation flow:

### Option A: FareHarbor Dashboard (Recommended)
1. Log into FareHarbor Dashboard → Items → [Each Tour/Rental Item]
2. Under "Custom Fields" or "Participant Questions":
   - Set Height/Weight/Shoe Size fields to **"Optional"** (not required)
3. Add an automated post-booking email asking participants to provide sizing details
4. This reduces checkout steps from 8 to 6, matching competitor KBA's flow

### Option B: JavaScript Workaround (Fallback)
If FareHarbor doesn't support optional fields, a client-side script can pre-fill default values
and hide the fields from view. This is less ideal but works as a stopgap.

### Competitor Comparison
- **Kailua Beach Adventures (KBA)**: Only asks for height/weight on guided tours (not basic rentals) → 6-step checkout
- **Active Oahu currently**: 8-step checkout with sizing for every participant on every booking

## Action Required
Michael: Log into FareHarbor Dashboard and set participant sizing fields to optional for self-guided tours and basic rentals.
'''
    (SITE_DIR.parent / "GRO-1198-fareharbor-checkout-config.md").write_text(content)
    print("  Created: GRO-1198-fareharbor-checkout-config.md")

# ============================================================
# GRO-1199, GRO-1200: Directory listing data
# ============================================================

def create_directory_listings():
    """Create structured business listing data for external directories."""
    listing_data = {
        "business_name": "Active Oahu Tours",
        "dba": "Active Oahu",
        "address": "134B Hamakua Dr, Kailua, HI 96734",
        "phone": "(808) 498-1894",
        "website": "https://activeoahutours.com",
        "email": "info@activeoahutours.com",
        "description": "Kayak tours, e-bike adventures, paddleboarding, and beach gear rentals on Oahu's Windward coast. Self-guided and guided tours to Mokoliʻi (Chinaman's Hat), Kailua Bay, Kāneʻohe Sandbar, Kahana River, and more. Based in Kailua since 2014.",
        "categories": ["Kayak Tours", "Beach Equipment Rentals", "Water Sports", "Eco Tours", "Outdoor Adventures"],
        "services": [
            "Kayak Rentals",
            "Guided Kayak Tours",
            "Self-Guided Kayak Tours",
            "Stand-Up Paddleboard Rentals",
            "E-Bike Rentals",
            "Snorkel Gear Rentals",
            "Beach Gear Rentals",
            "Multi-Day Equipment Rentals"
        ],
        "service_area": ["Kailua", "Lanikai", "Kaneohe", "Kualoa", "Laie", "Kahana", "North Shore", "Windward Oahu"],
        "hours": "Monday-Sunday 7:00 AM - 6:00 PM",
        "year_established": 2014,
        "social": {
            "facebook": "https://www.facebook.com/activeoahutours/",
            "instagram": "https://www.instagram.com/activeoahu/",
            "yelp": "https://www.yelp.com/biz/active-oahu-tours-kailua",
            "tripadvisor": "https://www.tripadvisor.com/Attraction_Review-g60656-d5079465-Reviews-Active_Oahu_Tours-Laie_Oahu_Hawaii.html"
        },
        "logo_url": "https://activeoahutours.com/wp-content/uploads/2019/06/Active-Oahu-Logo.jpg",
        "featured_image": "https://activeoahutours.com/wp-content/uploads/2021/06/DSC5297_2000-e1642616607887.jpg"
    }

    # Write listing data files
    listings_dir = SITE_DIR.parent / "directory-listings"
    listings_dir.mkdir(exist_ok=True)

    # gohawaii.com listing data
    gohawaii_content = f'''# gohawaii.com Business Listing — Active Oahu Tours

## Listing URL
https://www.gohawaii.com/ (submit via Hawaii Tourism Authority partner portal)

## Business Details
- **Business Name:** {listing_data['business_name']}
- **DBA:** {listing_data['dba']}
- **Address:** {listing_data['address']}
- **Phone:** {listing_data['phone']}
- **Website:** {listing_data['website']}
- **Email:** {listing_data['email']}
- **Hours:** {listing_data['hours']}
- **Year Established:** {listing_data['year_established']}

## Description for Listing
{listing_data['description']}

## Categories
{chr(10).join('- ' + c for c in listing_data['categories'])}

## Services
{chr(10).join('- ' + s for s in listing_data['services'])}

## Service Area
{chr(10).join('- ' + a for a in listing_data['service_area'])}

## Social Links
{chr(10).join(f'- {k}: {v}' for k, v in listing_data['social'].items())}

## Images
- Logo: {listing_data['logo_url']}
- Featured: {listing_data['featured_image']}

## SEO Notes
- gohawaii.com has DA (Domain Authority) of ~72
- Listing here provides a high-authority backlink
- Complete all fields for maximum visibility
- Add high-resolution photos (logo + 3-5 activity photos)
'''
    (listings_dir / "gohawaii-com-da72-listing.md").write_text(gohawaii_content)

    # paddling.com listing data
    paddling_content = f'''# paddling.com Business Listing — Active Oahu Tours

## Listing URL
https://paddling.com/ (submit via Go Outside Network)

## Business Details
- **Business Name:** {listing_data['business_name']}
- **DBA:** {listing_data['dba']}
- **Address:** {listing_data['address']}
- **Phone:** {listing_data['phone']}
- **Website:** {listing_data['website']}
- **Email:** {listing_data['email']}
- **Hours:** {listing_data['hours']}
- **Year Established:** {listing_data['year_established']}

## Description for Listing
{listing_data['description']}

## Categories
{chr(10).join('- ' + c for c in listing_data['categories'])}

## Services
{chr(10).join('- ' + s for s in listing_data['services'])}

## Service Area
{chr(10).join('- ' + a for a in listing_data['service_area'])}

## Social Links
{chr(10).join(f'- {k}: {v}' for k, v in listing_data['social'].items())}

## Images
- Logo: {listing_data['logo_url']}
- Featured: {listing_data['featured_image']}

## SEO Notes
- paddling.com has DA (Domain Authority) of ~59
- High-relevance niche directory for kayak/paddle sports
- Listing provides a targeted backlink in the paddling industry
- Include kayak-specific descriptions and keywords
'''
    (listings_dir / "paddling-com-da59-listing.md").write_text(paddling_content)
    print(f"  Created: directory-listings/gohawaii-com-da72-listing.md")
    print(f"  Created: directory-listings/paddling-com-da59-listing.md")
    return listings_dir

# ============================================================
# SITEMAP UPDATE (GRO-1204)
# ============================================================

def update_sitemap():
    """Add new pages to sitemap.xml."""
    sitemap_path = SITE_DIR.parent / "sitemap.xml"
    if not sitemap_path.exists():
        print("  WARN: sitemap.xml not found")
        return

    sitemap = sitemap_path.read_text()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    new_urls = [
        "oahu-kayak-safety-tide-index-map/",
    ]

    for url_path in new_urls:
        entry = f'''  <url>
    <loc>https://activeoahutours.com/{url_path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>'''

        if url_path not in sitemap:
            # Insert before closing </urlset>
            sitemap = sitemap.replace('</urlset>', entry + '\n</urlset>', 1)

    sitemap_path.write_text(sitemap)
    print(f"  Updated sitemap.xml with {len(new_urls)} new URLs")

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("GRO-1201: Creating Oahu Kayak Safety & Tide Index Map...")
    create_safety_tide_index()

    print("\nGRO-1204: Wiring tide charts into tour pages...")
    wired = wire_tide_charts()
    print(f"  Total tide references added: {wired}")

    print("\nGRO-1198: Creating FareHarbor checkout config note...")
    create_fareharbor_note()

    print("\nGRO-1199/1200: Creating directory listing data...")
    create_directory_listings()

    print("\nGRO-1204: Updating sitemap...")
    update_sitemap()

    print("\n" + "=" * 60)
    print("All tasks complete!")
