# Arch Secure

WARNING: This project is currently a work in progress and subject to significant changes.

This is a Python program that uses curses to provide a menu for selectively hardening an Arch Linux setup with settings based on [Madaians](https://madaidans-insecurities.github.io/guides/linux-hardening.html) and [theprivacyguide1](https://madaidans-insecurities.github.io/guides/linux-hardening.html).

[![asciicast](https://asciinema.org/a/0Fky2HE6jjSyDrP2qRoINSGC2.svg)](https://asciinema.org/a/0Fky2HE6jjSyDrP2qRoINSGC2)

A list of what it can do

* Kernel hardening via sysctl and boot parameters
* Disables IPv6 to reduce attack surface
* Mounts /proc with hidepid=2 to hide other users' processes
* Disables the potentially dangerous Netfilter automatic conntrack helper assignment to reduce attack surface
* Installs linux-hardened
* Enables AppArmor
* Restricts root access
* Installs and configures UFW as a firewall
* Changes your hostname to a generic one such as host
* Blocks all wireless devices with rfkill and blacklists the bluetooth kernel modules
* Creates a systemd service to spoof your MAC address at boot
* Uses a more restrictive umask
* Installs usbguard to blacklist USB devices
* Blacklists Thunderbolt and Firewire to prevent some DMA attacks
* Disables coredumps
* Enables microcode updates
* Disables NTP
* Enables IPv6 privacy extensions if IPv6 has not been disabled
* Blacklists uncommon network protocols
* Blacklists uncommon filesystems
* Installs haveged and jitterentropy to gather more entropy
* Blacklists the webcam, microphone and speaker kernel modules to prevent them from being used to spy on you

All of these are completely optional and you will be able to select if you want them or not.

This script only works on Arch Linux or Manjaro with GRUB or Syslinux as the bootloader and systemd as the init system.

## How to use it:

Clone this repo, go to src and do `python -m archsecure.main`
