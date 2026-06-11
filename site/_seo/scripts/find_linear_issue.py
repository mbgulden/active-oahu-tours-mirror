import os
import json
import urllib.request

api_key = os.environ.get("LINEAR_API_KEY")
if not api_key:
    print("Error: LINEAR_API_KEY environment variable is not set")
    exit(1)

url = "https://api.linear.app/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": api_key
}

# Query issue by its team key and number (e.g. "GRO-1181")
query = """
query Issue($id: String!) {
  issue(id: $id) {
    id
    title
    description
    state {
      id
      name
    }
    labels {
      nodes {
        id
        name
      }
    }
  }
}
"""
variables = {
    "id": "GRO-1181"
}
payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")

req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        print(json.dumps(res_data, indent=2))
except Exception as e:
    print(f"Error calling Linear API: {e}")
