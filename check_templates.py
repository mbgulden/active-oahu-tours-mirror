import sys
import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_body_nav_section(html_str):
    body_match = re.search(r'<body[^>]*>', html_str, re.IGNORECASE)
    if not body_match:
        return None
    nav_match = re.search(r'</nav>', html_str, re.IGNORECASE)
    if not nav_match:
        return None
    return html_str[body_match.start():nav_match.end()]

def main():
    prod_html = read_file('site/index.html')
    body_top_html = read_file('site/_templates/body_top.html')
    
    prod_nav = get_body_nav_section(prod_html)
    tmpl_nav = get_body_nav_section(body_top_html)
    
    print(f"Prod nav len: {len(prod_nav) if prod_nav else 0}")
    print(f"Tmpl nav len: {len(tmpl_nav) if tmpl_nav else 0}")
    
    if prod_nav and tmpl_nav:
        print("Are prod nav and template nav byte-for-byte identical?", prod_nav == tmpl_nav)
        if prod_nav != tmpl_nav:
            # print diff
            import difflib
            diff = list(difflib.unified_diff(
                tmpl_nav.splitlines(keepends=True),
                prod_nav.splitlines(keepends=True),
                fromfile='Template Nav',
                tofile='Prod Nav',
                n=3
            ))
            print("Diff:")
            print("".join(diff))

if __name__ == '__main__':
    main()
