#!/usr/bin/env python3
"""Propagate the GRO-1197 mobile header CSS to all site pages."""
from pathlib import Path
import re

SITE_DIR = Path("site")

MOBILE_CSS = """
              /* MOBILE HEADER: logo + phone + CTA on single line */
              @media (max-width: 768px) {
                #branding {
                  display: flex !important;
                  align-items: center !important;
                  justify-content: space-between !important;
                  flex-wrap: nowrap !important;
                  padding: 5px 10px !important;
                }
                #branding .aot-logo {
                  flex: 0 0 auto !important;
                  margin-right: 5px !important;
                }
                #branding .aot-logo img {
                  width: 100px !important;
                  height: auto !important;
                }
                #branding .social-header {
                  display: flex !important;
                  align-items: center !important;
                  gap: 6px !important;
                  flex: 1 1 auto !important;
                  justify-content: flex-end !important;
                }
                #branding .social-header h3 {
                  font-size: 12px !important;
                  margin: 0 !important;
                  white-space: nowrap !important;
                }
                #branding .social-header .btn {
                  font-size: 11px !important;
                  padding: 4px 8px !important;
                  white-space: nowrap !important;
                }
              }
              @media (max-width: 400px) {
                #branding .aot-logo img {
                  width: 75px !important;
                }
                #branding .social-header h3 {
                  font-size: 10px !important;
                }
                #branding .social-header .btn {
                  font-size: 10px !important;
                  padding: 3px 6px !important;
                }
              }"""

# Anchor text that comes right before where we insert
ANCHOR = """.weglot-flags.flag-0.en>a:before, .weglot-flags.flag-0.en>span:before {
                  background-image: url(https://cdn.jsdelivr.net/gh/weglot/languages@1.56.0/images/4x3/us.svg);
                  background-position: unset!important;
                  width: 26px!important;
                  height: 19px!important;
              }"""

# Check if the anchor exists and mobile CSS not already present
def needs_update(html):
    return ANCHOR in html and "MOBILE HEADER" not in html

def main():
    html_files = sorted(SITE_DIR.rglob("*.html"))
    # Skip templates, theme files, wp-includes
    html_files = [f for f in html_files
                  if '_templates' not in str(f)
                  and 'wp-content/themes' not in str(f)
                  and 'wp-includes' not in str(f)
                  and 'fonts.gstatic.com' not in str(f)
                  and '404.html' not in str(f)]

    updated = 0
    skipped = 0
    for path in html_files:
        html = path.read_text()
        if needs_update(html):
            new_html = html.replace(ANCHOR, ANCHOR + MOBILE_CSS, 1)
            path.write_text(new_html)
            updated += 1
        else:
            skipped += 1

    print(f"Updated: {updated} pages with mobile header CSS")
    print(f"Skipped: {skipped} pages (already updated or different structure)")

if __name__ == "__main__":
    main()
