import subprocess
import shutil

def harden_firewall(selected_option: str) -> bool:
    """
    Harden the firewall based on the selected option.
    Options: "Use UFW", "Use NFtables", "Use iptables".

    :param selected_option: The selected firewall option.
    :return: True if the firewall is hardened successfully, False otherwise.
    """
    try:
        if selected_option == "Use UFW":
            # Check if ufw is installed
            if not shutil.which("ufw"):
                return False
            # Get UFW status
            proc = subprocess.run(
                ["ufw", "status"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output = proc.stdout.decode().lower()
            if "inactive" in output:
                # Enable ufw
                subprocess.run(
                    ["sudo", "ufw", "enable"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                proc = subprocess.run(
                    ["ufw", "status"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                output = proc.stdout.decode().lower()
                return "active" in output
            else:
                return True

        elif selected_option == "Use NFtables":
            # Check if nft is installed
            if not shutil.which("nft"):
                return False
            # Enable and start nftables via systemctl
            subprocess.run(["sudo", "systemctl", "enable", "nftables"], check=True)
            subprocess.run(["sudo", "systemctl", "start", "nftables"], check=True)
            # Verify that nftables is active
            proc = subprocess.run(
                ["sudo", "systemctl", "is-active", "nftables"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            status = proc.stdout.decode().strip()
            return status == "active"

        elif selected_option == "Use iptables":
            # Check if iptables is installed
            if not shutil.which("iptables"):
                return False
            # List the INPUT chain rules using -S (which outputs in a simple text format)
            proc = subprocess.run(
                ["sudo", "iptables", "-S", "INPUT"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output = proc.stdout.decode().lower()
            if "-j drop" not in output:
                # Append a rule to drop all incoming packets
                subprocess.run(
                    ["sudo", "iptables", "-A", "INPUT", "-j", "DROP"],
                    check=True
                )
                # Verify that the rule was added
                proc2 = subprocess.run(
                    ["sudo", "iptables", "-S", "INPUT"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                output2 = proc2.stdout.decode().lower()
                return "-j drop" in output2
            return True

        else:
            return False

    except subprocess.CalledProcessError:
        return False
