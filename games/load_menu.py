"""Load game menu."""

import curses
from typing import Optional
from utils.save_manager import SaveManager
from utils.ui_helpers import center_text


class LoadMenu:
    """Menu for loading saved games."""
    
    GAME_NAMES = {
        'snake': 'Snake',
        'tetris': 'Tetris',
        'pacman': 'Pac-Man',
        'pong': 'Pong',
        '2048': '2048',
        'minesweeper': 'Minesweeper',
        'space_invaders': 'Space Invaders',
        'breakout': 'Breakout',
        'hangman': 'Hangman',
        'tictactoe': 'Tic-Tac-Toe',
        'wordle': 'Wordle'
    }
    
    def __init__(self):
        self.save_manager = SaveManager()
        self.current_game = 0
        self.current_slot = 0
        self.games_with_saves = []
        self._refresh_saves()
    
    def _refresh_saves(self):
        """Refresh list of games with saves."""
        all_saves = self.save_manager.get_all_saves()
        self.games_with_saves = list(all_saves.keys())
        if not self.games_with_saves:
            self.games_with_saves = list(self.GAME_NAMES.keys())  # Show all games
    
    def run(self) -> Optional[tuple]:
        """Run the load menu.
        
        Returns:
            Tuple of (game_name, slot) if a save was selected, None otherwise
        """
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        try:
            while True:
                self._draw(stdscr)
                key = stdscr.getch()
                
                if key == ord('q') or key == 27:  # Q or ESC
                    return None
                elif key == curses.KEY_UP:
                    if self.current_slot > 0:
                        self.current_slot -= 1
                    elif self.current_game > 0:
                        self.current_game -= 1
                        self.current_slot = 4
                elif key == curses.KEY_DOWN:
                    if self.current_slot < 4:
                        self.current_slot += 1
                    elif self.current_game < len(self.games_with_saves) - 1:
                        self.current_game += 1
                        self.current_slot = 0
                elif key == curses.KEY_LEFT:
                    if self.current_game > 0:
                        self.current_game -= 1
                        self.current_slot = 0
                elif key == curses.KEY_RIGHT:
                    if self.current_game < len(self.games_with_saves) - 1:
                        self.current_game += 1
                        self.current_slot = 0
                elif key == ord('\n') or key == ord('\r'):  # Enter
                    game_name = self.games_with_saves[self.current_game]
                    slot = self.current_slot + 1
                    if self.save_manager.has_save(game_name, slot):
                        return (game_name, slot)
                elif key == ord('d'):  # Delete save
                    game_name = self.games_with_saves[self.current_game]
                    slot = self.current_slot + 1
                    if self.save_manager.has_save(game_name, slot):
                        self.save_manager.delete_save(game_name, slot)
                        self._refresh_saves()
        finally:
            curses.endwin()
    
    def _draw(self, stdscr):
        """Draw the load menu."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "LOAD GAME"
        title_x = center_text(title, width)
        stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        if not self.games_with_saves:
            msg = "No saved games found"
            stdscr.addstr(height // 2, center_text(msg, width), msg)
            inst = "Q: Back"
            stdscr.addstr(height - 2, center_text(inst, width), inst)
            stdscr.refresh()
            return
        
        # Current game
        game_name = self.games_with_saves[self.current_game]
        game_display_name = self.GAME_NAMES.get(game_name, game_name.title())
        
        game_title = f"Game: {game_display_name} (← → to change)"
        stdscr.addstr(3, center_text(game_title, width), game_title)
        
        # Save slots
        saves = self.save_manager.get_save_list(game_name)
        y = 6
        
        stdscr.addstr(y, 5, "Save Slots:", curses.A_BOLD)
        y += 2
        
        for i, save_info in enumerate(saves):
            slot = save_info['slot']
            exists = save_info['exists']
            
            # Highlight current selection
            attr = curses.A_REVERSE if i == self.current_slot else curses.A_NORMAL
            
            if exists:
                timestamp = save_info['timestamp']
                formatted_time = self.save_manager.format_timestamp(timestamp)
                metadata = save_info['metadata']
                score = metadata.get('score', 'N/A')
                
                line = f"  Slot {slot}: {formatted_time} - Score: {score}"
            else:
                line = f"  Slot {slot}: (Empty)"
                attr |= curses.A_DIM
            
            stdscr.addstr(y, 5, line, attr)
            y += 1
        
        # Instructions
        y = height - 6
        instructions = [
            "↑↓: Select slot",
            "← →: Change game",
            "Enter: Load save",
            "D: Delete save",
            "Q: Cancel"
        ]
        for i, inst in enumerate(instructions):
            stdscr.addstr(y + i, center_text(inst, width), inst, curses.A_DIM)
        
        stdscr.refresh()

