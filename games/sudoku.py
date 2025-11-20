"""Sudoku puzzle game implementation."""

import curses
import random
from typing import List, Tuple, Optional, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class SudokuGame(BaseGame):
    """Sudoku number puzzle game."""
    
    def __init__(self):
        super().__init__('sudoku', min_height=24, min_width=80)
        
        # Grid state
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.fixed = [[False for _ in range(9)] for _ in range(9)]
        
        # Cursor position
        self.cursor_row = 0
        self.cursor_col = 0
        
        # Game state
        self.mistakes = 0
        self.max_mistakes = 3
        self.hints_used = 0
        self.max_hints = 3
        
        # Difficulty
        difficulty = self.settings.get('sudoku', 'difficulty', 'normal')
        self.cells_to_remove = {'easy': 30, 'normal': 40, 'hard': 50}.get(difficulty, 40)
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize the game."""
        self._generate_puzzle()
        self.game_start_time = __import__('time').time()
    
    def _generate_puzzle(self):
        """Generate a Sudoku puzzle."""
        # Start with empty grid
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill diagonal 3x3 boxes (they don't depend on each other)
        for box in range(0, 9, 3):
            self._fill_box(box, box)
        
        # Fill remaining cells
        self._fill_remaining(0, 3)
        
        # Copy to solution
        self.solution = [row[:] for row in self.grid]
        
        # Remove cells to create puzzle
        self._remove_cells()
        
        # Mark fixed cells
        for i in range(9):
            for j in range(9):
                self.fixed[i][j] = (self.grid[i][j] != 0)
    
    def _fill_box(self, row: int, col: int):
        """Fill a 3x3 box with random valid numbers."""
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        idx = 0
        for i in range(3):
            for j in range(3):
                self.grid[row + i][col + j] = nums[idx]
                idx += 1
    
    def _fill_remaining(self, row: int, col: int) -> bool:
        """Fill remaining cells recursively."""
        if col >= 9 and row < 8:
            row += 1
            col = 0
        if row >= 9 and col >= 9:
            return True
        
        if row < 3:
            if col < 3:
                col = 3
        elif row < 6:
            if col == int(row // 3) * 3:
                col += 3
        else:
            if col == 6:
                row += 1
                col = 0
                if row >= 9:
                    return True
        
        for num in range(1, 10):
            if self._is_safe(row, col, num):
                self.grid[row][col] = num
                if self._fill_remaining(row, col + 1):
                    return True
                self.grid[row][col] = 0
        
        return False
    
    def _is_safe(self, row: int, col: int, num: int) -> bool:
        """Check if number can be placed at position."""
        # Check row
        if num in self.grid[row]:
            return False
        
        # Check column
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.grid[i][j] == num:
                    return False
        
        return True
    
    def _remove_cells(self):
        """Remove cells to create puzzle."""
        count = self.cells_to_remove
        while count > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                count -= 1
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif not self.paused:
            # Movement
            if key == curses.KEY_UP and self.cursor_row > 0:
                self.cursor_row -= 1
            elif key == curses.KEY_DOWN and self.cursor_row < 8:
                self.cursor_row += 1
            elif key == curses.KEY_LEFT and self.cursor_col > 0:
                self.cursor_col -= 1
            elif key == curses.KEY_RIGHT and self.cursor_col < 8:
                self.cursor_col += 1
            
            # Number input
            elif key >= ord('1') and key <= ord('9'):
                if not self.fixed[self.cursor_row][self.cursor_col]:
                    num = int(chr(key))
                    self.grid[self.cursor_row][self.cursor_col] = num
                    
                    # Check if correct
                    if num != self.solution[self.cursor_row][self.cursor_col]:
                        self.mistakes += 1
                        if self.mistakes >= self.max_mistakes:
                            self.game_over = True
                    
                    # Check if puzzle complete
                    if self._check_complete():
                        self.won = True
                        self.game_over = True
                        self._calculate_score()
            
            # Clear cell
            elif key == ord(' ') or key == ord('0') or key == curses.KEY_BACKSPACE:
                if not self.fixed[self.cursor_row][self.cursor_col]:
                    self.grid[self.cursor_row][self.cursor_col] = 0
            
            # Hint
            elif key == ord('h'):
                if self.hints_used < self.max_hints:
                    if not self.fixed[self.cursor_row][self.cursor_col]:
                        self.grid[self.cursor_row][self.cursor_col] = \
                            self.solution[self.cursor_row][self.cursor_col]
                        self.hints_used += 1
        
        return True
    
    def _check_complete(self) -> bool:
        """Check if puzzle is complete and correct."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != self.solution[i][j]:
                    return False
        return True
    
    def _calculate_score(self):
        """Calculate final score."""
        import time
        elapsed = time.time() - self.game_start_time
        
        # Base score
        base_score = 1000
        
        # Time bonus (faster = higher score)
        time_bonus = max(0, 500 - int(elapsed / 2))
        
        # Mistake penalty
        mistake_penalty = self.mistakes * 100
        
        # Hint penalty
        hint_penalty = self.hints_used * 50
        
        self.score = max(0, base_score + time_bonus - mistake_penalty - hint_penalty)
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        pass  # Sudoku is turn-based
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        title = "SUDOKU"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Draw grid
        grid_start_y = 4
        grid_start_x = (self.width - 37) // 2
        
        # Grid lines
        for i in range(10):
            # Horizontal lines
            y = grid_start_y + i * 2
            char = '═' if i % 3 == 0 else '─'
            line = char * 37
            if i < 10:
                self.stdscr.addstr(y, grid_start_x, line)
            
            # Vertical lines (drawn with cells)
        
        # Draw cells
        for i in range(9):
            for j in range(9):
                cell_y = grid_start_y + i * 2 + 1
                cell_x = grid_start_x + j * 4 + 2
                
                # Cell value
                num = self.grid[i][j]
                
                # Determine attribute
                attr = curses.A_NORMAL
                if i == self.cursor_row and j == self.cursor_col:
                    attr = curses.A_REVERSE
                
                if self.fixed[i][j]:
                    attr |= curses.A_BOLD
                elif num != 0 and num != self.solution[i][j]:
                    attr |= curses.A_DIM  # Wrong number
                
                # Draw
                display = str(num) if num != 0 else " "
                self.stdscr.addstr(cell_y, cell_x, display, attr)
                
                # Vertical separators
                if j % 3 == 2 and j < 8:
                    self.stdscr.addstr(cell_y, cell_x + 2, "║")
        
        # Info
        info_y = grid_start_y + 19
        info_x = 5
        
        self.stdscr.addstr(info_y, info_x, f"Mistakes: {self.mistakes}/{self.max_mistakes}")
        info_y += 1
        self.stdscr.addstr(info_y, info_x, f"Hints Available: {self.max_hints - self.hints_used}")
        
        # Instructions
        inst_y = info_y + 2
        instructions = [
            "Arrow Keys: Move cursor",
            "1-9: Place number",
            "0/Space: Clear cell",
            "H: Use hint",
            "P: Pause | Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, info_x, inst, curses.A_DIM)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        import time
        state.update({
            'mistakes': self.mistakes,
            'hints_used': self.hints_used,
            'time': time.time() - self.game_start_time if self.game_start_time else 0,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'grid': self.grid,
            'solution': self.solution,
            'fixed': self.fixed,
            'cursor_row': self.cursor_row,
            'cursor_col': self.cursor_col,
            'mistakes': self.mistakes,
            'hints_used': self.hints_used,
            'game_start_time': self.game_start_time,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.grid = state.get('grid', [[0]*9 for _ in range(9)])
        self.solution = state.get('solution', [[0]*9 for _ in range(9)])
        self.fixed = state.get('fixed', [[False]*9 for _ in range(9)])
        self.cursor_row = state.get('cursor_row', 0)
        self.cursor_col = state.get('cursor_col', 0)
        self.mistakes = state.get('mistakes', 0)
        self.hints_used = state.get('hints_used', 0)
        self.game_start_time = state.get('game_start_time', __import__('time').time())
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "PUZZLE SOLVED!"
        else:
            title = "GAME OVER"
        
        import time
        elapsed = time.time() - self.game_start_time if self.game_start_time else 0
        
        extra_info = [
            f"Time: {int(elapsed)}s",
            f"Mistakes: {self.mistakes}",
            f"Hints Used: {self.hints_used}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

