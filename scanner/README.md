# SmartShield_X_AI — Personal Firewall (Monitor-only)

**Project:** SmartShield_X_AI — Personal Firewall using Python (Monitor-only GUI)
**Developer:** Avinash Patwal

## Overview
SmartShield is a professional internship project that demonstrates packet-level monitoring and rule-based detection using Python and a modern dark-themed Tkinter GUI. This distribution is the **monitor-only** edition (safe) and does **not** alter system firewall rules.

## Files
- `SmartShield_X_AI.py` — main GUI application (monitor-only)
- `rules.json` — rule configuration (editable)
- `smartshield_monitor.log` — live log (created at runtime)
- `SmartShield_Report.md` — project report content (2 pages)
- `README.md` — this file

## Requirements
- Python 3.8+
- scapy (`sudo pip3 install scapy`) — required for live packet sniffing
- tkinter (usually included; on Debian/Ubuntu: `sudo apt install python3-tk`)

> Note: On many systems sniffing requires root privileges. To run live sniffing, execute with `sudo`:
> ```bash
> sudo python3 SmartShield_X_AI.py
> ```
> If scapy is not available or you run without root, the GUI will launch but live sniffing will be disabled.

## How to run
1. Place all files in a single folder.
2. Edit `rules.json` to add IPs/ports/protocols to flag.
3. Start the app:
```bash
sudo python3 SmartShield_X_AI.py
```
4. Click **Start Monitoring**. Live packets appear in the left panel; flagged items show in the event panel.

## Report
See `SmartShield_Report.md` for the 2-page polished report. To convert it to PDF, open in Google Docs or use a Markdown-to-PDF tool.

## Ethical Use
Use SmartShield only on systems and networks you own or are authorized to test. Monitor-only tools still capture network metadata — respect privacy and legal rules.
