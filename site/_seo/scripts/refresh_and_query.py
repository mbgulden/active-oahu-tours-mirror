import json
import urllib.request
import urllib.parse
import urllib.error

def main():
    # Load credentials
    try:
        creds = json.load(open('/home/ubuntu/.jules/cache/oauth_creds.json'))
        refresh_token = creds.get('refresh_token')
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return

    # Load client keys
    try:
        keys = json.load(open('/home/ubuntu/.config/mcp-gdrive/gcp-oauth.keys.json'))
        client_id = keys['installed']['client_id']
        client_secret = keys['installed']['client_secret']
    except Exception as e:
        print(f"Error loading client keys: {e}")
        return

    # Refresh token request
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            access_token = res_data.get('access_token')
            print("Successfully refreshed access token!")
            
            # Now let's try to query Google Search Console
            gsc_url = "https://www.googleapis.com/webmasters/v3/sites/sc-domain:activeoahutours.com/searchAnalytics/query"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            body = {
                "startDate": "2026-05-11",
                "endDate": "2026-06-11",
                "dimensions": ["query", "page"],
                "rowLimit": 100
            }
            gsc_payload = json.dumps(body).encode("utf-8")
            gsc_req = urllib.request.Request(gsc_url, data=gsc_payload, headers=headers, method="POST")
            
            with urllib.request.urlopen(gsc_req) as gsc_res:
                gsc_data = json.loads(gsc_res.read().decode("utf-8"))
                print("GSC Query Success!")
                print(f"Rows returned: {len(gsc_data.get('rows', []))}")
                
                # Save the results
                with open("/home/ubuntu/work/active-oahu-static/site/_seo/raw/gsc_en_search_analytics.json", "w") as f:
                    json.dump(gsc_data, f, indent=2)
                    print("Saved to site/_seo/raw/gsc_en_search_analytics.json")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
