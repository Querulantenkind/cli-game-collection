# CLI Game Collection

A collection of classic games playable directly in your terminal! Built with Python and curses for a nostalgic gaming experience.

## Games

- **Snake** - The classic snake game. Eat food to grow and avoid hitting walls or yourself!
- **Tetris** - Stack falling blocks to clear lines and increase your score. The game gets faster as you level up!
- **Pac-Man** - Navigate the maze, collect dots, and avoid ghosts. Eat power pellets to turn the tables!
- **Pong** - Classic paddle game. Play against AI or a friend! First to 5 points wins.
- **2048** - Slide numbered tiles to combine them and reach 2048!
- **Minesweeper** - Find all mines without detonating any! Use logic and flags.
- **Space Invaders** - Shoot down invading aliens before they reach you!
- **Breakout** - Break all bricks with the ball and paddle!
- **Hangman** - Guess the word before the hangman is drawn!

## Installation

This project uses Python 3 and the built-in `curses` library (available on Unix-like systems).

1. Clone the repository:
```bash
git clone <repository-url>
cd cli-game-collection
```

2. Make sure you have Python 3 installed:
```bash
python3 --version
```

3. Run the game collection:
```bash
python3 main.py
```

## How to Play

### Snake
- Use **Arrow Keys** to control the snake's direction
- Eat the `*` (food) to grow and increase your score
- Avoid hitting the walls or your own tail
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Tetris
- Use **← →** to move pieces left and right
- Use **↓** for soft drop (faster fall)
- Use **↑** or **Space** to rotate pieces
- Clear lines to score points and level up
- The game speeds up as you progress
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Pac-Man
- Use **Arrow Keys** to navigate the maze
- Collect dots (`.`) to score points
- Eat power pellets (`O`) to make ghosts vulnerable
- Avoid ghosts when they're not frightened
- Eat frightened ghosts for bonus points
- Clear all dots to win!
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Pong
- **Player 1**: Use **W/S** or **↑↓** to move paddle
- **Player 2** (2-player mode): Use **I/K** to move paddle
- Press **A** to toggle between AI and 2-player mode
- First to 5 points wins!
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### 2048
- Use **Arrow Keys** to slide tiles in that direction
- Combine tiles with the same number to create higher numbers
- Goal is to reach 2048, but you can keep playing!
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Minesweeper
- Use **Arrow Keys** to move cursor
- Press **Space** or **Enter** to reveal a cell
- Press **F** to toggle flag on suspected mines
- Numbers show how many mines are adjacent
- You have 6 wrong guesses before game over
- Press **Q** to quit and return to the menu

### Space Invaders
- Use **← →** or **A/D** to move your ship
- Press **Space** to shoot
- Clear all enemies to win!
- You have 3 lives
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Breakout
- Use **← →** or **A/D** to move the paddle
- Break all bricks to win!
- You have 3 lives - don't let the ball fall
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Hangman
- Type letters (**A-Z**) to guess
- You have 6 wrong guesses before game over
- Score is based on how few wrong guesses you make
- Words are programming/computer related
- Press **Q** to quit and return to the menu

### Menu Navigation
- Use **↑** and **↓** arrow keys to navigate
- Press **Enter** to select a game
- Press **Q** to exit

### Settings
- Access the **Settings** menu from the main menu
- Configure game speed (slow, medium, fast) for each game
- Adjust difficulty levels (easy, normal, hard)
- Set starting level for Tetris
- Toggle high score display
- Press **R** to reset all settings to defaults
- Use **← →** to change setting values

### Statistics
- View your game statistics from the main menu
- See total games played, wins, losses
- Track play time and average scores
- View best scores per game
- Statistics are automatically tracked

### Help
- Access the **Help** menu from the main menu
- View controls and tips for each game
- General help for navigation and features
- Press **Q** to go back from help screens

## Features

- **High Score System** - Your best scores are automatically saved and displayed
- **Settings Menu** - Customize game speed, difficulty, and other options
- **Statistics Tracking** - Track games played, wins, play time, and more
- **Help & Tutorials** - In-game help system with controls and tips for each game
- **Shared Utilities** - Common UI components and helper functions for consistent experience
- **Base Game Class** - Reusable foundation for easy game development
- **Terminal Validation** - Automatic size checking prevents crashes on small terminals
- **Persistent Data** - High scores, settings, and statistics saved to `data/` directory
- **Cross-Game Integration** - Settings and high scores work across all games

## Requirements

- Python 3.6+
- Unix-like system (Linux, macOS) with curses support
- Terminal with at least 80x24 characters

## Architecture

### Base Game Class

All games can inherit from `BaseGame` in `utils/base_game.py` to get:
- Automatic manager initialization (high scores, settings, statistics)
- Curses setup and cleanup
- Terminal size validation
- Statistics tracking
- High score management
- Standardized game loop

### Terminal Validation

The collection includes terminal size validation to prevent crashes on small terminals. Games specify minimum terminal dimensions and show helpful error messages if the terminal is too small.

## Adding New Games

To add a new game:

### Option 1: Using BaseGame (Recommended)

1. Create a new file in the `games/` directory (e.g., `games/my_game.py`)
2. Inherit from `BaseGame` and implement required methods:
   ```python
   from utils.base_game import BaseGame
   
   class MyGame(BaseGame):
       def __init__(self):
           super().__init__('my_game', min_height=24, min_width=80)
           # Initialize your game state
       
       def _init_game(self):
           # Called once before game loop starts
           pass
       
       def _handle_input(self, key: int) -> bool:
           # Handle input, return False to quit
           if key == ord('q'):
               return False
           return True
       
       def _update_game(self, delta_time: float):
           # Update game state each frame
           pass
       
       def _draw_game(self):
           # Draw the game each frame
           self.stdscr.clear()
           # ... drawing code ...
       
       def _draw_game_over(self, is_new_high: bool = False):
           # Draw game over screen
           pass
   ```
3. Add an entry to the menu in `games/menu.py`:
   ```python
   ("My Game", self._run_my_game)
   ```
4. Add the corresponding method to run your game

### Option 2: Standalone Game

1. Create a new file in the `games/` directory
2. Implement a game class with a `run()` method
3. Manually initialize managers and handle curses setup
4. Add to menu as above

## License

MIT License - See LICENSE file for details