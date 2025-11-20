"""Tetris game implementation."""

import curses
import random
from typing import List, Tuple, Optional, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


# Tetromino shapes (rotations included)
TETROMINOES = {
    'I': [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)],
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ],
    'T': [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)],
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 2), (1, 1), (1, 2), (2, 1)],
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)],
    ],
    'L': [
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
}


class TetrisGame(BaseGame):
    """Classic Tetris game for the terminal."""
    
    def __init__(self):
        super().__init__('tetris', min_height=24, min_width=100)
        
        self.board_width = 10
        self.board_height = 20
        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.current_piece = None
        self.current_piece_type = None
        self.current_rotation = 0
        self.current_pos = (0, 0)
        
        # Starting level from settings
        starting_level = self.settings.get('tetris', 'starting_level', 1)
        self.level = starting_level
        self.lines_cleared = 0
        self.fall_time = 0
        
        # Base fall delay, adjusted by settings
        base_delay = 0.5
        speed_mult = self._get_game_speed()
        self.fall_delay = base_delay * speed_mult
    
    def _get_input_timeout(self) -> int:
        return 50  # 50ms for responsive controls
    
    def _init_game(self):
        """Initialize game state."""
        self._spawn_piece()
    
    def _spawn_piece(self):
        """Spawn a new tetromino at the top."""
        piece_type = random.choice(list(TETROMINOES.keys()))
        self.current_piece_type = piece_type
        self.current_rotation = 0
        self.current_piece = TETROMINOES[piece_type][0]
        # Start at top center
        self.current_pos = (0, self.board_width // 2 - 1)
        
        # Check if game over (can't place piece)
        if not self._is_valid_position():
            self.game_over = True
    
    def _is_valid_position(self, piece=None, pos=None):
        """Check if current piece position is valid."""
        if piece is None:
            piece = self.current_piece
        if pos is None:
            pos = self.current_pos
        
        for dy, dx in piece:
            y, x = pos[0] + dy, pos[1] + dx
            if x < 0 or x >= self.board_width or y >= self.board_height:
                return False
            if y >= 0 and self.board[y][x] != 0:
                return False
        return True
    
    def _move_piece(self, dy, dx):
        """Try to move the current piece. Returns True if successful."""
        new_pos = (self.current_pos[0] + dy, self.current_pos[1] + dx)
        old_pos = self.current_pos
        self.current_pos = new_pos
        
        if not self._is_valid_position():
            self.current_pos = old_pos
            return False
        return True
    
    def _rotate_piece(self):
        """Rotate the current piece."""
        rotations = TETROMINOES[self.current_piece_type]
        new_rotation = (self.current_rotation + 1) % len(rotations)
        new_piece = rotations[new_rotation]
        
        old_piece = self.current_piece
        old_rotation = self.current_rotation
        
        self.current_piece = new_piece
        self.current_rotation = new_rotation
        
        if not self._is_valid_position():
            self.current_piece = old_piece
            self.current_rotation = old_rotation
    
    def _lock_piece(self):
        """Lock the current piece into the board."""
        for dy, dx in self.current_piece:
            y, x = self.current_pos[0] + dy, self.current_pos[1] + dx
            if y >= 0:
                self.board[y][x] = 1
    
    def _clear_lines(self):
        """Clear completed lines and update score."""
        lines_to_clear = []
        for y in range(self.board_height):
            if all(self.board[y][x] != 0 for x in range(self.board_width)):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(self.board_width)])
        
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            # Score: 100 * lines^2 (more lines = exponentially more points)
            self.score += 100 * len(lines_to_clear) ** 2
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
            # Increase speed with level (but respect settings multiplier)
            base_delay = max(0.1, 0.5 - (self.level - 1) * 0.05)
            speed_mult = self._get_game_speed()
            self.fall_delay = base_delay * speed_mult
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif not self.paused:
            if key == curses.KEY_LEFT:
                self._move_piece(0, -1)
            elif key == curses.KEY_RIGHT:
                self._move_piece(0, 1)
            elif key == curses.KEY_DOWN:
                if not self._move_piece(1, 0):
                    self._lock_piece()
                    self._clear_lines()
                    self._spawn_piece()
            elif key == ord(' ') or key == curses.KEY_UP:
                self._rotate_piece()
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        if self.paused:
            return
        
        # Auto-fall
        self.fall_time += delta_time
        if self.fall_time >= self.fall_delay:
            self.fall_time = 0
            if not self._move_piece(1, 0):
                self._lock_piece()
                self._clear_lines()
                self._spawn_piece()
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        board_start_y = 2
        board_start_x = (self.width - self.board_width * 2) // 2
        
        # Draw border around board
        for y in range(self.board_height + 2):
            self.stdscr.addch(board_start_y + y, board_start_x - 1, '|')
            self.stdscr.addch(board_start_y + y, board_start_x + self.board_width * 2, '|')
        for x in range(self.board_width * 2 + 2):
            self.stdscr.addch(board_start_y - 1, board_start_x - 1 + x, '-')
            self.stdscr.addch(board_start_y + self.board_height, board_start_x - 1 + x, '-')
        
        # Draw board
        for y in range(self.board_height):
            for x in range(self.board_width):
                if self.board[y][x] != 0:
                    self.stdscr.addstr(board_start_y + y, board_start_x + x * 2, '██')
        
        # Draw current piece
        if self.current_piece:
            for dy, dx in self.current_piece:
                py, px = self.current_pos[0] + dy, self.current_pos[1] + dx
                if 0 <= py < self.board_height and 0 <= px < self.board_width:
                    self.stdscr.addstr(board_start_y + py, board_start_x + px * 2, '██', curses.A_BOLD)
        
        # Draw info
        info_x = board_start_x + self.board_width * 2 + 5
        self._draw_info_bar({'Level': self.level, 'Lines': self.lines_cleared})
        
        # Draw controls
        controls = [
            "← → : Move",
            "↓ : Soft drop",
            "↑/Space: Rotate",
            "P: Pause",
            "Q: Quit"
        ]
        for i, control in enumerate(controls):
            self.stdscr.addstr(10 + i, info_x, control)
        
        # Draw pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'level': self.level,
            'lines_cleared': self.lines_cleared,
        })
        return state
    
    def _save_results(self) -> bool:
        """Save high score with metadata."""
        # Call parent to record stats
        is_new_high = super()._save_results()
        
        # Also save with metadata
        self.high_score_manager.add_score(
            'tetris', 
            self.score,
            level=self.level,
            lines=self.lines_cleared
        )
        
        return is_new_high
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        extra_info = [
            f"Level Reached: {self.level}",
            f"Lines Cleared: {self.lines_cleared}"
        ]
        
        draw_game_over_screen(
            self.stdscr, "GAME OVER", self.score,
            self.high_score, is_new_high, extra_info
        )
