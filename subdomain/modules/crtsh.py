# modules/crtsh.py
import requests

def get_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=200)

        if response.status_code != 200:
            print(f"[!] crt.sh returned status code {response.status_code}")
            return []

        try:
            data = response.json()
        except ValueError:
            print("[!] crt.sh response is not valid JSON. Content preview:")
            print(response.text[:300])
            return []

        subdomains = set()
        for cert in data:
            name = cert.get("name_value")
            if not name:
                continue
            for entry in name.split("\n"):
                entry = entry.strip()
                if entry.endswith(domain) and not entry.startswith("*."):
                    subdomains.add(entry)

        return sorted(subdomains)

    except Exception as e:
        print(f"[!] Error fetching from crt.sh: {e}")
        return []
