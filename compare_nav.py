import re
import difflib

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_body_nav_section(html_str, filename=""):
    # Search for <body ...> up to </nav>
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

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    body_top_html = read_file('site/_templates/body_top.html')
    
    fw_nav, fw_err = get_body_nav_section(fw_html, "Flywheel Staging")
    prod_nav, prod_err = get_body_nav_section(prod_html, "Production index.html")
    
    print("Flywheel err:", fw_err)
    print("Production err:", prod_err)
    
    # Let's see if body_top has body to nav
    # body_top.html itself might start with <body> or just contain the nav code directly. Let's check.
    print(f"body_top_tmpl length: {len(body_top_html)}")
    print(f"body_top_tmpl starts with: {body_top_html[:200]!r}")
    print(f"body_top_tmpl ends with: {body_top_html[-200:]!r}")
    
    # Compare Staging vs Production
    if fw_nav and prod_nav:
        print(f"FW nav len: {len(fw_nav)}, Prod nav len: {len(prod_nav)}")
        identical = (fw_nav == prod_nav)
        print(f"FW vs Prod Nav identical: {identical}")
        
        diff = list(difflib.unified_diff(
            fw_nav.splitlines(keepends=True),
            prod_nav.splitlines(keepends=True),
            fromfile='Flywheel Staging',
            tofile='Production index.html',
            n=5
        ))
        
        print("\n=== FULL NAV DIFF ===")
        print("".join(diff))

if __name__ == '__main__':
    main()
