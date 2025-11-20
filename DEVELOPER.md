# Developer Guide

## Architecture Overview

The CLI Game Collection is built with a modular architecture that promotes code reuse and consistency.

## Core Components

### Base Game Class (`utils/base_game.py`)

The `BaseGame` class provides a foundation for all games, handling:
- **Manager Initialization**: Automatically sets up HighScoreManager, SettingsManager, and StatisticsManager
- **Curses Setup**: Handles all curses initialization and cleanup
- **Terminal Validation**: Validates terminal size before starting
- **Game Loop**: Provides a standardized game loop structure
- **Statistics Tracking**: Automatically records game start/end times
- **High Score Management**: Handles saving and checking high scores

### Terminal Utilities (`utils/terminal.py`)

Provides terminal validation to prevent crashes:
- `validate_terminal_size()`: Checks if terminal meets minimum requirements
- `show_terminal_size_error()`: Displays user-friendly error message
- `TerminalSizeError`: Exception raised when terminal is too small

### UI Helpers (`utils/ui_helpers.py`)

Common UI functions for consistent look and feel:
- Text centering
- Border drawing
- Menu item rendering
- Info panels
- Game over screens

## Creating a New Game with BaseGame

### Step 1: Create the Game Class

```python
from utils.base_game import BaseGame
import curses

class MyGame(BaseGame):
    def __init__(self):
        # Initialize with game name and minimum terminal size
        super().__init__('my_game', min_height=24, min_width=80)
        
        # Initialize your game-specific state
        self.custom_state = 0
```

### Step 2: Implement Required Methods

#### `_init_game()`
Called once before the game loop starts. Initialize game-specific starting state.

```python
def _init_game(self):
    # Set up initial game state
    self.custom_state = 0
```

#### `_handle_input(key: int) -> bool`
Handle user input. Return `False` to quit the game.

```python
def _handle_input(self, key: int) -> bool:
    if key == ord('q'):
        return False  # Quit
    elif key == ord('p'):
        self.paused = not self.paused
    elif key == curses.KEY_UP:
        # Handle up arrow
        pass
    return True  # Continue game
```

#### `_update_game(delta_time: float)`
Update game logic each frame. `delta_time` is seconds since last frame.

```python
def _update_game(self, delta_time: float):
    if self.paused:
        return
    
    # Update game state
    self.custom_state += delta_time
    
    # Check game over conditions
    if some_condition:
        self.game_over = True
```

#### `_draw_game()`
Draw the game each frame. Use `self.stdscr` for drawing.

```python
def _draw_game(self):
    self.stdscr.clear()
    
    # Draw game elements
    self.stdscr.addstr(5, 10, "My Game")
    
    # Use helper methods
    self._draw_info_bar({'Custom': self.custom_state})
    self._draw_pause_message()
    
    self.stdscr.refresh()
```

#### `_draw_game_over(is_new_high: bool)`
Draw the game over screen.

```python
def _draw_game_over(self, is_new_high: bool = False):
    from utils.ui_helpers import draw_game_over_screen
    
    extra_info = ["Custom info here"]
    draw_game_over_screen(
        self.stdscr, "GAME OVER", self.score,
        self.high_score, is_new_high, extra_info
    )
```

### Step 3: Optional Overrides

#### `_get_input_timeout() -> int`
Override to change input timeout (default: 100ms).

#### `_get_game_speed() -> float`
Override to customize speed multiplier calculation.

### Step 4: Add to Menu

In `games/menu.py`:

```python
from games.my_game import MyGame

class GameMenu:
    def __init__(self):
        self.games = [
            # ... existing games ...
            ("My Game", self._run_my_game),
            # ...
        ]
    
    def _run_my_game(self):
        game = MyGame()
        game.run()
```

### Step 5: Add Settings (Optional)

In `utils/settings.py`, add default settings:

```python
DEFAULT_SETTINGS = {
    # ... existing settings ...
    'my_game': {
        'speed': 'medium',
        'difficulty': 'normal',
    },
}
```

### Step 6: Add Help (Optional)

In `games/help_menu.py`, add help entry:

```python
GAME_HELP = {
    # ... existing help ...
    'my_game': {
        'title': 'My Game - Help',
        'description': 'Description of my game',
        'controls': [
            ('Key', 'Action'),
        ],
        'tips': [
            'Tip 1',
            'Tip 2',
        ]
    }
}
```

## Benefits of Using BaseGame

1. **Less Code**: No need to manually set up managers, curses, or statistics
2. **Consistency**: All games follow the same pattern
3. **Error Handling**: Terminal validation prevents crashes
4. **Maintainability**: Changes to common functionality only need to be made once
5. **Statistics**: Automatic tracking of play time and scores

## Example: Snake Game

See `games/snake.py` for a complete example of a game using `BaseGame`.

## Terminal Size Requirements

Always specify realistic minimum terminal sizes:
- Most games: `min_height=24, min_width=80`
- Larger games: `min_height=30, min_width=100`
- Simple games: `min_height=20, min_width=60`

The base class will automatically validate and show an error if the terminal is too small.

## Best Practices

1. **Use BaseGame**: Unless you have a specific reason not to
2. **Validate Terminal Size**: Always specify minimum dimensions
3. **Handle Pause**: Use `self.paused` flag and `_draw_pause_message()`
4. **Use UI Helpers**: Leverage `utils/ui_helpers.py` for consistent UI
5. **Save High Scores**: The base class handles this automatically
6. **Track Statistics**: Also handled automatically
7. **Clean Code**: Keep game logic separate from UI code

