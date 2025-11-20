"""Frogger game implementation."""

import curses
import random
from typing import List, Tuple, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class FroggerGame(BaseGame):
    """Frogger - Cross the road and river safely."""
    
    def __init__(self):
        super().__init__('frogger', min_height=24, min_width=80)
        
        # Frog position
        self.frog_y = 0
        self.frog_x = 0
        
        # Game dimensions
        self.board_height = 13
        self.board_width = 40
        
        # Obstacles (cars/logs)
        self.lanes = []
        self.lives = 3
        self.level = 1
        self.reached_goals = 0
        self.goals_needed = 5
        
        # Timing
        self.last_update_time = 0
        self.update_interval = 0.2
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize game state."""
        self.frog_y = self.board_height - 1
        self.frog_x = self.board_width // 2
        self._init_lanes()
    
    def _init_lanes(self):
        """Initialize lanes with obstacles."""
        self.lanes = []
        
        # Bottom 2 rows: safe zone (grass)
        self.lanes.append({'type': 'safe', 'obstacles': []})
        self.lanes.append({'type': 'safe', 'obstacles': []})
        
        # Next 5 rows: road with cars
        for i in range(5):
            direction = 1 if i % 2 == 0 else -1
            num_cars = 2 + (self.level // 2)
            obstacles = []
            for j in range(num_cars):
                x = (j * (self.board_width // num_cars)) % self.board_width
                obstacles.append(x)
            self.lanes.append({
                'type': 'road',
                'direction': direction,
                'speed': 1 + (i % 3),
                'obstacles': obstacles
            })
        
        # Middle row: safe zone
        self.lanes.append({'type': 'safe', 'obstacles': []})
        
        # Top 5 rows: river with logs
        for i in range(5):
            direction = 1 if i % 2 == 0 else -1
            num_logs = 2 + (self.level // 3)
            obstacles = []
            for j in range(num_logs):
                x = (j * (self.board_width // num_logs)) % self.board_width
                obstacles.append(x)
            self.lanes.append({
                'type': 'river',
                'direction': direction,
                'speed': 1,
                'obstacles': obstacles,
                'log_width': 5 + (i % 2)
            })
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif not self.paused:
            # Movement
            old_y, old_x = self.frog_y, self.frog_x
            
            if key == curses.KEY_UP and self.frog_y > 0:
                self.frog_y -= 1
                self.score += 10  # Points for moving forward
            elif key == curses.KEY_DOWN and self.frog_y < self.board_height - 1:
                self.frog_y += 1
            elif key == curses.KEY_LEFT and self.frog_x > 0:
                self.frog_x -= 1
            elif key == curses.KEY_RIGHT and self.frog_x < self.board_width - 1:
                self.frog_x += 1
            
            # Check if reached goal
            if self.frog_y == 0:
                self.reached_goals += 1
                self.score += 100
                if self.reached_goals >= self.goals_needed:
                    self.level += 1
                    self.reached_goals = 0
                    self.lives += 1  # Bonus life
                    self._init_lanes()
                # Reset frog
                self.frog_y = self.board_height - 1
                self.frog_x = self.board_width // 2
        
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        import time
        current_time = time.time()
        
        if current_time - self.last_update_time < self.update_interval:
            return
        
        self.last_update_time = current_time
        
        # Update obstacles
        for lane in self.lanes:
            if lane['type'] in ['road', 'river']:
                direction = lane['direction']
                speed = lane['speed']
                new_obstacles = []
                for x in lane['obstacles']:
                    new_x = (x + direction * speed) % self.board_width
                    new_obstacles.append(new_x)
                lane['obstacles'] = new_obstacles
        
        # Check collisions
        self._check_collisions()
    
    def _check_collisions(self):
        """Check for collisions with obstacles."""
        lane = self.lanes[self.frog_y]
        
        if lane['type'] == 'road':
            # Check if hit by car
            for car_x in lane['obstacles']:
                if abs(self.frog_x - car_x) < 2:
                    self._lose_life()
                    return
        
        elif lane['type'] == 'river':
            # Check if on a log
            on_log = False
            for log_x in lane['obstacles']:
                log_width = lane['log_width']
                if log_x <= self.frog_x < log_x + log_width:
                    on_log = True
                    # Move with the log
                    self.frog_x = (self.frog_x + lane['direction']) % self.board_width
                    break
            
            if not on_log:
                self._lose_life()
                return
    
    def _lose_life(self):
        """Lose a life."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        else:
            # Reset frog position
            self.frog_y = self.board_height - 1
            self.frog_x = self.board_width // 2
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        title = f"FROGGER - Level {self.level}"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Game board
        board_start_y = 3
        board_start_x = (self.width - self.board_width) // 2
        
        # Draw lanes
        for y, lane in enumerate(self.lanes):
            display_y = board_start_y + y
            
            # Lane background
            if lane['type'] == 'road':
                bg = '═' * self.board_width
                self.stdscr.addstr(display_y, board_start_x, bg, curses.A_DIM)
            elif lane['type'] == 'river':
                bg = '~' * self.board_width
                self.stdscr.addstr(display_y, board_start_x, bg, curses.A_DIM)
            else:  # safe
                bg = ' ' * self.board_width
                self.stdscr.addstr(display_y, board_start_x, bg)
            
            # Draw obstacles
            if lane['type'] == 'road':
                for car_x in lane['obstacles']:
                    if 0 <= car_x < self.board_width:
                        self.stdscr.addstr(display_y, board_start_x + car_x, '█', curses.A_BOLD)
            elif lane['type'] == 'river':
                for log_x in lane['obstacles']:
                    log_width = lane['log_width']
                    for i in range(log_width):
                        x = (log_x + i) % self.board_width
                        if 0 <= x < self.board_width:
                            self.stdscr.addstr(display_y, board_start_x + x, '▬')
        
        # Draw frog
        if 0 <= self.frog_y < len(self.lanes):
            self.stdscr.addstr(
                board_start_y + self.frog_y,
                board_start_x + self.frog_x,
                '@',
                curses.A_BOLD | curses.A_REVERSE
            )
        
        # Info
        info_y = board_start_y + self.board_height + 2
        self._draw_info_bar({'Lives': self.lives, 'Level': self.level, 
                            'Goals': f"{self.reached_goals}/{self.goals_needed}"})
        
        # Instructions
        inst_y = info_y + 2
        instructions = [
            "Arrow Keys: Move frog",
            "Goal: Reach the top!",
            "Avoid cars, stay on logs",
            "P: Pause | Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, 5, inst, curses.A_DIM)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'level': self.level,
            'lives': self.lives,
            'reached_goals': self.reached_goals,
        })
        return state
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        extra_info = [
            f"Level Reached: {self.level}",
            f"Goals Completed: {self.reached_goals}"
        ]
        
        draw_game_over_screen(
            self.stdscr, "GAME OVER", self.score,
            self.high_score, is_new_high, extra_info
        )

