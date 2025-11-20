# API Documentation

## Table of Contents
- [Core Classes](#core-classes)
- [Managers](#managers)
- [Utilities](#utilities)
- [Game Classes](#game-classes)

---

## Core Classes

### BaseGame

Abstract base class for all games in the collection.

**Location:** `utils/base_game.py`

```python
class BaseGame(ABC):
    def __init__(self, game_name: str, min_height: int = 24, min_width: int = 80):
        """Initialize base game.
        
        Args:
            game_name: Unique identifier for the game
            min_height: Minimum terminal height required
            min_width: Minimum terminal width required
        """
```

**Abstract Methods:**
- `_init_game()` - Initialize game-specific state
- `_handle_input(key: int) -> bool` - Handle user input
- `_update_game(delta_time: float)` - Update game state
- `_draw_game()` - Render the game
- `_draw_game_over(is_new_high: bool)` - Render game over screen
- `_get_game_state() -> Dict[str, Any]` - Get current game state for statistics
- `_serialize_state() -> Dict[str, Any]` - Serialize game state for saving
- `_deserialize_state(state: Dict[str, Any])` - Restore game from saved state

**Properties:**
- `stdscr` - Curses window object
- `height` - Terminal height
- `width` - Terminal width
- `score` - Current score
- `running` - Game running state
- `paused` - Game paused state
- `game_over` - Game over state

**Methods:**
- `run()` - Main entry point to start the game
- `pause()` - Pause the game
- `resume()` - Resume the game
- `end_game(won: bool)` - End the game

---

## Managers

### HighScoreManager

Manages high scores for all games.

**Location:** `utils/high_score.py`

```python
class HighScoreManager:
    def __init__(self, data_dir: str = './data'):
        """Initialize high score manager."""
```

**Methods:**
- `add_score(game: str, score: int) -> bool` - Add a score, returns True if new high
- `get_high_score(game: str) -> int` - Get highest score for a game
- `get_top_scores(game: str, limit: int = 10) -> List[Dict]` - Get top scores
- `save()` - Save scores to disk
- `load()` - Load scores from disk

**Data Format:**
```json
{
  "snake": [
    {"score": 500, "timestamp": "2025-11-20T10:30:00"},
    {"score": 450, "timestamp": "2025-11-19T15:20:00"}
  ]
}
```

### SettingsManager

Manages game settings and configuration.

**Location:** `utils/settings.py`

```python
class SettingsManager:
    def __init__(self, data_dir: str = './data'):
        """Initialize settings manager."""
```

**Methods:**
- `get(game: str, key: str, default=None) -> Any` - Get a setting value
- `set(game: str, key: str, value: Any)` - Set a setting value
- `get_speed_multiplier(game: str) -> float` - Get speed multiplier for game
- `get_difficulty_multiplier(game: str) -> float` - Get difficulty multiplier
- `save()` - Save settings to disk
- `load()` - Load settings from disk

**Settings Structure:**
```python
{
  "general": {
    "sound": True,
    "theme": "classic"
  },
  "snake": {
    "speed": "medium",  # slow, medium, fast
    "difficulty": "normal"  # easy, normal, hard
  }
}
```

### StatisticsManager

Tracks player statistics and performance.

**Location:** `utils/statistics.py`

```python
class StatisticsManager:
    def __init__(self, data_dir: str = './data'):
        """Initialize statistics manager."""
```

**Methods:**
- `record_game_start(game: str)` - Record game start time
- `record_game_end(game: str, score: int, won: bool, play_time: float)` - Record game end
- `get_game_stats(game: str) -> Dict` - Get statistics for a game
- `get_overall_stats() -> Dict` - Get overall statistics
- `get_win_rate(game: str) -> float` - Get win rate percentage
- `get_current_streak(game: str) -> int` - Get current win streak
- `get_score_trend(game: str, limit: int = 10) -> List[int]` - Get recent scores
- `generate_score_graph(scores: List[int], height: int = 5) -> List[str]` - ASCII graph

**Statistics Data:**
```json
{
  "snake": {
    "games_played": 50,
    "games_won": 30,
    "total_score": 12500,
    "best_score": 500,
    "average_score": 250,
    "total_play_time": 3600,
    "sessions": [
      {
        "timestamp": "2025-11-20T10:30:00",
        "score": 500,
        "won": true,
        "play_time": 120.5
      }
    ]
  }
}
```

### AchievementManager

Manages player achievements and rewards.

**Location:** `utils/achievements.py`

```python
class AchievementManager:
    def __init__(self, data_dir: str = './data'):
        """Initialize achievement manager."""
```

**Methods:**
- `check_achievements(game: str, game_state: Dict) -> List[str]` - Check and unlock achievements
- `unlock(achievement_id: str) -> bool` - Manually unlock an achievement
- `is_unlocked(achievement_id: str) -> bool` - Check if unlocked
- `get_all_achievements() -> List[Achievement]` - Get all achievements
- `get_unlocked_achievements() -> List[Achievement]` - Get unlocked only
- `get_locked_achievements() -> List[Achievement]` - Get locked only
- `get_total_points() -> int` - Get total achievement points

**Achievement Structure:**
```python
@dataclass
class Achievement:
    id: str
    title: str
    description: str
    category: str  # milestone, mastery, challenge, explorer, special
    points: int
    unlocked: bool = False
    unlock_time: str = ""
```

### ThemeManager

Manages visual themes for games.

**Location:** `utils/themes.py`

```python
class ThemeManager:
    def __init__(self):
        """Initialize theme manager."""
```

**Methods:**
- `get_current_theme() -> Theme` - Get active theme
- `set_theme(theme_id: str)` - Set active theme
- `get_all_themes() -> Dict[str, Theme]` - Get all available themes
- `apply_theme(stdscr)` - Apply theme to terminal

**Theme Structure:**
```python
@dataclass
class Theme:
    id: str
    name: str
    description: str
    border_style: str  # single, double, rounded, ascii
    colors: Dict[str, int]  # color_name -> curses color pair
```

### SaveManager

Manages game save states.

**Location:** `utils/save_manager.py`

```python
class SaveManager:
    def __init__(self, data_dir: str = './data'):
        """Initialize save manager."""
```

**Methods:**
- `save_game(game: str, slot: int, game_state: Dict, metadata: Dict) -> bool` - Save game
- `load_game(game: str, slot: int) -> Optional[Dict]` - Load game
- `delete_save(game: str, slot: int) -> bool` - Delete save
- `get_save_list(game: str) -> List[Dict]` - Get all save slots for game

**Save Format:**
```json
{
  "game": "snake",
  "slot": 1,
  "timestamp": "2025-11-20T10:30:00",
  "metadata": {
    "score": 250,
    "level": 5
  },
  "game_state": {
    "snake": [[10, 10], [10, 11]],
    "food": [15, 15],
    "direction": "right"
  }
}
```

### DailyChallengeManager

Manages daily rotating challenges.

**Location:** `utils/daily_challenges.py`

```python
class DailyChallengeManager:
    def __init__(self, data_dir: str = './data'):
        """Initialize daily challenge manager."""
```

**Methods:**
- `get_daily_challenges(count: int = 3) -> List[Challenge]` - Get today's challenges
- `mark_completed(challenge_id: str) -> bool` - Mark challenge complete
- `is_completed(challenge_id: str) -> bool` - Check if completed today
- `get_streak() -> int` - Get current daily streak
- `get_total_points() -> int` - Get total challenge points

**Challenge Structure:**
```python
@dataclass
class Challenge:
    id: str
    game: str
    title: str
    description: str
    target: int
    target_type: str  # score, time, combo, etc.
    points: int
```

---

## Utilities

### UI Helpers

Common UI rendering functions.

**Location:** `utils/ui_helpers.py`

**Functions:**
- `draw_box(stdscr, y, x, height, width, title="")` - Draw bordered box
- `draw_centered_text(stdscr, y, text, attr=0)` - Draw centered text
- `draw_game_over_screen(stdscr, score, is_new_high)` - Standard game over
- `draw_pause_screen(stdscr)` - Standard pause screen
- `get_text_input(stdscr, prompt, max_length)` - Get text input from user

### Terminal Utilities

Terminal size validation and error handling.

**Location:** `utils/terminal.py`

**Functions:**
- `validate_terminal_size(min_height, min_width) -> Tuple[bool, int, int]` - Validate size
- `show_terminal_size_error(min_height, min_width, current_height, current_width)` - Show error

### UI Animations

Visual effects and animations.

**Location:** `utils/ui_animations.py`

**Functions:**
- `show_splash_screen(stdscr, title, duration=2.0)` - Animated splash screen
- `draw_progress_bar(stdscr, y, x, width, progress, label="")` - Progress bar
- `fade_in_text(stdscr, y, x, text, duration=1.0)` - Fade-in text effect
- `pulse_text(stdscr, y, x, text, pulses=3)` - Pulsing text
- `show_notification(stdscr, message, duration=2.0)` - Toast notification
- `draw_animated_box(stdscr, y, x, height, width, title="")` - Animated box draw

---

## Game Classes

### Snake

Classic snake game implementation.

**Location:** `games/snake.py`

**Controls:**
- Arrow keys: Move
- P: Pause
- Q: Quit

**Game State:**
```python
{
    "score": int,
    "level": int,
    "snake_length": int,
    "food_eaten": int
}
```

### Tetris

Block-stacking puzzle game.

**Location:** `games/tetris.py`

**Controls:**
- Arrow keys: Move/Rotate
- Space: Hard drop
- P: Pause
- Q: Quit

### Pac-Man

Maze navigation game.

**Location:** `games/pacman.py`

**Controls:**
- Arrow keys: Move
- P: Pause
- Q: Quit

### Pong

Classic paddle game.

**Location:** `games/pong.py`

**Controls:**
- W/S or Arrow keys: Move paddle
- P: Pause
- Q: Quit

### 2048

Number merging puzzle.

**Location:** `games/game2048.py`

**Controls:**
- Arrow keys: Slide tiles
- R: Restart
- Q: Quit

### Minesweeper

Mine-revealing logic game.

**Location:** `games/minesweeper.py`

**Controls:**
- Arrow keys: Move cursor
- Space: Reveal cell
- F: Flag cell
- Q: Quit

### Space Invaders

Alien shooter game.

**Location:** `games/space_invaders.py`

**Controls:**
- Arrow keys: Move
- Space: Shoot
- P: Pause
- Q: Quit

### Breakout

Brick-breaking game.

**Location:** `games/breakout.py`

**Controls:**
- Arrow keys: Move paddle
- Space: Launch ball
- P: Pause
- Q: Quit

### Hangman

Word guessing game.

**Location:** `games/hangman.py`

**Controls:**
- A-Z: Guess letter
- Q: Quit

### Tic-Tac-Toe

Classic strategy game.

**Location:** `games/tictactoe.py`

**Controls:**
- Arrow keys: Move cursor
- Space/Enter: Place mark
- Q: Quit

**Modes:**
- 1 Player vs AI
- 2 Player

### Wordle

Word guessing game.

**Location:** `games/wordle.py`

**Controls:**
- A-Z: Type letters
- Enter: Submit guess
- Backspace: Delete letter
- Q: Quit

### Frogger

Lane-crossing game.

**Location:** `games/frogger.py`

**Controls:**
- Arrow keys: Move
- P: Pause
- Q: Quit

### Sudoku

Number placement puzzle.

**Location:** `games/sudoku.py`

**Controls:**
- Arrow keys: Move cursor
- 1-9: Enter number
- Delete/0: Clear cell
- Q: Quit

---

## Event System

Games can emit events that trigger achievements and statistics updates.

### Standard Events
- `game_start` - Game begins
- `game_end` - Game ends (includes score, won status)
- `score_milestone` - Score reaches threshold
- `level_up` - Player advances level
- `perfect_round` - No mistakes in round
- `speed_run` - Complete in record time

### Custom Events

Games can define custom events:

```python
self.achievement_manager.check_achievements(
    self.game_name,
    {
        'game': self.game_name,
        'score': self.score,
        'won': True,
        'custom_metric': value
    }
)
```

---

## Data Storage

All persistent data is stored in JSON format in the `./data/` directory:

```
data/
├── high_scores.json
├── settings.json
├── statistics.json
├── achievements.json
├── saves/
│   ├── snake_slot1.json
│   ├── tetris_slot1.json
│   └── ...
└── daily_challenges.json
```

### File Permissions
- Data directory: 0755
- JSON files: 0644

### Backup Recommendations
- Regular backups of `./data/` directory
- Version control for `settings.json` (user preferences)
- Cloud sync for cross-device play (future feature)

---

## Error Handling

### Terminal Size Errors
```python
try:
    game = SnakeGame()
    game.run()
except TerminalSizeError as e:
    print(f"Terminal too small: {e}")
```

### Save/Load Errors
```python
result = save_manager.save_game('snake', 1, state, metadata)
if not result:
    # Handle save failure
    pass
```

### Input Validation
All user input is validated before processing:
- Key codes checked against valid ranges
- String input sanitized
- Numeric input clamped to valid ranges

---

## Performance Considerations

### Frame Rate
- Target: 30 FPS for most games
- Actual: Depends on terminal emulator
- Uses time-based updates for consistency

### Memory Usage
- Minimal heap allocations during gameplay
- Preallocated buffers where possible
- Efficient data structures (deque for snake, etc.)

### CPU Usage
- Sleep between frames to reduce CPU load
- Efficient rendering (only changed areas when possible)
- Non-blocking input handling

---

## Extending the System

### Adding a New Manager

1. Create manager class in `utils/`
2. Initialize in `BaseGame.__init__`
3. Use throughout game lifecycle
4. Add tests to `tests/test_managers.py`

### Adding a New Theme

1. Define theme in `utils/themes.py`
2. Add to `THEMES` dictionary
3. Test with various games

### Adding New Achievements

1. Define in `utils/achievements.py`
2. Add to `ACHIEVEMENTS` list
3. Trigger via `check_achievements()`

---

## Version History

- **v1.0.0** - Initial release with 9 games
- **v1.1.0** - Added BaseGame architecture
- **v1.2.0** - Added achievements and themes
- **v1.3.0** - Added save/load and daily challenges
- **v1.4.0** - Added Tic-Tac-Toe, Wordle, Frogger, Sudoku
- **v1.5.0** - UI/UX improvements and animations
- **v1.6.0** - Testing framework and documentation

---

For more information, see:
- [README.md](README.md) - User guide
- [DEVELOPER.md](DEVELOPER.md) - Developer guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

