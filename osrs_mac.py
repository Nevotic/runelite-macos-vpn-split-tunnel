```python
#!/usr/bin/env python3
"""
OSRS Mac VPN Bypass Script
Dynamically routes Old School RuneScape and Jagex Launcher traffic
outside of active VPN connections on macOS via static routing.
"""

import socket
import subprocess
import concurrent.futures

# Essential domains for the Jagex Launcher and RuneLite
AUTH_DOMAINS = [
    "auth.jagex.com",
    "account.jagex.com",
    "api.jagex.com",
    "launcher.runescape.com",
    "secure.runescape.com",
    "api.runelite.net",
    "repo.runelite.net"
]

def get_physical_gateway():
    """
    Scans common macOS physical network interfaces to find the 
    active local router IP (gateway) bypassing the VPN tunnel.
    """
    for interface in ["en0", "en1", "en2", "en3"]:
        try:
            result = subprocess.run(
                ["ipconfig", "getoption", interface, "router"], 
                capture_output=True, text=True, check=True
            )
            gw = result.stdout.strip()
            if gw:
                return gw, interface
        except Exception:
            continue
    return None, None

def resolve_domain(domain):
    """Returns the IP address for a given domain, or None if it fails."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def resolve_world(world_index):
    """Constructs the OSRS world subdomain and resolves its IP."""
    hostname = f"oldschool{world_index}.runescape.com"
    return resolve_domain(hostname)

def fetch_all_ips():
    """
    Uses multithreading to rapidly resolve all required Jagex/RuneLite 
    domains and all possible active OSRS game worlds.
    """
    print("Resolving Jagex Auth servers and Game Worlds...")
    ips = set()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Resolve Authentication & Web Domains
        auth_results = executor.map(resolve_domain, AUTH_DOMAINS)
        
        # Resolve Game Worlds (Assuming max ~300 worlds)
        world_results = executor.map(resolve_world, range(1, 301))
        
    for ip in auth_results:
        if ip: 
            ips.add(ip)
        
    for ip in world_results:
        if ip: 
            ips.add(ip)
            
    return sorted(list(ips))

def main():
    print("=== OSRS Mac VPN Bypass ===")
    
    gateway, interface = get_physical_gateway()
    if not gateway:
        print("Error: Could not detect your local physical router.")
        print("Please ensure your Wi-Fi or Ethernet is connected.")
        return
        
    print(f"Detected local gateway: {gateway} on interface: {interface}")
    
    ips = fetch_all_ips()
    print(f"Successfully discovered {len(ips)} active Jagex/RuneLite IPs.")

    if not ips:
        print("No IPs found. Your network might be blocking DNS requests.")
        return

    print(f"\nRouting Launcher, RuneLite, and Game traffic directly through {gateway}...")

    added = 0
    for ip in ips:
        # Applies static route targeting the physical gateway
        cmd = ["sudo", "route", "-n", "add", "-host", ip, gateway]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            added += 1
        except subprocess.CalledProcessError:
            # Silently pass if the route already exists in the table
            pass

    print(f"\nSuccess! Applied {added} static routing rules.")
    print("You can now launch OSRS while your VPN remains active.")

if __name__ == "__main__":
    main()