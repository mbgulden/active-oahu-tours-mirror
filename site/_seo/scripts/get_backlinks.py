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
    print("Fetching competitors...")
    comps_data = await call_tool_safe("competitors", {"domain": domain, "locId": 2840, "language": "en"})
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/competitors.json", "w") as f:
        json.dump(comps_data, f, indent=2)
    
    # Extract competitor domains
    competitors = ["kailuabeachadventures.com", "surfnsea.com", "hawaiibeachtime.com", "hawaiiactivities.com"]
    if comps_data and "competitors" in comps_data:
        # If we got a list of competitors, we can add them
        for c in comps_data["competitors"]:
            c_domain = c.get("domain") or c.get("competitor")
            if c_domain and c_domain not in competitors:
                competitors.append(c_domain)
    print(f"Competitors list: {competitors}")
    
    # 2. Backlinks Overview for all domains
    print("Fetching backlinks overview...")
    overviews = {}
    for d in [domain] + competitors[:5]:  # limit to top 5 competitors to avoid hitting limits
        overviews[d] = await call_tool_safe("backlinks_overview", {"domain": d})
        await asyncio.sleep(1)
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/backlinks_overviews.json", "w") as f:
        json.dump(overviews, f, indent=2)
        
    # 3. Backlinks for AOT (paginated to get a good sample)
    print("Fetching backlinks for activeoahutours.com...")
    all_backlinks = []
    offset = 0
    for page in range(5):  # get up to 100 backlinks
        res = await call_tool_safe("backlinks", {"domain": domain, "limit": 20, "offset": offset, "one_per_domain": True})
        if "backlinks" in res and res["backlinks"]:
            all_backlinks.extend(res["backlinks"])
            print(f"Fetched page {page+1}, total so far: {len(all_backlinks)}")
            offset = res.get("previousKey", offset + 20)  # Ubersuggest uses previousKey or standard pagination
            # if we didn't get 20 backlinks, we might be done
            if len(res["backlinks"]) < 20:
                break
        else:
            print("No backlinks key in response or empty.")
            break
        await asyncio.sleep(1)
        
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/backlinks_activeoahutours.json", "w") as f:
        json.dump(all_backlinks, f, indent=2)
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/backlinks_activeoahutours.json", "w") as f:
        json.dump(all_backlinks, f, indent=2)

    # 4. Backlinks for top competitors (limit 20 each to avoid limits)
    for comp in competitors[:3]:
        print(f"Fetching backlinks for competitor: {comp}...")
        c_backlinks = await call_tool_safe("backlinks", {"domain": comp, "limit": 20, "one_per_domain": True})
        with open(f"/home/ubuntu/work/active-oahu-static/site/_seo/raw/backlinks_{comp.replace('.', '_')}.json", "w") as f:
            json.dump(c_backlinks, f, indent=2)
        await asyncio.sleep(1)

    # 5. Backlink Opportunity
    print("Fetching backlink opportunity...")
    pos_targets = [{"target": c, "scope": "domain"} for c in competitors[:3]]
    neg_targets = [{"target": domain, "scope": "domain"}]
    opp_data = await call_tool_safe("backlink_opportunity", {
        "positive_targets": pos_targets,
        "negative_targets": neg_targets,
        "limit": 50
    })
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/backlink_opportunities.json", "w") as f:
        json.dump(opp_data, f, indent=2)
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/data/ubersuggest/backlink_opportunities.json", "w") as f:
        json.dump(opp_data, f, indent=2)

    print("Data collection complete.")

if __name__ == "__main__":
    asyncio.run(main())
