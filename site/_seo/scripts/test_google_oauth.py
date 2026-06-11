import urllib.request
import json
import os

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
    try:
        with urllib.request.urlopen(req) as resp:
            tokens = json.loads(resp.read().decode("utf-8"))
            return tokens.get("access_token")
    except Exception as e:
        print(f"Error refreshing access token: {e}")
        return None

def test_ga4(access_token):
    property_id = "289642224"
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"
    
    # Test request body for last 30 days page sessions
    body = {
        "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "pagePath"}],
        "metrics": [{"name": "sessions"}],
        "limit": 5
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
            print("GA4 API Test Success!")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error calling GA4 API: {e}")
        if hasattr(e, "read"):
            print(e.read().decode("utf-8"))

if __name__ == "__main__":
    access_token = refresh_access_token()
    if access_token:
        print(f"Refreshed Access Token: {access_token[:15]}...")
        test_ga4(access_token)
    else:
        print("Failed to get access token.")
