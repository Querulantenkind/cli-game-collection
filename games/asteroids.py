"""Asteroids arcade game."""

import curses
import random
import math
from typing import List, Tuple, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class Asteroids(BaseGame):
    """Asteroids arcade game for the terminal."""
    
    def __init__(self):
        super().__init__('asteroids', min_height=24, min_width=80)
        
        # Player ship
        self.ship_x = 0.0
        self.ship_y = 0.0
        self.ship_angle = 0.0  # 0 = up, increases clockwise
        self.ship_dx = 0.0
        self.ship_dy = 0.0
        self.ship_alive = True
        
        # Game state
        self.asteroids: List[Dict] = []
        self.bullets: List[Dict] = []
        self.lives = 3
        self.level = 1
        self.asteroids_destroyed = 0
        
        # Physics constants
        self.THRUST_POWER = 0.5
        self.ROTATION_SPEED = 0.15
        self.MAX_SPEED = 2.0
        self.FRICTION = 0.98
        self.BULLET_SPEED = 3.0
        self.BULLET_LIFETIME = 1.5
        
        # Game area (excluding border)
        self.game_width = 78
        self.game_height = 22
        
        # Timing
        self.last_shot_time = 0
        self.shot_cooldown = 0.3
        self.respawn_time = 0
        self.invulnerable_until = 0
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize the game."""
        self.ship_x = self.game_width / 2
        self.ship_y = self.game_height / 2
        self.ship_angle = 0.0
        self.ship_dx = 0.0
        self.ship_dy = 0.0
        self.ship_alive = True
        self.lives = 3
        self.level = 1
        self.asteroids_destroyed = 0
        self._spawn_asteroids(4)
    
    def _spawn_asteroids(self, count: int):
        """Spawn asteroids for the level."""
        self.asteroids = []
        for _ in range(count):
            # Spawn away from player
            while True:
                x = random.uniform(5, self.game_width - 5)
                y = random.uniform(5, self.game_height - 5)
                dist = math.sqrt((x - self.ship_x)**2 + (y - self.ship_y)**2)
                if dist > 15:
                    break
            
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.3, 0.8)
            self.asteroids.append({
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': 3  # 3=large, 2=medium, 1=small
            })
    
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
        
        # Rotation
        if key == curses.KEY_LEFT or key == ord('a'):
            self.ship_angle -= self.ROTATION_SPEED
        elif key == curses.KEY_RIGHT or key == ord('d'):
            self.ship_angle += self.ROTATION_SPEED
        
        # Thrust
        elif key == curses.KEY_UP or key == ord('w'):
            if self.ship_alive:
                self.ship_dx += math.sin(self.ship_angle) * self.THRUST_POWER
                self.ship_dy -= math.cos(self.ship_angle) * self.THRUST_POWER
                # Limit speed
                speed = math.sqrt(self.ship_dx**2 + self.ship_dy**2)
                if speed > self.MAX_SPEED:
                    self.ship_dx = (self.ship_dx / speed) * self.MAX_SPEED
                    self.ship_dy = (self.ship_dy / speed) * self.MAX_SPEED
        
        # Shoot
        elif key == ord(' '):
            current_time = self.last_frame_time if self.last_frame_time else 0
            if self.ship_alive and current_time - self.last_shot_time >= self.shot_cooldown:
                self._shoot()
                self.last_shot_time = current_time
        
        return True
    
    def _shoot(self):
        """Fire a bullet."""
        bullet_dx = math.sin(self.ship_angle) * self.BULLET_SPEED
        bullet_dy = -math.cos(self.ship_angle) * self.BULLET_SPEED
        
        self.bullets.append({
            'x': self.ship_x,
            'y': self.ship_y,
            'dx': bullet_dx + self.ship_dx,
            'dy': bullet_dy + self.ship_dy,
            'lifetime': self.BULLET_LIFETIME
        })
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        current_time = self.last_frame_time if self.last_frame_time else 0
        
        # Update ship
        if self.ship_alive:
            self.ship_x += self.ship_dx
            self.ship_y += self.ship_dy
            
            # Apply friction
            self.ship_dx *= self.FRICTION
            self.ship_dy *= self.FRICTION
            
            # Wrap around screen
            self.ship_x = self.ship_x % self.game_width
            self.ship_y = self.ship_y % self.game_height
            
            # Check collisions with asteroids (if not invulnerable)
            if current_time > self.invulnerable_until:
                for asteroid in self.asteroids:
                    dist = math.sqrt((self.ship_x - asteroid['x'])**2 + 
                                   (self.ship_y - asteroid['y'])**2)
                    if dist < asteroid['size'] * 2:
                        self._ship_destroyed()
                        break
        elif current_time > self.respawn_time and self.lives > 0:
            # Respawn ship
            self.ship_alive = True
            self.ship_x = self.game_width / 2
            self.ship_y = self.game_height / 2
            self.ship_dx = 0.0
            self.ship_dy = 0.0
            self.invulnerable_until = current_time + 2.0
        
        # Update asteroids
        for asteroid in self.asteroids:
            asteroid['x'] = (asteroid['x'] + asteroid['dx']) % self.game_width
            asteroid['y'] = (asteroid['y'] + asteroid['dy']) % self.game_height
        
        # Update bullets
        bullets_to_remove = []
        for i, bullet in enumerate(self.bullets):
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            bullet['lifetime'] -= delta_time
            
            # Remove if expired or out of bounds
            if (bullet['lifetime'] <= 0 or 
                bullet['x'] < 0 or bullet['x'] >= self.game_width or
                bullet['y'] < 0 or bullet['y'] >= self.game_height):
                bullets_to_remove.append(i)
        
        for i in reversed(bullets_to_remove):
            self.bullets.pop(i)
        
        # Check bullet-asteroid collisions
        asteroids_to_remove = []
        asteroids_to_add = []
        bullets_to_remove = []
        
        for bullet_idx, bullet in enumerate(self.bullets):
            for asteroid_idx, asteroid in enumerate(self.asteroids):
                dist = math.sqrt((bullet['x'] - asteroid['x'])**2 + 
                               (bullet['y'] - asteroid['y'])**2)
                if dist < asteroid['size'] * 2:
                    # Hit!
                    if asteroid_idx not in asteroids_to_remove:
                        asteroids_to_remove.append(asteroid_idx)
                        bullets_to_remove.append(bullet_idx)
                        
                        # Score based on size
                        self.score += asteroid['size'] * 10
                        self.asteroids_destroyed += 1
                        
                        # Split asteroid if not smallest
                        if asteroid['size'] > 1:
                            for _ in range(2):
                                angle = random.uniform(0, 2 * math.pi)
                                speed = random.uniform(0.5, 1.2)
                                asteroids_to_add.append({
                                    'x': asteroid['x'],
                                    'y': asteroid['y'],
                                    'dx': math.cos(angle) * speed,
                                    'dy': math.sin(angle) * speed,
                                    'size': asteroid['size'] - 1
                                })
                    break
        
        # Remove hit asteroids and bullets
        for i in reversed(sorted(set(asteroids_to_remove))):
            self.asteroids.pop(i)
        for i in reversed(sorted(set(bullets_to_remove))):
            if i < len(self.bullets):
                self.bullets.pop(i)
        
        # Add split asteroids
        self.asteroids.extend(asteroids_to_add)
        
        # Check level completion
        if not self.asteroids and self.ship_alive:
            self.level += 1
            self._spawn_asteroids(3 + self.level)
    
    def _ship_destroyed(self):
        """Handle ship destruction."""
        self.ship_alive = False
        self.lives -= 1
        self.respawn_time = (self.last_frame_time if self.last_frame_time else 0) + 2.0
        
        if self.lives <= 0:
            self.game_over = True
            self.won = False
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title and stats
        title = f"Asteroids - Level {self.level}"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(0, title_x, title, curses.A_BOLD)
        
        # Draw lives
        lives_str = f"Lives: {'♥ ' * self.lives}"
        self.stdscr.addstr(0, 2, lives_str)
        
        # Draw score
        score_str = f"Score: {self.score}"
        self.stdscr.addstr(0, self.width - len(score_str) - 2, score_str)
        
        # Draw ship
        current_time = self.last_frame_time if self.last_frame_time else 0
        if self.ship_alive:
            ship_screen_x = int(self.ship_x) + 1
            ship_screen_y = int(self.ship_y) + 1
            
            # Determine ship character based on angle
            angle_deg = (self.ship_angle * 180 / math.pi) % 360
            if 337.5 <= angle_deg or angle_deg < 22.5:
                ship_char = '^'
            elif 22.5 <= angle_deg < 67.5:
                ship_char = '>'
            elif 67.5 <= angle_deg < 112.5:
                ship_char = 'v'
            elif 112.5 <= angle_deg < 157.5:
                ship_char = '<'
            elif 157.5 <= angle_deg < 202.5:
                ship_char = 'v'
            elif 202.5 <= angle_deg < 247.5:
                ship_char = '<'
            elif 247.5 <= angle_deg < 292.5:
                ship_char = '^'
            else:
                ship_char = '>'
            
            # Flash if invulnerable
            attr = curses.A_BOLD
            if current_time < self.invulnerable_until:
                if int(current_time * 10) % 2 == 0:
                    attr |= curses.A_REVERSE
            
            if 0 < ship_screen_y < self.height - 1 and 0 < ship_screen_x < self.width - 1:
                self.stdscr.addstr(ship_screen_y, ship_screen_x, ship_char, attr)
        
        # Draw asteroids
        for asteroid in self.asteroids:
            ax = int(asteroid['x']) + 1
            ay = int(asteroid['y']) + 1
            if 0 < ay < self.height - 1 and 0 < ax < self.width - 1:
                if asteroid['size'] == 3:
                    char = 'O'
                elif asteroid['size'] == 2:
                    char = 'o'
                else:
                    char = '.'
                self.stdscr.addstr(ay, ax, char, curses.A_NORMAL)
        
        # Draw bullets
        for bullet in self.bullets:
            bx = int(bullet['x']) + 1
            by = int(bullet['y']) + 1
            if 0 < by < self.height - 1 and 0 < bx < self.width - 1:
                self.stdscr.addstr(by, bx, '*', curses.A_BOLD)
        
        # Instructions
        inst_y = self.height - 2
        instructions = "← →: Rotate | ↑: Thrust | Space: Shoot | P: Pause | Q: Quit"
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
            'asteroids_destroyed': self.asteroids_destroyed,
            'lives_remaining': self.lives,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'ship_x': self.ship_x,
            'ship_y': self.ship_y,
            'ship_angle': self.ship_angle,
            'ship_dx': self.ship_dx,
            'ship_dy': self.ship_dy,
            'ship_alive': self.ship_alive,
            'asteroids': self.asteroids,
            'lives': self.lives,
            'level': self.level,
            'asteroids_destroyed': self.asteroids_destroyed,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.ship_x = state.get('ship_x', self.game_width / 2)
        self.ship_y = state.get('ship_y', self.game_height / 2)
        self.ship_angle = state.get('ship_angle', 0.0)
        self.ship_dx = state.get('ship_dx', 0.0)
        self.ship_dy = state.get('ship_dy', 0.0)
        self.ship_alive = state.get('ship_alive', True)
        self.asteroids = state.get('asteroids', [])
        self.lives = state.get('lives', 3)
        self.level = state.get('level', 1)
        self.asteroids_destroyed = state.get('asteroids_destroyed', 0)
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        title = "GAME OVER!"
        
        extra_info = [
            f"Level Reached: {self.level}",
            f"Asteroids Destroyed: {self.asteroids_destroyed}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

