"""UI animations and visual effects."""

import curses
import time
from typing import List, Tuple


def draw_box_animation(stdscr, y: int, x: int, height: int, width: int, 
                      char: str = '█', delay: float = 0.02):
    """Draw a box with animation.
    
    Args:
        stdscr: Curses window
        y: Top Y position
        x: Left X position
        height: Height of box
        width: Width of box
        char: Character to use
        delay: Delay between frames
    """
    # Top
    for i in range(width):
        try:
            stdscr.addch(y, x + i, char)
            stdscr.refresh()
            time.sleep(delay)
        except curses.error:
            pass
    
    # Right
    for i in range(1, height):
        try:
            stdscr.addch(y + i, x + width - 1, char)
            stdscr.refresh()
            time.sleep(delay)
        except curses.error:
            pass
    
    # Bottom (right to left)
    for i in range(width - 2, -1, -1):
        try:
            stdscr.addch(y + height - 1, x + i, char)
            stdscr.refresh()
            time.sleep(delay)
        except curses.error:
            pass
    
    # Left (bottom to top)
    for i in range(height - 2, 0, -1):
        try:
            stdscr.addch(y + i, x, char)
            stdscr.refresh()
            time.sleep(delay)
        except curses.error:
            pass


def fade_in_text(stdscr, y: int, x: int, text: str, delay: float = 0.05):
    """Fade in text character by character.
    
    Args:
        stdscr: Curses window
        y: Y position
        x: X position
        text: Text to display
        delay: Delay between characters
    """
    for i, char in enumerate(text):
        try:
            stdscr.addstr(y, x + i, char)
            stdscr.refresh()
            time.sleep(delay)
        except curses.error:
            pass


def draw_splash_screen(stdscr, title: str, subtitle: str = "", 
                       width: int = 60, height: int = 10):
    """Draw an animated splash screen.
    
    Args:
        stdscr: Curses window
        title: Main title
        subtitle: Subtitle text
        width: Width of splash box
        height: Height of splash box
    """
    screen_height, screen_width = stdscr.getmaxyx()
    start_y = (screen_height - height) // 2
    start_x = (screen_width - width) // 2
    
    stdscr.clear()
    
    # Draw animated border
    draw_box_animation(stdscr, start_y, start_x, height, width, '═', 0.01)
    
    # Title
    title_y = start_y + height // 2 - 1
    title_x = (screen_width - len(title)) // 2
    fade_in_text(stdscr, title_y, title_x, title, 0.03)
    
    # Subtitle
    if subtitle:
        sub_y = title_y + 2
        sub_x = (screen_width - len(subtitle)) // 2
        time.sleep(0.3)
        stdscr.addstr(sub_y, sub_x, subtitle)
        stdscr.refresh()
    
    time.sleep(1)


def draw_progress_bar(stdscr, y: int, x: int, width: int, 
                     progress: float, label: str = ""):
    """Draw a progress bar.
    
    Args:
        stdscr: Curses window
        y: Y position
        x: X position
        width: Width of progress bar
        progress: Progress value (0.0 to 1.0)
        label: Optional label
    """
    progress = max(0.0, min(1.0, progress))
    filled = int(width * progress)
    
    # Draw bar
    bar = "[" + "█" * filled + "░" * (width - filled) + "]"
    try:
        stdscr.addstr(y, x, bar)
        
        # Draw label and percentage
        if label:
            stdscr.addstr(y, x - len(label) - 1, label)
        
        percent_text = f" {int(progress * 100)}%"
        stdscr.addstr(y, x + len(bar) + 1, percent_text)
        
        stdscr.refresh()
    except curses.error:
        pass


def pulse_text(stdscr, y: int, x: int, text: str, cycles: int = 3, 
               delay: float = 0.2):
    """Make text pulse (alternate between bold and normal).
    
    Args:
        stdscr: Curses window
        y: Y position
        x: X position
        text: Text to pulse
        cycles: Number of pulse cycles
        delay: Delay between pulses
    """
    for _ in range(cycles):
        try:
            stdscr.addstr(y, x, text, curses.A_BOLD)
            stdscr.refresh()
            time.sleep(delay)
            
            stdscr.addstr(y, x, text, curses.A_NORMAL)
            stdscr.refresh()
            time.sleep(delay)
        except curses.error:
            pass


def draw_notification(stdscr, message: str, duration: float = 2.0, 
                     style: str = "info"):
    """Draw a notification message.
    
    Args:
        stdscr: Curses window
        message: Notification message
        duration: How long to display
        style: Style (info, success, warning, error)
    """
    height, width = stdscr.getmaxyx()
    
    # Style attributes
    styles = {
        'info': curses.A_NORMAL,
        'success': curses.A_BOLD,
        'warning': curses.A_REVERSE,
        'error': curses.A_REVERSE | curses.A_BOLD
    }
    
    attr = styles.get(style, curses.A_NORMAL)
    
    # Notification box
    box_width = len(message) + 4
    box_height = 3
    y = 2
    x = (width - box_width) // 2
    
    try:
        # Draw box
        for i in range(box_height):
            stdscr.addstr(y + i, x, " " * box_width, attr)
        
        # Draw message
        msg_y = y + 1
        msg_x = x + 2
        stdscr.addstr(msg_y, msg_x, message, attr)
        stdscr.refresh()
        
        # Wait
        time.sleep(duration)
        
        # Clear notification
        for i in range(box_height):
            stdscr.addstr(y + i, x, " " * box_width)
        stdscr.refresh()
    except curses.error:
        pass


def draw_countdown(stdscr, seconds: int = 3):
    """Draw a countdown animation.
    
    Args:
        stdscr: Curses window
        seconds: Number of seconds to count down
    """
    height, width = stdscr.getmaxyx()
    y = height // 2
    
    for i in range(seconds, 0, -1):
        # Clear previous
        stdscr.clear()
        stdscr.border(0)
        
        # Draw number
        num_str = str(i)
        x = (width - len(num_str)) // 2
        
        try:
            stdscr.addstr(y, x, num_str, curses.A_BOLD | curses.A_REVERSE)
            stdscr.refresh()
            time.sleep(1)
        except curses.error:
            pass
    
    # "GO!"
    stdscr.clear()
    stdscr.border(0)
    go_text = "GO!"
    x = (width - len(go_text)) // 2
    try:
        stdscr.addstr(y, x, go_text, curses.A_BOLD)
        stdscr.refresh()
        time.sleep(0.5)
    except curses.error:
        pass

