"""Pac-Man game implementation."""

import curses
import random
import time
from typing import List, Tuple
from enum import Enum
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


# Simple maze layout (1 = wall, 0 = path, 2 = dot, 3 = power pellet)
MAZE_LAYOUT = [
    "####################",
    "#..........##......#",
    "#.####.######.####.#",
    "#.#..#........#..#.#",
    "#.#..####  ####..#.#",
    "#..........##......#",
    "####.######.########",
    "   #.#..........#",
    "####.#.######.####",
    "#......##..........#",
    "#.####.######.####.#",
    "#.#..#........#..#.#",
    "#.#..####  ####..#.#",
    "#..........##......#",
    "####################",
]


class PacManGame(BaseGame):
    """Classic Pac-Man game for the terminal."""
    
    def __init__(self):
        super().__init__('pacman', min_height=24, min_width=80)
        
        self.maze = []
        self.pacman_pos = (1, 1)
        self.pacman_dir = Direction.RIGHT
        self.next_dir = Direction.RIGHT
        self.ghosts = [
            {'pos': (6, 9), 'dir': Direction.LEFT, 'frightened': False},
            {'pos': (6, 10), 'dir': Direction.RIGHT, 'frightened': False},
            {'pos': (8, 9), 'dir': Direction.UP, 'frightened': False},
            {'pos': (8, 10), 'dir': Direction.DOWN, 'frightened': False},
        ]
        self.dots_remaining = 0
        self.power_pellet_time = 0
        self.ghost_move_counter = 0
    
    def _get_input_timeout(self) -> int:
        base_timeout = 150
        speed_mult = self._get_game_speed()
        return int(base_timeout * speed_mult)
    
    def _init_game(self):
        """Initialize maze."""
        self._init_maze()
    
    def _init_maze(self):
        """Initialize the maze from layout."""
        self.maze = []
        self.dots_remaining = 0
        for row in MAZE_LAYOUT:
            maze_row = []
            for char in row:
                if char == '#':
                    maze_row.append(1)  # Wall
                elif char == ' ':
                    maze_row.append(1)  # Wall (spaces are walls)
                else:
                    if random.random() < 0.15:  # 15% chance for power pellet
                        maze_row.append(3)  # Power pellet
                        self.dots_remaining += 1
                    else:
                        maze_row.append(2)  # Dot
                        self.dots_remaining += 1
            self.maze.append(maze_row)
    
    def _can_move(self, pos, direction):
        """Check if a position is valid for movement."""
        dy, dx = direction.value
        new_y, new_x = pos[0] + dy, pos[1] + dx
        
        if new_y < 0 or new_y >= len(self.maze) or new_x < 0 or new_x >= len(self.maze[0]):
            return False
        
        return self.maze[new_y][new_x] != 1  # Not a wall
    
    def _move_pacman(self):
        """Move Pac-Man."""
        if self.next_dir != self.pacman_dir:
            if self._can_move(self.pacman_pos, self.next_dir):
                self.pacman_dir = self.next_dir
        
        if self._can_move(self.pacman_pos, self.pacman_dir):
            dy, dx = self.pacman_dir.value
            self.pacman_pos = (self.pacman_pos[0] + dy, self.pacman_pos[1] + dx)
            
            # Collect dot or power pellet
            y, x = self.pacman_pos
            if self.maze[y][x] == 2:  # Dot
                self.maze[y][x] = 0
                self.score += 10
                self.dots_remaining -= 1
            elif self.maze[y][x] == 3:  # Power pellet
                self.maze[y][x] = 0
                self.score += 50
                self.dots_remaining -= 1
                self.power_pellet_time = 10.0
                for ghost in self.ghosts:
                    ghost['frightened'] = True
    
    def _move_ghosts(self):
        """Move all ghosts with simple AI."""
        for ghost in self.ghosts:
            if ghost['frightened']:
                possible_dirs = [d for d in Direction if self._can_move(ghost['pos'], d)]
                if possible_dirs:
                    ghost['dir'] = random.choice(possible_dirs)
            else:
                py, px = self.pacman_pos
                gy, gx = ghost['pos']
                
                best_dir = ghost['dir']
                min_dist = float('inf')
                
                for direction in Direction:
                    if self._can_move(ghost['pos'], direction):
                        dy, dx = direction.value
                        new_pos = (gy + dy, gx + dx)
                        dist = abs(new_pos[0] - py) + abs(new_pos[1] - px)
                        if dist < min_dist:
                            min_dist = dist
                            best_dir = direction
                
                ghost['dir'] = best_dir
            
            if self._can_move(ghost['pos'], ghost['dir']):
                dy, dx = ghost['dir'].value
                ghost['pos'] = (ghost['pos'][0] + dy, ghost['pos'][1] + dx)
    
    def _check_collisions(self):
        """Check for collisions between Pac-Man and ghosts."""
        for ghost in self.ghosts:
            if ghost['pos'] == self.pacman_pos:
                if ghost['frightened']:
                    self.score += 200
                    ghost['pos'] = (6, 9)
                    ghost['frightened'] = False
                else:
                    self.game_over = True
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif key == ord('p'):
            self.paused = not self.paused
        elif not self.paused:
            if key == curses.KEY_UP:
                self.next_dir = Direction.UP
            elif key == curses.KEY_DOWN:
                self.next_dir = Direction.DOWN
            elif key == curses.KEY_LEFT:
                self.next_dir = Direction.LEFT
            elif key == curses.KEY_RIGHT:
                self.next_dir = Direction.RIGHT
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        if self.paused:
            return
        
        # Update power pellet timer
        if self.power_pellet_time > 0:
            self.power_pellet_time -= delta_time
            if self.power_pellet_time <= 0:
                for ghost in self.ghosts:
                    ghost['frightened'] = False
        
        # Move Pac-Man
        self._move_pacman()
        
        # Move ghosts (every other frame)
        self.ghost_move_counter += 1
        if self.ghost_move_counter >= 2:
            self.ghost_move_counter = 0
            self._move_ghosts()
        
        # Check collisions
        self._check_collisions()
        
        # Check win condition
        if self.dots_remaining == 0:
            self.won = True
            self.game_over = True
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        maze_start_y = 2
        maze_start_x = 2
        
        # Draw maze
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if cell == 1:  # Wall
                    self.stdscr.addch(maze_start_y + y, maze_start_x + x, '#', curses.A_BOLD)
                elif cell == 2:  # Dot
                    self.stdscr.addch(maze_start_y + y, maze_start_x + x, '.')
                elif cell == 3:  # Power pellet
                    self.stdscr.addch(maze_start_y + y, maze_start_x + x, 'O', curses.A_BOLD)
        
        # Draw Pac-Man
        self.stdscr.addch(maze_start_y + self.pacman_pos[0], maze_start_x + self.pacman_pos[1], 
                        'C', curses.A_BOLD)
        
        # Draw ghosts
        ghost_chars = ['G', 'G', 'G', 'G']
        for i, ghost in enumerate(self.ghosts):
            attr = curses.A_DIM if ghost['frightened'] else curses.A_BOLD
            self.stdscr.addch(maze_start_y + ghost['pos'][0], maze_start_x + ghost['pos'][1], 
                            ghost_chars[i], attr)
        
        # Info
        info_x = maze_start_x + len(self.maze[0]) + 3
        extra_info = {'Dots': self.dots_remaining}
        if self.power_pellet_time > 0:
            extra_info['Power'] = f"{int(self.power_pellet_time)}s"
        self._draw_info_bar(extra_info)
        
        # Controls
        controls = [
            "Arrow Keys: Move",
            "P: Pause",
            "Q: Quit"
        ]
        for i, control in enumerate(controls):
            self.stdscr.addstr(10 + i, info_x, control)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "YOU WIN!"
        else:
            title = "GAME OVER"
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, []
        )
