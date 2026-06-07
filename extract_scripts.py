import sys
from bs4 import BeautifulSoup

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    
    fw_soup = BeautifulSoup(fw_html, 'html.parser')
    prod_soup = BeautifulSoup(prod_html, 'html.parser')
    
    # Extract scripts that contain "navigation.js"
    fw_nav_scripts = [s.string for s in fw_soup.find_all('script') if s.string and 'navigation.js' in s.string]
    prod_nav_scripts = [s.string for s in prod_soup.find_all('script') if s.string and 'navigation.js' in s.string]
    
    print(f"Staging navigation.js script count: {len(fw_nav_scripts)}")
    print(f"Production navigation.js script count: {len(prod_nav_scripts)}")
    
    if fw_nav_scripts:
        with open('fw_navigation_js.txt', 'w', encoding='utf-8') as f:
            f.write(fw_nav_scripts[0])
            
    if prod_nav_scripts:
        with open('prod_navigation_js.txt', 'w', encoding='utf-8') as f:
            f.write(prod_nav_scripts[0])
            
    # Extract the custom toggle script in production (length 2358)
    prod_custom_scripts = [s.string for s in prod_soup.find_all('script') if s.string and 'Nav dropdown' in s.string]
    print(f"Production custom toggle script count: {len(prod_custom_scripts)}")
    if prod_custom_scripts:
        with open('prod_custom_toggle_js.txt', 'w', encoding='utf-8') as f:
            f.write(prod_custom_scripts[0])

if __name__ == '__main__':
    main()
