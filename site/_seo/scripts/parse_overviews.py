import json

with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/domain_overviews.json") as f:
    data = json.load(f)

print("Domains in overviews file:")
for dom, info in data.items():
    if "error" in info:
        print(f"- {dom}: ERROR: {info['error']}")
    elif "raw_text" in info:
        print(f"- {dom}: RAW TEXT (probably 403 error): {info['raw_text'][:200]}")
    else:
        print(f"- {dom}: Success! DA={info.get('domainAuthority')}, traffic={info.get('traffic')}, keywords={len(info.get('organicKeywords', []))}")
        if info.get('organicKeywords'):
            print(f"  Top keywords:")
            for kw in info['organicKeywords'][:5]:
                print(f"    * {kw['keyword']}: pos={kw['position']}, vol={kw['volume']}, traffic={kw['traffic']}")
