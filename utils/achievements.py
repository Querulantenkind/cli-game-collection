"""Achievement system for tracking player accomplishments."""

import json
import os
from pathlib import Path
from typing import Dict, List, Callable, Optional, Any
from datetime import datetime
from enum import Enum


class AchievementCategory(Enum):
    """Categories for organizing achievements."""
    SCORE = "Score"
    PERFECT = "Perfect"
    STREAK = "Streak"
    FIRST = "First"
    SPEED = "Speed"
    MASTERY = "Mastery"
    COLLECTION = "Collection"


class Achievement:
    """Represents a single achievement."""
    
    def __init__(self, achievement_id: str, name: str, description: str,
                 condition: Callable[[Dict[str, Any]], bool],
                 category: AchievementCategory = AchievementCategory.SCORE,
                 points: int = 10,
                 icon: str = "★"):
        """Initialize an achievement.
        
        Args:
            achievement_id: Unique identifier
            name: Display name
            description: What the player needs to do
            condition: Function that checks if achievement is earned
            category: Achievement category
            points: Points awarded (for future use)
            icon: Display icon
        """
        self.id = achievement_id
        self.name = name
        self.description = description
        self.condition = condition
        self.category = category
        self.points = points
        self.icon = icon
    
    def check(self, game_state: Dict[str, Any]) -> bool:
        """Check if achievement condition is met.
        
        Args:
            game_state: Current game state dictionary
            
        Returns:
            True if achievement is earned
        """
        try:
            return self.condition(game_state)
        except (KeyError, TypeError):
            return False


class AchievementManager:
    """Manages achievements and their unlocking."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the achievement manager.
        
        Args:
            data_dir: Directory to store achievement data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.unlocks_file = self.data_dir / "achievements.json"
        self._unlocked = self._load_unlocks()
        self._achievements = self._define_achievements()
    
    def _load_unlocks(self) -> Dict[str, Dict]:
        """Load unlocked achievements from file."""
        if not self.unlocks_file.exists():
            return {}
        
        try:
            with open(self.unlocks_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_unlocks(self):
        """Save unlocked achievements to file."""
        try:
            with open(self.unlocks_file, 'w') as f:
                json.dump(self._unlocked, f, indent=2)
        except IOError:
            pass
    
    def _define_achievements(self) -> Dict[str, Achievement]:
        """Define all achievements in the system."""
        achievements = {}
        
        # Snake achievements
        achievements['snake_100'] = Achievement(
            'snake_100', 'Snake Charmer', 'Reach 100 points in Snake',
            lambda s: s.get('game') == 'snake' and s.get('score', 0) >= 100,
            AchievementCategory.SCORE, 10
        )
        achievements['snake_500'] = Achievement(
            'snake_500', 'Snake Master', 'Reach 500 points in Snake',
            lambda s: s.get('game') == 'snake' and s.get('score', 0) >= 500,
            AchievementCategory.SCORE, 25
        )
        achievements['snake_perfect'] = Achievement(
            'snake_perfect', 'Perfect Snake', 'Win Snake without dying',
            lambda s: s.get('game') == 'snake' and s.get('won', False),
            AchievementCategory.PERFECT, 30
        )
        
        # Tetris achievements
        achievements['tetris_1000'] = Achievement(
            'tetris_1000', 'Tetris Novice', 'Reach 1000 points in Tetris',
            lambda s: s.get('game') == 'tetris' and s.get('score', 0) >= 1000,
            AchievementCategory.SCORE, 10
        )
        achievements['tetris_5000'] = Achievement(
            'tetris_5000', 'Tetris Expert', 'Reach 5000 points in Tetris',
            lambda s: s.get('game') == 'tetris' and s.get('score', 0) >= 5000,
            AchievementCategory.SCORE, 25
        )
        achievements['tetris_10_lines'] = Achievement(
            'tetris_10_lines', 'Line Master', 'Clear 10 lines in Tetris',
            lambda s: s.get('game') == 'tetris' and s.get('lines_cleared', 0) >= 10,
            AchievementCategory.MASTERY, 20
        )
        achievements['tetris_level_10'] = Achievement(
            'tetris_level_10', 'Level 10', 'Reach level 10 in Tetris',
            lambda s: s.get('game') == 'tetris' and s.get('level', 0) >= 10,
            AchievementCategory.MASTERY, 30
        )
        
        # 2048 achievements
        achievements['2048_512'] = Achievement(
            '2048_512', 'Halfway There', 'Reach 512 in 2048',
            lambda s: s.get('game') == '2048' and s.get('max_tile', 0) >= 512,
            AchievementCategory.SCORE, 15
        )
        achievements['2048_2048'] = Achievement(
            '2048_2048', 'Perfect 2048', 'Reach 2048 tile',
            lambda s: s.get('game') == '2048' and s.get('max_tile', 0) >= 2048,
            AchievementCategory.PERFECT, 50
        )
        achievements['2048_4096'] = Achievement(
            '2048_4096', 'Beyond 2048', 'Reach 4096 tile',
            lambda s: s.get('game') == '2048' and s.get('max_tile', 0) >= 4096,
            AchievementCategory.MASTERY, 75
        )
        
        # Minesweeper achievements
        achievements['minesweeper_win'] = Achievement(
            'minesweeper_win', 'Mine Sweeper', 'Win a game of Minesweeper',
            lambda s: s.get('game') == 'minesweeper' and s.get('won', False),
            AchievementCategory.FIRST, 20
        )
        achievements['minesweeper_fast'] = Achievement(
            'minesweeper_fast', 'Speed Sweeper', 'Win Minesweeper in under 60 seconds',
            lambda s: (s.get('game') == 'minesweeper' and s.get('won', False) and
                      s.get('time', float('inf')) < 60),
            AchievementCategory.SPEED, 30
        )
        
        # Pac-Man achievements
        achievements['pacman_win'] = Achievement(
            'pacman_win', 'Maze Master', 'Clear all dots in Pac-Man',
            lambda s: s.get('game') == 'pacman' and s.get('won', False),
            AchievementCategory.FIRST, 20
        )
        achievements['pacman_1000'] = Achievement(
            'pacman_1000', 'Pac-Man Pro', 'Reach 1000 points in Pac-Man',
            lambda s: s.get('game') == 'pacman' and s.get('score', 0) >= 1000,
            AchievementCategory.SCORE, 25
        )
        
        # Space Invaders achievements
        achievements['space_invaders_win'] = Achievement(
            'space_invaders_win', 'Alien Hunter', 'Clear all enemies in Space Invaders',
            lambda s: s.get('game') == 'space_invaders' and s.get('won', False),
            AchievementCategory.FIRST, 20
        )
        achievements['space_invaders_500'] = Achievement(
            'space_invaders_500', 'Space Ace', 'Reach 500 points in Space Invaders',
            lambda s: s.get('game') == 'space_invaders' and s.get('score', 0) >= 500,
            AchievementCategory.SCORE, 25
        )
        
        # Breakout achievements
        achievements['breakout_win'] = Achievement(
            'breakout_win', 'Brick Breaker', 'Break all bricks in Breakout',
            lambda s: s.get('game') == 'breakout' and s.get('won', False),
            AchievementCategory.FIRST, 20
        )
        achievements['breakout_perfect'] = Achievement(
            'breakout_perfect', 'Perfect Breakout', 'Win Breakout without losing a life',
            lambda s: (s.get('game') == 'breakout' and s.get('won', False) and
                      s.get('lives', 0) >= 3),
            AchievementCategory.PERFECT, 40
        )
        
        # Hangman achievements
        achievements['hangman_win'] = Achievement(
            'hangman_win', 'Word Master', 'Win a game of Hangman',
            lambda s: s.get('game') == 'hangman' and s.get('won', False),
            AchievementCategory.FIRST, 15
        )
        achievements['hangman_perfect'] = Achievement(
            'hangman_perfect', 'Perfect Guess', 'Win Hangman with no wrong guesses',
            lambda s: (s.get('game') == 'hangman' and s.get('won', False) and
                      s.get('wrong_guesses', 6) == 0),
            AchievementCategory.PERFECT, 35
        )
        
        # Pong achievements
        achievements['pong_win'] = Achievement(
            'pong_win', 'Pong Champion', 'Win a game of Pong',
            lambda s: s.get('game') == 'pong' and s.get('won', False),
            AchievementCategory.FIRST, 15
        )
        achievements['pong_5_0'] = Achievement(
            'pong_5_0', 'Perfect Game', 'Win Pong 5-0',
            lambda s: (s.get('game') == 'pong' and s.get('won', False) and
                      s.get('score1', 0) == 5 and s.get('score2', 0) == 0),
            AchievementCategory.PERFECT, 30
        )
        
        # Tic-Tac-Toe achievements
        achievements['tictactoe_win'] = Achievement(
            'tictactoe_win', 'Tic-Tac-Toe Winner', 'Win a game of Tic-Tac-Toe',
            lambda s: s.get('game') == 'tictactoe' and s.get('won', False),
            AchievementCategory.FIRST, 15
        )
        achievements['tictactoe_3moves'] = Achievement(
            'tictactoe_3moves', 'Quick Victory', 'Win Tic-Tac-Toe in 3 moves',
            lambda s: (s.get('game') == 'tictactoe' and s.get('won', False) and
                      s.get('moves', 99) <= 5),  # 3 player moves = 5 total (X-O-X-O-X)
            AchievementCategory.PERFECT, 25
        )
        
        # Wordle achievements
        achievements['wordle_win'] = Achievement(
            'wordle_win', 'Word Master', 'Win a game of Wordle',
            lambda s: s.get('game') == 'wordle' and s.get('won', False),
            AchievementCategory.FIRST, 15
        )
        achievements['wordle_1guess'] = Achievement(
            'wordle_1guess', 'Lucky Guess', 'Win Wordle in 1 guess',
            lambda s: (s.get('game') == 'wordle' and s.get('won', False) and
                      s.get('guesses_used', 6) == 1),
            AchievementCategory.PERFECT, 50
        )
        achievements['wordle_3guesses'] = Achievement(
            'wordle_3guesses', 'Word Expert', 'Win Wordle in 3 guesses or less',
            lambda s: (s.get('game') == 'wordle' and s.get('won', False) and
                      s.get('guesses_used', 6) <= 3),
            AchievementCategory.MASTERY, 30
        )
        
        # Sudoku achievements
        achievements['sudoku_win'] = Achievement(
            'sudoku_win', 'Sudoku Solver', 'Complete a Sudoku puzzle',
            lambda s: s.get('game') == 'sudoku' and s.get('won', False),
            AchievementCategory.FIRST, 20
        )
        achievements['sudoku_perfect'] = Achievement(
            'sudoku_perfect', 'Perfect Logic', 'Complete Sudoku with no mistakes',
            lambda s: (s.get('game') == 'sudoku' and s.get('won', False) and
                      s.get('mistakes', 3) == 0),
            AchievementCategory.PERFECT, 40
        )
        achievements['sudoku_no_hints'] = Achievement(
            'sudoku_no_hints', 'Pure Solver', 'Complete Sudoku without using hints',
            lambda s: (s.get('game') == 'sudoku' and s.get('won', False) and
                      s.get('hints_used', 3) == 0),
            AchievementCategory.MASTERY, 35
        )
        
        # Frogger achievements
        achievements['frogger_level_5'] = Achievement(
            'frogger_level_5', 'Frog Master', 'Reach level 5 in Frogger',
            lambda s: s.get('game') == 'frogger' and s.get('level', 0) >= 5,
            AchievementCategory.MASTERY, 25
        )
        
        # Collection achievements (checked separately via stats)
        achievements['play_all'] = Achievement(
            'play_all', 'Game Explorer', 'Play all games at least once',
            lambda s: s.get('games_played_count', 0) >= 13,  # Updated for new games
            AchievementCategory.COLLECTION, 50
        )
        achievements['win_all'] = Achievement(
            'win_all', 'Master Gamer', 'Win all games at least once',
            lambda s: s.get('games_won_count', 0) >= 13,  # Updated for new games
            AchievementCategory.COLLECTION, 100
        )
        achievements['first_high_score'] = Achievement(
            'first_high_score', 'High Scorer', 'Get your first high score',
            lambda s: s.get('is_new_high', False),
            AchievementCategory.FIRST, 20
        )
        
        return achievements
    
    def check_achievements(self, game_name: str, game_state: Dict[str, Any]) -> List[str]:
        """Check and unlock achievements based on game state.
        
        Args:
            game_name: Name of the game
            game_state: Current game state dictionary
            
        Returns:
            List of newly unlocked achievement IDs
        """
        game_state['game'] = game_name
        newly_unlocked = []
        
        for achievement_id, achievement in self._achievements.items():
            # Skip if already unlocked
            if achievement_id in self._unlocked:
                continue
            
            # Check if achievement is for this game or is a collection achievement
            if achievement_id.startswith(game_name) or achievement_id in ['play_all', 'win_all', 'first_high_score']:
                if achievement.check(game_state):
                    self.unlock(achievement_id)
                    newly_unlocked.append(achievement_id)
        
        return newly_unlocked
    
    def unlock(self, achievement_id: str):
        """Unlock an achievement.
        
        Args:
            achievement_id: ID of the achievement to unlock
        """
        if achievement_id not in self._unlocked:
            self._unlocked[achievement_id] = {
                'unlocked_at': datetime.now().isoformat(),
                'points': self._achievements.get(achievement_id, Achievement('', '', '', lambda s: False)).points
            }
            self._save_unlocks()
    
    def is_unlocked(self, achievement_id: str) -> bool:
        """Check if an achievement is unlocked.
        
        Args:
            achievement_id: ID of the achievement
            
        Returns:
            True if unlocked
        """
        return achievement_id in self._unlocked
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get an achievement by ID.
        
        Args:
            achievement_id: ID of the achievement
            
        Returns:
            Achievement object or None
        """
        return self._achievements.get(achievement_id)
    
    def get_unlocked_achievements(self) -> Dict[str, Dict]:
        """Get all unlocked achievements.
        
        Returns:
            Dictionary of unlocked achievement data
        """
        return self._unlocked.copy()
    
    def get_all_achievements(self) -> Dict[str, Achievement]:
        """Get all achievements (locked and unlocked).
        
        Returns:
            Dictionary of all achievements
        """
        return self._achievements.copy()
    
    def get_achievements_by_category(self, category: AchievementCategory) -> List[Achievement]:
        """Get all achievements in a category.
        
        Args:
            category: Achievement category
            
        Returns:
            List of achievements in that category
        """
        return [a for a in self._achievements.values() if a.category == category]
    
    def get_total_points(self) -> int:
        """Get total points from unlocked achievements.
        
        Returns:
            Total points earned
        """
        return sum(data.get('points', 0) for data in self._unlocked.values())
    
    def get_progress(self, achievement_id: str, game_state: Dict[str, Any]) -> Optional[float]:
        """Get progress towards an achievement (0.0 to 1.0).
        
        Args:
            achievement_id: ID of the achievement
            game_state: Current game state
            
        Returns:
            Progress as float 0.0-1.0, or None if not applicable
        """
        achievement = self._achievements.get(achievement_id)
        if not achievement or achievement_id in self._unlocked:
            return None
        
        # Simple progress calculation for score-based achievements
        if 'score' in achievement_id.lower() or 'points' in achievement_id.lower():
            # This is a simplified version - could be enhanced
            return None  # Would need specific logic per achievement
        
        return None

