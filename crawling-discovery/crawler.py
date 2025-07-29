#!/usr/bin/env python3
"""
Domain Crawling Automation Script
Automates crawling for a given domain using multiple tools:
- waymore
- waybackurls
- gau
- katana (3 modes: depth-first, breadth-first, headless)
"""

import os
import sys
import subprocess
import threading
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import shutil

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colored(message: str, color: str = Colors.ENDC, bold: bool = False):
    """Print colored output to terminal"""
    if bold:
        message = Colors.BOLD + message
    print(f"{color}{message}{Colors.ENDC}")

def check_tool_availability(tool_name: str) -> bool:
    """Check if a tool is available in PATH"""
    return shutil.which(tool_name) is not None

def run_command(command: List[str], output_file: Optional[str] = None, timeout: int = 3600) -> bool:
    """Run a command and optionally save output to file"""
    try:
        print_colored(f"Running: {' '.join(command)}", Colors.OKBLUE)
        
        if output_file:
            with open(output_file, 'w') as f:
                result = subprocess.run(
                    command,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=timeout
                )
        else:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
        
        if result.returncode == 0:
            print_colored(f"✓ Command completed successfully", Colors.OKGREEN)
            return True
        else:
            print_colored(f"✗ Command failed with return code {result.returncode}", Colors.FAIL)
            if result.stderr:
                print_colored(f"Error: {result.stderr}", Colors.FAIL)
            return False
            
    except subprocess.TimeoutExpired:
        print_colored(f"✗ Command timed out after {timeout} seconds", Colors.WARNING)
        return False
    except FileNotFoundError:
        print_colored(f"✗ Command not found: {command[0]}", Colors.FAIL)
        return False
    except Exception as e:
        print_colored(f"✗ Unexpected error: {str(e)}", Colors.FAIL)
        return False

def run_waymore(domain: str, output_dir: str) -> bool:
    """Run waymore tool"""
    output_file = os.path.join(output_dir, "waymore_output.txt")
    command = ["waymore", "-i", domain, "-mode", "U", "-oU"]
    return run_command(command, output_file)

def run_waybackurls(domain: str, output_dir: str) -> bool:
    """Run waybackurls tool"""
    subdomains_file = os.path.join(output_dir, "subdomains.txt")
    output_file = os.path.join(output_dir, "waybackurls_output.txt")
    
    # First check if subdomains.txt exists
    if not os.path.exists(subdomains_file):
        print_colored(f"Warning: {subdomains_file} not found, creating empty file", Colors.WARNING)
        with open(subdomains_file, 'w') as f:
            f.write(f"{domain}\n")
    
    # Run waybackurls
    command = ["cat", subdomains_file, "|", "waybackurls"]
    return run_command(command, output_file)

def run_gau(domain: str, output_dir: str) -> bool:
    """Run gau tool"""
    subdomains_file = os.path.join(output_dir, "subdomains.txt")
    output_file = os.path.join(output_dir, "gau_output.txt")
    
    # First check if subdomains.txt exists
    if not os.path.exists(subdomains_file):
        print_colored(f"Warning: {subdomains_file} not found, creating empty file", Colors.WARNING)
        with open(subdomains_file, 'w') as f:
            f.write(f"{domain}\n")
    
    # Run gau
    command = ["cat", subdomains_file, "|", "gau"]
    return run_command(command, output_file)

def run_katana(domain: str, output_dir: str, mode: str) -> bool:
    """Run katana tool in specified mode"""
    output_file = os.path.join(output_dir, f"katana_{mode}.txt")
    
    if mode == "depth-first":
        command = ["katana", "-d", "5", "-jc", "-ct", "1h", "-aff", "-fx", "-s", "depth-first", "-o", output_file]
    elif mode == "breadth-first":
        command = ["katana", "-d", "5", "-jc", "-ct", "1h", "-aff", "-fx", "-s", "breadth-first", "-o", output_file]
    elif mode == "headless":
        command = ["katana", "-d", "5", "-jc", "-ct", "1h", "-aff", "-fx", "-headless", "-o", output_file]
    else:
        print_colored(f"Invalid katana mode: {mode}", Colors.FAIL)
        return False
    
    return run_command(command)

def run_katana_threaded(domain: str, output_dir: str) -> List[bool]:
    """Run katana in all three modes using threading"""
    modes = ["depth-first", "breadth-first", "headless"]
    results = [False] * len(modes)
    threads = []
    
    def run_katana_mode(mode: str, index: int):
        print_colored(f"Starting katana in {mode} mode...", Colors.OKCYAN)
        results[index] = run_katana(domain, output_dir, mode)
    
    # Start threads for each mode
    for i, mode in enumerate(modes):
        thread = threading.Thread(target=run_katana_mode, args=(mode, i))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return results

def check_required_tools() -> bool:
    """Check if all required tools are available"""
    tools = ["waymore", "waybackurls", "gau", "katana"]
    missing_tools = []
    
    print_colored("Checking tool availability...", Colors.HEADER)
    
    for tool in tools:
        if check_tool_availability(tool):
            print_colored(f"✓ {tool} is available", Colors.OKGREEN)
        else:
            print_colored(f"✗ {tool} is not available", Colors.FAIL)
            missing_tools.append(tool)
    
    if missing_tools:
        print_colored(f"\nMissing tools: {', '.join(missing_tools)}", Colors.WARNING)
        print_colored("Please install the missing tools before running this script.", Colors.WARNING)
        return False
    
    return True

def create_output_directory(domain: str) -> str:
    """Create output directory for the domain"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"crawl_results_{domain}_{timestamp}"
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        print_colored(f"Created output directory: {output_dir}", Colors.OKGREEN)
        return output_dir
    except Exception as e:
        print_colored(f"Failed to create output directory: {str(e)}", Colors.FAIL)
        sys.exit(1)

def read_domains_from_file(file_path: str) -> List[str]:
    """Read domains from a file"""
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        return domains
    except Exception as e:
        print_colored(f"Failed to read domains from file: {str(e)}", Colors.FAIL)
        return []

def crawl_domain(domain: str) -> bool:
    """Perform crawling for a single domain"""
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f"Starting crawl for domain: {domain}", Colors.HEADER)
    print_colored(f"{'='*60}", Colors.HEADER)
    
    # Create output directory
    output_dir = create_output_directory(domain)
    
    # Track success/failure
    success_count = 0
    total_tools = 5  # waymore, waybackurls, gau, katana (3 modes)
    
    # Run waymore
    print_colored("\n1. Running waymore...", Colors.OKCYAN)
    if run_waymore(domain, output_dir):
        success_count += 1
    
    # Run waybackurls
    print_colored("\n2. Running waybackurls...", Colors.OKCYAN)
    if run_waybackurls(domain, output_dir):
        success_count += 1
    
    # Run gau
    print_colored("\n3. Running gau...", Colors.OKCYAN)
    if run_gau(domain, output_dir):
        success_count += 1
    
    # Run katana in all modes (threaded)
    print_colored("\n4. Running katana in all modes (threaded)...", Colors.OKCYAN)
    katana_results = run_katana_threaded(domain, output_dir)
    success_count += sum(katana_results)
    
    # Summary
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f"Crawl completed for {domain}", Colors.HEADER)
    print_colored(f"Success: {success_count}/{total_tools} tools completed successfully", Colors.OKGREEN)
    print_colored(f"Output directory: {output_dir}", Colors.OKBLUE)
    print_colored(f"{'='*60}", Colors.HEADER)
    
    return success_count == total_tools

def main():
    parser = argparse.ArgumentParser(
        description="Automated domain crawling using multiple tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python crawler.py example.com
  python crawler.py -f domains.txt
  python crawler.py --check-tools
        """
    )
    
    parser.add_argument("domain", nargs="?", help="Domain to crawl")
    parser.add_argument("-f", "--file", help="File containing list of domains")
    parser.add_argument("--check-tools", action="store_true", help="Check if required tools are available")
    
    args = parser.parse_args()
    
    # Check tools if requested
    if args.check_tools:
        if check_required_tools():
            print_colored("\nAll tools are available! Ready to crawl.", Colors.OKGREEN)
        else:
            print_colored("\nSome tools are missing. Please install them first.", Colors.FAIL)
        return
    
    # Validate input
    if not args.domain and not args.file:
        print_colored("Error: Please provide either a domain or a file with domains", Colors.FAIL)
        parser.print_help()
        sys.exit(1)
    
    # Check if tools are available
    if not check_required_tools():
        print_colored("\nSome required tools are missing. Use --check-tools to see what's needed.", Colors.FAIL)
        sys.exit(1)
    
    # Get domains to process
    domains = []
    if args.file:
        domains = read_domains_from_file(args.file)
        if not domains:
            print_colored("No domains found in file or file is empty", Colors.FAIL)
            sys.exit(1)
    else:
        domains = [args.domain]
    
    # Process each domain
    total_domains = len(domains)
    successful_crawls = 0
    
    print_colored(f"\nStarting crawl for {total_domains} domain(s)...", Colors.HEADER)
    
    for i, domain in enumerate(domains, 1):
        print_colored(f"\nProcessing domain {i}/{total_domains}: {domain}", Colors.OKBLUE)
        
        if crawl_domain(domain):
            successful_crawls += 1
        
        # Add delay between domains to avoid overwhelming the system
        if i < total_domains:
            print_colored("Waiting 5 seconds before next domain...", Colors.WARNING)
            time.sleep(5)
    
    # Final summary
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored("CRAWL SUMMARY", Colors.HEADER)
    print_colored(f"{'='*60}", Colors.HEADER)
    print_colored(f"Total domains processed: {total_domains}", Colors.OKBLUE)
    print_colored(f"Successful crawls: {successful_crawls}", Colors.OKGREEN)
    print_colored(f"Failed crawls: {total_domains - successful_crawls}", Colors.FAIL)
    print_colored(f"{'='*60}", Colors.HEADER)

if __name__ == "__main__":
    main()
