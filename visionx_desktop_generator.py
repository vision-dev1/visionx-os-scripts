import os

OUTPUT_DIR = os.path.expanduser("~/.local/share/applications/")

modules = {
    "Network": [
        "nmap", "tcpdump", "wireshark", "tshark", "bettercap"
    ],
    "Exploitation": [
        "msfconsole", "msfvenom", "searchsploit", "nc"
    ],
    "OSINT": [
        "recon-ng", "theHarvester", "sherlock", "whois"
    ],
    "WebSecurity": [
        "burpsuite", "nikto", "sqlmap", "gobuster", "ffuf"
    ],
    "PasswordCracking": [
        "hashcat", "john", "hydra", "medusa", "cewl"
    ],
    "ReverseEngineering": [
        "gdb", "strace", "binwalk", "radare2", "ghidra"
    ],
    "Wireless": [
        "aircrack-ng", "reaver", "wifite", "hcxtools"
    ],
    "DailyUse": [
        "htop", "vim", "tmux", "curl", "wget"
    ],
    "DevStack": [
        "python3", "node", "go", "docker", "git"
    ]
}

# GUI tools (run directly)
gui_tools = {
    "wireshark", "burpsuite", "ghidra"
}

def make_desktop(tool, category):
    safe_name = f"visionx-{tool}.desktop"
    path = os.path.join(OUTPUT_DIR, safe_name)

    if tool in gui_tools:
        exec_cmd = tool
        terminal = "false"
    else:
        exec_cmd = f"xfce4-terminal --hold -e \"bash -c '{tool}; exec bash'\""
        terminal = "false"

    content = f"""[Desktop Entry]
Name={tool}
Exec={exec_cmd}
Type=Application
Terminal={terminal}
Categories=VisionX-{category};
"""

    with open(path, "w") as f:
        f.write(content)

    print(f"Created: {path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for category, tools in modules.items():
        for tool in tools:
            make_desktop(tool, category)

    print("\nDONE: VisionX menu generated.")

if __name__ == "__main__":
    main()
