"""Breakout/Arkanoid brick breaker game implementation."""

import curses
import random
from typing import List, Tuple
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class BreakoutGame(BaseGame):
    """Breakout/Arkanoid game for the terminal."""
    
    def __init__(self):
        super().__init__('breakout', min_height=24, min_width=100)
        
        self.board_width = 50
        self.board_height = 20
        
        # Paddle
        self.paddle_x = self.board_width // 2 - 3
        self.paddle_width = 6
        
        # Ball
        self.ball_x = self.board_width // 2
        self.ball_y = self.board_height - 3
        self.ball_vx = random.choice([-1, 1])
        self.ball_vy = -1
        
        # Bricks
        self.bricks = []
        self.brick_rows = 4
        self.brick_cols = 10
        
        # Game state
        self.lives = 3
        
        # Game speed
        self.base_speed = 0.1
        self.game_speed = self.base_speed * self._get_game_speed()
        self.last_move_time = 0
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize bricks."""
        self._init_bricks()
    
    def _init_bricks(self):
        """Initialize brick layout."""
        self.bricks = []
        brick_width = 4
        brick_spacing = 1
        start_y = 2
        start_x = 2
        
        for row in range(self.brick_rows):
            for col in range(self.brick_cols):
                x = start_x + col * (brick_width + brick_spacing)
                y = start_y + row
                if x + brick_width < self.board_width:
                    self.bricks.append({
                        'x': x,
                        'y': y,
                        'width': brick_width,
                        'alive': True
                    })
    
    def _update_ball(self):
        """Update ball position and handle collisions."""
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy
        
        # Wall collisions
        if self.ball_x <= 0 or self.ball_x >= self.board_width - 1:
            self.ball_vx = -self.ball_vx
            self.ball_x = max(0, min(self.board_width - 1, self.ball_x))
        
        if self.ball_y <= 0:
            self.ball_vy = -self.ball_vy
            self.ball_y = 0
        
        # Bottom - lose life
        if self.ball_y >= self.board_height - 1:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                # Reset ball
                self.ball_x = self.board_width // 2
                self.ball_y = self.board_height - 3
                self.ball_vx = random.choice([-1, 1])
                self.ball_vy = -1
        
        # Paddle collision
        if (self.ball_y >= self.board_height - 3 and 
            self.paddle_x <= self.ball_x < self.paddle_x + self.paddle_width):
            self.ball_vy = -abs(self.ball_vy)
            hit_pos = (self.ball_x - self.paddle_x) / self.paddle_width
            self.ball_vx = int((hit_pos - 0.5) * 2)
            if self.ball_vx == 0:
                self.ball_vx = random.choice([-1, 1])
            self.ball_y = self.board_height - 3
        
        # Brick collisions
        for brick in self.bricks:
            if not brick['alive']:
                continue
            
            if (brick['y'] <= self.ball_y < brick['y'] + 1 and
                brick['x'] <= self.ball_x < brick['x'] + brick['width']):
                brick['alive'] = False
                self.ball_vy = -self.ball_vy
                self.score += 10
                break
    
    def _check_win(self):
        """Check if all bricks are destroyed."""
        if all(not brick['alive'] for brick in self.bricks):
            self.won = True
            self.game_over = True
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif not self.paused:
            if key == curses.KEY_LEFT or key == ord('a'):
                self.paddle_x = max(0, self.paddle_x - 2)
            elif key == curses.KEY_RIGHT or key == ord('d'):
                self.paddle_x = min(self.board_width - self.paddle_width, 
                                   self.paddle_x + 2)
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
        self._check_win()
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        board_start_y = 2
        board_start_x = (self.width - self.board_width) // 2
        
        # Border
        for y in range(self.board_height + 2):
            self.stdscr.addch(board_start_y + y, board_start_x - 1, '|')
            self.stdscr.addch(board_start_y + y, board_start_x + self.board_width, '|')
        for x in range(self.board_width + 2):
            self.stdscr.addch(board_start_y - 1, board_start_x - 1 + x, '-')
            self.stdscr.addch(board_start_y + self.board_height, board_start_x - 1 + x, '-')
        
        # Draw bricks
        for brick in self.bricks:
            if brick['alive']:
                for i in range(brick['width']):
                    self.stdscr.addch(board_start_y + brick['y'], board_start_x + brick['x'] + i, 
                                    '#', curses.A_BOLD)
        
        # Draw paddle
        for i in range(self.paddle_width):
            self.stdscr.addch(board_start_y + self.board_height - 2, board_start_x + self.paddle_x + i, 
                            '=', curses.A_BOLD)
        
        # Draw ball
        self.stdscr.addch(board_start_y + int(self.ball_y), board_start_x + int(self.ball_x), 'O', 
                        curses.A_BOLD)
        
        # Info
        self._draw_info_bar({'Lives': self.lives})
        
        # Instructions
        inst_y = board_start_y + self.board_height + 2
        instructions = [
            "← → or A/D: Move paddle",
            "P: Pause",
            "Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, 2, inst)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "YOU WIN!"
        else:
            title = "GAME OVER"
        
        extra_info = [
            f"Lives Remaining: {self.lives}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )
