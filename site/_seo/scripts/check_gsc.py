import json
import urllib.request
import urllib.error

def query_gsc():
    try:
        creds = json.load(open('/home/ubuntu/.jules/cache/oauth_creds.json'))
        access_token = creds.get('access_token')
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return

    url = "https://www.googleapis.com/webmasters/v3/sites/sc-domain:activeoahutours.com/searchAnalytics/query"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Let's request top queries and pages for the last 30 days
    body = {
        "startDate": "2026-05-11",
        "endDate": "2026-06-11",
        "dimensions": ["query", "page"],
        "rowLimit": 100
    }
    
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            print("GSC Query Success!")
            print(json.dumps(res_data, indent=2)[:1000])
            # Save the results
            with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/gsc_en_search_analytics.json", "w") as f:
                json.dump(res_data, f, indent=2)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"Other Error calling GSC API: {e}")

if __name__ == "__main__":
    query_gsc()
