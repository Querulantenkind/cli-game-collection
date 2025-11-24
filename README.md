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
- **Tic-Tac-Toe** - Classic 3x3 game. Get three in a row to win! Play against AI or a friend.
- **Wordle** - Guess the 5-letter word in 6 tries! Programming/tech themed words.
- **Frogger** - Cross the road and river! Avoid cars, ride logs, reach the goals.
- **Sudoku** - Classic number puzzle! Fill the 9x9 grid with logic.
- **Connect Four** - Drop pieces to get four in a row! Play against AI or a friend.
- **Battleship** - Strategic naval combat. Place ships and sink the enemy fleet!
- **Conway's Game of Life** - Watch cellular automaton patterns evolve and grow.
- **Asteroids** - Classic space shooter. Destroy asteroids and survive!
- **Centipede** - Shoot the descending centipede before it reaches you!
- **Missile Command** - Defend your cities from incoming ballistic missiles!

## 🚀 Quick Start

### Installation

This project uses Python 3 and the built-in `curses` library (available on Unix-like systems).

**Prerequisites:**
- Python 3.6 or higher
- Unix-like system (Linux, macOS, WSL on Windows)
- Terminal with minimum 80x24 character size

**Setup:**

```bash
# Clone the repository
git clone <repository-url>
cd cli-game-collection

# Verify Python version
python3 --version

# Run the game collection
python3 main.py

# Or use make (recommended)
make run
```

### First Time Setup

The game will automatically create a `data/` directory to store:
- High scores
- Game settings
- Statistics
- Saved games
- Achievement progress

No external dependencies required! 🎉

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

### Tic-Tac-Toe
- Use **Arrow Keys** to move the cursor
- Press **Space** or **Enter** to place your mark (X)
- Press **M** to toggle between AI and 2-player mode
- Get three in a row (horizontal, vertical, or diagonal) to win
- Press **P** to pause/unpause
- Press **Q** to quit and return to the menu

### Wordle
- Type **A-Z** letters to build your guess
- Press **Enter** to submit when you have 5 letters
- Press **Backspace** to delete letters
- **[X]** = Correct letter in correct position
- **X** = Letter is in the word but wrong position
- **·X·** = Letter is not in the word
- You have 6 guesses to find the word
- All words are programming/tech related
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

## ✨ Features

### 🎮 Games (19)
- **Snake** - Classic endless growth game
- **Tetris** - Block stacking puzzle
- **Pac-Man** - Maze navigation with ghosts
- **Pong** - Paddle sports classic
- **2048** - Number merging puzzle
- **Minesweeper** - Logic-based mine detection
- **Space Invaders** - Alien shooter
- **Breakout** - Brick breaking arcade
- **Hangman** - Word guessing with programming terms
- **Tic-Tac-Toe** - Strategy board game with AI
- **Wordle** - 5-letter word guessing (tech themed)
- **Frogger** - Lane-crossing challenge
- **Sudoku** - Number placement puzzle
- **Connect Four** - Four-in-a-row strategy game
- **Battleship** - Naval combat and strategy
- **Conway's Game of Life** - Cellular automaton simulation
- **Asteroids** - Classic space shooter
- **Centipede** - Arcade bug-shooting action
- **Missile Command** - City defense game

### 🏆 Progression Systems
- **High Scores** - Top 10 scores per game, automatically tracked
- **Achievements** - 50 achievements across all games with point system
- **Daily Challenges** - 3 rotating challenges daily with streak tracking
- **Statistics** - Comprehensive tracking with graphs and trends
  - Win rates and streaks
  - Score history and trends
  - Play time tracking
  - Session history

### 💾 Persistence
- **Save/Load System** - 5 save slots per game
- **Auto-Save Settings** - Preferences persist between sessions
- **Statistics Tracking** - Complete game history
- **Achievement Progress** - Never lose your unlocks

### 🎨 Customization
- **5 Visual Themes** - Classic, Dark, Neon, Retro, Minimal
- **Speed Settings** - Slow, Medium, Fast for each game
- **Difficulty Levels** - Easy, Normal, Hard
- **UI Animations** - Splash screens, notifications, effects

### 🛠️ Developer Features
- **BaseGame Architecture** - Reusable game foundation
- **Manager System** - Centralized state management
- **Terminal Validation** - Automatic size checking
- **UI Utilities** - Shared drawing and animation functions
- **Testing Framework** - Unit tests for core systems
- **Documentation** - Comprehensive API and developer guides

## 📋 Requirements

- **Python** 3.6 or higher
- **Operating System** Unix-like system (Linux, macOS, WSL)
- **Terminal** Minimum 80x24 characters
- **Dependencies** None! Uses only Python standard library

### Tested On
- ✅ Linux (Arch, Ubuntu, Debian)
- ✅ macOS (Terminal.app, iTerm2)
- ✅ Windows WSL (Ubuntu)

### Terminal Emulators
- ✅ GNOME Terminal
- ✅ Konsole
- ✅ iTerm2
- ✅ Alacritty
- ✅ Kitty
- ⚠️ Windows CMD (not supported - use WSL)

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

## 📊 Project Structure

```
cli-game-collection/
├── main.py                 # Entry point
├── games/                  # Game implementations
│   ├── menu.py            # Main menu
│   ├── snake.py           # Snake game
│   ├── tetris.py          # Tetris game
│   ├── ... (11 more games)
│   ├── settings_menu.py   # Settings interface
│   ├── statistics_menu.py # Statistics display
│   ├── help_menu.py       # Help system
│   ├── achievements_menu.py # Achievements viewer
│   ├── load_menu.py       # Save/load interface
│   └── challenges_menu.py # Daily challenges
├── utils/                  # Shared utilities
│   ├── base_game.py       # Base game class
│   ├── high_score.py      # High score manager
│   ├── settings.py        # Settings manager
│   ├── statistics.py      # Statistics manager
│   ├── achievements.py    # Achievement system
│   ├── themes.py          # Theme manager
│   ├── save_manager.py    # Save/load system
│   ├── daily_challenges.py # Daily challenge system
│   ├── ui_helpers.py      # UI utilities
│   ├── ui_animations.py   # Animation effects
│   └── terminal.py        # Terminal validation
├── tests/                  # Test suite
│   ├── test_managers.py   # Manager tests
│   ├── test_games.py      # Game tests
│   └── run_tests.py       # Test runner
├── scripts/               # Utility scripts
│   └── check_quality.py  # Code quality checker
├── data/                  # Runtime data (auto-created)
│   ├── high_scores.json
│   ├── settings.json
│   ├── statistics.json
│   ├── achievements.json
│   ├── daily_challenges.json
│   └── saves/            # Game save files
├── README.md             # This file
├── API.md                # API documentation
├── DEVELOPER.md          # Developer guide
├── CONTRIBUTING.md       # Contribution guidelines
├── CHANGELOG.md          # Version history
├── ENHANCEMENT_ROADMAP.md # Future features
├── PROJECT_SUMMARY.md    # Complete overview
├── Makefile              # Build commands
└── requirements.txt      # No dependencies!
```

## 🧪 Testing

```bash
# Run all tests
make test
# or
python3 tests/run_tests.py

# Check code quality
python3 scripts/check_quality.py

# Run linting
make lint
```

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code of conduct
- Development setup
- Coding standards
- Pull request process

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📚 Documentation

- **[README.md](README.md)** - User guide and getting started (this file)
- **[API.md](API.md)** - Complete API reference
- **[DEVELOPER.md](DEVELOPER.md)** - Developer guide for adding games
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[ENHANCEMENT_ROADMAP.md](ENHANCEMENT_ROADMAP.md)** - Future plans

## 🎯 Roadmap

### Completed ✅
- [x] Core game collection (13 games)
- [x] High score system
- [x] Settings management
- [x] Statistics tracking
- [x] Achievement system
- [x] Theme system
- [x] Save/load system
- [x] Daily challenges
- [x] UI animations
- [x] Testing framework
- [x] Complete documentation

### Planned 🚀
- [ ] More games (Asteroids, Conway's Game of Life, etc.)
- [ ] Game mode variations (Snake modes, Tetris modes)
- [ ] Replay system
- [ ] Tournament mode
- [ ] Multiplayer networking
- [ ] Leaderboards
- [ ] Custom themes
- [ ] Sound effects (optional)

See [ENHANCEMENT_ROADMAP.md](ENHANCEMENT_ROADMAP.md) for detailed plans.

## ❓ FAQ

**Q: Does this work on Windows?**
A: Use WSL (Windows Subsystem for Linux) for full compatibility.

**Q: My terminal is too small!**
A: Resize to at least 80x24. The game will show helpful error messages.

**Q: Where is my data stored?**
A: All data is in the `./data/` directory in JSON format.

**Q: Can I customize the games?**
A: Yes! Check [DEVELOPER.md](DEVELOPER.md) for adding games and [CONTRIBUTING.md](CONTRIBUTING.md) for modification guidelines.

**Q: Are there any external dependencies?**
A: No! Only Python 3.6+ standard library is required.

**Q: How do I reset my high scores?**
A: Delete `data/high_scores.json` or use the settings menu reset option.

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Inspired by classic arcade games and terminal gaming communities.

Built with ❤️ using Python's curses library.

---

**Happy Gaming! 🎮**

For support, issues, or feature requests, please open an issue on GitHub.