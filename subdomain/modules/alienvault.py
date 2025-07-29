import requests

def get_subdomains(domain):
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            print(f"[!] AlienVault OTX returned status code {response.status_code}")
            return []

        data = response.json()
        subdomains = set()
        for record in data.get("passive_dns", []):
            hostname = record.get("hostname")
            if hostname and hostname.endswith(domain) and not hostname.startswith("*."):
                subdomains.add(hostname.strip())

        return sorted(subdomains)

    except Exception as e:
        print(f"[!] Error fetching from AlienVault OTX: {e}")
        return []
