#!/bin/bash
# ==========================================================================
#  CyberGenie | Setup Script
#  Purpose  : Bootstraps bug bounty directories, stubs, and permissions
#  Author   : canstralian
#  License  : Apache 2.0
# ==========================================================================

set -euo pipefail

CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[*] Initializing CyberGenie bounty automation scaffold...${NC}"

# Create required directories
mkdir -p scripts/bounty
mkdir -p results/recon results/scan results/exploits

echo "[+] Directory structure created."

# Download or create script stubs with logic
declare -a scripts=("recon.sh" "scan.sh" "exploit.sh" "report.sh")
for script in "${scripts[@]}"; do
    if [[ ! -f "scripts/bounty/$script" ]]; then
        cp /dev/null "scripts/bounty/$script"
    fi
    echo "#!/bin/bash" > "scripts/bounty/$script"
    chmod +x "scripts/bounty/$script"
    
    # Add logic based on the script name
    case "$script" in
        "recon.sh")
            echo -e "# Recon script\n# This performs reconnaissance and gathers information.\n" > "scripts/bounty/$script"
            echo -e "subfinder -d example.com -o results/recon/subdomains.txt\namass enum -d example.com -o results/recon/amass.txt\n" >> "scripts/bounty/$script"
            echo "[+] Created: scripts/bounty/$script with recon logic"
            ;;
        "scan.sh")
            echo -e "# Scan script\n# This performs scanning against the discovered targets.\n" > "scripts/bounty/$script"
            echo -e "httpx -l results/recon/subdomains.txt -o results/scan/https.txt\nnuclei -l results/scan/https.txt -t /path/to/nuclei-templates/ -o results/scan/nuclei_output.txt\n" >> "scripts/bounty/$script"
            echo "[+] Created: scripts/bounty/$script with scanning logic"
            ;;
        "exploit.sh")
            echo -e "# Exploit script\n# This attempts to exploit identified vulnerabilities.\n" > "scripts/bounty/$script"
            echo -e "nikto -h results/scan/https.txt -o results/exploits/nikto_output.txt\n" >> "scripts/bounty/$script"
            echo "[+] Created: scripts/bounty/$script with exploit logic"
            ;;
        "report.sh")
            echo -e "# Report script\n# This generates a report of findings.\n" > "scripts/bounty/$script"
            echo -e "echo 'Recon Results:' > results/final_report.md\ncat results/recon/* >> results/final_report.md\ncat results/scan/* >> results/final_report.md\ncat results/exploits/* >> results/final_report.md\n" >> "scripts/bounty/$script"
            echo "[+] Created: scripts/bounty/$script with reporting logic"
            ;;
        *)
            echo "[!] Unknown script: $script"
            ;;
    esac
done

# Set executable bit
chmod +x scripts/bounty/*.sh

echo -e "${CYAN}[*] Setup complete. You can now edit or run your scripts.${NC}"