## Contributing to CLI Game Collection

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/cli-game-collection.git
   cd cli-game-collection
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Requirements
- Python 3.6+
- Unix-like system (Linux, macOS)
- Terminal with curses support

### Installation
```bash
# No external dependencies required
python3 main.py
```

## How to Contribute

### Adding a New Game

1. **Create game file** in `games/` directory:
   ```python
   from utils.base_game import BaseGame
   from utils.ui_helpers import draw_game_over_screen
   
   class MyGame(BaseGame):
       def __init__(self):
           super().__init__('mygame', min_height=24, min_width=80)
       
       def _init_game(self):
           # Initialize game state
           pass
       
       def _handle_input(self, key: int) -> bool:
           # Handle input
           return True
       
       def _update_game(self, delta_time: float):
           # Update game state
           pass
       
       def _draw_game(self):
           # Draw the game
           pass
       
       def _draw_game_over(self, is_new_high: bool = False):
           # Draw game over screen
           pass
   ```

2. **Add to menu** in `games/menu.py`:
   ```python
   from games.mygame import MyGame
   
   # In __init__:
   ("My Game", self._run_mygame),
   
   # Add method:
   def _run_mygame(self):
       game = MyGame()
       game.run()
   ```

3. **Add settings** in `utils/settings.py`:
   ```python
   'mygame': {
       'speed': 'medium',
       'difficulty': 'normal',
   }
   ```

4. **Add achievements** in `utils/achievements.py`

5. **Add help entry** in `games/help_menu.py`

### Fixing Bugs

1. **Check existing issues** - Avoid duplicates
2. **Create an issue** - Describe the bug
3. **Fix the bug** - Write tests if applicable
4. **Submit PR** - Reference the issue

### Adding Features

1. **Discuss first** - Open an issue to discuss major features
2. **Follow architecture** - Use existing patterns
3. **Update documentation** - README, CHANGELOG, help text
4. **Add tests** - Cover new functionality

## Coding Standards

### Python Style
- Follow PEP 8
- Use type hints
- Write docstrings for classes and functions
- Keep functions focused and small

### Example:
```python
def calculate_score(base: int, bonus: int, penalty: int) -> int:
    """Calculate final score.
    
    Args:
        base: Base score value
        bonus: Bonus points
        penalty: Penalty points to subtract
        
    Returns:
        Final calculated score
    """
    return max(0, base + bonus - penalty)
```

### File Organization
- **games/** - Game implementations
- **utils/** - Shared utilities and managers
- **tests/** - Test files
- **data/** - Runtime data (not tracked in git)

### Naming Conventions
- **Classes**: PascalCase (`SnakeGame`, `HighScoreManager`)
- **Functions**: snake_case (`_handle_input`, `get_high_score`)
- **Constants**: UPPER_CASE (`MAX_SCORE`, `DEFAULT_SPEED`)
- **Private**: Leading underscore (`_internal_method`)

## Testing

### Running Tests
```bash
python3 tests/run_tests.py
```

### Writing Tests
```python
import unittest

class TestMyFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_feature(self):
        """Test description."""
        self.assertEqual(actual, expected)
```

### Test Coverage
- Aim for >70% coverage
- Test edge cases
- Test error handling
- Mock external dependencies

## Pull Request Process

### Before Submitting
1. **Test your changes** - Run all tests
2. **Update documentation** - README, CHANGELOG, docstrings
3. **Follow style guidelines** - PEP 8, type hints
4. **Check for linter errors** - No warnings
5. **Rebase on main** - Ensure clean merge

### PR Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No linter warnings
- [ ] CHANGELOG.md updated
```

### Review Process
1. **Automated checks** - Tests must pass
2. **Code review** - At least one approval
3. **Address feedback** - Make requested changes
4. **Merge** - Squash and merge

## Documentation

### Code Documentation
- **Docstrings** - All public functions/classes
- **Type hints** - Function signatures
- **Comments** - Explain complex logic
- **Examples** - Show usage patterns

### User Documentation
- **README.md** - Update for new features
- **CHANGELOG.md** - Document changes
- **Help entries** - Add game instructions

## Questions?

- **Open an issue** - For questions and discussions
- **Check documentation** - DEVELOPER.md, README.md
- **Review existing code** - Learn from examples

## Thank You!

Your contributions help make this project better for everyone. We appreciate your time and effort!

