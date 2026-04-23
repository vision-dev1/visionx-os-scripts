#!/usr/bin/env python3
"""
VisionX Launcher Generator
Dynamically detects installed tools and generates .desktop files for XFCE.
"""

import os
import shutil
import subprocess

# ─── CONFIG ───────────────────────────────────────────────────────────────────

TERMINAL       = "xfce4-terminal"
OUTPUT_DIR     = os.path.expanduser("~/.local/share/applications")
FILE_PREFIX    = "vx-launcher"

# ─── MODULE DEFINITIONS ───────────────────────────────────────────────────────
# Format per tool:
#   "binary_name": ("Display Label", is_gui, "xdg_category")
#
# is_gui=True  → launch directly
# is_gui=False → wrap in terminal

MODULES = {
    "Network": {
        "xdg_category": "Network",
        "tools": {
            "nmap":        ("nmap",        False, "Network"),
            "netdiscover": ("netdiscover", False, "Network"),
            "tcpdump":     ("tcpdump",     False, "Network"),
            "tshark":      ("tshark",      False, "Network"),
            "wireshark":   ("wireshark",   True,  "Network"),
            "bettercap":   ("bettercap",   False, "Network"),
            "nc":          ("netcat (nc)", False, "Network"),
            "curl":        ("curl",        False, "Network"),
            "wget":        ("wget",        False, "Network"),
            "whois":       ("whois",       False, "Network"),
            "dig":         ("dig",         False, "Network"),
            "traceroute":  ("traceroute",  False, "Network"),
            "arp-scan":    ("arp-scan",    False, "Network"),
            "masscan":     ("masscan",     False, "Network"),
            "socat":       ("socat",       False, "Network"),
        }
    },
    "Exploitation": {
        "xdg_category": "Network",
        "tools": {
            "msfconsole":   ("Metasploit Console",  False, "Network"),
            "msfvenom":     ("msfvenom",             False, "Network"),
            "searchsploit": ("searchsploit",         False, "Network"),
            "sqlmap":       ("sqlmap",               False, "Network"),
            "commix":       ("commix",               False, "Network"),
            "beef-xss":     ("BeEF XSS",             False, "Network"),
            "exploitdb":    ("ExploitDB",            False, "Network"),
            "crackmapexec": ("CrackMapExec",         False, "Network"),
            "evil-winrm":   ("Evil-WinRM",           False, "Network"),
        }
    },
    "OSINT": {
        "xdg_category": "Network",
        "tools": {
            "theHarvester": ("theHarvester", False, "Network"),
            "recon-ng":     ("recon-ng",     False, "Network"),
            "sherlock":     ("sherlock",     False, "Network"),
            "maltego":      ("Maltego",      True,  "Network"),
            "spiderfoot":   ("SpiderFoot",   False, "Network"),
            "amass":        ("amass",        False, "Network"),
            "subfinder":    ("subfinder",    False, "Network"),
            "dnsx":         ("dnsx",         False, "Network"),
            "httpx":        ("httpx",        False, "Network"),
            "whois":        ("whois",        False, "Network"),
            "exiftool":     ("exiftool",     False, "Network"),
        }
    },
    "WebSecurity": {
        "xdg_category": "Network",
        "tools": {
            "burpsuite":  ("Burp Suite",   True,  "Network"),
            "nikto":      ("nikto",        False, "Network"),
            "gobuster":   ("gobuster",     False, "Network"),
            "ffuf":       ("ffuf",         False, "Network"),
            "dirb":       ("dirb",         False, "Network"),
            "wfuzz":      ("wfuzz",        False, "Network"),
            "zaproxy":    ("OWASP ZAP",    True,  "Network"),
            "sqlmap":     ("sqlmap",       False, "Network"),
            "arjun":      ("arjun",        False, "Network"),
            "whatweb":    ("whatweb",      False, "Network"),
            "wafw00f":    ("wafw00f",      False, "Network"),
            "nuclei":     ("nuclei",       False, "Network"),
        }
    },
    "PasswordCracking": {
        "xdg_category": "Utility",
        "tools": {
            "hashcat":   ("hashcat",        False, "Utility"),
            "john":      ("John the Ripper",False, "Utility"),
            "hydra":     ("hydra",          False, "Utility"),
            "medusa":    ("medusa",         False, "Utility"),
            "crunch":    ("crunch",         False, "Utility"),
            "cewl":      ("cewl",           False, "Utility"),
            "ophcrack":  ("ophcrack",       True,  "Utility"),
            "fcrackzip": ("fcrackzip",      False, "Utility"),
            "hash-id":   ("hash-id",        False, "Utility"),
        }
    },
    "ReverseEngineering": {
        "xdg_category": "Development",
        "tools": {
            "ghidra":    ("Ghidra",         True,  "Development"),
            "radare2":   ("radare2",        False, "Development"),
            "r2":        ("radare2 (r2)",   False, "Development"),
            "gdb":       ("GDB Debugger",   False, "Development"),
            "gdbserver": ("GDB Server",     False, "Development"),
            "objdump":   ("objdump",        False, "Development"),
            "binwalk":   ("binwalk",        False, "Development"),
            "ltrace":    ("ltrace",         False, "Development"),
            "strace":    ("strace",         False, "Development"),
            "strings":   ("strings",        False, "Development"),
            "pwndbg":    ("pwndbg",         False, "Development"),
            "peda":      ("peda",           False, "Development"),
        }
    },
    "Wireless": {
        "xdg_category": "Network",
        "tools": {
            "aircrack-ng":  ("aircrack-ng",  False, "Network"),
            "airmon-ng":    ("airmon-ng",    False, "Network"),
            "airodump-ng":  ("airodump-ng",  False, "Network"),
            "aireplay-ng":  ("aireplay-ng",  False, "Network"),
            "wifite":       ("wifite",       False, "Network"),
            "reaver":       ("reaver",       False, "Network"),
            "bully":        ("bully",        False, "Network"),
            "kismet":       ("Kismet",       True,  "Network"),
            "hostapd":      ("hostapd",      False, "Network"),
            "iwconfig":     ("iwconfig",     False, "Network"),
        }
    },
    "DailyUse": {
        "xdg_category": "Utility",
        "tools": {
            "htop":        ("htop",          False, "Utility"),
            "tmux":        ("tmux",          False, "Utility"),
            "vim":         ("Vim Editor",    False, "Utility"),
            "nano":        ("nano",          False, "Utility"),
            "mousepad":    ("Mousepad",      True,  "Utility"),
            "thunar":      ("Thunar FM",     True,  "Utility"),
            "firefox":     ("Firefox",       True,  "Network"),
            "chromium":    ("Chromium",      True,  "Network"),
            "code":        ("VS Code",       True,  "Development"),
            "gedit":       ("gedit",         True,  "Utility"),
            "feh":         ("feh",           False, "Utility"),
            "scrot":       ("scrot",         False, "Utility"),
            "xclip":       ("xclip",         False, "Utility"),
            "neofetch":    ("neofetch",      False, "Utility"),
        }
    },
    "DeveloperStack": {
        "xdg_category": "Development",
        "tools": {
            "python3":  ("Python 3",         False, "Development"),
            "python2":  ("Python 2",         False, "Development"),
            "node":     ("Node.js",          False, "Development"),
            "npm":      ("npm",              False, "Development"),
            "go":       ("Go",               False, "Development"),
            "ruby":     ("Ruby",             False, "Development"),
            "perl":     ("Perl",             False, "Development"),
            "java":     ("Java",             False, "Development"),
            "gcc":      ("GCC Compiler",     False, "Development"),
            "gdb":      ("GDB Debugger",     False, "Development"),
            "git":      ("Git",              False, "Development"),
            "docker":   ("Docker",           False, "Development"),
            "docker-compose": ("Docker Compose", False, "Development"),
            "make":     ("make",             False, "Development"),
            "cmake":    ("cmake",            False, "Development"),
            "code":     ("VS Code",          True,  "Development"),
            "pwntools": ("pwntools",         False, "Development"),
        }
    },
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def is_installed(binary: str) -> str | None:
    """Return full path if binary is on PATH, else None."""
    path = shutil.which(binary)
    if path:
        return path
    # Fallback: check dpkg for package name matching binary
    try:
        result = subprocess.run(
            ["dpkg", "-l", binary],
            capture_output=True, text=True
        )
        if result.returncode == 0 and "ii" in result.stdout:
            return f"/usr/bin/{binary}"  # best guess
    except FileNotFoundError:
        pass
    return None


def make_exec_line(binary_path: str, is_gui: bool) -> str:
    """Build the Exec= line for the .desktop file."""
    if is_gui:
        return binary_path
    else:
        return (
            f"{TERMINAL} --hold -e "
            f"'bash -c \"{binary_path}; echo; echo [Press Enter to close]; read\"'"
        )


def sanitize(name: str) -> str:
    """Make a safe filename slug."""
    return name.lower().replace(" ", "-").replace("/", "-").replace("_", "-")


def write_desktop(module: str, binary: str, label: str,
                  exec_line: str, category: str) -> str:
    slug     = sanitize(f"{module}-{binary}")
    filename = f"{FILE_PREFIX}-{slug}.desktop"
    filepath = os.path.join(OUTPUT_DIR, filename)

    content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={module} - {label}
Comment={module} tool: {binary}
Exec={exec_line}
Icon=utilities-terminal
Categories={category};
Terminal=false
StartupNotify=false
Keywords={module};{binary};security;kali;visionx;
"""
    with open(filepath, "w") as f:
        f.write(content)
    os.chmod(filepath, 0o644)
    return filename


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_written = 0
    skipped       = 0
    seen_slugs    = set()  # prevent duplicate entries across modules

    print("=" * 60)
    print("  VisionX Launcher Generator")
    print("=" * 60)

    for module, config in MODULES.items():
        tools     = config["tools"]
        written   = []
        not_found = []

        for binary, (label, is_gui, category) in tools.items():
            slug = sanitize(f"{module}-{binary}")
            if slug in seen_slugs:
                continue  # skip exact duplicate (same module+binary)
            seen_slugs.add(slug)

            path = is_installed(binary)
            if path:
                exec_line = make_exec_line(path, is_gui)
                fname     = write_desktop(module, binary, label, exec_line, category)
                written.append(f"  ✅  {label:30s} → {fname}")
                total_written += 1
            else:
                not_found.append(f"  ⬜  {label:30s} (not installed)")
                skipped += 1

        print(f"\n[{module}]")
        for line in written:
            print(line)
        if not_found:
            print(f"  --- {len(not_found)} tool(s) not found ---")
            for line in not_found:
                print(line)

    print("\n" + "=" * 60)
    print(f"  Generated : {total_written} .desktop files")
    print(f"  Skipped   : {skipped} (not installed)")
    print(f"  Output    : {OUTPUT_DIR}")
    print("=" * 60)

    # Refresh XFCE desktop database
    print("\nRefreshing desktop database...")
    result = subprocess.run(
        ["update-desktop-database", OUTPUT_DIR],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅  update-desktop-database OK")
    else:
        print(f"⚠️  update-desktop-database error: {result.stderr.strip()}")


if __name__ == "__main__":
    main()
