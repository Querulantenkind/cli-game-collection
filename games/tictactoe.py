"""Tic-Tac-Toe game with AI opponent."""

import curses
import random
from typing import List, Tuple, Optional, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class TicTacToeGame(BaseGame):
    """Tic-Tac-Toe game for the terminal."""
    
    def __init__(self):
        super().__init__('tictactoe', min_height=24, min_width=80)
        
        # Game state
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X = player, O = AI
        self.cursor_x = 1
        self.cursor_y = 1
        self.game_mode = 'ai'  # 'ai' or '2player'
        self.winner = None
        self.moves_made = 0
        
        # AI difficulty from settings
        difficulty = self.settings.get('tictactoe', 'difficulty', 'normal')
        self.ai_level = {'easy': 0.3, 'normal': 0.7, 'hard': 1.0}.get(difficulty, 0.7)
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize the game."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.cursor_x = 1
        self.cursor_y = 1
        self.winner = None
        self.moves_made = 0
    
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
        
        if key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(2, self.cursor_y + 1)
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(2, self.cursor_x + 1)
        elif key == ord(' ') or key == ord('\n') or key == ord('\r'):
            # Place mark
            if self.board[self.cursor_y][self.cursor_x] == ' ':
                self._make_move(self.cursor_y, self.cursor_x)
        elif key == ord('m'):
            # Toggle mode
            self.game_mode = '2player' if self.game_mode == 'ai' else 'ai'
            self._init_game()
        
        return True
    
    def _make_move(self, y: int, x: int):
        """Make a move on the board."""
        if self.board[y][x] == ' ':
            self.board[y][x] = self.current_player
            self.moves_made += 1
            
            # Check for winner
            self.winner = self._check_winner()
            if self.winner or self.moves_made == 9:
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
            time.sleep(0.3)
            self._ai_move()
    
    def _ai_move(self):
        """Make an AI move."""
        # Use random chance based on difficulty
        if random.random() < self.ai_level:
            # Smart move
            move = self._get_best_move()
        else:
            # Random move
            move = self._get_random_move()
        
        if move:
            self._make_move(move[0], move[1])
    
    def _get_best_move(self) -> Optional[Tuple[int, int]]:
        """Get the best move using minimax algorithm."""
        # Check for winning move
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == ' ':
                    self.board[y][x] = 'O'
                    if self._check_winner() == 'O':
                        self.board[y][x] = ' '
                        return (y, x)
                    self.board[y][x] = ' '
        
        # Check for blocking move
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == ' ':
                    self.board[y][x] = 'X'
                    if self._check_winner() == 'X':
                        self.board[y][x] = ' '
                        return (y, x)
                    self.board[y][x] = ' '
        
        # Take center if available
        if self.board[1][1] == ' ':
            return (1, 1)
        
        # Take a corner
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for y, x in corners:
            if self.board[y][x] == ' ':
                return (y, x)
        
        # Take any available space
        return self._get_random_move()
    
    def _get_random_move(self) -> Optional[Tuple[int, int]]:
        """Get a random valid move."""
        available = []
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == ' ':
                    available.append((y, x))
        return random.choice(available) if available else None
    
    def _check_winner(self) -> Optional[str]:
        """Check if there's a winner."""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for x in range(3):
            if self.board[0][x] == self.board[1][x] == self.board[2][x] != ' ':
                return self.board[0][x]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        
        return None
    
    def _calculate_score(self) -> int:
        """Calculate score based on outcome."""
        if self.winner == 'X':
            # Player wins - score based on how quickly
            return max(100 - (self.moves_made * 10), 10)
        elif self.winner == 'O':
            # AI wins
            return 0
        else:
            # Draw
            return 20
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        title = f"Tic-Tac-Toe - {self.game_mode.upper()} Mode"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Draw board
        board_start_y = 5
        board_start_x = (self.width - 17) // 2
        
        # Draw grid
        for i in range(4):
            # Horizontal lines
            self.stdscr.addstr(board_start_y + i * 2, board_start_x, 
                             "─────┼─────┼─────" if i < 3 else "")
        
        for i in range(3):
            # Vertical separators and content
            for j in range(3):
                cell_y = board_start_y + i * 2 - 1
                cell_x = board_start_x + j * 6 + 2
                
                # Cell content
                mark = self.board[i][j]
                attr = curses.A_NORMAL
                
                # Highlight cursor position
                if i == self.cursor_y and j == self.cursor_x:
                    attr = curses.A_REVERSE
                
                # Draw mark
                if mark == 'X':
                    attr |= curses.A_BOLD
                
                self.stdscr.addstr(cell_y, cell_x, f"  {mark}  ", attr)
        
        # Current player
        turn_text = f"Current: {self.current_player} {'(You)' if self.current_player == 'X' else '(AI)' if self.game_mode == 'ai' else '(P2)'}"
        self.stdscr.addstr(board_start_y + 8, (self.width - len(turn_text)) // 2, turn_text)
        
        # Score
        if self.score > 0:
            score_text = f"Score: {self.score}"
            self.stdscr.addstr(board_start_y + 10, (self.width - len(score_text)) // 2, score_text)
        
        # Instructions
        inst_y = board_start_y + 12
        instructions = [
            "Arrow Keys: Move cursor",
            "Space/Enter: Place mark",
            "M: Toggle AI/2-Player mode",
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

