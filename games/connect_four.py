"""Connect Four game with AI opponent."""

import curses
import random
from typing import List, Tuple, Optional, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class ConnectFourGame(BaseGame):
    """Connect Four game for the terminal."""
    
    def __init__(self):
        super().__init__('connect_four', min_height=24, min_width=80)
        
        # Game constants
        self.ROWS = 6
        self.COLS = 7
        
        # Game state
        self.board = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 'X'  # X = player, O = AI
        self.cursor_col = 3
        self.game_mode = 'ai'  # 'ai' or '2player'
        self.winner = None
        self.moves_made = 0
        self.winning_positions = []
        
        # AI difficulty from settings
        difficulty = self.settings.get('connect_four', 'difficulty', 'normal')
        self.ai_level = {'easy': 0.3, 'normal': 0.7, 'hard': 1.0}.get(difficulty, 0.7)
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize the game."""
        self.board = [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 'X'
        self.cursor_col = 3
        self.winner = None
        self.moves_made = 0
        self.winning_positions = []
    
    def _handle_input(self, key: int) -> bool:
        """Handle player input."""
        if key == ord('q'):
            self.game_over = True
            return False
        
        if key == ord('p'):
            self.paused = not self.paused
            return True
        
        if self.paused:
            return True
        
        # Can only move if it's player's turn
        if self.game_mode == 'ai' and self.current_player == 'O':
            return True
        
        if key == curses.KEY_LEFT:
            self.cursor_col = max(0, self.cursor_col - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_col = min(self.COLS - 1, self.cursor_col + 1)
        elif key == ord(' ') or key == ord('\n') or key == ord('\r'):
            # Drop piece
            if self._is_valid_move(self.cursor_col):
                self._make_move(self.cursor_col)
        elif key == ord('m'):
            # Toggle mode
            self.game_mode = '2player' if self.game_mode == 'ai' else 'ai'
            self._init_game()
        
        return True
    
    def _is_valid_move(self, col: int) -> bool:
        """Check if a column has space."""
        return self.board[0][col] == ' '
    
    def _get_drop_row(self, col: int) -> int:
        """Get the row where a piece would land in a column."""
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == ' ':
                return row
        return -1
    
    def _make_move(self, col: int):
        """Make a move in the specified column."""
        row = self._get_drop_row(col)
        if row >= 0:
            self.board[row][col] = self.current_player
            self.moves_made += 1
            
            # Check for winner
            self.winner, self.winning_positions = self._check_winner(row, col)
            if self.winner or self.moves_made == self.ROWS * self.COLS:
                self.game_over = True
                self.won = (self.winner == 'X')
                self.score = self._calculate_score()
            else:
                # Switch player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        # If it's AI's turn, make a move
        if self.game_mode == 'ai' and self.current_player == 'O' and not self.game_over:
            # Small delay for AI move
            import time
            time.sleep(0.5)
            self._ai_move()
    
    def _ai_move(self):
        """Make an AI move."""
        # Use random chance based on difficulty
        if random.random() < self.ai_level:
            # Smart move
            col = self._get_best_move()
        else:
            # Random move
            col = self._get_random_move()
        
        if col is not None:
            self._make_move(col)
    
    def _get_best_move(self) -> Optional[int]:
        """Get the best move using heuristics."""
        # Check for winning move
        for col in range(self.COLS):
            if self._is_valid_move(col):
                row = self._get_drop_row(col)
                self.board[row][col] = 'O'
                winner, _ = self._check_winner(row, col)
                self.board[row][col] = ' '
                if winner == 'O':
                    return col
        
        # Check for blocking move
        for col in range(self.COLS):
            if self._is_valid_move(col):
                row = self._get_drop_row(col)
                self.board[row][col] = 'X'
                winner, _ = self._check_winner(row, col)
                self.board[row][col] = ' '
                if winner == 'X':
                    return col
        
        # Prefer center columns
        center_cols = [3, 2, 4, 1, 5, 0, 6]
        for col in center_cols:
            if self._is_valid_move(col):
                return col
        
        return self._get_random_move()
    
    def _get_random_move(self) -> Optional[int]:
        """Get a random valid move."""
        valid_cols = [col for col in range(self.COLS) if self._is_valid_move(col)]
        return random.choice(valid_cols) if valid_cols else None
    
    def _check_winner(self, last_row: int, last_col: int) -> Tuple[Optional[str], List[Tuple[int, int]]]:
        """Check if there's a winner starting from the last move."""
        player = self.board[last_row][last_col]
        if player == ' ':
            return None, []
        
        # Check all four directions
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal down-right
            (1, -1)   # Diagonal down-left
        ]
        
        for dy, dx in directions:
            positions = [(last_row, last_col)]
            
            # Check forward direction
            r, c = last_row + dy, last_col + dx
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == player:
                positions.append((r, c))
                r += dy
                c += dx
            
            # Check backward direction
            r, c = last_row - dy, last_col - dx
            while 0 <= r < self.ROWS and 0 <= c < self.COLS and self.board[r][c] == player:
                positions.append((r, c))
                r -= dy
                c -= dx
            
            if len(positions) >= 4:
                return player, positions
        
        return None, []
    
    def _calculate_score(self) -> int:
        """Calculate score based on outcome."""
        if self.winner == 'X':
            # Player wins - score based on how quickly
            return max(200 - (self.moves_made * 5), 50)
        elif self.winner == 'O':
            # AI wins
            return 0
        else:
            # Draw
            return 10
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        title = f"Connect Four - {self.game_mode.upper()} Mode"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Draw board
        board_start_y = 5
        board_start_x = (self.width - (self.COLS * 4 + 1)) // 2
        
        # Draw cursor (floating piece)
        if self.current_player == 'X' or self.game_mode == '2player':
            cursor_x = board_start_x + self.cursor_col * 4 + 2
            piece_char = self.current_player
            self.stdscr.addstr(board_start_y - 2, cursor_x, piece_char, curses.A_BOLD | curses.A_REVERSE)
            self.stdscr.addstr(board_start_y - 1, cursor_x, '|')
        
        # Draw board grid
        for row in range(self.ROWS):
            line = "│"
            for col in range(self.COLS):
                cell = self.board[row][col]
                attr = curses.A_NORMAL
                
                # Highlight winning positions
                if (row, col) in self.winning_positions:
                    attr = curses.A_BOLD | curses.A_REVERSE
                elif cell == 'X':
                    attr = curses.A_BOLD
                
                line += f" {cell} │"
            
            self.stdscr.addstr(board_start_y + row * 2, board_start_x, line, attr)
            
            # Draw horizontal separator
            if row < self.ROWS - 1:
                separator = "├" + "───┼" * (self.COLS - 1) + "───┤"
                self.stdscr.addstr(board_start_y + row * 2 + 1, board_start_x, separator)
        
        # Draw bottom border
        bottom = "└" + "───┴" * (self.COLS - 1) + "───┘"
        self.stdscr.addstr(board_start_y + self.ROWS * 2, board_start_x, bottom)
        
        # Draw column numbers
        col_nums = " " + "   ".join(str(i + 1) for i in range(self.COLS))
        self.stdscr.addstr(board_start_y + self.ROWS * 2 + 1, board_start_x, col_nums)
        
        # Current player
        turn_text = f"Current: {self.current_player} {'(You)' if self.current_player == 'X' else '(AI)' if self.game_mode == 'ai' else '(P2)'}"
        self.stdscr.addstr(board_start_y + self.ROWS * 2 + 3, (self.width - len(turn_text)) // 2, turn_text)
        
        # Score
        if self.score > 0:
            score_text = f"Score: {self.score}"
            self.stdscr.addstr(board_start_y + self.ROWS * 2 + 4, (self.width - len(score_text)) // 2, score_text)
        
        # Instructions
        inst_y = board_start_y + self.ROWS * 2 + 6
        instructions = [
            "← →: Move cursor",
            "Space/Enter: Drop piece",
            "M: Toggle AI/2-Player",
            "P: Pause | Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, (self.width - len(inst)) // 2, inst)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'moves': self.moves_made,
            'winner': self.winner,
            'mode': self.game_mode,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'board': self.board,
            'current_player': self.current_player,
            'cursor_col': self.cursor_col,
            'game_mode': self.game_mode,
            'moves_made': self.moves_made,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.board = state.get('board', [[' ' for _ in range(self.COLS)] for _ in range(self.ROWS)])
        self.current_player = state.get('current_player', 'X')
        self.cursor_col = state.get('cursor_col', 3)
        self.game_mode = state.get('game_mode', 'ai')
        self.moves_made = state.get('moves_made', 0)
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.winner == 'X':
            title = "YOU WIN!"
        elif self.winner == 'O':
            title = "AI WINS!" if self.game_mode == 'ai' else "PLAYER 2 WINS!"
        else:
            title = "DRAW!"
        
        extra_info = [
            f"Moves: {self.moves_made}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

