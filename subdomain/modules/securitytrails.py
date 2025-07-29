import requests

def get_subdomains(domain, api_key):
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {
        "Accept": "application/json",
        "APIKEY": api_key
    }

    try:
        response = requests.get(url, headers=headers, timeout=100)
        if response.status_code != 200:
            print(f"[!] SecurityTrails API error: {response.status_code} - {response.text}")
            return []

        data = response.json()
        subdomains = data.get("subdomains", [])
        return [f"{sub}.{domain}" for sub in subdomains if not sub.startswith("*")]

    except Exception as e:
        print(f"[!] Error fetching from SecurityTrails: {e}")
        return []
