import sys
import re
from bs4 import BeautifulSoup

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_nav_soup(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')
    # Let's find the main navigation element
    # site-navigation class or id is common
    nav = soup.find('nav', id='site-navigation')
    if not nav:
        nav = soup.find('nav')
    return nav

def main():
    fw_html = read_file('/tmp/flywheel-staging.html')
    prod_html = read_file('site/index.html')
    
    fw_nav = get_nav_soup(fw_html)
    prod_nav = get_nav_soup(prod_html)
    
    if not fw_nav or not prod_nav:
        print("Nav soup not found!")
        return
        
    fw_links = fw_nav.find_all('a')
    prod_links = prod_nav.find_all('a')
    
    print(f"Staging has {len(fw_links)} links in nav.")
    print(f"Production has {len(prod_links)} links in nav.")
    
    # Let's extract text and href of all links
    fw_link_data = [(a.text.strip(), a.get('href')) for a in fw_links]
    prod_link_data = [(a.text.strip(), a.get('href')) for a in prod_links]
    
    print("\nStaging links:")
    for idx, (text, href) in enumerate(fw_link_data):
        print(f"  {idx+1}. {text} -> {href}")
        
    print("\nProduction links:")
    for idx, (text, href) in enumerate(prod_link_data):
        print(f"  {idx+1}. {text} -> {href}")

if __name__ == '__main__':
    main()
