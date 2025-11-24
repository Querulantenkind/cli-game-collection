"""Centipede arcade game."""

import curses
import random
from typing import List, Tuple, Dict, Any, Set
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class CentipedeGame(BaseGame):
    """Centipede arcade game for the terminal."""
    
    def __init__(self):
        super().__init__('centipede', min_height=24, min_width=80)
        
        # Game constants
        self.GAME_WIDTH = 76
        self.GAME_HEIGHT = 20
        self.PLAYER_ZONE = 5  # Bottom 5 rows are player zone
        
        # Player state
        self.player_x = self.GAME_WIDTH // 2
        self.player_y = self.GAME_HEIGHT - 2
        
        # Game state
        self.centipede: List[Tuple[int, int]] = []
        self.centipede_direction = 1  # 1 = right, -1 = left
        self.mushrooms: Set[Tuple[int, int]] = set()
        self.bullets: List[Tuple[int, int]] = []
        self.spider: Dict[str, Any] = {}
        
        # Stats
        self.lives = 3
        self.level = 1
        self.segments_destroyed = 0
        
        # Timing
        self.last_shot_time = 0
        self.shot_cooldown = 0.2
        self.centipede_move_timer = 0
        self.centipede_move_interval = 0.2
        self.spider_spawn_timer = 0
        self.spider_spawn_interval = 5.0
        
        # Speed from settings
        speed = self.settings.get('centipede', 'speed', 'medium')
        speed_multiplier = {'slow': 1.5, 'medium': 1.0, 'fast': 0.7}.get(speed, 1.0)
        self.centipede_move_interval *= speed_multiplier
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize the game."""
        self.player_x = self.GAME_WIDTH // 2
        self.player_y = self.GAME_HEIGHT - 2
        self.lives = 3
        self.level = 1
        self.segments_destroyed = 0
        self._spawn_level()
    
    def _spawn_level(self):
        """Spawn centipede and mushrooms for the level."""
        # Create centipede at top
        centipede_length = min(10 + self.level, 20)
        self.centipede = []
        start_x = self.GAME_WIDTH // 2
        for i in range(centipede_length):
            self.centipede.append((0, start_x - i))
        self.centipede_direction = 1
        
        # Spawn mushrooms
        num_mushrooms = 20 + (self.level * 5)
        self.mushrooms = set()
        for _ in range(num_mushrooms):
            # Don't spawn in player zone
            x = random.randint(0, self.GAME_WIDTH - 1)
            y = random.randint(0, self.GAME_HEIGHT - self.PLAYER_ZONE - 1)
            self.mushrooms.add((y, x))
        
        self.bullets = []
        self.spider = {}
    
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
        
        # Player movement
        if key == curses.KEY_LEFT or key == ord('a'):
            self.player_x = max(0, self.player_x - 1)
        elif key == curses.KEY_RIGHT or key == ord('d'):
            self.player_x = min(self.GAME_WIDTH - 1, self.player_x + 1)
        elif key == curses.KEY_UP or key == ord('w'):
            self.player_y = max(self.GAME_HEIGHT - self.PLAYER_ZONE, self.player_y - 1)
        elif key == curses.KEY_DOWN or key == ord('s'):
            self.player_y = min(self.GAME_HEIGHT - 1, self.player_y + 1)
        
        # Shoot
        elif key == ord(' '):
            current_time = self.last_frame_time if self.last_frame_time else 0
            if current_time - self.last_shot_time >= self.shot_cooldown:
                self.bullets.append((self.player_y - 1, self.player_x))
                self.last_shot_time = current_time
        
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        current_time = self.last_frame_time if self.last_frame_time else 0
        
        # Update bullets
        new_bullets = []
        for by, bx in self.bullets:
            by -= 1
            if by >= 0:
                # Check mushroom collision
                if (by, bx) in self.mushrooms:
                    self.mushrooms.discard((by, bx))
                    self.score += 1
                    continue
                
                # Check centipede collision
                hit = False
                for i, (cy, cx) in enumerate(self.centipede):
                    if cy == by and cx == bx:
                        # Hit a segment
                        self.score += 10
                        self.segments_destroyed += 1
                        
                        # Split centipede
                        head = self.centipede[:i]
                        tail = self.centipede[i+1:]
                        self.centipede = head
                        
                        # Tail becomes new centipede (if any)
                        if tail:
                            # Add tail back (simplified - just keep going)
                            self.centipede.extend(tail)
                        
                        # Create mushroom where segment was
                        self.mushrooms.add((cy, cx))
                        hit = True
                        break
                
                # Check spider collision
                if self.spider and not hit:
                    if self.spider['y'] == by and self.spider['x'] == bx:
                        self.score += 50
                        self.spider = {}
                        hit = True
                
                if not hit:
                    new_bullets.append((by, bx))
        
        self.bullets = new_bullets
        
        # Update centipede
        self.centipede_move_timer += delta_time
        if self.centipede_move_timer >= self.centipede_move_interval:
            self.centipede_move_timer = 0
            self._move_centipede()
        
        # Update spider
        if self.spider:
            # Move spider diagonally in player zone
            self.spider['x'] += self.spider['dx']
            self.spider['y'] += random.choice([-1, 0, 1])
            
            # Bound spider
            if self.spider['x'] < 0 or self.spider['x'] >= self.GAME_WIDTH:
                self.spider['dx'] *= -1
                self.spider['x'] = max(0, min(self.GAME_WIDTH - 1, self.spider['x']))
            
            self.spider['y'] = max(self.GAME_HEIGHT - self.PLAYER_ZONE, 
                                  min(self.GAME_HEIGHT - 1, self.spider['y']))
            
            # Check player collision
            if abs(self.spider['x'] - self.player_x) <= 1 and abs(self.spider['y'] - self.player_y) <= 1:
                self._lose_life()
                self.spider = {}
            
            # Remove spider after some time
            self.spider['lifetime'] -= delta_time
            if self.spider['lifetime'] <= 0:
                self.spider = {}
        else:
            # Spawn spider
            self.spider_spawn_timer += delta_time
            if self.spider_spawn_timer >= self.spider_spawn_interval:
                self.spider_spawn_timer = 0
                self._spawn_spider()
        
        # Check if level complete
        if not self.centipede:
            self.level += 1
            self.score += 100
            self._spawn_level()
    
    def _move_centipede(self):
        """Move the centipede."""
        if not self.centipede:
            return
        
        new_centipede = []
        move_down = False
        
        for i, (y, x) in enumerate(self.centipede):
            new_x = x + self.centipede_direction
            new_y = y
            
            # Check if we need to move down
            if new_x < 0 or new_x >= self.GAME_WIDTH or (new_y, new_x) in self.mushrooms:
                move_down = True
                new_x = x
                new_y = y + 1
                
                # Reverse direction when moving down
                if i == 0:  # Only reverse for head
                    self.centipede_direction *= -1
            
            # Check if centipede reached player zone
            if new_y >= self.GAME_HEIGHT - self.PLAYER_ZONE:
                # Check player collision
                if abs(new_x - self.player_x) <= 1 and new_y == self.player_y:
                    self._lose_life()
                    return
            
            # Check if centipede reached bottom
            if new_y >= self.GAME_HEIGHT:
                continue  # Remove this segment
            
            new_centipede.append((new_y, new_x))
        
        self.centipede = new_centipede
    
    def _spawn_spider(self):
        """Spawn a spider in the player zone."""
        self.spider = {
            'x': random.choice([0, self.GAME_WIDTH - 1]),
            'y': random.randint(self.GAME_HEIGHT - self.PLAYER_ZONE, self.GAME_HEIGHT - 1),
            'dx': random.choice([-1, 1]),
            'lifetime': 8.0
        }
    
    def _lose_life(self):
        """Player loses a life."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            self.won = False
        else:
            # Reset player position
            self.player_x = self.GAME_WIDTH // 2
            self.player_y = self.GAME_HEIGHT - 2
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title and stats
        title = f"Centipede - Level {self.level}"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(0, title_x, title, curses.A_BOLD)
        
        # Lives
        lives_str = f"Lives: {'♥ ' * self.lives}"
        self.stdscr.addstr(0, 2, lives_str)
        
        # Score
        score_str = f"Score: {self.score}"
        self.stdscr.addstr(0, self.width - len(score_str) - 2, score_str)
        
        # Offset for game area
        offset_x = 2
        offset_y = 2
        
        # Draw mushrooms
        for my, mx in self.mushrooms:
            screen_y = offset_y + my
            screen_x = offset_x + mx
            if 0 < screen_y < self.height - 1 and 0 < screen_x < self.width - 1:
                self.stdscr.addstr(screen_y, screen_x, 'M', curses.A_NORMAL)
        
        # Draw centipede
        for i, (cy, cx) in enumerate(self.centipede):
            screen_y = offset_y + cy
            screen_x = offset_x + cx
            if 0 < screen_y < self.height - 1 and 0 < screen_x < self.width - 1:
                char = 'O' if i == 0 else 'o'  # Head vs body
                self.stdscr.addstr(screen_y, screen_x, char, curses.A_BOLD)
        
        # Draw spider
        if self.spider:
            sy = offset_y + self.spider['y']
            sx = offset_x + self.spider['x']
            if 0 < sy < self.height - 1 and 0 < sx < self.width - 1:
                self.stdscr.addstr(sy, sx, 'X', curses.A_BOLD)
        
        # Draw bullets
        for by, bx in self.bullets:
            screen_y = offset_y + by
            screen_x = offset_x + bx
            if 0 < screen_y < self.height - 1 and 0 < screen_x < self.width - 1:
                self.stdscr.addstr(screen_y, screen_x, '|', curses.A_BOLD)
        
        # Draw player
        py = offset_y + self.player_y
        px = offset_x + self.player_x
        if 0 < py < self.height - 1 and 0 < px < self.width - 1:
            self.stdscr.addstr(py, px, '^', curses.A_BOLD | curses.A_REVERSE)
        
        # Draw player zone line
        zone_y = offset_y + self.GAME_HEIGHT - self.PLAYER_ZONE
        zone_line = "─" * self.GAME_WIDTH
        if 0 < zone_y < self.height - 1:
            self.stdscr.addstr(zone_y, offset_x, zone_line, curses.A_DIM)
        
        # Instructions
        inst_y = self.height - 2
        instructions = "Arrow Keys: Move | Space: Shoot | P: Pause | Q: Quit"
        inst_x = (self.width - len(instructions)) // 2
        self.stdscr.addstr(inst_y, inst_x, instructions)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'level': self.level,
            'segments_destroyed': self.segments_destroyed,
            'lives_remaining': self.lives,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'player_x': self.player_x,
            'player_y': self.player_y,
            'centipede': self.centipede,
            'mushrooms': list(self.mushrooms),
            'lives': self.lives,
            'level': self.level,
            'segments_destroyed': self.segments_destroyed,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.player_x = state.get('player_x', self.GAME_WIDTH // 2)
        self.player_y = state.get('player_y', self.GAME_HEIGHT - 2)
        self.centipede = state.get('centipede', [])
        self.mushrooms = set(tuple(m) for m in state.get('mushrooms', []))
        self.lives = state.get('lives', 3)
        self.level = state.get('level', 1)
        self.segments_destroyed = state.get('segments_destroyed', 0)
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        title = "GAME OVER!"
        
        extra_info = [
            f"Level Reached: {self.level}",
            f"Segments Destroyed: {self.segments_destroyed}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

