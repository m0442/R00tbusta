import os
import json

def save_to_txt(subdomains, domain):
    os.makedirs("../output", exist_ok=True)
    filepath = f"../output/subdomains.txt"
    with open(filepath, "w") as f:
        for sub in subdomains:
            f.write(sub + "\n")
    print(f"[+] Results saved to {filepath}")

def save_to_json(subdomains, domain):
    # Only keep subdomains with valid IPs
    resolvable = [entry for entry in subdomains if entry.get("ip")]
    os.makedirs("../output", exist_ok=True)
    filepath = "../output/subdomains.json"
    with open(filepath, "w") as f:
        json.dump(resolvable, f, indent=2)
    print(f"[+] JSON results saved to {filepath}")