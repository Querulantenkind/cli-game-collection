"""Conway's Game of Life cellular automaton."""

import curses
import random
import time as time_module
from typing import List, Tuple, Dict, Any, Set
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class ConwayGame(BaseGame):
    """Conway's Game of Life simulation."""
    
    # Common patterns
    PATTERNS = {
        'glider': [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
        'blinker': [(0, 0), (0, 1), (0, 2)],
        'toad': [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)],
        'beacon': [(0, 0), (0, 1), (1, 0), (2, 3), (3, 2), (3, 3)],
        'pulsar': [
            (2, 4), (2, 5), (2, 6), (2, 10), (2, 11), (2, 12),
            (4, 2), (4, 7), (4, 9), (4, 14),
            (5, 2), (5, 7), (5, 9), (5, 14),
            (6, 2), (6, 7), (6, 9), (6, 14),
            (7, 4), (7, 5), (7, 6), (7, 10), (7, 11), (7, 12),
            (9, 4), (9, 5), (9, 6), (9, 10), (9, 11), (9, 12),
            (10, 2), (10, 7), (10, 9), (10, 14),
            (11, 2), (11, 7), (11, 9), (11, 14),
            (12, 2), (12, 7), (12, 9), (12, 14),
            (14, 4), (14, 5), (14, 6), (14, 10), (14, 11), (14, 12),
        ],
    }
    
    def __init__(self):
        super().__init__('conway', min_height=24, min_width=80)
        
        # Game constants
        self.GRID_WIDTH = 60
        self.GRID_HEIGHT = 18
        
        # Game state
        self.grid: Set[Tuple[int, int]] = set()
        self.cursor_x = self.GRID_WIDTH // 2
        self.cursor_y = self.GRID_HEIGHT // 2
        self.running = False
        self.generation = 0
        self.population = 0
        
        # Speed control
        speed = self.settings.get('conway', 'speed', 'medium')
        speed_map = {'slow': 0.5, 'medium': 0.2, 'fast': 0.05}
        self.update_interval = speed_map.get(speed, 0.2)
        self.last_update = 0
        
        # Statistics
        self.max_population = 0
        self.stable_count = 0
        self.last_population = 0
    
    def _get_input_timeout(self) -> int:
        return 50
    
    def _init_game(self):
        """Initialize the game."""
        self.grid = set()
        self.generation = 0
        self.population = 0
        self.running = False
    
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
        
        # Cursor movement
        if key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(self.GRID_HEIGHT - 1, self.cursor_y + 1)
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.GRID_WIDTH - 1, self.cursor_x + 1)
        
        # Cell toggle
        elif key == ord(' '):
            cell = (self.cursor_y, self.cursor_x)
            if cell in self.grid:
                self.grid.remove(cell)
            else:
                self.grid.add(cell)
            self._update_population()
        
        # Simulation control
        elif key == ord('\n') or key == ord('\r'):
            self.running = not self.running
        elif key == ord('s'):
            # Step one generation
            if not self.running:
                self._next_generation()
        
        # Grid control
        elif key == ord('c'):
            # Clear grid
            self.grid.clear()
            self.generation = 0
            self.population = 0
            self.running = False
        elif key == ord('r'):
            # Random fill
            self.grid.clear()
            density = 0.3
            for y in range(self.GRID_HEIGHT):
                for x in range(self.GRID_WIDTH):
                    if random.random() < density:
                        self.grid.add((y, x))
            self._update_population()
            self.generation = 0
        
        # Pattern insertion
        elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
            pattern_map = {
                ord('1'): 'glider',
                ord('2'): 'blinker',
                ord('3'): 'toad',
                ord('4'): 'beacon',
                ord('5'): 'pulsar',
            }
            pattern_name = pattern_map.get(key)
            if pattern_name:
                self._insert_pattern(pattern_name)
        
        return True
    
    def _insert_pattern(self, pattern_name: str):
        """Insert a pattern at cursor position."""
        pattern = self.PATTERNS.get(pattern_name, [])
        for dy, dx in pattern:
            y, x = self.cursor_y + dy, self.cursor_x + dx
            if 0 <= y < self.GRID_HEIGHT and 0 <= x < self.GRID_WIDTH:
                self.grid.add((y, x))
        self._update_population()
    
    def _update_population(self):
        """Update population count."""
        self.population = len(self.grid)
        if self.population > self.max_population:
            self.max_population = self.population
    
    def _count_neighbors(self, y: int, x: int) -> int:
        """Count live neighbors of a cell."""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                ny, nx = y + dy, x + dx
                if (ny, nx) in self.grid:
                    count += 1
        return count
    
    def _next_generation(self):
        """Compute next generation."""
        # Check all cells that might change
        cells_to_check = set()
        for y, x in self.grid:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < self.GRID_HEIGHT and 0 <= nx < self.GRID_WIDTH:
                        cells_to_check.add((ny, nx))
        
        new_grid = set()
        for y, x in cells_to_check:
            neighbors = self._count_neighbors(y, x)
            is_alive = (y, x) in self.grid
            
            # Conway's rules
            if is_alive and neighbors in [2, 3]:
                new_grid.add((y, x))
            elif not is_alive and neighbors == 3:
                new_grid.add((y, x))
        
        self.grid = new_grid
        self.generation += 1
        self._update_population()
        
        # Check for stability
        if self.population == self.last_population:
            self.stable_count += 1
        else:
            self.stable_count = 0
        self.last_population = self.population
        
        # Score based on generations and max population
        self.score = self.generation + (self.max_population // 10)
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        if self.running:
            self.last_update += delta_time
            if self.last_update >= self.update_interval:
                self.last_update = 0
                self._next_generation()
                
                # Auto-end after 1000 generations or if extinct
                if self.generation >= 1000 or self.population == 0:
                    self.game_over = True
                    self.won = (self.generation >= 1000)
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        title = "Conway's Game of Life"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Stats
        stats_y = 2
        status = "RUNNING" if self.running else "PAUSED"
        stats = [
            f"Gen: {self.generation}  Pop: {self.population}  Max: {self.max_population}  Status: {status}",
        ]
        for i, stat in enumerate(stats):
            stat_x = (self.width - len(stat)) // 2
            self.stdscr.addstr(stats_y + i, stat_x, stat)
        
        # Draw grid
        grid_start_y = 4
        grid_start_x = (self.width - self.GRID_WIDTH) // 2
        
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                cell_y = grid_start_y + y
                cell_x = grid_start_x + x
                
                is_alive = (y, x) in self.grid
                is_cursor = (y == self.cursor_y and x == self.cursor_x)
                
                if is_alive:
                    char = '#'
                    attr = curses.A_BOLD
                elif is_cursor:
                    char = '+'
                    attr = curses.A_REVERSE
                else:
                    char = '.'
                    attr = curses.A_DIM
                
                if is_cursor and is_alive:
                    attr = curses.A_BOLD | curses.A_REVERSE
                
                self.stdscr.addstr(cell_y, cell_x, char, attr)
        
        # Instructions
        inst_y = grid_start_y + self.GRID_HEIGHT + 1
        instructions = [
            "Arrow Keys: Move | Space: Toggle cell | Enter: Start/Stop",
            "S: Step | C: Clear | R: Random | 1-5: Insert pattern",
            "Patterns: 1=Glider 2=Blinker 3=Toad 4=Beacon 5=Pulsar",
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
        state.update({
            'generation': self.generation,
            'max_population': self.max_population,
            'stable_count': self.stable_count,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'grid': list(self.grid),
            'generation': self.generation,
            'population': self.population,
            'max_population': self.max_population,
            'running': self.running,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.grid = set(tuple(cell) for cell in state.get('grid', []))
        self.generation = state.get('generation', 0)
        self.population = state.get('population', 0)
        self.max_population = state.get('max_population', 0)
        self.running = state.get('running', False)
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "SIMULATION COMPLETE!"
        elif self.population == 0:
            title = "EXTINCTION!"
        else:
            title = "SIMULATION ENDED"
        
        extra_info = [
            f"Generations: {self.generation}",
            f"Max Population: {self.max_population}",
            f"Final Population: {self.population}"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

