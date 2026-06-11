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
    queries = ["Kawela Bay", "Kawela Bay kayak", "Kawela Bay snorkeling"]
    results = {}
    for q in queries:
        print(f"Querying: {q}")
        try:
            res = await call("keyword_overview", {"keyword": q, "locId": 2840, "language": "en"})
            results[q] = res
        except Exception as e:
            results[q] = {"error": str(e)}
        await asyncio.sleep(1.5)
        
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
