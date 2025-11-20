"""Pong game implementation."""

import curses
import time
import random
from typing import Tuple, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class PongGame(BaseGame):
    """Classic Pong game for the terminal."""
    
    def __init__(self):
        super().__init__('pong', min_height=24, min_width=100)
        
        self.board_height = 20
        self.board_width = 60
        self.paddle_height = 3
        self.paddle_speed = 1
        
        # Left paddle (player 1)
        self.paddle1_y = self.board_height // 2 - self.paddle_height // 2
        # Right paddle (player 2 or AI)
        self.paddle2_y = self.board_height // 2 - self.paddle_height // 2
        
        # Ball
        self.ball_x = self.board_width // 2
        self.ball_y = self.board_height // 2
        self.ball_vx = 1
        self.ball_vy = random.choice([-1, 1])
        
        # Scores
        self.score1 = 0
        self.score2 = 0
        self.max_score = 5
        self.winner = None
        
        # AI
        self.ai_mode = True
        self.ai_difficulty = 0.7
        
        # Game speed
        self.base_speed = 0.05
        self.game_speed = self.base_speed * self._get_game_speed()
        self.last_move_time = 0
    
    def _get_input_timeout(self) -> int:
        return int(self.game_speed * 1000)
    
    def _init_game(self):
        """Initialize game state."""
        pass  # Already initialized
    
    def _update_ball(self):
        """Update ball position and handle collisions."""
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        
        # Top/bottom wall collision
        if self.ball_y <= 0 or self.ball_y >= self.board_height - 1:
            self.ball_vy = -self.ball_vy
            self.ball_y = max(0, min(self.board_height - 1, self.ball_y))
        
        # Paddle collisions
        if (self.ball_x == 0 and 
            self.paddle1_y <= self.ball_y < self.paddle1_y + self.paddle_height):
            self.ball_vx = abs(self.ball_vx)
            hit_pos = (self.ball_y - self.paddle1_y) / self.paddle_height
            self.ball_vy = int((hit_pos - 0.5) * 2)
            if self.ball_vy == 0:
                self.ball_vy = random.choice([-1, 1])
        
        if (self.ball_x == self.board_width - 1 and
            self.paddle2_y <= self.ball_y < self.paddle2_y + self.paddle_height):
            self.ball_vx = -abs(self.ball_vx)
            hit_pos = (self.ball_y - self.paddle2_y) / self.paddle_height
            self.ball_vy = int((hit_pos - 0.5) * 2)
            if self.ball_vy == 0:
                self.ball_vy = random.choice([-1, 1])
    
    def _move_ai(self):
        """Move AI paddle to track the ball."""
        target_y = self.ball_y - self.paddle_height // 2
        
        if random.random() > self.ai_difficulty:
            target_y += random.randint(-2, 2)
        
        if target_y < self.paddle2_y:
            self.paddle2_y = max(0, self.paddle2_y - self.paddle_speed)
        elif target_y > self.paddle2_y:
            self.paddle2_y = min(self.board_height - self.paddle_height,
                                self.paddle2_y + self.paddle_speed)
    
    def _reset_ball(self):
        """Reset ball to center after scoring."""
        self.ball_x = self.board_width // 2
        self.ball_y = self.board_height // 2
        self.ball_vx = random.choice([-1, 1])
        self.ball_vy = random.choice([-1, 1])
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif key == ord('a'):
            self.ai_mode = not self.ai_mode
        elif not self.paused:
            if key == ord('w') or key == curses.KEY_UP:
                self.paddle1_y = max(0, self.paddle1_y - self.paddle_speed)
            elif key == ord('s') or key == curses.KEY_DOWN:
                self.paddle1_y = min(self.board_height - self.paddle_height, 
                                    self.paddle1_y + self.paddle_speed)
            
            if not self.ai_mode:
                if key == ord('i'):
                    self.paddle2_y = max(0, self.paddle2_y - self.paddle_speed)
                elif key == ord('k'):
                    self.paddle2_y = min(self.board_height - self.paddle_height,
                                        self.paddle2_y + self.paddle_speed)
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        if self.paused:
            return
        
        # Move ball at fixed intervals
        self.last_move_time += delta_time
        if self.last_move_time < self.game_speed:
            return
        self.last_move_time = 0
        
        self._update_ball()
        
        # AI movement
        if self.ai_mode:
            self._move_ai()
        
        # Check scoring
        if self.ball_x < 0:
            self.score2 += 1
            self._reset_ball()
        elif self.ball_x >= self.board_width:
            self.score1 += 1
            self._reset_ball()
        
        # Check game over
        if self.score1 >= self.max_score:
            self.game_over = True
            self.winner = 1
            self.won = True
        elif self.score2 >= self.max_score:
            self.game_over = True
            self.winner = 2
            self.won = False
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        board_start_y = 2
        board_start_x = (self.width - self.board_width) // 2
        
        # Draw board border
        for y in range(self.board_height + 2):
            self.stdscr.addch(board_start_y + y, board_start_x - 1, '|')
            self.stdscr.addch(board_start_y + y, board_start_x + self.board_width, '|')
        for x in range(self.board_width + 2):
            self.stdscr.addch(board_start_y - 1, board_start_x - 1 + x, '-')
            self.stdscr.addch(board_start_y + self.board_height, board_start_x - 1 + x, '-')
        
        # Draw paddles
        for i in range(self.paddle_height):
            self.stdscr.addch(board_start_y + self.paddle1_y + i, board_start_x, '|', curses.A_BOLD)
            self.stdscr.addch(board_start_y + self.paddle2_y + i, board_start_x + self.board_width - 1, 
                            '|', curses.A_BOLD)
        
        # Draw ball
        self.stdscr.addch(board_start_y + int(self.ball_y), board_start_x + int(self.ball_x), 'O', 
                        curses.A_BOLD)
        
        # Draw scores
        score1_text = f"P1: {self.score1}"
        score2_text = f"P2: {self.score2}"
        self.stdscr.addstr(board_start_y - 1, board_start_x + 2, score1_text)
        self.stdscr.addstr(board_start_y - 1, board_start_x + self.board_width - len(score2_text) - 2, 
                         score2_text)
        
        # Info
        info_x = board_start_x + self.board_width + 5
        mode_text = "AI Mode" if self.ai_mode else "2-Player"
        self._draw_info_bar({'Mode': mode_text, 'First to': self.max_score})
        
        # Controls
        controls = [
            "W/S or ↑↓: P1",
            "I/K: P2 (2P)",
            "A: Toggle AI",
            "P: Pause",
            "Q: Quit"
        ]
        for i, control in enumerate(controls):
            self.stdscr.addstr(10 + i, info_x, control)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'score1': self.score1,
            'score2': self.score2,
        })
        return state
    
    def _save_results(self) -> bool:
        """Save results - use player 1 score."""
        self.score = self.score1
        return super()._save_results()
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.winner == 1:
            title = "PLAYER 1 WINS!"
        else:
            title = "PLAYER 2 WINS!"
        
        extra_info = [f"Final Score: {self.score1} - {self.score2}"]
        
        draw_game_over_screen(
            self.stdscr, title, self.score1,
            self.high_score, is_new_high, extra_info
        )
