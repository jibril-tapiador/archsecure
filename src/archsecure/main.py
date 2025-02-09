import curses
import sys

from archsecure.ui.menu import build_menu_structure, run_menu
from archsecure.harden.executor import execute_hardening

def main(stdscr):
    curses.start_color()
    curses.use_default_colors()
    # Color pair 1: Normal text.
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    # Color pair 2: Success (green checkmark).
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    # Color pair 3: Marker for highlighted menu item (green, bold).
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    # Color pair 4: Error (red).
    curses.init_pair(4, curses.COLOR_RED, -1)
    # Color pair 5: Highlighted menu text (black on cyan).
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_CYAN)

    main_menu = build_menu_structure()
    selected = run_menu(main_menu, stdscr)

    if selected == "Secure Computer!":
        execute_hardening(main_menu, stdscr)
    else:
        sys.exit(0)

if __name__ == '__main__':
    curses.wrapper(main)
