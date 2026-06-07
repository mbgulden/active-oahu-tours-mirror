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
    
    fw_style = fw_soup.find('style', id='kadence_blocks_css-inline-css').string or ''
    prod_style = prod_soup.find('style', id='kadence_blocks_css-inline-css').string or ''
    
    # Let's search for PM.png in both
    for match in ['PM.png', 'pm.png', 'AM.png', 'am.png']:
        idx = fw_style.find(match)
        if idx != -1:
            print(f"FW match {match} at {idx}: {fw_style[max(0, idx-50):idx+50]!r}")
        idx = prod_style.find(match)
        if idx != -1:
            print(f"Prod match {match} at {idx}: {prod_style[max(0, idx-50):idx+50]!r}")

if __name__ == '__main__':
    main()
