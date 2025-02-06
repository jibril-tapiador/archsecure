import curses
import sys
import textwrap
from typing import Callable, List, Optional

from archsecure.ui.descriptions import descriptions


class MenuItem:
    """
    A single menu item.
    """
    def __init__(
        self,
        label: str,
        item_type: str = "checkbox",
        checked: bool = False,
        submenu: Optional["Menu"] = None,
        action: Optional[Callable[[], None]] = None,
    ):
        """
        :param label: The text label for the menu item.
        :param item_type: One of "checkbox", "radio", "action", or "back".
                          "action" indicates no indicator should be drawn.
        :param checked: Whether the item is checked.
        :param submenu: A submenu (Menu instance) if this item leads to another menu.
        :param action: A callable to execute if the item is an action.
        """
        self.label = label
        self.item_type = item_type
        self.checked = checked
        self.submenu = submenu
        self.action = action

    def effective_checked(self) -> bool:
        """
        Return the effective checked state. For items with submenus,
        return True if any child (other than back items) is checked.
        """
        if self.submenu:
            return any(child.effective_checked() for child in self.submenu.items if child.item_type != "back")
        return self.checked


class Menu:
    """
    Represents a menu with multiple items.
    """
    def __init__(self, items: List[MenuItem], parent: Optional["Menu"] = None, is_main: bool = False):
        self.items: List[MenuItem] = items.copy()
        self.parent = parent
        self.position = 0

        # If this is a submenu, add a Back option.
        if self.parent is not None:
            self.items.append(MenuItem("<- Back", item_type="back"))
        # If this is the main menu, add action items for execution.
        if parent is None and is_main:
            self.items.append(MenuItem("Secure Computer!", item_type="action", action=lambda: None))
            self.items.append(MenuItem("Abort", item_type="action", action=lambda: sys.exit(0)))

    def navigate(self, offset: int) -> None:
        """
        Adjust the current position by offset, bounded by [0, len(items)-1].
        """
        self.position = max(0, min(self.position + offset, len(self.items) - 1))


def _render_menu(stdscr: curses.window, menu: Menu, start_row: int = 3, menu_start_x: int = 4) -> int:
    """
    Render the menu items onto stdscr.
    Returns the computed menu width.
    """
    menu_texts: List[str] = []
    max_text_width = 0

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
        max_text_width = max(max_text_width, len(text))
    # Reserve space for the marker ("> ") on highlighted items.
    max_text_width += 3

    for idx, text in enumerate(menu_texts):
        mode = curses.color_pair(2) if idx == menu.position else curses.A_NORMAL

        y_index = start_row + idx
        if text in {"Secure Computer!", "Abort", "<- Back"}:
            y_index += 1

        # If the item is highlighted, draw the green marker separately.
        if idx == menu.position:
            try:
                stdscr.addstr(y_index, menu_start_x - 2, "> ", curses.color_pair(3))
            except curses.error:
                pass
        try:
            stdscr.addstr(y_index, menu_start_x, text, mode)
        except curses.error:
            pass

    return max_text_width


def _draw_info_panel(stdscr: curses.window, label: str, panel_x: int) -> None:
    """
    Draw a bordered info panel starting at panel_x and filling the remaining width.
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


def _clear_info_panel(stdscr: curses.window, panel_x: int) -> None:
    """
    Clear the info panel area.
    """
    max_y, max_x = stdscr.getmaxyx()
    panel_width = max_x - panel_x - 2
    panel_height = max_y - 4
    panel_y = 2
    clear_win = stdscr.subwin(panel_height, panel_width, panel_y, panel_x)
    clear_win.clear()
    clear_win.refresh()


def build_menu_structure() -> Menu:
    """
    Build the complete menu structure.
    """
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


def run_menu(menu: Menu, stdscr: curses.window) -> Optional[str]:
    """
    The main loop to run the given menu until an action is selected.
    Returns the label of the selected action item, if any.
    """
    win = stdscr.subwin(0, 0)
    win.keypad(True)
    curses.curs_set(0)

    while True:
        win.clear()
        stdscr.addstr(1, 2, "Up/Down: Navigate  Tab/Enter: Select/Toggle", curses.A_BOLD)
        start_row = 3
        menu_start_x = 4

        # Render menu items and compute width for info panel.
        menu_width = _render_menu(stdscr, menu, start_row, menu_start_x)

        # Determine panel x position and draw or clear info panel.
        panel_x = menu_start_x + menu_width + 1
        current = menu.items[menu.position]
        if current.label not in {"Secure Computer!", "Abort", "<- Back"}:
            _draw_info_panel(stdscr, current.label, panel_x)
        else:
            _clear_info_panel(stdscr, panel_x)

        win.refresh()
        key = win.getch()

        if key in (ord("q"), 27):
            if menu.parent:
                return None
            sys.exit(0)
        elif key == curses.KEY_UP:
            menu.navigate(-1)
        elif key == curses.KEY_DOWN:
            menu.navigate(1)
        elif key in (9, curses.KEY_ENTER, ord("\n")):
            current = menu.items[menu.position]
            if current.item_type == "back":
                return None
            elif current.submenu:
                run_menu(current.submenu, stdscr)
            elif current.action:
                return current.label
            else:
                if current.item_type == "radio":
                    # Toggle radio; if checking, uncheck siblings.
                    new_state = not current.checked
                    current.checked = new_state
                    if new_state:
                        for item in menu.items:
                            if item is not current and item.item_type == "radio":
                                item.checked = False
                elif current.item_type == "checkbox":
                    current.checked = not current.checked


if __name__ == "__main__":
    # For quick testing, run this module directly.
    curses.wrapper(lambda stdscr: run_menu(build_menu_structure(), stdscr))
