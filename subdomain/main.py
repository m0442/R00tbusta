import argparse
import socket
import os
from dotenv import load_dotenv
from modules.crtsh import get_subdomains as crtsh_get_subdomains
from modules.securitytrails import get_subdomains as st_get_subdomains
from modules.alienvault import get_subdomains as av_get_subdomains
from modules.anubis import get_subdomains as anubis_get_subdomains
from modules.dnsdumpster import get_subdomains as dnsdumpster_get_subdomains
from modules.wayback import get_subdomains as wayback_get_subdomains
from utils import save_to_txt, save_to_json

# Load API keys from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
SECURITYTRAILS_API_KEY = os.getenv("SECURITYTRAILS_API_KEY")
DNSDUMPSTER_API_KEY = os.getenv("DNSDUMPSTER_API_KEY")

def is_resolvable(domain):
    """Check if the subdomain resolves to an IP address."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumerator (crt.sh + SecurityTrails + AlienVault + Anubis + DNSDumpster + Wayback)")
    parser.add_argument("domain", help="Target domain")
    parser.add_argument("-s", "--save", action="store_true", help="Save results to subdomains.txt")
    parser.add_argument("-c", "--check", action="store_true", help="Only show subdomains that resolve (DNS check)")
    parser.add_argument("-o", "--output", choices=["json"], help="Output format (json)")
    args = parser.parse_args()

    print(f"[*] Enumerating subdomains for: {args.domain}")

    all_sources = [
        ("crt.sh", crtsh_get_subdomains),
        ("SecurityTrails", lambda d: st_get_subdomains(d, SECURITYTRAILS_API_KEY) if SECURITYTRAILS_API_KEY else []),
        ("AlienVault", av_get_subdomains),
        ("Anubis", anubis_get_subdomains),
        ("DNSDumpster", dnsdumpster_get_subdomains),
        ("Wayback", wayback_get_subdomains),
    ]

    seen = set()
    unique_results = []
    source_stats = {}

    for name, func in all_sources:
        print(f"[*] Using source: {name}")
        try:
            subs = func(args.domain)
        except Exception as e:
            print(f"[!] Error in source {name}: {e}")
            subs = []

        print(f"[✓] {name} found {len(subs)} subdomains.")

        unique_this_source = []
        for sub in subs:
            if sub not in seen:
                unique_this_source.append(sub)
                seen.add(sub)
        unique_results.extend(unique_this_source)
        source_stats[name] = len(unique_this_source)

    print(f"[✓] Total combined unique subdomains: {len(unique_results)}")
    for source, count in source_stats.items():
        print(f"[✓] Unique to {source} (first seen): {count}")

    # DNS resolution
    results = []
    for sub in unique_results:
        if args.check and not is_resolvable(sub):
            continue
        ip = None
        try:
            ip = socket.gethostbyname(sub)
        except:
            pass
        results.append({"domain": sub, "ip": ip})

    if results:
        if args.output == "json":
            save_to_json(results, args.domain)
        else:
            print(f"[+] Final subdomain list ({len(results)}):")
            for entry in results:
                ip = entry['ip'] if entry['ip'] else "Unresolved"
                print(f" - {entry['domain']} ({ip})")
            if args.save:
                save_to_txt([entry['domain'] for entry in results], args.domain)
    else:
        print("[-] No valid subdomains found.")

if __name__ == "__main__":
    main()
