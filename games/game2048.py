"""2048 number puzzle game implementation."""

import curses
import random
from typing import List, Tuple
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class Game2048(BaseGame):
    """2048 number puzzle game for the terminal."""
    
    def __init__(self):
        super().__init__('2048', min_height=24, min_width=80)
        
        self.grid_size = 4
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.won = False
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize with 2 tiles."""
        self._add_random_tile()
        self._add_random_tile()
    
    def _add_random_tile(self):
        """Add a random tile (2 or 4) to an empty cell."""
        empty_cells = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == 0:
                    empty_cells.append((y, x))
        
        if empty_cells:
            y, x = random.choice(empty_cells)
            self.grid[y][x] = 2 if random.random() < 0.9 else 4
    
    def _move_left(self):
        """Move tiles left and merge."""
        moved = False
        for y in range(self.grid_size):
            row = [cell for cell in self.grid[y] if cell != 0]
            merged = []
            i = 0
            while i < len(row):
                if i < len(row) - 1 and row[i] == row[i + 1]:
                    merged.append(row[i] * 2)
                    self.score += row[i] * 2
                    i += 2
                else:
                    merged.append(row[i])
                    i += 1
            merged.extend([0] * (self.grid_size - len(merged)))
            if self.grid[y] != merged:
                moved = True
            self.grid[y] = merged
        return moved
    
    def _move_right(self):
        """Move tiles right and merge."""
        moved = False
        for y in range(self.grid_size):
            row = [cell for cell in self.grid[y] if cell != 0]
            merged = []
            i = len(row) - 1
            while i >= 0:
                if i > 0 and row[i] == row[i - 1]:
                    merged.insert(0, row[i] * 2)
                    self.score += row[i] * 2
                    i -= 2
                else:
                    merged.insert(0, row[i])
                    i -= 1
            merged = [0] * (self.grid_size - len(merged)) + merged
            if self.grid[y] != merged:
                moved = True
            self.grid[y] = merged
        return moved
    
    def _move_up(self):
        """Move tiles up and merge."""
        moved = False
        for x in range(self.grid_size):
            col = [self.grid[y][x] for y in range(self.grid_size) if self.grid[y][x] != 0]
            merged = []
            i = 0
            while i < len(col):
                if i < len(col) - 1 and col[i] == col[i + 1]:
                    merged.append(col[i] * 2)
                    self.score += col[i] * 2
                    i += 2
                else:
                    merged.append(col[i])
                    i += 1
            merged.extend([0] * (self.grid_size - len(merged)))
            for y in range(self.grid_size):
                if self.grid[y][x] != merged[y]:
                    moved = True
                self.grid[y][x] = merged[y]
        return moved
    
    def _move_down(self):
        """Move tiles down and merge."""
        moved = False
        for x in range(self.grid_size):
            col = [self.grid[y][x] for y in range(self.grid_size) if self.grid[y][x] != 0]
            merged = []
            i = len(col) - 1
            while i >= 0:
                if i > 0 and col[i] == col[i - 1]:
                    merged.insert(0, col[i] * 2)
                    self.score += col[i] * 2
                    i -= 2
                else:
                    merged.insert(0, col[i])
                    i -= 1
            merged = [0] * (self.grid_size - len(merged)) + merged
            for y in range(self.grid_size):
                if self.grid[y][x] != merged[y]:
                    moved = True
                self.grid[y][x] = merged[y]
        return moved
    
    def _can_move(self):
        """Check if any moves are possible."""
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == 0:
                    return True
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                value = self.grid[y][x]
                if (x < self.grid_size - 1 and self.grid[y][x + 1] == value) or \
                   (y < self.grid_size - 1 and self.grid[y + 1][x] == value):
                    return True
        
        return False
    
    def _check_win(self):
        """Check if 2048 tile exists."""
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == 2048:
                    self.won = True
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif not self.paused:
            moved = False
            if key == curses.KEY_LEFT:
                moved = self._move_left()
            elif key == curses.KEY_RIGHT:
                moved = self._move_right()
            elif key == curses.KEY_UP:
                moved = self._move_up()
            elif key == curses.KEY_DOWN:
                moved = self._move_down()
            
            if moved:
                self._add_random_tile()
                self._check_win()
                if not self._can_move():
                    self.game_over = True
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        # 2048 is turn-based, no continuous updates needed
        pass
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        # Title
        title = "2048"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(0, title_x, title, curses.A_BOLD)
        
        # Info bar
        self._draw_info_bar()
        
        # Draw grid
        board_start_y = 2
        board_start_x = (self.width - self.grid_size * 6) // 2
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                value = self.grid[y][x]
                cell_y = board_start_y + y * 2
                cell_x = board_start_x + x * 6
                
                # Draw cell border
                self.stdscr.addstr(cell_y, cell_x, "+-----+")
                self.stdscr.addstr(cell_y + 1, cell_x, "|     |")
                self.stdscr.addstr(cell_y + 2, cell_x, "+-----+")
                
                # Draw value
                if value > 0:
                    value_str = str(value)
                    value_x = cell_x + 3 - len(value_str) // 2
                    self.stdscr.addstr(cell_y + 1, value_x, value_str, curses.A_BOLD)
        
        # Instructions
        inst_y = board_start_y + self.grid_size * 2 + 2
        instructions = [
            "Arrow Keys: Move",
            "P: Pause",
            "Q: Quit",
            "Goal: Reach 2048!"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, 2, inst)
        
        # Pause message
        self._draw_pause_message()
        
        # Win message
        if self.won and not self.game_over:
            win_msg = "You reached 2048! Keep playing?"
            msg_x = (self.width - len(win_msg)) // 2
            msg_y = inst_y + len(instructions) + 1
            self.stdscr.addstr(msg_y, msg_x, win_msg, curses.A_BOLD)
        
        self.stdscr.refresh()
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "YOU WIN!"
        else:
            title = "GAME OVER"
        
        extra_info = [f"Final Score: {self.score}"]
        if self.won:
            extra_info.append("You reached 2048!")
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )
