"""Battleship game with AI opponent."""

import curses
import random
from typing import List, Tuple, Optional, Dict, Any, Set
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class BattleshipGame(BaseGame):
    """Battleship game for the terminal."""
    
    # Ship definitions: (name, length)
    SHIPS = [
        ('Carrier', 5),
        ('Battleship', 4),
        ('Cruiser', 3),
        ('Submarine', 3),
        ('Destroyer', 2),
    ]
    
    def __init__(self):
        super().__init__('battleship', min_height=24, min_width=80)
        
        # Game constants
        self.GRID_SIZE = 10
        
        # Game state
        self.player_grid = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.ai_grid = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.player_shots = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.ai_shots = [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        
        # Ship tracking
        self.player_ships: Set[Tuple[int, int]] = set()
        self.ai_ships: Set[Tuple[int, int]] = set()
        self.player_hits = 0
        self.ai_hits = 0
        
        # Cursor and game phase
        self.cursor_x = 0
        self.cursor_y = 0
        self.phase = 'setup'  # 'setup', 'player_turn', 'ai_turn', 'game_over'
        self.current_ship_idx = 0
        self.ship_horizontal = True
        
        # AI targeting
        self.ai_last_hit = None
        self.ai_targets = []
        
        # Stats
        self.player_shots_fired = 0
        self.ai_shots_fired = 0
        self.total_ship_cells = sum(ship[1] for ship in self.SHIPS)
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize the game."""
        # Place AI ships randomly
        self._place_ai_ships()
        self.phase = 'setup'
        self.current_ship_idx = 0
    
    def _place_ai_ships(self):
        """Randomly place AI ships."""
        self.ai_ships.clear()
        for ship_name, ship_len in self.SHIPS:
            placed = False
            while not placed:
                horizontal = random.choice([True, False])
                if horizontal:
                    row = random.randint(0, self.GRID_SIZE - 1)
                    col = random.randint(0, self.GRID_SIZE - ship_len)
                    positions = [(row, col + i) for i in range(ship_len)]
                else:
                    row = random.randint(0, self.GRID_SIZE - ship_len)
                    col = random.randint(0, self.GRID_SIZE - 1)
                    positions = [(row + i, col) for i in range(ship_len)]
                
                # Check if positions are free
                if all(pos not in self.ai_ships for pos in positions):
                    self.ai_ships.update(positions)
                    for row, col in positions:
                        self.ai_grid[row][col] = 'S'
                    placed = True
    
    def _can_place_ship(self, row: int, col: int, length: int, horizontal: bool) -> bool:
        """Check if a ship can be placed at the given position."""
        if horizontal:
            if col + length > self.GRID_SIZE:
                return False
            positions = [(row, col + i) for i in range(length)]
        else:
            if row + length > self.GRID_SIZE:
                return False
            positions = [(row + i, col) for i in range(length)]
        
        return all(pos not in self.player_ships for pos in positions)
    
    def _place_player_ship(self, row: int, col: int, length: int, horizontal: bool):
        """Place a player ship."""
        if horizontal:
            positions = [(row, col + i) for i in range(length)]
        else:
            positions = [(row + i, col) for i in range(length)]
        
        self.player_ships.update(positions)
        for r, c in positions:
            self.player_grid[r][c] = 'S'
    
    def _handle_input(self, key: int) -> bool:
        """Handle player input."""
        if key == ord('q'):
            self.game_over = True
            return False
        
        if key == ord('p') and self.phase != 'setup':
            self.paused = not self.paused
            return True
        
        if self.paused:
            return True
        
        if self.phase == 'setup':
            return self._handle_setup_input(key)
        elif self.phase == 'player_turn':
            return self._handle_attack_input(key)
        
        return True
    
    def _handle_setup_input(self, key: int) -> bool:
        """Handle input during ship placement."""
        if key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(self.GRID_SIZE - 1, self.cursor_y + 1)
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.GRID_SIZE - 1, self.cursor_x + 1)
        elif key == ord('r'):
            # Rotate ship
            self.ship_horizontal = not self.ship_horizontal
        elif key == ord(' ') or key == ord('\n') or key == ord('\r'):
            # Place ship
            ship_name, ship_len = self.SHIPS[self.current_ship_idx]
            if self._can_place_ship(self.cursor_y, self.cursor_x, ship_len, self.ship_horizontal):
                self._place_player_ship(self.cursor_y, self.cursor_x, ship_len, self.ship_horizontal)
                self.current_ship_idx += 1
                if self.current_ship_idx >= len(self.SHIPS):
                    self.phase = 'player_turn'
        
        return True
    
    def _handle_attack_input(self, key: int) -> bool:
        """Handle input during attack phase."""
        if key == curses.KEY_UP:
            self.cursor_y = max(0, self.cursor_y - 1)
        elif key == curses.KEY_DOWN:
            self.cursor_y = min(self.GRID_SIZE - 1, self.cursor_y + 1)
        elif key == curses.KEY_LEFT:
            self.cursor_x = max(0, self.cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            self.cursor_x = min(self.GRID_SIZE - 1, self.cursor_x + 1)
        elif key == ord(' ') or key == ord('\n') or key == ord('\r'):
            # Fire at position
            if self.player_shots[self.cursor_y][self.cursor_x] == ' ':
                self._player_attack(self.cursor_y, self.cursor_x)
        
        return True
    
    def _player_attack(self, row: int, col: int):
        """Player attacks a position."""
        self.player_shots_fired += 1
        if (row, col) in self.ai_ships:
            self.player_shots[row][col] = 'X'  # Hit
            self.player_hits += 1
            self.score += 10
            
            if self.player_hits >= self.total_ship_cells:
                self.won = True
                self.game_over = True
        else:
            self.player_shots[row][col] = 'O'  # Miss
        
        if not self.game_over:
            self.phase = 'ai_turn'
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        if self.phase == 'ai_turn':
            import time
            time.sleep(0.5)
            self._ai_attack()
            self.phase = 'player_turn'
    
    def _ai_attack(self):
        """AI attacks a position."""
        # Smart AI that hunts after hitting
        target = None
        
        if self.ai_targets:
            # Continue targeting nearby cells
            target = self.ai_targets.pop(0)
        elif self.ai_last_hit:
            # Add adjacent cells to targets
            row, col = self.ai_last_hit
            adjacent = [
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1)
            ]
            for r, c in adjacent:
                if (0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE and
                    self.ai_shots[r][c] == ' '):
                    self.ai_targets.append((r, c))
            
            if self.ai_targets:
                target = self.ai_targets.pop(0)
        
        # Random shot if no targets
        if target is None:
            available = [(r, c) for r in range(self.GRID_SIZE) 
                        for c in range(self.GRID_SIZE)
                        if self.ai_shots[r][c] == ' ']
            if available:
                target = random.choice(available)
        
        if target:
            row, col = target
            self.ai_shots_fired += 1
            if (row, col) in self.player_ships:
                self.ai_shots[row][col] = 'X'  # Hit
                self.ai_hits += 1
                self.ai_last_hit = (row, col)
                
                if self.ai_hits >= self.total_ship_cells:
                    self.won = False
                    self.game_over = True
            else:
                self.ai_shots[row][col] = 'O'  # Miss
                if self.ai_last_hit == (row, col):
                    self.ai_last_hit = None
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        if self.phase == 'setup':
            title = "Battleship - Ship Placement"
        else:
            title = "Battleship - Battle Phase"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Draw grids side by side
        grid_y = 4
        left_grid_x = 5
        right_grid_x = self.width - 30
        
        # Left grid label
        if self.phase == 'setup':
            label = "Your Ships"
        else:
            label = "Your Fleet"
        self.stdscr.addstr(grid_y - 2, left_grid_x + 5, label, curses.A_BOLD)
        
        # Right grid label
        if self.phase != 'setup':
            label = "Enemy Waters"
            self.stdscr.addstr(grid_y - 2, right_grid_x + 3, label, curses.A_BOLD)
        
        # Draw left grid (player's ships)
        self._draw_grid(grid_y, left_grid_x, self.player_grid, self.ai_shots, 
                       show_ships=True, show_cursor=(self.phase == 'setup'))
        
        # Draw right grid (enemy grid) only during battle
        if self.phase != 'setup':
            self._draw_grid(grid_y, right_grid_x, self.ai_grid, self.player_shots,
                           show_ships=False, show_cursor=(self.phase == 'player_turn'))
        
        # Instructions based on phase
        inst_y = grid_y + 13
        if self.phase == 'setup':
            ship_name, ship_len = self.SHIPS[self.current_ship_idx]
            instructions = [
                f"Placing: {ship_name} (Length: {ship_len})",
                "Arrow Keys: Move cursor",
                "R: Rotate ship",
                "Space: Place ship",
                "Q: Quit"
            ]
        else:
            instructions = [
                f"Your Hits: {self.player_hits}/{self.total_ship_cells}  AI Hits: {self.ai_hits}/{self.total_ship_cells}",
                f"Shots: You {self.player_shots_fired} - AI {self.ai_shots_fired}",
                "Arrow Keys: Move cursor",
                "Space: Fire!",
                "P: Pause | Q: Quit"
            ]
        
        for i, inst in enumerate(instructions):
            inst_x = (self.width - len(inst)) // 2
            self.stdscr.addstr(inst_y + i, inst_x, inst)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _draw_grid(self, y: int, x: int, grid: List[List[str]], shots: List[List[str]],
                   show_ships: bool, show_cursor: bool):
        """Draw a grid."""
        # Column headers
        header = "   " + " ".join(str(i) for i in range(self.GRID_SIZE))
        self.stdscr.addstr(y - 1, x, header)
        
        for row in range(self.GRID_SIZE):
            # Row header
            self.stdscr.addstr(y + row, x, chr(ord('A') + row) + " ")
            
            # Grid cells
            for col in range(self.GRID_SIZE):
                cell_x = x + 3 + col * 2
                cell_y = y + row
                
                # Determine what to show
                shot = shots[row][col]
                has_ship = grid[row][col] == 'S'
                
                if shot == 'X':
                    char = 'X'
                    attr = curses.A_BOLD
                elif shot == 'O':
                    char = 'o'
                    attr = curses.A_DIM
                elif show_ships and has_ship:
                    char = 'S'
                    attr = curses.A_NORMAL
                else:
                    char = '.'
                    attr = curses.A_DIM
                
                # Highlight cursor
                if show_cursor and row == self.cursor_y and col == self.cursor_x:
                    attr |= curses.A_REVERSE
                
                self.stdscr.addstr(cell_y, cell_x, char, attr)
        
        # Draw ship preview during setup
        if show_cursor and self.phase == 'setup':
            ship_name, ship_len = self.SHIPS[self.current_ship_idx]
            if self._can_place_ship(self.cursor_y, self.cursor_x, ship_len, self.ship_horizontal):
                if self.ship_horizontal:
                    for i in range(ship_len):
                        if self.cursor_x + i < self.GRID_SIZE:
                            cell_x = x + 3 + (self.cursor_x + i) * 2
                            self.stdscr.addstr(y + self.cursor_y, cell_x, '#', 
                                             curses.A_BOLD | curses.A_REVERSE)
                else:
                    for i in range(ship_len):
                        if self.cursor_y + i < self.GRID_SIZE:
                            cell_x = x + 3 + self.cursor_x * 2
                            self.stdscr.addstr(y + self.cursor_y + i, cell_x, '#',
                                             curses.A_BOLD | curses.A_REVERSE)
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'player_hits': self.player_hits,
            'ai_hits': self.ai_hits,
            'player_shots': self.player_shots_fired,
            'ai_shots': self.ai_shots_fired,
            'accuracy': (self.player_hits / self.player_shots_fired * 100) if self.player_shots_fired > 0 else 0,
        })
        return state
    
    def _serialize_state(self) -> Dict[str, Any]:
        """Serialize game state for saving."""
        state = super()._serialize_state()
        state.update({
            'player_grid': self.player_grid,
            'ai_grid': self.ai_grid,
            'player_shots': self.player_shots,
            'ai_shots': self.ai_shots,
            'player_ships': list(self.player_ships),
            'ai_ships': list(self.ai_ships),
            'player_hits': self.player_hits,
            'ai_hits': self.ai_hits,
            'phase': self.phase,
            'player_shots_fired': self.player_shots_fired,
            'ai_shots_fired': self.ai_shots_fired,
        })
        return state
    
    def _deserialize_state(self, state: Dict[str, Any]):
        """Deserialize and restore game state."""
        super()._deserialize_state(state)
        self.player_grid = state.get('player_grid', [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)])
        self.ai_grid = state.get('ai_grid', [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)])
        self.player_shots = state.get('player_shots', [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)])
        self.ai_shots = state.get('ai_shots', [[' ' for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)])
        self.player_ships = set(tuple(pos) for pos in state.get('player_ships', []))
        self.ai_ships = set(tuple(pos) for pos in state.get('ai_ships', []))
        self.player_hits = state.get('player_hits', 0)
        self.ai_hits = state.get('ai_hits', 0)
        self.phase = state.get('phase', 'setup')
        self.player_shots_fired = state.get('player_shots_fired', 0)
        self.ai_shots_fired = state.get('ai_shots_fired', 0)
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "VICTORY!"
            accuracy = (self.player_hits / self.player_shots_fired * 100) if self.player_shots_fired > 0 else 0
            self.score = max(100, int(200 - self.player_shots_fired + accuracy))
        else:
            title = "DEFEAT!"
        
        extra_info = [
            f"Your Shots: {self.player_shots_fired}",
            f"AI Shots: {self.ai_shots_fired}",
            f"Your Accuracy: {(self.player_hits / self.player_shots_fired * 100):.1f}%" if self.player_shots_fired > 0 else "N/A"
        ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

