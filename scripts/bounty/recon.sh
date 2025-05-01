#!/bin/bash
# scripts/bounty/recon.sh

# Ensure the script exits on error
set -e

# Passive reconnaissance using Subfinder and Amass
echo "[*] Starting passive reconnaissance..."
subfinder -dL domains.txt -o subdomains.txt
amass enum -passive -df domains.txt -o amass_subdomains.txt

# Combine and deduplicate results
cat subdomains.txt amass_subdomains.txt | sort -u > all_subdomains.txt

echo "[*] Passive reconnaissance completed. Results saved to all_subdomains.txt"