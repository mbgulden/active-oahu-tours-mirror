import os
import sys
import json
from html.parser import HTMLParser

class JSONLDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_jsonld = False
        self.jsonld_contents = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            attrs_dict = dict(attrs)
            if attrs_dict.get('type') == 'application/ld+json':
                self.in_jsonld = True

    def handle_endtag(self, tag):
        if tag.lower() == 'script' and self.in_jsonld:
            self.in_jsonld = False

    def handle_data(self, data):
        if self.in_jsonld:
            self.jsonld_contents.append(data)

def validate_file(filepath):
    print(f"Validating: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    parser = JSONLDParser()
    parser.feed(html_content)
    
    errors = []
    for idx, content in enumerate(parser.jsonld_contents):
        try:
            # Parse the JSON
            parsed = json.loads(content)
            type_val = parsed.get('@type') or parsed.get('type')
            if isinstance(parsed, list):
                type_val = [item.get('@type') or item.get('type') for item in parsed]
            print(f"  [OK] JSON-LD block {idx+1} is valid JSON. Type: {type_val}")
        except json.JSONDecodeError as e:
            errors.append((idx+1, str(e), content))
            print(f"  [ERROR] JSON-LD block {idx+1} has invalid JSON: {e}")
            
    return errors

if __name__ == "__main__":
    target_files = [
        "site/activities/kawela-bay-self-guided-kayak-tour/index.html",
        "site/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html",
        "site/ja/activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html",
        "site/activities/kahana-rainforest-river-oahu-kayak-tour/index.html",
        "site/ja/activities/kahana-rainforest-river-oahu-kayak-tour/index.html",
        "site/guides/oahu-kayak-safety-tide-guide/index.html",
        "site/guides/index.html"
    ]
    
    all_ok = True
    for file_rel in target_files:
        filepath = os.path.join("/home/ubuntu/work/active-oahu-static", file_rel)
        if not os.path.exists(filepath):
            print(f"File does not exist: {filepath}")
            all_ok = False
            continue
        errors = validate_file(filepath)
        if errors:
            all_ok = False
            
    if all_ok:
        print("\nAll JSON-LD schemas parsed successfully with 0 errors!")
        sys.exit(0)
    else:
        print("\nValidation FAILED! See errors above.")
        sys.exit(1)
