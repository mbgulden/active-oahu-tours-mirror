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
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"raw_text": text}

async def main():
    path = "/home/ubuntu/work/active-oahu-static-1171/site/_seo/raw/domain_overviews.json"
    with open(path) as f:
        data = json.load(f)

    patched = False
    for dom in ["hawaiibeachtime.com", "hawaiiactivities.com"]:
        # If it's not present or it has an error/403, we fetch it
        info = data.get(dom, {})
        if "raw_text" in info or "error" in info or not info:
            print(f"Fetching domain_overview for {dom}...")
            res = await call("domain_overview", {"domain": dom, "locId": 2840, "language": "en"})
            if "raw_text" in res and "limit" in res["raw_text"]:
                print(f"Failed to fetch {dom}: {res['raw_text']}")
            else:
                data[dom] = res
                patched = True
                print(f"Successfully fetched {dom}!")
            await asyncio.sleep(1)

    if patched:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print("Updated domain_overviews.json with patched data.")
    else:
        print("No updates made.")

if __name__ == "__main__":
    asyncio.run(main())
