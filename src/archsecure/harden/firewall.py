import subprocess

def harden_firewall(selected_option: str) -> bool:
    """
    Harden the firewall based on the selected option.
    Options: "Use UFW", "Use NFtables", "Use iptables".

    :param selected_option: The selected firewall option.
    :return: True if successful, False otherwise.
    """
    try:
        if selected_option == "Use UFW":
            # Check if ufw is installed
            subprocess.run("command -v ufw", check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # Check ufw status
            proc = subprocess.run(["ufw", "status"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.decode().lower()
            if "inactive" in output:
                # Enable ufw
                subprocess.run(["sudo", "ufw", "enable"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc = subprocess.run(["ufw", "status"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = proc.stdout.decode().lower()
                return "active" in output
            else:
                return True
        elif selected_option == "Use NFtables":
            # Check if nft is installed
            subprocess.run("command -v nft", check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # Stub: Enable nftables (for real use, check current rules and adjust accordingly)
            subprocess.run(["sudo", "systemctl", "enable", "nftables"], check=True)
            subprocess.run(["sudo", "systemctl", "start", "nftables"], check=True)
            return True
        elif selected_option == "Use iptables":
            # Check if iptables is installed
            subprocess.run("command -v iptables", check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            # Stub: Check for a rule blocking incoming connections; if not present, add one.
            proc = subprocess.run(["sudo", "iptables", "-L", "INPUT", "--line-numbers"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = proc.stdout.decode().lower()
            if "drop" not in output:
                subprocess.run(["sudo", "iptables", "-A", "INPUT", "-j", "DROP"], check=True)
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False
