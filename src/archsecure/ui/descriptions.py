descriptions = {
    # Main menu descriptions:
    "Harden Firewall": "Blocks all incoming connections.",
    "Harden Kernel": "Hardens the linux kernel and reduces the attack surface.",
    "Install & Enable Apparmor": (
        "AppArmor is a Linux security module implementing Mandatory Access Control (MAC), "
        "which enforces administrator-defined policies to restrict application access to files, directories, "
        "and network resources."
    ),
    "Install & Configure VPN": (
        "A VPN encrypts your data, eliminating any opportunity for others on the same network to intercept your traffic."
    ),
    "Harden Xorg": (
        "Xorg is an old, bloated implementation of the X Window System with known vulnerabilities. "
        "Limiting its privileges can reduce the impact of potential exploits."
    ),
    "Disable TCP and ICMP Timestamps": (
        "Disable timestamps to prevent clock skew fingerprinting attacks."
    ),
    "Disable NTP Client": (
        "NTP is insecure and can leak system time. Disable it and consider using the hardware clock instead."
    ),
    "Securely Randomize Mac Address on boot": (
        "Randomize the MAC address on each boot to enhance privacy."
    ),

    # Submenu items for Harden Firewall:
    "Use UFW": "lorem ipsum",
    "Use NFtables": "lorem ipsum",

    # Submenu items for Harden Kernel:
    "Kernel Self-Protection": "lorem ipsum",
    "Harden Network Stack": "lorem ipsum",
    "Apply CPU mitigations": "lorem ipsum",
    "Disable redundant Kernel components": "lorem ipsum",

    # Submenu items for Install & Enable Apparmor:
    "Auto boot in Grub": "lorem ipsum",
    "Include Common Profiles": "lorem ipsum",
    "Include Whonix Profiles (For those under constant attack)": "lorem ipsum",

    # Submenu items for Install & Configure VPN:
    "Install Openvpn": "lorem ipsum",
    "Deploy VPN Kill Switch": "lorem ipsum",
    "Download OVPN files": "lorem ipsum",
    "Download NordVPN OVPN files": "lorem ipsum",
    "Download ExpressVPN OVPN files": "lorem ipsum",
    "Download ProtonVPN OVPN files": "lorem ipsum",
    "Auto Configure DNS": "lorem ipsum",
    "NordVPN": "lorem ipsum",
    "ExpressVPN": "lorem ipsum",
    "ProtonVPN": "lorem ipsum"
}
