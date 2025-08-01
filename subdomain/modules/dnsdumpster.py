import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("DNSDUMPSTER_API_KEY")

def get_subdomains(domain):
    if not API_KEY:
        print("[!] DNSDUMPSTER_API_KEY not found in .env file")
        return []

    url = f"https://api.dnsdumpster.com/domain/{domain}"
    headers = {"X-API-Key": API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"[!] DNSDumpster API returned status code {response.status_code}")
            return []

        data = response.json()
        subdomains = set()

        for section in ["a", "cname", "mx", "ns"]:
            for entry in data.get(section, []):
                host = entry.get("host")
                if host and host.endswith(domain) and not host.startswith("*."):
                    subdomains.add(host.strip())

        return sorted(subdomains)

    except Exception as e:
        print(f"[!] Error fetching from DNSDumpster API: {e}")
        return []