import curses
import time
from archsecure.harden import firewall
from archsecure.ui.menu import MenuItem

def execute_hardening(main_menu, stdscr: curses.window) -> None:
    """
    Execute hardening based on the main menu selections.
    If no main menu items (excluding actions/back) are effectively checked, nothing happens.
    Otherwise, clear the screen and run the hardening process.

    :param main_menu: The main menu object.
    :param stdscr: The curses standard screen.
    """
    progress_items = [item for item in main_menu.items if item.item_type not in ("action", "back")]
    if not any(item.effective_checked() for item in progress_items):
        return

    run_hardening_process(progress_items, stdscr)

def run_hardening_process(progress_items, stdscr: curses.window) -> None:
    """
    Run the hardening process sequentially for each main menu item.
    Displays a centered progress screen with statuses and a spinner animation.
    Three rows below the progress list, an extra message is displayed.

    :param progress_items: List of main menu MenuItem objects.
    :param stdscr: The curses standard screen.
    """
    spinner_chars = ['|', '/', '-', '\\']
    statuses = {item.label: "" for item in progress_items}

    # Extra message while processing.
    extra_msg = "Press Ctrl + C to cancel"

    for i, item in enumerate(progress_items):
        if not item.effective_checked():
            statuses[item.label] = "skipped"
            refresh_progress(stdscr, progress_items, statuses, extra_msg)
            time.sleep(0.5)
            continue

        statuses[item.label] = spinner_chars[0]
        for j in range(i+1, len(progress_items)):
            statuses[progress_items[j].label] = (
                spinner_chars[0] if progress_items[j].effective_checked() else "skipped"
            )

        result = process_item_with_spinner(item, stdscr, progress_items, statuses, spinner_chars, extra_msg)
        statuses[item.label] = "✔" if result else "error!"
        refresh_progress(stdscr, progress_items, statuses, extra_msg)
        time.sleep(0.5)

    # When processing is complete, update the extra message.
    extra_msg = "Computer Secured! Press any key to exit."
    refresh_progress(stdscr, progress_items, statuses, extra_msg)
    stdscr.getch()

def process_item_with_spinner(item, stdscr, progress_items, statuses, spinner_chars, extra_msg) -> bool:
    """
    Process a menu item with a spinner animation.
    For "Harden Firewall", call the actual firewall hardening function.
    For other items, simulate a successful process.

    :param item: The current MenuItem.
    :param stdscr: The curses standard screen.
    :param progress_items: List of main menu items.
    :param statuses: Dictionary mapping item labels to status strings.
    :param spinner_chars: List of spinner characters.
    :param extra_msg: The extra message to be displayed below the progress items.
    :return: True on success, False on failure.
    """
    spinner_index = 0
    process_duration = 3.0  # seconds
    start_time = time.time()

    while time.time() - start_time < process_duration:
        statuses[item.label] = spinner_chars[spinner_index % len(spinner_chars)]
        refresh_progress(stdscr, progress_items, statuses, extra_msg)
        spinner_index += 1
        time.sleep(0.1)

    if item.label == "Harden Firewall":
        selected_option = None
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

def refresh_progress(stdscr: curses.window, progress_items, statuses, extra_msg: str) -> None:
    """
    Refresh the progress screen with updated statuses.
    The progress items (labels) are centered horizontally (as a group) and their statuses are aligned in a fixed-width column.
    Three rows below the progress items, the extra message is displayed at the same x coordinate as the progress list.

    :param stdscr: The curses standard screen.
    :param progress_items: List of main menu items.
    :param statuses: Dictionary mapping item labels to status strings.
    :param extra_msg: The message to display 3 rows below the progress items.
    """
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    # Compute maximum label length.
    max_label_length = max(len(item.label) for item in progress_items)
    gap = 5  # space between label and status columns
    status_width = 10  # fixed width for the status column
    total_width = max_label_length + gap + status_width
    start_x = (max_x - total_width) // 2  # center the progress list as a group
    start_row = 3

    for i, item in enumerate(progress_items):
        label = item.label
        status = statuses.get(label, "")
        label_str = label.ljust(max_label_length)
        stdscr.addstr(start_row + i, start_x, label_str)
        status_str = status.rjust(status_width)
        attr = 0
        if status == "✔":
            attr = curses.color_pair(2)
        elif status == "error!":
            attr = curses.A_BOLD | curses.color_pair(4)
        stdscr.addstr(start_row + i, start_x + max_label_length + gap, status_str, attr)

    # Draw the extra message 3 rows below the progress items, aligned with start_x.
    msg_y = start_row + len(progress_items) + 3
    stdscr.addstr(msg_y, start_x, extra_msg, curses.A_BOLD)
    stdscr.refresh()
