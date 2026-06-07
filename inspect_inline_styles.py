import sys
import re
import difflib
from bs4 import BeautifulSoup

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_style_content(soup, style_id):
    style = soup.find('style', id=style_id)
    if style:
        return (style.string or '').strip()
    return None

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    
    fw_soup = BeautifulSoup(fw_html, 'html.parser')
    prod_soup = BeautifulSoup(prod_html, 'html.parser')
    
    mismatch_ids = ['kadence-blocks-global-variables-inline-css', 'kadence_blocks_css-inline-css', 'wp-block-heading-inline-css']
    
    for style_id in mismatch_ids:
        fw_val = get_style_content(fw_soup, style_id)
        prod_val = get_style_content(prod_soup, style_id)
        
        if fw_val is None or prod_val is None:
            print(f"ID {style_id} not found in one of the files.")
            continue
            
        print(f"=== style id: {style_id} ===")
        print(f"Flywheel length: {len(fw_val)}")
        print(f"Production length: {len(prod_val)}")
        
        diff = list(difflib.unified_diff(
            fw_val.splitlines(keepends=True),
            prod_val.splitlines(keepends=True),
            fromfile='Staging',
            tofile='Production',
            n=3
        ))
        
        # Let's print out what is different
        # Since the styles might be minified (single line), unified_diff on lines might show the entire line as changed.
        # If it's a single line, let's compare character-by-character or split by ';' or '}' to make it readable.
        if len(fw_val.splitlines()) <= 5:
            # Try splitting by '}' or ';' to format CSS nicely
            fw_fmt = fw_val.replace('}', '}\n').replace('{', ' {\n').replace(';', ';\n')
            prod_fmt = prod_val.replace('}', '}\n').replace('{', ' {\n').replace(';', ';\n')
            
            diff_fmt = list(difflib.unified_diff(
                fw_fmt.splitlines(keepends=True),
                prod_fmt.splitlines(keepends=True),
                fromfile='Staging-Formatted',
                tofile='Production-Formatted',
                n=3
            ))
            print("Formatted Diff (first 20 lines):")
            print("".join(diff_fmt[:40]))
        else:
            print("Diff (first 20 lines):")
            print("".join(diff[:20]))
        print()

if __name__ == '__main__':
    main()
