#!/bin/bash
# =====================================================================
#  CyberGenie | Bug Bounty Automation Script
#  Filename : scan.sh
#  Purpose  : Active Scanning and Vulnerability Enumeration
#  Author   : canstralian
#  License  : Apache 2.0
# =====================================================================

set -euo pipefail

CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "============================================"
echo "      CyberGenie | Bug Bounty Script"
echo "      -> scan.sh"
echo "      -> Started at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"
echo -e "${NC}"

INPUT="results/recon/all_subdomains.txt"
OUTPUT_DIR="results/scan"
mkdir -p "$OUTPUT_DIR"

# Probing for alive hosts
echo "[*] Probing alive hosts..."
httpx -l "$INPUT" -silent -o "$OUTPUT_DIR/alive.txt"

# Vulnerability scanning with nuclei
echo "[*] Running nuclei scans..."
nuclei -l "$OUTPUT_DIR/alive.txt" -o "$OUTPUT_DIR/nuclei.txt"

echo "[*] Scanning complete. Results in $OUTPUT_DIR/"