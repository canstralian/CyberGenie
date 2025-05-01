#!/bin/bash
# =====================================================================
#  CyberGenie | Bug Bounty Automation Script
#  Filename : recon.sh
#  Purpose  : Passive Reconnaissance
#  Author   : canstralian
#  License  : Apache 2.0
# =====================================================================

set -euo pipefail

CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "============================================"
echo "      CyberGenie | Bug Bounty Script"
echo "      -> recon.sh"
echo "      -> Started at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"
echo -e "${NC}"

# Input and output
INPUT_FILE="domains.txt"
OUTPUT_DIR="results/recon"
mkdir -p "$OUTPUT_DIR"

# Subfinder
echo "[*] Running subfinder..."
subfinder -dL "$INPUT_FILE" -o "$OUTPUT_DIR/subfinder.txt"

# Amass (passive)
echo "[*] Running amass (passive)..."
amass enum -passive -df "$INPUT_FILE" -o "$OUTPUT_DIR/amass.txt"

# Combine and deduplicate
cat "$OUTPUT_DIR"/*.txt | sort -u > "$OUTPUT_DIR/all_subdomains.txt"
echo "[*] Recon complete. Output saved to $OUTPUT_DIR/all_subdomains.txt"