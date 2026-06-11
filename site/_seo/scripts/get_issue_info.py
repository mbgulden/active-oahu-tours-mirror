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

def query_linear(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data
    except Exception as e:
        print(f"Error querying Linear: {e}")
        return None

if __name__ == "__main__":
    query = """
    query GetIssue($id: String!) {
      issue(id: $id) {
        id
        identifier
        title
        description
        state {
          id
          name
        }
        assignee {
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
    variables = {"id": "GRO-1171"}
    res = query_linear(query, variables)
    print(json.dumps(res, indent=2))
