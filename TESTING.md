# Testing Guide

## Overview

This document describes the testing infrastructure for the CLI Game Collection.

## Test Structure

```
tests/
├── __init__.py          # Package initialization
├── test_managers.py     # Tests for manager classes
├── test_games.py        # Tests for game logic
└── run_tests.py         # Test runner
```

## Running Tests

### Quick Start

```bash
# Run all tests
make test

# Or directly
python3 tests/run_tests.py

# Run specific test file
python3 -m unittest tests/test_managers.py
python3 -m unittest tests/test_games.py

# Run specific test class
python3 -m unittest tests.test_managers.TestHighScoreManager

# Run specific test method
python3 -m unittest tests.test_managers.TestHighScoreManager.test_add_score
```

### Verbose Output

```bash
# With verbose output
python3 tests/run_tests.py -v
```

## Test Coverage

### Manager Tests (test_managers.py)

#### HighScoreManager
- ✅ Add score functionality
- ✅ Multiple score handling
- ✅ Top 10 limit enforcement
- ✅ Score persistence

#### SettingsManager
- ✅ Default settings loading
- ✅ Get/set functionality
- ✅ Speed multiplier calculation
- ✅ Settings persistence

#### StatisticsManager
- ✅ Game recording
- ✅ Win rate calculation
- ✅ Statistics aggregation
- ✅ Session tracking

#### AchievementManager
- ✅ Achievement checking
- ✅ Unlock functionality
- ✅ Progress tracking
- ✅ Points calculation

#### SaveManager
- ✅ Save game functionality
- ✅ Load game functionality
- ✅ Multiple save slots
- ✅ Metadata handling

#### ThemeManager
- ✅ Theme retrieval
- ✅ Theme switching
- ✅ Theme application

#### DailyChallengeManager
- ✅ Daily challenge generation
- ✅ Completion marking
- ✅ Streak tracking

### Game Tests (test_games.py)

#### SnakeGame
- ✅ Initialization

#### TetrisGame
- ✅ Initialization

#### TicTacToeGame
- ✅ Initialization
- ✅ Row winner detection
- ✅ Column winner detection
- ✅ Diagonal winner detection

#### WordleGame
- ✅ Initialization
- ✅ Word list validation

## Writing Tests

### Test Template

```python
import unittest
import tempfile
import shutil
from pathlib import Path

class TestYourFeature(unittest.TestCase):
    """Test YourFeature functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary directory for test data
        self.test_dir = tempfile.mkdtemp()
        self.feature = YourFeature(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_feature(self):
        """Test specific feature."""
        # Arrange
        expected = "expected_value"
        
        # Act
        actual = self.feature.do_something()
        
        # Assert
        self.assertEqual(actual, expected)
```

### Assertion Methods

```python
# Equality
self.assertEqual(a, b)
self.assertNotEqual(a, b)

# Truth
self.assertTrue(x)
self.assertFalse(x)

# Identity
self.assertIs(a, b)
self.assertIsNot(a, b)

# None
self.assertIsNone(x)
self.assertIsNotNone(x)

# Membership
self.assertIn(a, b)
self.assertNotIn(a, b)

# Comparison
self.assertGreater(a, b)
self.assertLess(a, b)
self.assertGreaterEqual(a, b)
self.assertLessEqual(a, b)

# Exceptions
self.assertRaises(ValueError, func, arg)
with self.assertRaises(ValueError):
    func(arg)
```

## Testing Best Practices

### 1. Isolation

Each test should be independent and not rely on other tests.

```python
def setUp(self):
    """Create fresh test environment for each test."""
    self.test_dir = tempfile.mkdtemp()
    self.manager = HighScoreManager(self.test_dir)

def tearDown(self):
    """Clean up after each test."""
    shutil.rmtree(self.test_dir)
```

### 2. Arrange-Act-Assert Pattern

```python
def test_add_score(self):
    """Test adding a score."""
    # Arrange
    game = 'snake'
    score = 100
    
    # Act
    is_new_high = self.manager.add_score(game, score)
    
    # Assert
    self.assertTrue(is_new_high)
    self.assertEqual(self.manager.get_high_score(game), 100)
```

### 3. Descriptive Names

```python
# Good
def test_add_score_returns_true_for_new_high_score(self):
    """Test that adding a new high score returns True."""
    pass

# Less descriptive
def test_score(self):
    """Test score."""
    pass
```

### 4. Test Edge Cases

```python
def test_empty_score_list(self):
    """Test getting high score when no scores exist."""
    score = self.manager.get_high_score('nonexistent_game')
    self.assertEqual(score, 0)

def test_max_scores_limit(self):
    """Test that only top 10 scores are kept."""
    for i in range(15):
        self.manager.add_score('snake', i * 10)
    
    scores = self.manager.get_top_scores('snake')
    self.assertEqual(len(scores), 10)
```

## Testing Games

### Challenges

Games use curses which requires terminal initialization. Most game logic tests need mocking or integration testing.

### Current Approach

- Test game initialization
- Test standalone methods that don't require curses
- Test game logic (like winner detection in Tic-Tac-Toe)
- Integration testing done manually

### Future Improvements

1. **Mock Curses**
   ```python
   from unittest.mock import Mock, patch
   
   @patch('curses.initscr')
   def test_game_with_mock(self, mock_initscr):
       game = SnakeGame()
       # Test game logic
   ```

2. **Extract Business Logic**
   - Move game logic out of curses-dependent methods
   - Test pure functions separately
   - Example: Snake movement, Tetris rotation

3. **Integration Tests**
   - Test full game flow with real terminal
   - Requires different test runner
   - Manual testing still valuable

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Run tests
        run: python3 tests/run_tests.py
```

## Code Quality Checks

### Running Quality Checks

```bash
# Run quality checker
python3 scripts/check_quality.py

# Check syntax only
python3 -m py_compile games/*.py utils/*.py

# Run linter
make lint
```

### Quality Metrics

- **Syntax Errors**: 0 (required)
- **Docstring Coverage**: >90% (goal)
- **Line Length**: <100 characters (warning)
- **Cyclomatic Complexity**: <10 (warning)

## Manual Testing Checklist

### Before Release

- [ ] All automated tests pass
- [ ] Each game launches without errors
- [ ] Menu navigation works
- [ ] Settings save and load
- [ ] High scores persist
- [ ] Statistics update correctly
- [ ] Achievements unlock properly
- [ ] Save/load system works
- [ ] Daily challenges rotate
- [ ] Themes apply correctly
- [ ] Help menu displays correctly
- [ ] Terminal size validation works
- [ ] Pause/resume functions
- [ ] Game over screens display
- [ ] All controls responsive

### Game-Specific Testing

For each game:
- [ ] Controls work as documented
- [ ] Score increments correctly
- [ ] Game over conditions trigger
- [ ] New high scores saved
- [ ] Achievements unlock appropriately
- [ ] Settings affect gameplay
- [ ] Pause/resume maintains state
- [ ] Save/load preserves game state

## Performance Testing

### Metrics to Monitor

1. **Frame Rate**
   - Target: 30+ FPS
   - Measure: Visual smoothness

2. **Input Latency**
   - Target: <50ms
   - Test: Responsiveness feel

3. **Memory Usage**
   - Target: <50MB
   - Monitor: System resources

4. **Startup Time**
   - Target: <2 seconds
   - Measure: Time to menu

### Profiling

```bash
# Profile a game
python3 -m cProfile -o profile.stats main.py

# Analyze profile
python3 -m pstats profile.stats
```

## Troubleshooting Tests

### Tests Won't Run

```bash
# Verify Python version
python3 --version  # Should be 3.6+

# Check file permissions
ls -la tests/

# Verify imports work
python3 -c "import tests.test_managers"
```

### Import Errors

```bash
# Add project to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or use run_tests.py which handles this
python3 tests/run_tests.py
```

### Test Failures

1. Check if data directory conflicts
2. Verify file permissions
3. Check for hardcoded paths
4. Review test isolation
5. Examine error messages carefully

## Coverage Reports

### Using coverage.py (Optional)

```bash
# Install coverage
pip install coverage

# Run with coverage
coverage run tests/run_tests.py

# Generate report
coverage report

# HTML report
coverage html
open htmlcov/index.html
```

### Current Coverage

- **Managers**: ~80% (high value, fully tested)
- **Games**: ~20% (curses limitations)
- **Utilities**: ~60% (tested where possible)
- **Overall**: ~50%

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure tests pass
3. Add to appropriate test file
4. Update this documentation
5. Include in PR description

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

**Remember**: Good tests make refactoring safe and bugs rare! 🧪

