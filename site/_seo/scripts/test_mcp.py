import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

TOKEN = open('/tmp/ubs_token').read().strip()
URL = "https://ubersuggest-mcp.neilpatelapi.com/mcp"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

async def main():
    async with streamablehttp_client(URL, headers=HEADERS) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("All Available Tools:")
            for t in tools.tools:
                print(f"- {t.name}: {t.description}")
                # print schema only for tools that match our analysis needs
                if t.name in ["domain_overview", "domain_keywords", "domain_top_pages", "serp_analysis", "competitors"]:
                    print(f"  Input Schema: {json.dumps(t.inputSchema, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
