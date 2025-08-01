import requests
import re
import os

def get_subdomains(domain):
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}&output=json&fl=original"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            print(f"[!] Wayback Machine returned status code {response.status_code}")
            return []

        data = response.json()
        if not data or len(data) < 2:
            return []

        raw_urls = [row[0] for row in data[1:]]
        subdomains = set()

        for url in raw_urls:
            # Remove protocol if exists
            url = re.sub(r"^https?://", "", url)
            parts = url.split("/")[0].strip()
            if parts.endswith(domain) and not parts.startswith("*."):
                subdomains.add(parts)

        return sorted(subdomains)

    except Exception as e:
        print(f"[!] Error fetching from Wayback Machine: {e}")
        return []