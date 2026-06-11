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
    print("Suggesting locations for Japan...")
    try:
        locs = await call("location_suggest", {"query": "Japan"})
        print("Japan Location Suggestions:")
        print(json.dumps(locs, indent=2))
    except Exception as e:
        print(f"location_suggest failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
