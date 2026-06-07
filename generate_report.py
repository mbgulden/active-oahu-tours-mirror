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

def get_body_nav_section(html_str, filename=""):
    # Find position of <body ...> up to </nav>
    body_match = re.search(r'<body[^>]*>', html_str, re.IGNORECASE)
    if not body_match:
        return None, f"No body tag found in {filename}"
    
    # We want from start of <body> to </nav>
    nav_match = re.search(r'</nav>', html_str, re.IGNORECASE)
    if not nav_match:
        return None, f"No </nav> tag found in {filename}"
    
    start_pos = body_match.start()
    end_pos = nav_match.end()
    
    return html_str[start_pos:end_pos], None

def show_diff(str1, str2, label1, label2):
    lines1 = str1.splitlines(keepends=True)
    lines2 = str2.splitlines(keepends=True)
    diff = list(difflib.unified_diff(lines1, lines2, fromfile=label1, tofile=label2, n=3))
    return "".join(diff)

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    head_tmpl_html = read_file('site/_templates/head.html')
    body_top_tmpl_html = read_file('site/_templates/body_top.html')
    
    fw_soup = BeautifulSoup(fw_html, 'html.parser')
    prod_soup = BeautifulSoup(prod_html, 'html.parser')
    head_tmpl_soup = BeautifulSoup(head_tmpl_html, 'html.parser')
    body_top_tmpl_soup = BeautifulSoup(body_top_tmpl_html, 'html.parser')
    
    with open('full_comparison_output.txt', 'w', encoding='utf-8') as out:
        # Write general information
        out.write("=== ACTIVE OAHU TOURS WEB SITE COMPARISON ===\n\n")
        
        # 1. CSS Links
        out.write("--- 1. CSS LINKS IN HEAD ---\n")
        fw_css = get_css_links(fw_soup.head)
        prod_css = get_css_links(prod_soup.head)
        head_tmpl_css = get_css_links(head_tmpl_soup)
        
        out.write(f"Staging CSS links: {len(fw_css)}\n")
        out.write(f"Production CSS links: {len(prod_css)}\n")
        out.write(f"head.html template CSS links: {len(head_tmpl_css)}\n\n")
        
        fw_norm_hrefs = [c['normalized_href'] for c in fw_css]
        prod_norm_hrefs = [c['normalized_href'] for c in prod_css]
        head_tmpl_norm_hrefs = [c['normalized_href'] for c in head_tmpl_css]
        
        missing_in_fw = [h for h in prod_norm_hrefs if h not in fw_norm_hrefs]
        missing_in_prod = [h for h in fw_norm_hrefs if h not in prod_norm_hrefs]
        
        out.write(f"Hrefs in Production but not in Staging: {missing_in_fw}\n")
        out.write(f"Hrefs in Staging but not in Production: {missing_in_prod}\n\n")
        
        # 2. Inline Styles
        out.write("--- 2. INLINE STYLES ---\n")
        fw_styles = get_inline_styles(fw_soup)
        prod_styles = get_inline_styles(prod_soup)
        
        out.write(f"Flywheel inline styles count: {len(fw_styles)}\n")
        out.write(f"Production inline styles count: {len(prod_styles)}\n\n")
        
        fw_styles_by_id = {s['id']: s for s in fw_styles if s['id']}
        prod_styles_by_id = {s['id']: s for s in prod_styles if s['id']}
        
        all_ids = sorted(list(set(list(fw_styles_by_id.keys()) + list(prod_styles_by_id.keys()))))
        for style_id in all_ids:
            if style_id in fw_styles_by_id and style_id in prod_styles_by_id:
                s_fw = fw_styles_by_id[style_id]
                s_prod = prod_styles_by_id[style_id]
                if s_fw['hash'] != s_prod['hash']:
                    out.write(f"Style ID: {style_id} MISMATCH!\n")
                    diff = show_diff(s_fw['content'], s_prod['content'], f"Staging {style_id}", f"Production {style_id}")
                    out.write(diff + "\n\n")
                else:
                    out.write(f"Style ID: {style_id} MATCHES (Length: {len(s_fw['content'])})\n")
            elif style_id in fw_styles_by_id:
                out.write(f"Style ID: {style_id} ONLY IN STAGING!\n\n")
            else:
                out.write(f"Style ID: {style_id} ONLY IN PRODUCTION!\n\n")
                
        # 3. Navigation HTML Structure from body through nav
        out.write("--- 3. NAVIGATION HTML STRUCTURE ---\n")
        fw_nav_sect, fw_err = get_body_nav_section(fw_html, "Flywheel Staging")
        prod_nav_sect, prod_err = get_body_nav_section(prod_html, "Production index.html")
        
        if fw_err or prod_err:
            out.write(f"Error getting nav section: FW={fw_err}, Prod={prod_err}\n")
        else:
            identical = (fw_nav_sect == prod_nav_sect)
            out.write(f"Are staging and production nav sections byte-for-byte identical? {identical}\n")
            out.write(f"Staging nav length: {len(fw_nav_sect)}, Production nav length: {len(prod_nav_sect)}\n")
            if not identical:
                diff_nav = show_diff(fw_nav_sect, prod_nav_sect, "Staging Nav", "Production Nav")
                out.write("Diff in Nav Section:\n")
                out.write(diff_nav + "\n")
                
        # 4. Mobile Menu JS
        out.write("--- 4. MOBILE MENU JAVASCRIPT ---\n")
        # Let's write script tags to output file to find where javascript is
        fw_scripts = [s.string for s in fw_soup.find_all('script') if s.string]
        prod_scripts = [s.string for s in prod_soup.find_all('script') if s.string]
        out.write(f"Staging has {len(fw_scripts)} inline scripts.\n")
        out.write(f"Production has {len(prod_scripts)} inline scripts.\n")

if __name__ == '__main__':
    main()
