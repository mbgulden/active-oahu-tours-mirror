import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def find_script_references(html, name):
    print(f"=== Script refs in {name} ===")
    # Look for script tags
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for s in soup.find_all('script'):
        src = s.get('src')
        if src:
            if 'navigation' in src or 'style' in src or 'theme' in src or 'menu' in src or 'custom' in src or 'activeoahu' in src:
                print(f"  Src: {src}")
        else:
            code = s.string or ''
            if 'menu-toggle' in code or 'navigation' in code or 'toggled' in code or 'menuToggle' in code or 'aria-expanded' in code:
                print(f"  Inline Script (length {len(code)}):")
                print(code[:500])
                if len(code) > 500:
                    print("... (truncated)")

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    
    find_script_references(fw_html, "Staging")
    find_script_references(prod_html, "Production")

if __name__ == '__main__':
    main()
