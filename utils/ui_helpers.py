"""Shared UI helper functions for games."""

import curses
from typing import List, Tuple, Optional


def center_text(text: str, width: int) -> int:
    """Calculate x position to center text.
    
    Args:
        text: Text to center
        width: Total width available
        
    Returns:
        X position for centered text
    """
    return (width - len(text)) // 2


def draw_border(stdscr, y: int, x: int, height: int, width: int, 
                char: str = '#'):
    """Draw a border around a rectangular area.
    
    Args:
        stdscr: Curses window
        y: Top Y position
        x: Left X position
        height: Height of border
        width: Width of border
        char: Character to use for border
    """
    # Top and bottom
    for i in range(width):
        stdscr.addch(y, x + i, char)
        stdscr.addch(y + height - 1, x + i, char)
    
    # Left and right
    for i in range(height):
        stdscr.addch(y + i, x, char)
        stdscr.addch(y + i, x + width - 1, char)


def draw_text_box(stdscr, y: int, x: int, text: str, 
                  attr: int = curses.A_NORMAL, centered: bool = False):
    """Draw text at a position, optionally centered.
    
    Args:
        stdscr: Curses window
        y: Y position
        x: X position (or left edge if centered)
        text: Text to draw
        attr: Curses attributes
        centered: If True, center text at x position
    """
    if centered:
        x = center_text(text, stdscr.getmaxyx()[1])
    stdscr.addstr(y, x, text, attr)


def draw_menu_item(stdscr, y: int, x: int, text: str, selected: bool = False,
                   centered: bool = False):
    """Draw a menu item with optional selection highlight.
    
    Args:
        stdscr: Curses window
        y: Y position
        x: X position
        text: Menu item text
        selected: Whether item is selected
        centered: Whether to center the text
    """
    if centered:
        x = center_text(text, stdscr.getmaxyx()[1])
    
    if selected:
        stdscr.addstr(y, x, text, curses.A_REVERSE)
    else:
        stdscr.addstr(y, x, text)


def draw_info_panel(stdscr, y: int, x: int, items: List[Tuple[str, any]], 
                    label_width: int = 12):
    """Draw an info panel with label-value pairs.
    
    Args:
        stdscr: Curses window
        y: Starting Y position
        x: X position
        items: List of (label, value) tuples
        label_width: Width reserved for labels
    """
    for i, (label, value) in enumerate(items):
        label_text = f"{label}:"
        value_text = str(value)
        stdscr.addstr(y + i, x, label_text.ljust(label_width))
        stdscr.addstr(y + i, x + label_width, value_text)


def draw_game_over_screen(stdscr, title: str, score: int, 
                         high_score: Optional[int] = None,
                         is_new_high: bool = False,
                         extra_info: List[str] = None):
    """Draw a standardized game over screen.
    
    Args:
        stdscr: Curses window
        title: Game over title (e.g., "GAME OVER" or "YOU WIN!")
        score: Final score
        high_score: Current high score (optional)
        is_new_high: Whether this is a new high score
        extra_info: Additional info lines to display
    """
    height, width = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.border(0)
    
    texts = [title]
    
    if is_new_high:
        texts.append("NEW HIGH SCORE!")
    elif high_score is not None:
        texts.append(f"High Score: {high_score}")
    
    texts.append(f"Final Score: {score}")
    
    if extra_info:
        texts.extend(extra_info)
    
    texts.append("Press any key to return to menu")
    
    start_y = height // 2 - len(texts) // 2
    
    for i, text in enumerate(texts):
        text_x = center_text(text, width)
        attr = curses.A_BOLD if (i == 0 or (is_new_high and i == 1)) else curses.A_NORMAL
        stdscr.addstr(start_y + i, text_x, text, attr)
    
    stdscr.refresh()


def draw_centered_message(stdscr, message: str, attr: int = curses.A_BOLD | curses.A_REVERSE):
    """Draw a centered message overlay.
    
    Args:
        stdscr: Curses window
        message: Message to display
        attr: Curses attributes
    """
    height, width = stdscr.getmaxyx()
    y = height // 2
    x = center_text(message, width)
    stdscr.addstr(y, x, message, attr)

