import sys
from bs4 import BeautifulSoup

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def normalize_text(text):
    if not text:
        return ""
    text = text.replace('https://activeoahutours2.flywheelstaging.com', '')
    text = text.replace('http://activeoahutours2.flywheelstaging.com', '')
    text = text.replace('\u202f', '-')
    return text.strip()

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    
    fw_soup = BeautifulSoup(fw_html, 'html.parser')
    prod_soup = BeautifulSoup(prod_html, 'html.parser')
    
    fw_style = fw_soup.find('style', id='kadence_blocks_css-inline-css').string or ''
    prod_style = prod_soup.find('style', id='kadence_blocks_css-inline-css').string or ''
    
    fw_norm = normalize_text(fw_style)
    prod_norm = normalize_text(prod_style)
    
    print("kadence_blocks_css-inline-css identical when normalized?", fw_norm == prod_norm)
    if fw_norm != prod_norm:
        # find where they start to differ
        for i, (c1, c2) in enumerate(zip(fw_norm, prod_norm)):
            if c1 != c2:
                print(f"Differ at char {i}: FW={fw_norm[i:i+50]!r} vs Prod={prod_norm[i:i+50]!r}")
                break

if __name__ == '__main__':
    main()
