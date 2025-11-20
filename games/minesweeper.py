"""Minesweeper logic puzzle game implementation."""

import curses
import random
import time
from typing import List, Tuple, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class MinesweeperGame(BaseGame):
    """Minesweeper game for the terminal."""
    
    def __init__(self):
        super().__init__('minesweeper', min_height=24, min_width=80)
        
        self.width = 16
        self.height = 12
        self.mine_count = 20
        
        # Grid: -1 = mine, 0-8 = adjacent mine count
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # Revealed: True = revealed, False = hidden
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        # Flagged: True = flagged
        self.flagged = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        self.first_click = True
        self.cells_revealed = 0
        self.start_time = None
        
        # Cursor position
        self.cursor_x = self.width // 2
        self.cursor_y = self.height // 2
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize game state."""
        pass  # Mines placed on first click
    
    def _place_mines(self, exclude_y: int, exclude_x: int):
        """Place mines randomly, excluding the first clicked cell."""
        mines_placed = 0
        while mines_placed < self.mine_count:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if (y == exclude_y and x == exclude_x) or self.grid[y][x] == -1:
                continue
            self.grid[y][x] = -1
            mines_placed += 1
        
        # Calculate adjacent mine counts
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != -1:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dy == 0 and dx == 0:
                                continue
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                if self.grid[ny][nx] == -1:
                                    count += 1
                    self.grid[y][x] = count
    
    def _reveal_cell(self, y: int, x: int):
        """Reveal a cell and recursively reveal adjacent cells if zero."""
        if not (0 <= y < self.height and 0 <= x < self.width):
            return
        if self.revealed[y][x] or self.flagged[y][x]:
            return
        
        self.revealed[y][x] = True
        self.cells_revealed += 1
        
        # If mine, game over
        if self.grid[y][x] == -1:
            self.game_over = True
            self.won = False
            return
        
        # If zero, reveal adjacent cells
        if self.grid[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    self._reveal_cell(y + dy, x + dx)
    
    def _check_win(self):
        """Check if all non-mine cells are revealed."""
        total_cells = self.width * self.height
        if self.cells_revealed == total_cells - self.mine_count:
            self.won = True
            self.game_over = True
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(self.height - 1, self.cursor_y + 1)
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.width - 1, self.cursor_x + 1)
        elif key == ord(' ') or key == ord('\n'):
            # Reveal cell
            if not self.flagged[self.cursor_y][self.cursor_x]:
                if self.first_click:
                    self._place_mines(self.cursor_y, self.cursor_x)
                    self.first_click = False
                    self.start_time = time.time()
                self._reveal_cell(self.cursor_y, self.cursor_x)
                self._check_win()
        elif key == ord('f'):
            # Toggle flag
            if not self.revealed[self.cursor_y][self.cursor_x]:
                self.flagged[self.cursor_y][self.cursor_x] = \
                    not self.flagged[self.cursor_y][self.cursor_x]
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        # Minesweeper is turn-based, no continuous updates
        pass
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        # Title
        title = "Minesweeper"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(0, title_x, title, curses.A_BOLD)
        
        # Info
        flags_used = sum(sum(row) for row in self.flagged)
        info_text = f"Flags: {flags_used}/{self.mine_count}"
        self.stdscr.addstr(0, 2, info_text)
        
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            time_text = f"Time: {elapsed}s"
            self.stdscr.addstr(0, self.width - len(time_text) - 2, time_text)
        
        # Draw grid
        board_start_y = 2
        board_start_x = (self.width - self.width * 2) // 2
        
        for y in range(self.height):
            for x in range(self.width):
                cell_y = board_start_y + y
                cell_x = board_start_x + x * 2
                
                # Cursor highlight
                is_cursor = (y == self.cursor_y and x == self.cursor_x)
                attr = curses.A_REVERSE if is_cursor else curses.A_NORMAL
                
                if self.revealed[y][x]:
                    if self.grid[y][x] == -1:
                        self.stdscr.addstr(cell_y, cell_x, "*", curses.A_BOLD)
                    elif self.grid[y][x] == 0:
                        self.stdscr.addstr(cell_y, cell_x, " ", attr)
                    else:
                        num_str = str(self.grid[y][x])
                        self.stdscr.addstr(cell_y, cell_x, num_str, attr)
                elif self.flagged[y][x]:
                    self.stdscr.addstr(cell_y, cell_x, "F", curses.A_BOLD, attr)
                else:
                    self.stdscr.addstr(cell_y, cell_x, "#", attr)
        
        # Instructions
        inst_y = board_start_y + self.height + 1
        instructions = [
            "Arrow Keys: Move cursor",
            "Space/Enter: Reveal",
            "F: Toggle flag",
            "Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, 2, inst)
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        if self.start_time:
            state['time'] = int(time.time() - self.start_time)
        return state
    
    def _save_results(self) -> bool:
        """Save results - only save if won (time-based score)."""
        if self.won and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.score = elapsed  # Score is time
            # For high score, lower time is better, but we store as score
            is_new_high = self.high_score_manager.add_score(
                'minesweeper', 
                elapsed,
                time=elapsed
            )
            if is_new_high:
                self.high_score = elapsed
            
            # Record stats
            play_time = time.time() - self.start_time
            self.stats.record_game_end(self.game_name, elapsed, True, play_time)
            return is_new_high
        else:
            # Still record stats
            play_time = time.time() - self.start_time if self.start_time else 0
            self.stats.record_game_end(self.game_name, 0, False, play_time)
            return False
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "YOU WIN!"
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            extra_info = [f"Time: {elapsed} seconds"]
        else:
            title = "GAME OVER"
            extra_info = ["You hit a mine!"]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )
