import curses
import time
from archsecure.harden import firewall
from archsecure.ui.menu import MenuItem

def execute_hardening(main_menu, stdscr: curses.window) -> None:
    """
    Execute hardening based on the main menu selections.
    If no main menu items (excluding actions/back) are checked, nothing happens.
    Otherwise, clear the screen and run the hardening process.

    :param main_menu: The main menu object.
    :param stdscr: The curses standard screen.
    """
    progress_items = [item for item in main_menu.items if item.item_type not in ("action", "back")]
    # Use effective_checked() to detect if any submenu item has been checked.
    if not any(item.effective_checked() for item in progress_items):
        return

    run_hardening_process(progress_items, stdscr)

def run_hardening_process(progress_items, stdscr: curses.window) -> None:
    """
    Run the hardening process sequentially for each main menu item.
    Displays a progress screen with statuses and a spinner for items in progress.

    :param progress_items: List of main menu MenuItem objects.
    :param stdscr: The curses standard screen.
    """
    spinner_chars = ['|', '/', '-', '\\']
    statuses = {item.label: "" for item in progress_items}

    for i, item in enumerate(progress_items):
        # If this main menu item was not selected, mark it as skipped.
        if not item.effective_checked():
            statuses[item.label] = "skipped"
            refresh_progress(stdscr, progress_items, statuses)
            time.sleep(0.5)
            continue

        # Set initial spinner state.
        statuses[item.label] = spinner_chars[0]
        # For subsequent items that are checked, set spinner; otherwise, "skipped".
        for j in range(i+1, len(progress_items)):
            statuses[progress_items[j].label] = (spinner_chars[0]
                if progress_items[j].effective_checked() else "skipped")

        result = process_item_with_spinner(item, stdscr, progress_items, statuses, spinner_chars)
        statuses[item.label] = "✔" if result else "error!"
        refresh_progress(stdscr, progress_items, statuses)
        time.sleep(0.5)

    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    message = "Computer Secured! Press any key to exit."
    stdscr.addstr(max_y // 2, (max_x - len(message)) // 2, message, curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()

def process_item_with_spinner(item, stdscr, progress_items, statuses, spinner_chars) -> bool:
    """
    Process a menu item with a spinner animation.
    For "Harden Firewall", call the actual firewall hardening function.
    For other items, simulate a successful process.

    :param item: The current MenuItem.
    :param stdscr: The curses standard screen.
    :param progress_items: List of main menu items.
    :param statuses: Dictionary mapping item labels to status strings.
    :param spinner_chars: List of spinner characters.
    :return: True on success, False on failure.
    """
    spinner_index = 0
    process_duration = 3.0  # seconds
    start_time = time.time()

    while time.time() - start_time < process_duration:
        statuses[item.label] = spinner_chars[spinner_index % len(spinner_chars)]
        refresh_progress(stdscr, progress_items, statuses)
        spinner_index += 1
        time.sleep(0.1)

    if item.label == "Harden Firewall":
        selected_option = None
        # In the submenu, check for a radio button that is selected.
        if item.submenu:
            for sub_item in item.submenu.items:
                if sub_item.item_type == "radio" and sub_item.checked:
                    selected_option = sub_item.label
                    break
        if selected_option is None:
            return False
        else:
            return firewall.harden_firewall(selected_option)
    else:
        # For items not yet implemented, simulate success.
        return True

def refresh_progress(stdscr: curses.window, progress_items, statuses) -> None:
    """
    Refresh the progress screen with updated statuses.

    :param stdscr: The curses standard screen.
    :param progress_items: List of main menu items.
    :param statuses: Dictionary mapping item labels to status strings.
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    title = "Hardening Process"
    stdscr.addstr(1, (max_x - len(title)) // 2, title, curses.A_BOLD)
    start_row = 3
    for i, item in enumerate(progress_items):
        label = item.label
        status = statuses.get(label, "")
        stdscr.addstr(start_row + i, 2, label)
        attr = 0
        if status == "✔":
            attr = curses.color_pair(2)
        elif status == "error!":
            attr = curses.A_BOLD | curses.color_pair(4)
        stdscr.addstr(start_row + i, max_x - len(status) - 2, status, attr)
    stdscr.refresh()
