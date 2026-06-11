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
            target_tools = [
                "backlinks_overview",
                "backlinks",
                "anchor_texts",
                "linking_domains",
                "backlink_opportunity",
                "competitors",
                "domain_overview"
            ]
            for t in tools.tools:
                if t.name in target_tools:
                    print(f"Tool: {t.name}")
                    print(json.dumps(t.inputSchema, indent=2))
                    print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
