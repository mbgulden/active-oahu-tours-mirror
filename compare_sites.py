import sys
import re
import hashlib
import difflib
from bs4 import BeautifulSoup

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def normalize_url(url):
    if not url:
        return url
    prefix = 'https://activeoahutours2.flywheelstaging.com'
    if url.startswith(prefix):
        return url[len(prefix):]
    return url

def get_css_links(soup):
    links = []
    if not soup:
        return links
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        media = link.get('media')
        id_val = link.get('id')
        links.append({'href': href, 'normalized_href': normalize_url(href), 'media': media, 'id': id_val})
    return links

def get_inline_styles(soup):
    styles = []
    if not soup:
        return styles
    for style in soup.find_all('style'):
        id_val = style.get('id')
        content = style.string or ''
        styles.append({'id': id_val, 'content': content.strip(), 'hash': hashlib.md5(content.strip().encode('utf-8')).hexdigest()})
    return styles

def get_body_nav_section(html_str):
    # Search for <body ...> up to </nav>
    body_match = re.search(r'<body[^>]*>', html_str, re.IGNORECASE)
    if not body_match:
        return None, "No body tag found"
    
    # We want from start of <body> to </nav>
    nav_match = re.search(r'</nav>', html_str, re.IGNORECASE)
    if not nav_match:
        return None, "No </nav> tag found"
    
    start_pos = body_match.start()
    end_pos = nav_match.end()
    
    return html_str[start_pos:end_pos], None

def show_diff(str1, str2, label1, label2):
    lines1 = str1.splitlines(keepends=True)
    lines2 = str2.splitlines(keepends=True)
    diff = list(difflib.unified_diff(lines1, lines2, fromfile=label1, tofile=label2, n=3))
    return "".join(diff)

def main():
    fw_path = '/tmp/flywheel-staging.html'
    prod_path = 'site/index.html'
    head_tmpl_path = 'site/_templates/head.html'
    body_top_tmpl_path = 'site/_templates/body_top.html'
    
    fw_html = read_file(fw_path)
    prod_html = read_file(prod_path)
    head_tmpl_html = read_file(head_tmpl_path)
    body_top_tmpl_html = read_file(body_top_tmpl_path)
    
    fw_soup = BeautifulSoup(fw_html, 'html.parser')
    prod_soup = BeautifulSoup(prod_html, 'html.parser')
    head_tmpl_soup = BeautifulSoup(head_tmpl_html, 'html.parser')
    
    # 1. Compare CSS Links
    print("=== 1. CSS LINKS IN HEAD ===")
    fw_css = get_css_links(fw_soup.head)
    prod_css = get_css_links(prod_soup.head)
    head_tmpl_css = get_css_links(head_tmpl_soup)
    
    print(f"Staging CSS links: {len(fw_css)}")
    print(f"Production CSS links: {len(prod_css)}")
    print(f"head.html template CSS links: {len(head_tmpl_css)}")
    
    # Normalize hrefs
    fw_norm_hrefs = [c['normalized_href'] for c in fw_css]
    prod_norm_hrefs = [c['normalized_href'] for c in prod_css]
    head_tmpl_norm_hrefs = [c['normalized_href'] for c in head_tmpl_css]
    
    # Differences:
    missing_in_fw = [h for h in prod_norm_hrefs if h not in fw_norm_hrefs]
    missing_in_prod = [h for h in fw_norm_hrefs if h not in prod_norm_hrefs]
    print(f"Normalized hrefs in Production but not in Staging: {missing_in_fw}")
    print(f"Normalized hrefs in Staging but not in Production: {missing_in_prod}")
    
    # Differences between head.html template and production index.html
    missing_in_head_tmpl = [h for h in prod_norm_hrefs if h not in head_tmpl_norm_hrefs]
    missing_in_prod_from_tmpl = [h for h in head_tmpl_norm_hrefs if h not in prod_norm_hrefs]
    print(f"Normalized hrefs in Production but not in head.html: {missing_in_head_tmpl}")
    print(f"Normalized hrefs in head.html but not in Production: {missing_in_prod_from_tmpl}")

    # 2. Compare Inline Styles
    print("\n=== 2. INLINE STYLES ===")
    fw_styles = get_inline_styles(fw_soup)
    prod_styles = get_inline_styles(prod_soup)
    
    fw_styles_by_id = {s['id']: s for s in fw_styles if s['id']}
    prod_styles_by_id = {s['id']: s for s in prod_styles if s['id']}
    
    all_ids = sorted(list(set(list(fw_styles_by_id.keys()) + list(prod_styles_by_id.keys()))))
    for style_id in all_ids:
        if style_id in fw_styles_by_id and style_id in prod_styles_by_id:
            s_fw = fw_styles_by_id[style_id]
            s_prod = prod_styles_by_id[style_id]
            if s_fw['hash'] != s_prod['hash']:
                print(f"Style ID: {style_id} MISMATCH!")
                diff = show_diff(s_fw['content'], s_prod['content'], f"Staging {style_id}", f"Production {style_id}")
                print(diff[:1000]) # Print first 1000 chars of diff
                if len(diff) > 1000:
                    print("... (truncated)")
            else:
                print(f"Style ID: {style_id} MATCHES (Length: {len(s_fw['content'])})")
        elif style_id in fw_styles_by_id:
            print(f"Style ID: {style_id} ONLY IN STAGING!")
        else:
            print(f"Style ID: {style_id} ONLY IN PRODUCTION!")
            
    # Print the style block only in Production:
    if 'wpb-google-fonts-css' in prod_styles_by_id:
        print("\nContent of wpb-google-fonts-css (only in production):")
        print(prod_styles_by_id['wpb-google-fonts-css']['content'])

    # 3. Navigation HTML Structure from body through nav
    print("\n=== 3. NAVIGATION HTML STRUCTURE ===")
    fw_nav_sect, fw_err = get_body_nav_section(fw_html)
    prod_nav_sect, prod_err = get_body_nav_section(prod_html)
    
    if fw_err or prod_err:
        print(f"Error getting nav section: FW={fw_err}, Prod={prod_err}")
    else:
        # Check if they are byte-for-byte identical
        identical = (fw_nav_sect == prod_nav_sect)
        print(f"Are staging and production nav sections byte-for-byte identical? {identical}")
        if not identical:
            print("Length: Staging nav section length:", len(fw_nav_sect))
            print("Length: Production nav section length:", len(prod_nav_sect))
            diff_nav = show_diff(fw_nav_sect, prod_nav_sect, "Staging Nav", "Production Nav")
            print("Diff in Nav Section (first 2000 chars):")
            print(diff_nav[:2000])
            if len(diff_nav) > 2000:
                print("... (truncated)")
                
            # Let's save full diff somewhere or check it carefully
            with open('nav_diff.txt', 'w') as f:
                f.write(diff_nav)

if __name__ == '__main__':
    main()
