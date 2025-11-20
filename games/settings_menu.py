"""Settings menu for configuring games."""

import curses
from utils.settings import SettingsManager


class SettingsMenu:
    """Interactive settings menu."""
    
    def __init__(self):
        self.settings = SettingsManager()
        self.current_category = 0
        self.current_setting = 0
        self.categories = ['snake', 'tetris', 'pacman', 'pong', '2048', 'minesweeper',
                          'space_invaders', 'breakout', 'hangman', 'general']
        self.category_names = {
            'snake': 'Snake',
            'tetris': 'Tetris',
            'pacman': 'Pac-Man',
            'pong': 'Pong',
            '2048': '2048',
            'minesweeper': 'Minesweeper',
            'space_invaders': 'Space Invaders',
            'breakout': 'Breakout',
            'hangman': 'Hangman',
            'general': 'General'
        }
        self.setting_options = {
            'speed': ['slow', 'medium', 'fast'],
            'difficulty': ['easy', 'normal', 'hard'],
            'ghost_speed': ['slow', 'normal', 'fast'],
            'starting_level': list(range(1, 11)),
            'show_high_scores': [True, False],
            'sound_enabled': [True, False],
            'theme': ['classic', 'dark', 'neon', 'retro', 'minimal'],
        }
    
    def run(self):
        """Display and handle the settings menu."""
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        try:
            while True:
                self._draw_menu(stdscr)
                key = stdscr.getch()
                
                if key == ord('q'):
                    break
                elif key == curses.KEY_UP:
                    if self.current_setting > 0:
                        self.current_setting -= 1
                    elif self.current_category > 0:
                        self.current_category -= 1
                        self.current_setting = self._get_max_setting_index()
                elif key == curses.KEY_DOWN:
                    max_setting = self._get_max_setting_index()
                    if self.current_setting < max_setting:
                        self.current_setting += 1
                    elif self.current_category < len(self.categories) - 1:
                        self.current_category += 1
                        self.current_setting = 0
                elif key == curses.KEY_LEFT or key == ord('-'):
                    self._change_setting(-1)
                elif key == curses.KEY_RIGHT or key == ord('+') or key == ord('='):
                    self._change_setting(1)
                elif key == ord('r'):
                    self.settings.reset_to_defaults()
        finally:
            curses.endwin()
    
    def _get_max_setting_index(self) -> int:
        """Get the maximum setting index for current category."""
        category = self.categories[self.current_category]
        settings = self.settings.get_game_settings(category)
        return max(0, len(settings) - 1)
    
    def _change_setting(self, direction: int):
        """Change the current setting value."""
        category = self.categories[self.current_category]
        settings = self.settings.get_game_settings(category)
        setting_keys = list(settings.keys())
        
        if not setting_keys or self.current_setting >= len(setting_keys):
            return
        
        key = setting_keys[self.current_setting]
        current_value = settings[key]
        
        if key in self.setting_options:
            options = self.setting_options[key]
            try:
                current_index = options.index(current_value)
                new_index = (current_index + direction) % len(options)
                new_value = options[new_index]
                self.settings.set(category, key, new_value)
            except (ValueError, IndexError):
                pass
    
    def _draw_menu(self, stdscr):
        """Draw the settings menu."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "Settings"
        title_x = (width - len(title)) // 2
        stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Instructions
        instructions = "↑↓: Navigate | ←→: Change | R: Reset | Q: Back"
        inst_x = (width - len(instructions)) // 2
        stdscr.addstr(2, inst_x, instructions)
        
        # Draw categories and settings
        start_y = 4
        y = start_y
        
        for cat_idx, category in enumerate(self.categories):
            # Category header
            cat_name = self.category_names[category]
            attr = curses.A_BOLD | curses.A_REVERSE if cat_idx == self.current_category else curses.A_BOLD
            stdscr.addstr(y, 5, f"{cat_name}:", attr)
            y += 1
            
            # Settings for this category
            settings = self.settings.get_game_settings(category)
            for set_idx, (key, value) in enumerate(settings.items()):
                is_selected = (cat_idx == self.current_category and set_idx == self.current_setting)
                
                # Format setting name
                setting_name = key.replace('_', ' ').title()
                
                # Format value
                if isinstance(value, bool):
                    value_str = "ON" if value else "OFF"
                elif isinstance(value, int):
                    value_str = str(value)
                else:
                    value_str = value.upper()
                
                # Display
                if is_selected:
                    stdscr.addstr(y, 10, f"> {setting_name}: [{value_str}]", curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 10, f"  {setting_name}: [{value_str}]")
                y += 1
            
            y += 1  # Space between categories
        
        stdscr.refresh()

