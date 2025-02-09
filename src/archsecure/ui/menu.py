import curses
import sys
import textwrap
from typing import List, Tuple

from archsecure.ui.descriptions import descriptions


class MenuItem:
    """
    Represents a single menu item.
    """
    def __init__(self, label: str, item_type: str = "checkbox", checked: bool = False,
                 submenu: 'Menu' = None, action: callable = None) -> None:
        """
        Initialize a MenuItem.

        :param label: The display text of the menu item.
        :param item_type: One of "checkbox", "radio", "action", or "back".
                          "action" means no indicator is drawn.
        :param checked: Initial checked state.
        :param submenu: A submenu if this item leads to another menu.
        :param action: A callable executed when the item is selected.
        """
        self.label = label
        self.item_type = item_type
        self.checked = checked
        self.submenu = submenu
        self.action = action

    def effective_checked(self) -> bool:
        """
        Return the effective checked state.

        For items with a submenu, returns True if any non-back child is checked.
        Otherwise, returns the item's own checked state.
        """
        if self.submenu is not None:
            return any(item.effective_checked() for item in self.submenu.items if item.item_type != "back")
        return self.checked


class Menu:
    """
    Represents a menu, which may include nested submenus.
    """
    def __init__(self, items: List[MenuItem], parent: 'Menu' = None, is_main: bool = False) -> None:
        """
        Initialize a Menu.

        :param items: List of MenuItem objects.
        :param parent: Parent Menu, if any.
        :param is_main: True if this is the main menu.
        """
        self.items = items[:]
        self.parent = parent
        self.position = 0

        if self.parent is not None:
            self.items.append(MenuItem("<- Back", item_type="back"))
        if parent is None and is_main:
            # Append action items for the main menu.
            self.items.append(MenuItem("Secure Computer!", item_type="action", action=lambda: None))
            self.items.append(MenuItem("Abort", item_type="action", action=lambda: sys.exit(0)))

    def navigate(self, n: int) -> None:
        """
        Move the selection by n positions, ensuring the index remains valid.
        """
        self.position = max(0, min(self.position + n, len(self.items) - 1))


def draw_info_panel(stdscr: curses.window, label: str, panel_x: int) -> None:
    """
    Draw a bordered info panel filling the space to the right of panel_x.

    :param stdscr: The main curses window.
    :param label: The key label to use for the info description.
    :param panel_x: The x-coordinate where the panel starts.
    """
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


def clear_info_panel(stdscr: curses.window, panel_x: int) -> None:
    """
    Clear the area where the info panel is drawn.

    :param stdscr: The main curses window.
    :param panel_x: The x-coordinate where the panel starts.
    """
    max_y, max_x = stdscr.getmaxyx()
    panel_width = max_x - panel_x - 2
    panel_height = max_y - 4
    panel_y = 2

    clear_win = stdscr.subwin(panel_height, panel_width, panel_y, panel_x)
    clear_win.clear()
    clear_win.refresh()


def _build_menu_layout(menu: Menu, start_row: int) -> Tuple[List[Tuple[int, str, int]], int]:
    """
    Build a layout for the menu items that includes a 2-line vertical gap
    before the first action or back item.

    :param menu: The Menu instance.
    :param start_row: The starting y-coordinate for drawing.
    :return: A tuple with a list of (original_index, text, y_coord) and the max width (including marker space).
    """
    layout = []
    current_y = start_row
    max_width = 0
    for i, item in enumerate(menu.items):
        # Insert a 2-line vertical gap when transitioning from non-action to action/back.
        if i > 0 and item.item_type in ("action", "back") and menu.items[i - 1].item_type not in ("action", "back"):
            current_y += 2

        indicator = ""
        if item.item_type in ("checkbox", "radio") or item.submenu is not None:
            if item.item_type == "checkbox":
                indicator = "[X]" if item.effective_checked() else "[ ]"
            elif item.item_type == "radio":
                indicator = "(X)" if item.checked else "( )"
            elif item.submenu is not None:
                indicator = "[X]" if item.effective_checked() else "[ ]"
        text = f"{indicator} {item.label}" if indicator else item.label
        max_width = max(max_width, len(text))
        layout.append((i, text, current_y))
        current_y += 1

    return layout, max_width + 3  # Reserve extra space for the "> " marker


def _draw_menu_item(window: curses.window, item_index: int, text: str, y: int, menu: Menu, menu_start_x: int) -> None:
    """
    Draw a single menu item at the specified y coordinate.

    If this item is the currently selected one, it is highlighted and preceded by a bold green ">".

    :param window: The curses window to draw on.
    :param item_index: The original index of the item in the menu.
    :param text: The text of the menu item.
    :param y: The y-coordinate at which to draw.
    :param menu: The Menu instance.
    :param menu_start_x: The x-coordinate where the menu text begins.
    """
    if item_index == menu.position:
        mode = curses.color_pair(5)
        try:
            # Draw the bold green marker (using color pair 3 and A_BOLD)
            window.addstr(y, menu_start_x - 2, "> ", curses.color_pair(3) | curses.A_BOLD)
        except curses.error:
            pass
        try:
            window.addstr(y, menu_start_x, text, mode)
        except curses.error:
            pass
    else:
        try:
            window.addstr(y, menu_start_x, text)
        except curses.error:
            pass


def build_menu_structure() -> Menu:
    """
    Construct and return the full nested menu structure.
    """
    # Harden Firewall submenu (radio buttons) – now with iptables added.
    firewall_menu = Menu([
        MenuItem("Use UFW", item_type="radio"),
        MenuItem("Use NFtables", item_type="radio"),
        MenuItem("Use iptables", item_type="radio"),
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


def run_menu(menu: Menu, stdscr: curses.window) -> str:
    """
    Run the menu loop using the provided curses window.

    :param menu: The Menu instance to display.
    :param stdscr: The main curses window.
    :return: The label of the selected action item, if any.
    """
    window = stdscr.subwin(0, 0)
    window.keypad(True)
    curses.curs_set(0)

    # Header text per requirements.
    header_text = "Up/Down: Navigate  Tab/Enter: Select/Toggle"
    start_row = 3
    menu_start_x = 2  # Updated left margin

    while True:
        window.clear()
        stdscr.addstr(1, 2, header_text, curses.A_BOLD)

        layout, menu_width = _build_menu_layout(menu, start_row)
        for orig_idx, text, y in layout:
            _draw_menu_item(window, orig_idx, text, y, menu, menu_start_x)

        # Info panel is drawn to the right.
        panel_x = menu_start_x + menu_width + 1
        current = menu.items[menu.position]
        if current.label not in {"Secure Computer!", "Abort", "<- Back"}:
            draw_info_panel(stdscr, current.label, panel_x)
        else:
            clear_info_panel(stdscr, panel_x)

        window.refresh()
        key = window.getch()

        if key in (ord('q'), 27):
            if menu.parent is not None:
                return ""
            else:
                sys.exit(0)
        elif key == curses.KEY_UP:
            menu.navigate(-1)
        elif key == curses.KEY_DOWN:
            menu.navigate(1)
        elif key in (9, curses.KEY_ENTER, ord('\n')):
            current = menu.items[menu.position]
            if current.item_type == "back":
                return ""
            elif current.submenu is not None:
                result = run_menu(current.submenu, stdscr)
                if result:
                    return result
            elif current.action is not None:
                return current.label
            else:
                # Toggle checkable items.
                if current.item_type == "radio":
                    current.checked = not current.checked
                    if current.checked:
                        for item in menu.items:
                            if item is not current and item.item_type == "radio":
                                item.checked = False
                elif current.item_type == "checkbox":
                    current.checked = not current.checked

    return ""
