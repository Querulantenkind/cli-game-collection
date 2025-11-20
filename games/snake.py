"""Snake game implementation."""

import curses
import random
import time
from typing import List, Tuple
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class SnakeGame(BaseGame):
    """Classic Snake game for the terminal."""
    
    def __init__(self):
        super().__init__('snake', min_height=24, min_width=80)
        
        self.direction = (1, 0)  # Right
        self.snake = [(10, 10), (10, 9), (10, 8)]
        self.food = None
        
        # Base speed, adjusted by settings
        self.base_speed = 0.1
        self.game_speed = self.base_speed * self._get_game_speed()
        self.last_move_time = 0
    
    def _get_input_timeout(self) -> int:
        """Get input timeout."""
        return 100
    
    def _init_game(self):
        """Initialize game state."""
        self._spawn_food()
    
    def _spawn_food(self):
        """Spawn food at a random location."""
        while True:
            food_y = random.randint(1, self.height - 2)
            food_x = random.randint(1, self.width - 2)
            if (food_y, food_x) not in self.snake:
                self.food = (food_y, food_x)
                break
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif key == curses.KEY_UP and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == curses.KEY_DOWN and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif key == curses.KEY_LEFT and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == curses.KEY_RIGHT and self.direction != (0, -1):
            self.direction = (0, 1)
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        # Move snake at fixed intervals
        self.last_move_time += delta_time
        if self.last_move_time < self.game_speed:
            return
        self.last_move_time = 0
        
        # Move snake
        head_y, head_x = self.snake[0]
        new_head = (head_y + self.direction[0], head_x + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 1 or new_head[0] >= self.height - 1 or
            new_head[1] < 1 or new_head[1] >= self.width - 1):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self._spawn_food()
        else:
            self.snake.pop()
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        # Draw border
        self.stdscr.border(0)
        
        # Draw snake
        for i, (y, x) in enumerate(self.snake):
            if i == 0:
                self.stdscr.addch(y, x, 'O', curses.A_BOLD)  # Head
            else:
                self.stdscr.addch(y, x, 'o')
        
        # Draw food
        if self.food:
            self.stdscr.addch(self.food[0], self.food[1], '*', curses.A_BOLD)
        
        # Draw info bar
        self._draw_info_bar()
        
        # Draw controls
        controls = "Q: Quit | P: Pause | Arrow Keys: Move"
        self.stdscr.addstr(0, self.width - len(controls) - 1, controls)
        
        # Draw pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        extra_info = []
        if not is_new_high and self.high_score is not None:
            extra_info.append(f"High Score: {self.high_score}")
        
        draw_game_over_screen(
            self.stdscr, "GAME OVER", self.score,
            self.high_score, is_new_high, extra_info
        )
