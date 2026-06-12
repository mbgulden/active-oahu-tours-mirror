import asyncio
import json
import os
import sys
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TOKEN = open('/tmp/ubs_token').read().strip()
URL = "https://ubersuggest-mcp.neilpatelapi.com/mcp"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Ensure directories exist
os.makedirs("/home/ubuntu/work/active-oahu-static-1171/site/_seo/raw", exist_ok=True)

async def call_tool_safe(tool, args):
    print(f"Calling tool: {tool} with args: {args}")
    for attempt in range(3):
        try:
            async with streamablehttp_client(URL, headers=HEADERS) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(tool, args)
                    text = result.content[0].text if result.content else "{}"
                    # Some tools return text that might be JSON or error message
                    try:
                        data = json.loads(text)
                        return data
                    except json.JSONDecodeError:
                        print(f"Failed to parse JSON from response: {text[:200]}")
                        return {"raw_text": text}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {tool} with error: {e}")
            await asyncio.sleep(2)
    return {"error": "failed after 3 attempts"}

async def run_phase1_and_2_and_3():
    domains = [
        "activeoahutours.com",
        "kailuabeachadventures.com",
        "hawaiibeachtime.com"
    ]

    
    # 1. Domain Overviews
    overviews = {}
    for dom in domains:
        res = await call_tool_safe("domain_overview", {"domain": dom, "locId": 2840, "language": "en"})
        overviews[dom] = res
        await asyncio.sleep(1)
    
    with open("/home/ubuntu/work/active-oahu-static-1171/site/_seo/raw/domain_overviews.json", "w") as f:
        json.dump(overviews, f, indent=2)
    print("Saved domain overviews.")

    # 2. Domain Keywords (limit 100)
    keywords = {}
    for dom in domains:
        res = await call_tool_safe("domain_keywords", {"domain": dom, "locId": 2840, "language": "en", "limit": 100})
        keywords[dom] = res
        await asyncio.sleep(1)
        
    with open("/home/ubuntu/work/active-oahu-static-1171/site/_seo/raw/domain_keywords.json", "w") as f:
        json.dump(keywords, f, indent=2)
    print("Saved domain keywords.")

    # 3. Top Pages Analysis (limit 20)
    # Only need top pages for competitors
    top_pages = {}
    for dom in domains[1:]:
        res = await call_tool_safe("domain_top_pages", {"domain": dom, "locId": 2840, "language": "en", "limit": 20})
        top_pages[dom] = res
        await asyncio.sleep(1)
        
    with open("/home/ubuntu/work/active-oahu-static-1171/site/_seo/raw/top_pages.json", "w") as f:
        json.dump(top_pages, f, indent=2)
    print("Saved top pages.")

if __name__ == "__main__":
    asyncio.run(run_phase1_and_2_and_3())
