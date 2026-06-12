import urllib.request
import json

# Load Google credentials dynamically
import json
with open("/home/ubuntu/.google_oauth_creds.json") as f_creds:
    creds_data = json.load(f_creds)
client_id = creds_data["client_id"]
client_secret = creds_data["client_secret"]
refresh_token = creds_data["refresh_token"]

def refresh_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8")).get("access_token")

def test_metrics(access_token):
    property_id = "289642224"
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    
    # Let's test different metrics
    body = {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [
            {"name": "sessions"},
            {"name": "bounceRate"},
            {"name": "averageSessionDuration"},
            {"name": "conversions"}
        ],
        "limit": 2
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print("Success!")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, "read"):
            print(e.read().decode("utf-8"))

if __name__ == "__main__":
    token = refresh_access_token()
    test_metrics(token)
