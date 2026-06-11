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
os.makedirs("/home/ubuntu/work/active-oahu-static/site/_seo/raw", exist_ok=True)

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
                        data = json.loads(text)
                        return data
                    except json.JSONDecodeError:
                        print(f"Failed to parse JSON from response: {text[:200]}")
                        return {"raw_text": text}
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {tool} with error: {e}")
            await asyncio.sleep(2)
    return {"error": "failed after 3 attempts"}

async def main():
    keywords = [
        "kayak rental",
        "kayak tour",
        "paddleboard rental",
        "Oahu beach gear",
        "Lanikai kayak",
        "Kailua kayak",
        "Mokulua kayak",
        "Chinaman's Hat kayak",
        "Kaneohe Sandbar kayak",
        "Oahu kayak rental"
    ]
    
    serp_data = {}
    for kw in keywords:
        res = await call_tool_safe("serp_analysis", {"keyword": kw, "locId": 2840, "language": "en", "limit": 10})
        serp_data[kw] = res
        await asyncio.sleep(1.5)
        
    with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/serp_analyses.json", "w") as f:
        json.dump(serp_data, f, indent=2)
    print("Saved SERP analyses.")

if __name__ == "__main__":
    asyncio.run(main())
