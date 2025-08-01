import requests

def get_subdomains(domain):
    url = f"https://anubisdb.com/anubis/subdomains/{domain}"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            print(f"[!] Anubis returned status code {response.status_code}")
            return []

        data = response.json()
        subdomains = [sub.strip() for sub in data if sub.endswith(domain) and not sub.startswith("*.")]
        return sorted(set(subdomains))

    except Exception as e:
        print(f"[!] Error fetching from Anubis: {e}")
        return []
