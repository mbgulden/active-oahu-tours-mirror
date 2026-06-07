from bs4 import BeautifulSoup

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    prod_html = read_file('site/index.html')
    soup = BeautifulSoup(prod_html, 'html.parser')
    
    print("=== All script tags in Production index.html ===")
    for idx, s in enumerate(soup.find_all('script')):
        src = s.get('src')
        if src:
            print(f"  {idx+1}. Src: {src}")
        else:
            print(f"  {idx+1}. Inline (length {len(s.string or '')})")
            
    print("\n=== All script tags in Staging html ===")
    fw_html = read_file('/tmp/flywheel-staging.html')
    fw_soup = BeautifulSoup(fw_html, 'html.parser')
    for idx, s in enumerate(fw_soup.find_all('script')):
        src = s.get('src')
        if src:
            print(f"  {idx+1}. Src: {src}")
        else:
            print(f"  {idx+1}. Inline (length {len(s.string or '')})")

if __name__ == '__main__':
    main()
