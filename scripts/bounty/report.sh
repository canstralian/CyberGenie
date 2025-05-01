#!/bin/bash
# =====================================================================
#  CyberGenie | Bug Bounty Automation Script
#  Filename : report.sh
#  Purpose  : Format and Export Vulnerability Report
#  Author   : canstralian
#  License  : Apache 2.0
# =====================================================================

set -euo pipefail

CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "============================================"
echo "      CyberGenie | Bug Bounty Script"
echo "      -> report.sh"
echo "      -> Started at: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================"
echo -e "${NC}"

INPUT="results/exploits/exploitable.txt"
REPORT="results/final_report.md"

echo "[*] Generating markdown report..."

cat <<EOF > "$REPORT"
# CyberGenie Bug Bounty Report

**Generated:** $(date)

## Exploitable Targets

\`\`\`
$(cat "$INPUT")
\`\`\`

## Summary

- Total Subdomains: $(wc -l < results/recon/all_subdomains.txt)
- Alive Hosts: $(wc -l < results/scan/alive.txt)
- Critical/High Findings: $(wc -l < "$INPUT")

EOF

echo "[*] Report written to $REPORT"