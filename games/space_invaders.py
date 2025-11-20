"""Space Invaders shooter game implementation."""

import curses
import random
from typing import List, Tuple
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class SpaceInvadersGame(BaseGame):
    """Space Invaders game for the terminal."""
    
    def __init__(self):
        super().__init__('space_invaders', min_height=24, min_width=100)
        
        self.board_width = 50
        self.board_height = 20
        
        # Player
        self.player_x = self.board_width // 2
        self.player_y = self.board_height - 2
        
        # Bullets
        self.bullets = []
        
        # Enemies
        self.enemies = []
        self.enemy_direction = 1
        self.enemy_speed = 0.3
        self.enemy_move_timer = 0
        
        # Enemy bullets
        self.enemy_bullets = []
        self.enemy_shoot_timer = 0
        
        # Game state
        self.lives = 3
        self.level = 1
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize enemies."""
        self._spawn_enemies()
    
    def _spawn_enemies(self):
        """Spawn enemies in formation."""
        self.enemies = []
        rows = 3
        cols = 8
        start_y = 2
        start_x = 5
        
        for row in range(rows):
            for col in range(cols):
                y = start_y + row
                x = start_x + col * 5
                self.enemies.append({'y': y, 'x': x, 'alive': True})
    
    def _move_enemies(self, delta_time: float):
        """Move enemies and handle direction changes."""
        self.enemy_move_timer += delta_time
        if self.enemy_move_timer >= self.enemy_speed:
            self.enemy_move_timer = 0
            
            change_dir = False
            for enemy in self.enemies:
                if not enemy['alive']:
                    continue
                if (self.enemy_direction == 1 and enemy['x'] >= self.board_width - 2) or \
                   (self.enemy_direction == -1 and enemy['x'] <= 1):
                    change_dir = True
                    break
            
            if change_dir:
                self.enemy_direction *= -1
                for enemy in self.enemies:
                    if enemy['alive']:
                        enemy['y'] += 1
                        if enemy['y'] >= self.player_y:
                            self.game_over = True
            else:
                for enemy in self.enemies:
                    if enemy['alive']:
                        enemy['x'] += self.enemy_direction
    
    def _update_bullets(self):
        """Update player bullets."""
        new_bullets = []
        for bullet in self.bullets:
            y, x = bullet
            y -= 1
            if y > 0:
                new_bullets.append((y, x))
        self.bullets = new_bullets
    
    def _update_enemy_bullets(self):
        """Update enemy bullets."""
        new_bullets = []
        for bullet in self.enemy_bullets:
            y, x = bullet
            y += 1
            if y < self.board_height:
                new_bullets.append((y, x))
        self.enemy_bullets = new_bullets
    
    def _check_collisions(self):
        """Check for collisions."""
        bullets_to_remove = []
        for i, bullet in enumerate(self.bullets):
            by, bx = bullet
            for enemy in self.enemies:
                if not enemy['alive']:
                    continue
                if abs(enemy['y'] - by) < 1 and abs(enemy['x'] - bx) < 2:
                    enemy['alive'] = False
                    bullets_to_remove.append(i)
                    self.score += 10
                    break
        
        for i in sorted(bullets_to_remove, reverse=True):
            self.bullets.pop(i)
        
        for bullet in self.enemy_bullets:
            by, bx = bullet
            if abs(self.player_y - by) < 1 and abs(self.player_x - bx) < 2:
                self.lives -= 1
                self.enemy_bullets.remove(bullet)
                if self.lives <= 0:
                    self.game_over = True
    
    def _enemy_shoot(self, delta_time: float):
        """Make enemies shoot randomly."""
        self.enemy_shoot_timer += delta_time
        if self.enemy_shoot_timer >= 1.0:
            self.enemy_shoot_timer = 0
            alive_enemies = [e for e in self.enemies if e['alive']]
            if alive_enemies and random.random() < 0.3:
                enemy = random.choice(alive_enemies)
                self.enemy_bullets.append((enemy['y'] + 1, enemy['x']))
    
    def _check_win(self):
        """Check if all enemies are destroyed."""
        if all(not enemy['alive'] for enemy in self.enemies):
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
                self.player_x = max(1, self.player_x - 1)
            elif key == curses.KEY_RIGHT or key == ord('d'):
                self.player_x = min(self.board_width - 2, self.player_x + 1)
            elif key == ord(' ') or key == ord('\n'):
                if len(self.bullets) < 3:
                    self.bullets.append((self.player_y - 1, self.player_x))
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        if self.paused:
            return
        
        self._move_enemies(delta_time)
        self._update_bullets()
        self._update_enemy_bullets()
        self._enemy_shoot(delta_time)
        self._check_collisions()
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
        
        # Draw enemies
        for enemy in self.enemies:
            if enemy['alive']:
                self.stdscr.addch(board_start_y + enemy['y'], board_start_x + enemy['x'], '^', 
                                curses.A_BOLD)
        
        # Draw player
        self.stdscr.addch(board_start_y + self.player_y, board_start_x + self.player_x, 'A', 
                        curses.A_BOLD)
        
        # Draw bullets
        for by, bx in self.bullets:
            self.stdscr.addch(board_start_y + by, board_start_x + bx, '|', curses.A_BOLD)
        
        for by, bx in self.enemy_bullets:
            self.stdscr.addch(board_start_y + by, board_start_x + bx, '.', curses.A_DIM)
        
        # Info
        self._draw_info_bar({'Lives': self.lives})
        
        # Instructions
        inst_y = board_start_y + self.board_height + 2
        instructions = [
            "← → or A/D: Move",
            "Space: Shoot",
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
