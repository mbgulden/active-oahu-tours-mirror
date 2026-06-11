import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TOKEN = open('/tmp/ubs_token').read().strip()
URL = "https://ubersuggest-mcp.neilpatelapi.com/mcp"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

async def call(tool, args):
    async with streamablehttp_client(URL, headers=HEADERS) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool, args)
            text = result.content[0].text if result.content else "{}"
            return json.loads(text)

async def main():
    print("Testing keyword_overview...")
    try:
        res = await call("keyword_overview", {"keyword": "kayak rental", "locId": 2840, "language": "en"})
        print("keyword_overview response:")
        print(json.dumps(res, indent=2)[:500])
    except Exception as e:
        print(f"keyword_overview failed: {e}")

    print("\nTesting serp_analysis...")
    try:
        res = await call("serp_analysis", {"keyword": "kayak rental", "locId": 2840, "language": "en", "limit": 5})
        print("serp_analysis response:")
        print(json.dumps(res, indent=2)[:500])
    except Exception as e:
        print(f"serp_analysis failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
