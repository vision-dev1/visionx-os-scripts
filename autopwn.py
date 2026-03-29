#!/usr/bin/env python3
import subprocess
import sys
import socket
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

R = Fore.RED + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
C = Fore.CYAN + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
DIM = Style.DIM
NC = Style.RESET_ALL

def banner():
    print(f"\n{R}{'='*46}")
    print(f"  VisionX OS - AutoPwn Engine")
    print(f"{'='*46}{NC}")

def section(title):
    print(f"\n{C}-- {title} --{NC}")

def found(msg):
    print(f"  {G}[+]{NC} {msg}")

def warn(msg):
    print(f"  {Y}[!]{NC} {msg}")

def info(msg):
    print(f"  {C}[~]{NC} {msg}")

def suggest(msg):
    print(f"  {G}[>]{NC} {msg}")

def error(msg):
    print(f"  {R}[x]{NC} {msg}")

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout.strip()
    except Exception:
        return ""

def detect_target_type(target):
    if target.startswith("http"):
        return "web"
    try:
        socket.inet_aton(target)
        return "ip"
    except socket.error:
        return "domain"

def run_recon(target):
    section("PHASE 1 - Reconnaissance")
    results = {}

    info("Resolving DNS...")
    dns = run_cmd(f"dig +short {target} @8.8.8.8")
    if dns:
        found(f"DNS: {dns.replace(chr(10), ', ')}")
        results['ips'] = dns.split('\n')
    else:
        warn("Could not resolve DNS")
        results['ips'] = []

    info("Checking subdomains...")
    subdomains = []
    for sub in ['www', 'mail', 'ftp', 'admin', 'dev', 'api']:
        ip = run_cmd(f"dig +short {sub}.{target} @8.8.8.8")
        if ip:
            subdomains.append(f"{sub}.{target}")
            found(f"Subdomain: {sub}.{target} -> {ip}")
    results['subdomains'] = subdomains

    suggest(f"Next: visionx scan {target}")
    return results

def run_scan(target):
    section("PHASE 2 - Port Scanning")
    results = {}

    info("Scanning top 100 ports...")
    nmap_out = run_cmd(f"nmap -T4 --top-ports 100 {target} 2>/dev/null")

    open_ports = []
    services = []

    for line in nmap_out.split('\n'):
        if '/tcp' in line and 'open' in line:
            parts = line.split()
            port = parts[0]
            service = parts[2] if len(parts) > 2 else 'unknown'
            open_ports.append(port)
            services.append((port, service))
            found(f"Open port: {port} ({service})")

    if not open_ports:
        warn("No open ports found")

    results['ports'] = open_ports
    results['services'] = services

    suggest(f"Next: visionx exploit suggest {target}")
    return results

def run_vuln_analysis(target, scan_results):
    section("PHASE 3 - Vulnerability Analysis")
    results = {}
    vulns = []

    services = scan_results.get('services', [])

    for port, service in services:
        info(f"Checking {service} on {port}...")
        port_num = port.split('/')[0]

        if port_num == '21':
            warn("FTP detected - check for anonymous login")
            suggest(f"hydra -l anonymous -p anonymous ftp://{target}")
        elif port_num == '22':
            warn("SSH detected - check for weak passwords")
            suggest(f"hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://{target}")
        elif port_num in ['80', '443']:
            warn("Web server detected")
            suggest(f"visionx web scan {target}")
        elif port_num == '3306':
            warn("MySQL detected - check default credentials")
            suggest(f"hydra -l root -P /usr/share/wordlists/rockyou.txt mysql://{target}")
        elif port_num == '445':
            warn("SMB detected - check for EternalBlue")
            suggest(f"visionx exploit run ms17-010 {target}")

        sploit = run_cmd(f"searchsploit {service} 2>/dev/null | head -3")
        if sploit:
            for line in sploit.split('\n')[:2]:
                if line.strip() and '---' not in line:
                    vulns.append(line.strip())
                    warn(f"Possible vuln: {line.strip()[:60]}")

    results['vulns'] = vulns
    return results

def run_exploit_suggestions(target, scan_results):
    section("PHASE 4 - Exploit Suggestions")
    services = scan_results.get('services', [])

    if not services:
        warn("No services found")
        return

    for port, service in services:
        suggest(f"msfconsole -x 'search {service}'")

    suggest(f"visionx exploit suggest {target}")

def autopwn(target):
    banner()
    print(f"\n  {W}Target: {C}{target}{NC}")
    print(f"  {W}Time:   {DIM}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{NC}")
    print(f"\n  {R}[!] Only test targets you own or have permission to test.{NC}\n")

    target_type = detect_target_type(target)
    info(f"Target type: {target_type}")

    recon_results = run_recon(target)
    scan_results = run_scan(target)
    vuln_results = run_vuln_analysis(target, scan_results)
    run_exploit_suggestions(target, scan_results)

    section("AUTOPWN SUMMARY")
    found(f"IPs found:   {len(recon_results.get('ips', []))}")
    found(f"Subdomains:  {len(recon_results.get('subdomains', []))}")
    found(f"Open ports:  {len(scan_results.get('ports', []))}")
    found(f"Vulns found: {len(vuln_results.get('vulns', []))}")
    print()
    suggest(f"visionx report {target}")
    suggest(f"visionx profile {target}")
    print(f"\n{G}{'='*46}{NC}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        error("Usage: autopwn.py <target>")
        sys.exit(1)
    autopwn(sys.argv[1])
