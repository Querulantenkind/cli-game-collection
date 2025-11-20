"""Terminal utilities and validation."""

import curses
from typing import Tuple, Optional


class TerminalSizeError(Exception):
    """Raised when terminal is too small for the game."""
    pass


def validate_terminal_size(min_height: int, min_width: int, 
                          stdscr: Optional[curses.window] = None) -> Tuple[int, int]:
    """Validate terminal size and return current dimensions.
    
    Args:
        min_height: Minimum required height
        min_width: Minimum required width
        stdscr: Optional curses window (if None, creates temporary one)
        
    Returns:
        Tuple of (height, width) of current terminal
        
    Raises:
        TerminalSizeError: If terminal is too small
    """
    if stdscr is None:
        temp_stdscr = curses.initscr()
        try:
            height, width = temp_stdscr.getmaxyx()
        finally:
            curses.endwin()
    else:
        height, width = stdscr.getmaxyx()
    
    if height < min_height or width < min_width:
        raise TerminalSizeError(
            f"Terminal too small! Required: {min_width}x{min_height}, "
            f"Current: {width}x{height}. Please resize your terminal."
        )
    
    return height, width


def show_terminal_size_error(stdscr, min_height: int, min_width: int):
    """Display a user-friendly terminal size error message.
    
    Args:
        stdscr: Curses window
        min_height: Minimum required height
        min_width: Minimum required width
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    messages = [
        "TERMINAL TOO SMALL",
        "",
        f"Required size: {min_width}x{min_height}",
        f"Current size: {width}x{height}",
        "",
        "Please resize your terminal window",
        "and try again.",
        "",
        "Press any key to return to menu..."
    ]
    
    start_y = height // 2 - len(messages) // 2
    for i, msg in enumerate(messages):
        x = (width - len(msg)) // 2
        attr = curses.A_BOLD if i == 0 else curses.A_NORMAL
        stdscr.addstr(start_y + i, x, msg, attr)
    
    stdscr.refresh()
    stdscr.getch()

