import os
import json
import urllib.request
import sys

api_key = os.environ.get("LINEAR_API_KEY")
if not api_key:
    print("Error: LINEAR_API_KEY environment variable is not set")
    exit(1)

issue_id = "759cf866-f18e-49ba-8046-776346e1c651"
url = "https://api.linear.app/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": api_key
}

def post_comment(body):
    query = """
    mutation CommentCreate($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
        comment {
          id
        }
      }
    }
    """
    variables = {
        "issueId": issue_id,
        "body": body
    }
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if res_data.get("errors"):
                print("API returned errors:")
                print(json.dumps(res_data["errors"], indent=2))
                return False
            print("Comment posted successfully:")
            print(json.dumps(res_data, indent=2))
            return True
    except Exception as e:
        print(f"Error posting comment: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 post_comment_gro1246.py <comment_text_or_file_path>")
        exit(1)
        
    path = sys.argv[1]
    if os.path.exists(path):
        with open(path, 'r') as f:
            body = f.read()
    else:
        body = path
        
    post_comment(body)
