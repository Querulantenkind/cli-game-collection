"""Missile Command defense game."""

import curses
import random
import math
from typing import List, Tuple, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class MissileCommandGame(BaseGame):
    """Missile Command defense game for the terminal."""
    
    def __init__(self):
        super().__init__('missile_command', min_height=24, min_width=80)
        
        # Game constants
        self.GAME_WIDTH = 76
        self.GAME_HEIGHT = 20
        
        # Base positions (3 missile bases)
        self.bases = [
            {'x': 10, 'ammo': 10, 'alive': True},
            {'x': self.GAME_WIDTH // 2, 'ammo': 10, 'alive': True},
            {'x': self.GAME_WIDTH - 10, 'ammo': 10, 'alive': True}
        ]
        
        # City positions (6 cities between bases)
        city_spacing = self.GAME_WIDTH // 8
        self.cities = [
            {'x': city_spacing * 1, 'alive': True},
            {'x': city_spacing * 2, 'alive': True},
            {'x': city_spacing * 3, 'alive': True},
            {'x': city_spacing * 5, 'alive': True},
            {'x': city_spacing * 6, 'alive': True},
            {'x': city_spacing * 7, 'alive': True},
        ]
        
        # Crosshair
        self.crosshair_x = self.GAME_WIDTH // 2
        self.crosshair_y = self.GAME_HEIGHT // 2
        
        # Active base
        self.active_base = 1  # Middle base
        
        # Missiles and explosions
        self.enemy_missiles: List[Dict] = []
        self.player_missiles: List[Dict] = []
        self.explosions: List[Dict] = []
        
        # Game state
        self.wave = 1
        self.wave_active = False
        self.wave_start_time = 0
        self.missiles_in_wave = 0
        self.missiles_spawned = 0
        
        # Timing
        self.spawn_timer = 0
        self.spawn_interval = 1.0
        
        # Score
        self.cities_saved = 0
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize the game."""
        # Reset bases
        for base in self.bases:
            base['ammo'] = 10
            base['alive'] = True
        
        # Reset cities
        for city in self.cities:
            city['alive'] = True
        
        self.wave = 1
        self.wave_active = False
        self.enemy_missiles = []
        self.player_missiles = []
        self.explosions = []
        self._start_wave()
    
    def _start_wave(self):
        """Start a new wave."""
        self.wave_active = True
        self.missiles_in_wave = 5 + (self.wave * 2)
        self.missiles_spawned = 0
        self.spawn_timer = 0
        self.spawn_interval = max(0.3, 1.0 - (self.wave * 0.05))
    
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
        
        # Move crosshair
        if key == curses.KEY_LEFT:
            self.crosshair_x = max(0, self.crosshair_x - 2)
        elif key == curses.KEY_RIGHT:
            self.crosshair_x = min(self.GAME_WIDTH - 1, self.crosshair_x + 2)
        elif key == curses.KEY_UP:
            self.crosshair_y = max(0, self.crosshair_y - 1)
        elif key == curses.KEY_DOWN:
            self.crosshair_y = min(self.GAME_HEIGHT - 1, self.crosshair_y + 1)
        
        # Switch base
        elif key == ord('1'):
            self.active_base = 0
        elif key == ord('2'):
            self.active_base = 1
        elif key == ord('3'):
            self.active_base = 2
        
        # Fire missile
        elif key == ord(' '):
            self._fire_missile()
        
        return True
    
    def _fire_missile(self):
        """Fire a defensive missile."""
        base = self.bases[self.active_base]
        if base['alive'] and base['ammo'] > 0:
            base['ammo'] -= 1
            
            # Calculate path from base to crosshair
            start_x = base['x']
            start_y = self.GAME_HEIGHT - 1
            
            self.player_missiles.append({
                'x': start_x,
                'y': start_y,
                'target_x': self.crosshair_x,
                'target_y': self.crosshair_y,
                'dx': (self.crosshair_x - start_x) / 30.0,
                'dy': (self.crosshair_y - start_y) / 30.0,
            })
    
    def _spawn_enemy_missile(self):
        """Spawn an enemy missile."""
        # Random spawn at top
        start_x = random.randint(0, self.GAME_WIDTH - 1)
        
        # Random target (city or base)
        targets = []
        for city in self.cities:
            if city['alive']:
                targets.append(('city', city['x']))
        for base in self.bases:
            if base['alive']:
                targets.append(('base', base['x']))
        
        if targets:
            target_type, target_x = random.choice(targets)
            target_y = self.GAME_HEIGHT - 1
            
            # Calculate velocity
            distance = math.sqrt((target_x - start_x)**2 + (target_y - 0)**2)
            speed = 0.5 + (self.wave * 0.05)
            
            self.enemy_missiles.append({
                'x': start_x,
                'y': 0,
                'target_x': target_x,
                'target_y': target_y,
                'dx': (target_x - start_x) / distance * speed,
                'dy': target_y / distance * speed,
            })
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        # Spawn enemy missiles
        if self.wave_active and self.missiles_spawned < self.missiles_in_wave:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self._spawn_enemy_missile()
                self.missiles_spawned += 1
        
        # Update enemy missiles
        missiles_to_remove = []
        for i, missile in enumerate(self.enemy_missiles):
            missile['x'] += missile['dx']
            missile['y'] += missile['dy']
            
            # Check if reached target
            dist = math.sqrt((missile['x'] - missile['target_x'])**2 + 
                           (missile['y'] - missile['target_y'])**2)
            if dist < 1.0:
                # Impact!
                self._enemy_impact(missile['target_x'], missile['target_y'])
                missiles_to_remove.append(i)
        
        for i in reversed(missiles_to_remove):
            self.enemy_missiles.pop(i)
        
        # Update player missiles
        missiles_to_remove = []
        for i, missile in enumerate(self.player_missiles):
            missile['x'] += missile['dx']
            missile['y'] += missile['dy']
            
            # Check if reached target
            dist = math.sqrt((missile['x'] - missile['target_x'])**2 + 
                           (missile['y'] - missile['target_y'])**2)
            if dist < 1.0:
                # Create explosion
                self.explosions.append({
                    'x': missile['target_x'],
                    'y': missile['target_y'],
                    'radius': 0.0,
                    'max_radius': 5.0,
                    'expanding': True,
                })
                missiles_to_remove.append(i)
        
        for i in reversed(missiles_to_remove):
            self.player_missiles.pop(i)
        
        # Update explosions
        explosions_to_remove = []
        for i, explosion in enumerate(self.explosions):
            if explosion['expanding']:
                explosion['radius'] += 0.3
                if explosion['radius'] >= explosion['max_radius']:
                    explosion['expanding'] = False
            else:
                explosion['radius'] -= 0.2
                if explosion['radius'] <= 0:
                    explosions_to_remove.append(i)
            
            # Check collisions with enemy missiles
            for j, missile in enumerate(self.enemy_missiles):
                dist = math.sqrt((missile['x'] - explosion['x'])**2 + 
                               (missile['y'] - explosion['y'])**2)
                if dist < explosion['radius']:
                    if j not in missiles_to_remove:
                        self.score += 25
                        missiles_to_remove.append(j)
        
        for i in reversed(explosions_to_remove):
            self.explosions.pop(i)
        
        # Remove destroyed enemy missiles
        for i in reversed(sorted(set(missiles_to_remove))):
            if i < len(self.enemy_missiles):
                self.enemy_missiles.pop(i)
        
        # Check wave completion
        if (self.wave_active and self.missiles_spawned >= self.missiles_in_wave and 
            not self.enemy_missiles and not self.player_missiles and not self.explosions):
            self._end_wave()
    
    def _enemy_impact(self, x: float, y: float):
        """Handle enemy missile impact."""
        # Check cities
        for city in self.cities:
            if city['alive'] and abs(city['x'] - x) < 3:
                city['alive'] = False
                return
        
        # Check bases
        for base in self.bases:
            if base['alive'] and abs(base['x'] - x) < 3:
                base['alive'] = False
                return
    
    def _end_wave(self):
        """End the current wave."""
        self.wave_active = False
        
        # Bonus for surviving cities
        for city in self.cities:
            if city['alive']:
                self.score += 100
                self.cities_saved += 1
        
        # Bonus for remaining ammo
        for base in self.bases:
            if base['alive']:
                self.score += base['ammo'] * 5
        
        # Check game over conditions
        cities_alive = sum(1 for city in self.cities if city['alive'])
        bases_alive = sum(1 for base in self.bases if base['alive'])
        
        if cities_alive == 0 or bases_alive == 0:
            self.game_over = True
            self.won = False
        else:
            # Next wave
            self.wave += 1
            
            # Resupply bases
            for base in self.bases:
                if base['alive']:
                    base['ammo'] = 10
            
            import time
            time.sleep(1.0)
            self._start_wave()
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title and stats
        title = f"Missile Command - Wave {self.wave}"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(0, title_x, title, curses.A_BOLD)
        
        # Score
        score_str = f"Score: {self.score}"
        self.stdscr.addstr(0, self.width - len(score_str) - 2, score_str)
        
        # Offset for game area
        offset_x = 2
        offset_y = 2
        
        # Draw cities
        for city in self.cities:
            cx = offset_x + int(city['x'])
            cy = offset_y + self.GAME_HEIGHT - 1
            if city['alive']:
                self.stdscr.addstr(cy, cx, '█', curses.A_BOLD)
            else:
                self.stdscr.addstr(cy, cx, '░', curses.A_DIM)
        
        # Draw bases
        for i, base in enumerate(self.bases):
            bx = offset_x + base['x']
            by = offset_y + self.GAME_HEIGHT - 1
            if base['alive']:
                char = '▲' if i == self.active_base else '△'
                attr = curses.A_BOLD | curses.A_REVERSE if i == self.active_base else curses.A_BOLD
                self.stdscr.addstr(by, bx, char, attr)
                # Show ammo
                ammo_str = str(base['ammo'])
                self.stdscr.addstr(by - 1, bx, ammo_str, curses.A_DIM)
            else:
                self.stdscr.addstr(by, bx, 'X', curses.A_DIM)
        
        # Draw enemy missiles
        for missile in self.enemy_missiles:
            mx = offset_x + int(missile['x'])
            my = offset_y + int(missile['y'])
            if 0 <= my < offset_y + self.GAME_HEIGHT and 0 <= mx < offset_x + self.GAME_WIDTH:
                self.stdscr.addstr(my, mx, '↓', curses.A_BOLD)
        
        # Draw player missiles
        for missile in self.player_missiles:
            mx = offset_x + int(missile['x'])
            my = offset_y + int(missile['y'])
            if 0 <= my < offset_y + self.GAME_HEIGHT and 0 <= mx < offset_x + self.GAME_WIDTH:
                self.stdscr.addstr(my, mx, '↑', curses.A_BOLD)
        
        # Draw explosions
        for explosion in self.explosions:
            ex = int(explosion['x'])
            ey = int(explosion['y'])
            radius = int(explosion['radius'])
            
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if dx*dx + dy*dy <= radius*radius:
                        draw_x = offset_x + ex + dx
                        draw_y = offset_y + ey + dy
                        if (0 <= draw_y < offset_y + self.GAME_HEIGHT and 
                            0 <= draw_x < offset_x + self.GAME_WIDTH):
                            self.stdscr.addstr(draw_y, draw_x, '*', curses.A_BOLD)
        
        # Draw crosshair
        cx = offset_x + self.crosshair_x
        cy = offset_y + self.crosshair_y
        if 0 <= cy < offset_y + self.GAME_HEIGHT and 0 <= cx < offset_x + self.GAME_WIDTH:
            self.stdscr.addstr(cy, cx, '+', curses.A_REVERSE | curses.A_BOLD)
        
        # Instructions
        inst_y = offset_y + self.GAME_HEIGHT + 1
        instructions = [
            "Arrow Keys: Move crosshair | 1/2/3: Select base | Space: Fire",
            "P: Pause | Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            inst_x = (self.width - len(inst)) // 2
            self.stdscr.addstr(inst_y + i, inst_x, inst)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        cities_alive = sum(1 for city in self.cities if city['alive'])
        state.update({
            'wave': self.wave,
            'cities_alive': cities_alive,
            'cities_saved': self.cities_saved,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'bases': self.bases,
            'cities': self.cities,
            'wave': self.wave,
            'cities_saved': self.cities_saved,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.bases = state.get('bases', self.bases)
        self.cities = state.get('cities', self.cities)
        self.wave = state.get('wave', 1)
        self.cities_saved = state.get('cities_saved', 0)
        self._start_wave()
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        cities_alive = sum(1 for city in self.cities if city['alive'])
        if cities_alive > 0:
            title = "CITIES SAVED!"
            self.won = True
        else:
            title = "ALL CITIES DESTROYED!"
        
        extra_info = [
            f"Wave Reached: {self.wave}",
            f"Cities Saved: {self.cities_saved}",
            f"Cities Surviving: {cities_alive}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

