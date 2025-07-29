import argparse
import socket
import os
from dotenv import load_dotenv
from modules.crtsh import get_subdomains as crtsh_get_subdomains
from modules.securitytrails import get_subdomains as st_get_subdomains
from modules.alienvault import get_subdomains as av_get_subdomains
from utils import save_to_txt, save_to_json

# Load API keys from .env
load_dotenv()
SECURITYTRAILS_API_KEY = os.getenv("SECURITYTRAILS_API_KEY")

def is_resolvable(domain):
    """Check if the subdomain resolves to an IP address."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumerator (crt.sh + SecurityTrails + AlienVault)")
    parser.add_argument("domain", help="Target domain")
    parser.add_argument("-s", "--save", action="store_true", help="Save results to subdomains.txt")
    parser.add_argument("-c", "--check", action="store_true", help="Only show subdomains that resolve (DNS check)")
    parser.add_argument("-o", "--output", choices=["json"], help="Output format (json)")
    args = parser.parse_args()

    print(f"[*] Enumerating subdomains for: {args.domain}")

    # -------- Source 1: crt.sh --------
    print("[*] Using source: crt.sh")
    subs_crtsh = []
    try:
        subs_crtsh = crtsh_get_subdomains(args.domain)
    except Exception as e:
        print(f"[!] Error in source crt.sh: {e}")
    print(f"[✓] crt.sh found {len(subs_crtsh)} subdomains.")

    # -------- Source 2: SecurityTrails --------
    print("[*] Using source: SecurityTrails")
    subs_st = []
    if SECURITYTRAILS_API_KEY:
        try:
            subs_st = st_get_subdomains(args.domain, SECURITYTRAILS_API_KEY)
        except Exception as e:
            print(f"[!] Error in source SecurityTrails: {e}")
        print(f"[✓] SecurityTrails found {len(subs_st)} subdomains.")
    else:
        print("[!] SECURITYTRAILS_API_KEY not found. Skipping SecurityTrails.")

    # -------- Source 3: AlienVault OTX --------
    print("[*] Using source: AlienVault OTX")
    subs_av = []
    try:
        subs_av = av_get_subdomains(args.domain)
    except Exception as e:
        print(f"[!] Error in source AlienVault OTX: {e}")
    print(f"[✓] AlienVault OTX found {len(subs_av)} subdomains.")

    # -------- First-seen attribution per source --------
    seen = set()
    unique_crtsh = []
    unique_st = []
    unique_av = []

    for sub in subs_crtsh:
        if sub not in seen:
            unique_crtsh.append(sub)
            seen.add(sub)

    for sub in subs_st:
        if sub not in seen:
            unique_st.append(sub)
            seen.add(sub)

    for sub in subs_av:
        if sub not in seen:
            unique_av.append(sub)
            seen.add(sub)

    union_subdomains = unique_crtsh + unique_st + unique_av

    print(f"[✓] Total combined unique subdomains: {len(union_subdomains)}")
    print(f"[✓] Unique to crt.sh (first seen): {len(unique_crtsh)}")
    print(f"[✓] Unique to SecurityTrails (first seen): {len(unique_st)}")
    print(f"[✓] Unique to AlienVault (first seen): {len(unique_av)}")

    # -------- DNS resolution (IP address collection) --------
    results = []
    for sub in union_subdomains:
        if args.check:
            if not is_resolvable(sub):
                continue
        ip = None
        try:
            ip = socket.gethostbyname(sub)
        except:
            pass
        results.append({"domain": sub, "ip": ip})

    # -------- Output handling --------
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