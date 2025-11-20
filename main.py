#!/usr/bin/env python3
"""
CLI Game Collection - Main Entry Point
A collection of classic games playable in the terminal.
"""

import sys
from games.snake import SnakeGame
from games.menu import GameMenu


def main():
    """Main entry point for the CLI game collection."""
    try:
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

