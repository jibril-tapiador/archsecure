import curses
import sys
import textwrap

from archsecure.ui.descriptions import descriptions

class MenuItem:
    def __init__(self, label, item_type="checkbox", checked=False, submenu=None, action=None):
        """
        label: text label to display.
        item_type: "checkbox", "radio", "action", or "back".
                   "action" means no indicator is shown.
        checked: boolean state (only used if applicable).
        submenu: a Menu instance if this item leads to a submenu.
        action: a callable to execute if the item is an action.
        """
        self.label = label
        self.item_type = item_type
        self.checked = checked
        self.submenu = submenu
        self.action = action

    def effective_checked(self):
        """Return the effective checked state."""
        if self.submenu is not None:
            return any(item.effective_checked() for item in self.submenu.items if item.item_type != "back")
        return self.checked

class Menu:
    def __init__(self, items, parent=None, is_main=False):
        self.items = items[:]
        self.parent = parent
        self.position = 0

        if self.parent is not None:
            self.items.append(MenuItem("<- Back", item_type="back"))
        if parent is None and is_main:
            # "Secure Computer!" and "Abort" are action items.
            self.items.append(MenuItem("Secure Computer!", item_type="action", action=lambda: None))
            self.items.append(MenuItem("Abort", item_type="action", action=lambda: sys.exit(0)))

    def navigate(self, n):
        self.position = max(0, min(self.position + n, len(self.items) - 1))

def draw_info_panel(stdscr, label, panel_x):
    max_y, max_x = stdscr.getmaxyx()
    panel_width = max_x - panel_x - 2
    panel_height = max_y - 4
    panel_y = 2
    info_win = stdscr.subwin(panel_height, panel_width, panel_y, panel_x)
    info_win.clear()
    info_win.box()
    try:
        info_win.addstr(0, 2, " info ")
    except curses.error:
        pass
    desc = descriptions.get(label, "")
    if desc:
        wrapped = textwrap.wrap(desc, panel_width - 4)
        for idx, line in enumerate(wrapped, start=2):
            if idx < panel_height - 1:
                try:
                    info_win.addstr(idx, 2, line)
                except curses.error:
                    pass
    info_win.refresh()

def clear_info_panel(stdscr, panel_x):
    max_y, max_x = stdscr.getmaxyx()
    panel_width = max_x - panel_x - 2
    panel_height = max_y - 4
    panel_y = 2
    clear_win = stdscr.subwin(panel_height, panel_width, panel_y, panel_x)
    clear_win.clear()
    clear_win.refresh()

def build_menu_structure():
    # Harden Firewall submenu (radio buttons)
    firewall_menu = Menu([
        MenuItem("Use UFW", item_type="radio"),
        MenuItem("Use NFtables", item_type="radio"),
    ], parent=True)

    # Harden Kernel submenu (checkboxes)
    kernel_menu = Menu([
        MenuItem("Kernel Self-Protection", item_type="checkbox"),
        MenuItem("Harden Network Stack", item_type="checkbox"),
        MenuItem("Apply CPU mitigations", item_type="checkbox"),
        MenuItem("Disable redundant Kernel components", item_type="checkbox"),
    ], parent=True)

    # Install & Enable Apparmor submenu (checkboxes)
    apparmor_menu = Menu([
        MenuItem("Auto boot in Grub", item_type="checkbox"),
        MenuItem("Include Common Profiles", item_type="checkbox"),
        MenuItem("Include Whonix Profiles (For those under constant attack)", item_type="checkbox"),
    ], parent=True)

    # Install & Configure VPN submenu
    download_ovpn_menu = Menu([
        MenuItem("Download NordVPN OVPN files", item_type="checkbox"),
        MenuItem("Download ExpressVPN OVPN files", item_type="checkbox"),
        MenuItem("Download ProtonVPN OVPN files", item_type="checkbox"),
    ], parent=True)
    auto_dns_menu = Menu([
        MenuItem("NordVPN", item_type="radio"),
        MenuItem("ExpressVPN", item_type="radio"),
        MenuItem("ProtonVPN", item_type="radio"),
    ], parent=True)
    openvpn_menu = Menu([
        MenuItem("Install Openvpn", item_type="checkbox"),
        MenuItem("Deploy VPN Kill Switch", item_type="checkbox"),
        MenuItem("Download OVPN files", submenu=download_ovpn_menu),
        MenuItem("Auto Configure DNS", submenu=auto_dns_menu),
    ], parent=True)

    # Main menu
    main_menu = Menu([
        MenuItem("Harden Firewall", submenu=firewall_menu),
        MenuItem("Harden Kernel", submenu=kernel_menu),
        MenuItem("Install & Enable Apparmor", submenu=apparmor_menu),
        MenuItem("Install & Configure VPN", submenu=openvpn_menu),
        MenuItem("Harden Xorg", item_type="checkbox"),
        MenuItem("Disable TCP and ICMP Timestamps", item_type="checkbox"),
        MenuItem("Disable NTP Client", item_type="checkbox"),
        MenuItem("Securely Randomize Mac Address on boot", item_type="checkbox"),
    ], parent=None, is_main=True)

    return main_menu

def run_menu(menu, stdscr):
    window = stdscr.subwin(0, 0)
    window.keypad(True)
    curses.curs_set(0)

    while True:
        window.clear()
        stdscr.addstr(1, 2, "Up/Down: Navigate  Tab/Enter: Select/Toggle", curses.A_BOLD)
        start_row = 3
        menu_start_x = 4

        # Compute menu texts.
        menu_texts = []
        menu_width = 0
        for item in menu.items:
            indicator = ""
            if item.item_type in ("checkbox", "radio") or item.submenu is not None:
                if item.item_type == "checkbox":
                    indicator = "[X]" if item.effective_checked() else "[ ]"
                elif item.item_type == "radio":
                    indicator = "(X)" if item.checked else "( )"
                elif item.submenu is not None:
                    indicator = "[X]" if item.effective_checked() else "[ ]"
            text = f"{indicator} {item.label}" if indicator else item.label
            menu_texts.append(text)
            menu_width = max(menu_width, len(text))
        menu_width += 3  # for marker

        # Draw menu items.
        for index, text in enumerate(menu_texts):
            item = menu.items[index]
            if index == menu.position:
                mode = curses.color_pair(2)
                try:
                    window.addstr(start_row + index, menu_start_x - 2, "> ", curses.color_pair(3))
                except curses.error:
                    pass
                try:
                    window.addstr(start_row + index, menu_start_x, text, mode)
                except curses.error:
                    pass
            else:
                try:
                    window.addstr(start_row + index, menu_start_x, text)
                except curses.error:
                    pass

        # Draw info panel.
        current = menu.items[menu.position]
        panel_x = menu_start_x + menu_width + 1
        if current.label not in {"Secure Computer!", "Abort", "<- Back"}:
            draw_info_panel(stdscr, current.label, panel_x)
        else:
            clear_info_panel(stdscr, panel_x)

        window.refresh()
        key = window.getch()
        if key in (ord('q'), 27):
            if menu.parent is not None:
                return None
            else:
                sys.exit(0)
        elif key == curses.KEY_UP:
            menu.navigate(-1)
        elif key == curses.KEY_DOWN:
            menu.navigate(1)
        elif key in (9, curses.KEY_ENTER, ord('\n')):
            current = menu.items[menu.position]
            if current.item_type == "back":
                return None
            elif current.submenu is not None:
                run_menu(current.submenu, stdscr)
            elif current.action is not None:
                # Return the label for actions.
                return current.label
            else:
                if current.item_type == "radio":
                    current.checked = not current.checked
                    if current.checked:
                        for item in menu.items:
                            if item is not current and item.item_type == "radio":
                                item.checked = False
                elif current.item_type == "checkbox":
                    current.checked = not current.checked

if __name__ == '__main__':
    # For development, you can test the menu directly.
    curses.wrapper(lambda stdscr: run_menu(build_menu_structure(), stdscr))
