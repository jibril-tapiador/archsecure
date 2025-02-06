import curses
import sys

from archsecure.ui.menu import build_menu_structure, run_menu
from archsecure.harden.executor import execute_hardening

def main(stdscr):
    # Initialize colors.
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)             # Normal text.
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # Highlighted text.
    curses.init_pair(3, curses.COLOR_GREEN, -1)              # Marker color (green on default bg).

    # Build and run the menu.
    menu = build_menu_structure()
    selected = run_menu(menu, stdscr)

    # When the user selects "Secure Computer!" (or later an "apply" command),
    # the executor would be called to run the hardening routines.
    if selected == "Secure Computer!":
        execute_hardening(menu)  # Stub call: the executor reads menu state and applies changes.
    else:
        # For testing, simply exit.
        sys.exit(0)

if __name__ == '__main__':
    curses.wrapper(main)
