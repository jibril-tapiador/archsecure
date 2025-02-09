# src/arch_hardener/ui/descriptions.py

descriptions = {
    # Main menu descriptions:
    "Harden Firewall": (
        "Configures the system's firewall to block all incoming connections. "
        "Select a preferred firewall solution from the submenu to secure your network."
    ),
    "Harden Kernel": (
        "Adjusts kernel parameters to reduce the system's attack surface by enabling self-protection features "
        "and applying hardening measures against exploits."
    ),
    "Install & Enable Apparmor": (
        "Installs and enables AppArmor to restrict application behavior via mandatory access control, "
        "using common profiles to limit access."
    ),
    "Install & Configure VPN": (
        "Encrypts traffic and hides your IP address by installing and configuring a VPN solution, "
        "thus protecting online communications."
    ),
    "Harden Xorg": (
        "Reduces vulnerabilities in graphical systems by applying hardening measures to Xorg, "
        "limiting the risk of exploits."
    ),
    "Disable TCP and ICMP Timestamps": (
        "Prevents time-based fingerprinting attacks by disabling TCP and ICMP timestamps, "
        "thereby reducing system time leakage."
    ),
    "Disable NTP Client": (
        "Disables the NTP client to avoid system time leaks and potential security risks, "
        "favoring more secure time synchronization methods."
    ),
    "Securely Randomize Mac Address on boot": (
        "Ensures a new MAC address is generated at each boot to improve privacy on public networks "
        "and reduce tracking risks."
    ),

    # Submenu descriptions for Harden Firewall:
    "Use UFW": (
        "UFW is a firewall management tool that provides a simple interface for controlling iptables rules."
    ),
    "Use NFtables": (
        "NFtables serves as a modern replacement for iptables, offering a streamlined firewall solution for Linux systems."
    ),
    "Use iptables": (
        "iptables blocks incoming connections and provides detailed control over firewall rules."
    ),

    # Submenu descriptions for Harden Kernel:
    "Kernel Self-Protection": (
        "Enables kernel self-protection features that reduce exploitation risks and enhance resistance to attacks."
    ),
    "Harden Network Stack": (
        "Configures network parameters to protect against common network-based attacks, tightening security at the kernel level."
    ),
    "Apply CPU mitigations": (
        "Applies CPU-level mitigations to defend against hardware vulnerabilities and protect the system from exploits."
    ),
    "Disable redundant Kernel components": (
        "Disables unnecessary kernel components to reduce potential attack vectors, streamlining the system and minimizing exposure."
    ),

    # Submenu descriptions for Install & Enable Apparmor:
    "Auto boot in Grub": (
        "Adds required parameters to Grub to ensure AppArmor is enabled at boot and starts automatically."
    ),
    "Include Common Profiles": (
        "Installs common AppArmor profiles to secure popular applications and provide baseline system protection."
    ),
    "Include Whonix Profiles (For those under constant attack)": (
        "Installs Whonix profiles for environments under constant attack, further restricting application access."
    ),

    # Submenu descriptions for Install & Configure VPN:
    "Install Openvpn": (
        "Installs OpenVPN, a widely used open-source VPN solution that provides core functionality for secure connections."
    ),
    "Deploy VPN Kill Switch": (
        "Configures a VPN kill switch to halt all traffic if the VPN disconnects unexpectedly, preventing data leaks."
    ),
    "Download OVPN files": (
        "Downloads OpenVPN configuration files from your VPN provider; select the appropriate configuration in the submenu."
    ),
    "Download NordVPN OVPN files": (
        "Downloads OpenVPN configuration files for NordVPN, preparing the necessary settings."
    ),
    "Download ExpressVPN OVPN files": (
        "Downloads OpenVPN configuration files for ExpressVPN, providing the required configuration."
    ),
    "Download ProtonVPN OVPN files": (
        "Downloads OpenVPN configuration files for ProtonVPN, setting up the required configuration."
    ),
    "Auto Configure DNS": (
        "Automatically configures DNS settings for secure routing of queries when connected to the VPN."
    ),
    "NordVPN": (
        "Selects NordVPN settings for DNS configuration."
    ),
    "ExpressVPN": (
        "Selects ExpressVPN settings for DNS configuration."
    ),
    "ProtonVPN": (
        "Selects ProtonVPN settings for DNS configuration."
    )
}
