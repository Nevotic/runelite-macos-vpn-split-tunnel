# RuneLite macOS VPN Split Tunnel

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

## How to Run (Step-by-Step)

### Step 1: Save the Script
If you are not comfortable with Terminal commands like `git clone`, you can manually save the script using TextEdit:
1. Open the **TextEdit** app on your Mac.
2. In the top menu bar, click **Format** -> **Make Plain Text** (This is crucial; otherwise, Mac saves it as a formatted document which breaks the code).
3. Copy all the code from the `osrs_mac.py` file in this repository and paste it into the document.
4. Save the file to your **Desktop** and name it exactly: `osrs_mac.py`

### Step 2: Configure Your VPN
Ensure your VPN is connected and active. 
**Important:** Open your VPN settings and ensure any strict "Kill Switch" feature is turned **OFF**, as this will aggressively block the local network routing our script uses.

### Step 3: Run the Script
1. Press `Cmd + Space` on your keyboard to open Spotlight Search, type `Terminal`, and hit **Enter**.
2. Tell the Terminal to look at your Desktop folder by pasting this command and hitting **Enter**:
   `cd ~/Desktop`
3. Run the script using Python with administrator privileges:
   `sudo python3 osrs_mac.py`
   *(Note on Passwords: Because this script safely modifies your Mac's temporary network routing table, it requires your Mac login password. As you type your password, no characters or asterisks will appear on the screen. This is a normal macOS security feature. Just type your password blindly and press Enter.)*
4. Wait a few seconds for the script to fetch the IPs and apply the routes. Once it says "Success!", open the Jagex Launcher or RuneLite and play!

## Resetting the Routes
The routing rules created by this script are temporary and stored in your Mac's RAM. To clear the rules and revert everything back to normal, simply turn your Mac's Wi-Fi off and back on again, or reboot your computer. You will need to run the script again after a reboot if you want to play.

## Disclaimer
By routing Old School RuneScape traffic outside of your VPN, your real IP address will be visible to Jagex servers and your ISP. Use this script only if you are comfortable with this privacy trade-off.
