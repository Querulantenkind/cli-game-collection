#!/usr/bin/env python3
"""
CLI Game Collection - Main Entry Point
A collection of classic games playable in the terminal.
"""

import sys
import curses
from games.menu import GameMenu
from utils.ui_animations import draw_splash_screen


def show_splash(stdscr):
    """Show animated splash screen."""
    draw_splash_screen(
        stdscr,
        "CLI GAME COLLECTION",
        "11 Classic Games • Press any key to continue",
        width=60,
        height=8
    )
    stdscr.getch()


def main():
    """Main entry point for the CLI game collection."""
    try:
        # Show splash screen
        curses.wrapper(show_splash)
        
        # Run menu
        menu = GameMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

