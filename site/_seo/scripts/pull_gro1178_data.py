import asyncio
import json
import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TOKEN = open('/tmp/ubs_token').read().strip()
URL = "https://ubersuggest-mcp.neilpatelapi.com/mcp"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Ensure directories exist
os.makedirs("/home/ubuntu/work/active-oahu-static/site/_seo/raw", exist_ok=True)
os.makedirs("/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest", exist_ok=True)

async def call_tool_safe(tool, args):
    print(f"Calling tool: {tool} with args: {args}")
    for attempt in range(3):
        try:
            async with streamablehttp_client(URL, headers=HEADERS) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool, args)
                    text = result.content[0].text if result.content else "{}"
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        print(f"JSON decode failed for {tool}. Raw response: {text[:300]}")
                        return {"raw_text": text}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {tool} with error: {e}")
            await asyncio.sleep(2)
    return {"error": "failed after 3 attempts"}

async def main():
    domain = "activeoahutours.com"
    
    # 1. Competitors
    print("Fetching competitors for activeoahutours.com...")
    comps_data = await call_tool_safe("competitors", {"domain": domain, "locId": 2840, "language": "en"})
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/gro1178_competitors.json", "w") as f:
        json.dump(comps_data, f, indent=2)
    
    # Extract top 3 competitors from Ubersuggest
    competitors = []
    if comps_data and "competitors" in comps_data:
        for c in comps_data["competitors"]:
            c_domain = c.get("domain") or c.get("competitor")
            if c_domain and c_domain != domain:
                competitors.append(c_domain)
    
    # Fallback if competitors is empty
    if not competitors:
        competitors = ["kailuabeachadventures.com", "surfnsea.com", "hawaiibeachtime.com"]
        
    print(f"Top competitors identified: {competitors[:3]}")
    
    # Save the list to data folder as well
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/gro1178_competitors_list.json", "w") as f:
        json.dump(competitors, f, indent=2)
        
    # 2. AOT domain keywords (limit 200)
    print("Fetching keywords for activeoahutours.com...")
    aot_kws = await call_tool_safe("domain_keywords", {
        "domain": domain,
        "limit": 200,
        "locId": 2840,
        "language": "en"
    })
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/gro1178_activeoahutours_keywords.json", "w") as f:
        json.dump(aot_kws, f, indent=2)
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/gro1178_activeoahutours_keywords.json", "w") as f:
        json.dump(aot_kws, f, indent=2)
        
    # 3. AOT top pages (limit 50)
    print("Fetching top pages for activeoahutours.com...")
    aot_pages = await call_tool_safe("domain_top_pages", {
        "domain": domain,
        "limit": 50,
        "locId": 2840,
        "language": "en"
    })
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/gro1178_activeoahutours_top_pages.json", "w") as f:
        json.dump(aot_pages, f, indent=2)
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/gro1178_activeoahutours_top_pages.json", "w") as f:
        json.dump(aot_pages, f, indent=2)

    # 4. Competitor keywords (top 3, limit 100 each)
    for comp in competitors[:3]:
        print(f"Fetching keywords for competitor: {comp}...")
        comp_kws = await call_tool_safe("domain_keywords", {
            "domain": comp,
            "limit": 100,
            "locId": 2840,
            "language": "en"
        })
        filename = f"gro1178_{comp.replace('.', '_')}_keywords.json"
        with open(f"/home/ubuntu/work/active-oahu-static/site/_seo/raw/{filename}", "w") as f:
            json.dump(comp_kws, f, indent=2)
        with open(f"/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/{filename}", "w") as f:
            json.dump(comp_kws, f, indent=2)
        await asyncio.sleep(1)

    print("Ubersuggest data pull complete.")

if __name__ == "__main__":
    asyncio.run(main())
