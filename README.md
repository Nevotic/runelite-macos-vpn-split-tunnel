# OSRS Mac VPN Bypass

This Python script allows macOS users to seamlessly play Old School RuneScape (via RuneLite or the Jagex Launcher) while keeping a commercial VPN (like ProtonVPN, NordVPN, etc.) fully active. 

It solves the common issue where Cloudflare blocks known VPN IP addresses, preventing the Jagex Launcher from authenticating or the game client from connecting to a world.

## How It Works
macOS does not natively support IP-based split tunneling for VPNs. This script acts as a workaround by interacting directly with the macOS routing table. 
1. It dynamically detects your physical local network gateway (your Wi-Fi or Ethernet router).
2. It uses multithreaded DNS resolution to fetch the IPs of Jagex Authentication servers, RuneLite APIs, and all 300+ active OSRS game worlds.
3. It forces macOS to route traffic for those specific Jagex IPs through your physical router, completely bypassing the VPN tunnel.

Your game connects directly via your ISP, while the rest of your Mac's internet traffic remains safely encrypted inside the VPN.

## Features
- **Zero Dependencies:** Uses only Python's built-in standard libraries. No need for `pip install`.
- **Lightning Fast:** Uses `concurrent.futures` to sweep ~300 Jagex subdomains in seconds.
- **Set and Forget:** Run it once while your VPN is active, and you can freely world-hop or restart the client without toggling your VPN on and off.

## Requirements
- macOS
- Python 3.x
- Administrator (`sudo`) privileges (required to modify the macOS routing table)

## Usage
1. Ensure your VPN is **connected and active** (and disable any strict "Kill Switch" features that block local network routing).
2. Open your Terminal.
3. Clone the repository or download the script:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/osrs-mac-vpn-bypass.git](https://github.com/YOUR_USERNAME/osrs-mac-vpn-bypass.git)
   cd osrs-mac-vpn-bypass
