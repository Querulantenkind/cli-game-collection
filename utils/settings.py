"""Settings management system."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class SettingsManager:
    """Manages game settings and configuration."""
    
    DEFAULT_SETTINGS = {
        'snake': {
            'speed': 'medium',  # slow, medium, fast
            'difficulty': 'normal',  # easy, normal, hard
        },
        'tetris': {
            'speed': 'medium',
            'difficulty': 'normal',
            'starting_level': 1,
        },
        'pacman': {
            'speed': 'medium',
            'difficulty': 'normal',
            'ghost_speed': 'normal',  # slow, normal, fast
        },
        'pong': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        '2048': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'minesweeper': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'space_invaders': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'breakout': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'hangman': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'tictactoe': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'wordle': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'frogger': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'sudoku': {
            'speed': 'medium',
            'difficulty': 'normal',
        },
        'general': {
            'show_high_scores': True,
            'sound_enabled': False,
            'theme': 'classic',  # classic, dark, neon, retro, minimal
        }
    }
    
    SPEED_MULTIPLIERS = {
        'slow': 1.5,
        'medium': 1.0,
        'fast': 0.6,
    }
    
    DIFFICULTY_MULTIPLIERS = {
        'easy': 0.7,
        'normal': 1.0,
        'hard': 1.5,
    }
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the settings manager.
        
        Args:
            data_dir: Directory to store settings file
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.settings_file = self.data_dir / "settings.json"
        self._settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        if not self.settings_file.exists():
            return self.DEFAULT_SETTINGS.copy()
        
        try:
            with open(self.settings_file, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                settings = self.DEFAULT_SETTINGS.copy()
                for key, value in loaded.items():
                    if isinstance(value, dict) and key in settings:
                        settings[key].update(value)
                    else:
                        settings[key] = value
                return settings
        except (json.JSONDecodeError, IOError):
            return self.DEFAULT_SETTINGS.copy()
    
    def _save_settings(self):
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't save
    
    def get(self, category: str, key: str, default: Any = None) -> Any:
        """Get a setting value.
        
        Args:
            category: Settings category (e.g., 'snake', 'tetris', 'general')
            key: Setting key
            default: Default value if not found
            
        Returns:
            Setting value or default
        """
        return self._settings.get(category, {}).get(key, default)
    
    def set(self, category: str, key: str, value: Any):
        """Set a setting value.
        
        Args:
            category: Settings category
            key: Setting key
            value: Setting value
        """
        if category not in self._settings:
            self._settings[category] = {}
        self._settings[category][key] = value
        self._save_settings()
    
    def get_game_settings(self, game_name: str) -> Dict[str, Any]:
        """Get all settings for a specific game.
        
        Args:
            game_name: Name of the game
            
        Returns:
            Dictionary of game settings
        """
        return self._settings.get(game_name, {}).copy()
    
    def get_speed_multiplier(self, game_name: str) -> float:
        """Get speed multiplier for a game based on settings.
        
        Args:
            game_name: Name of the game
            
        Returns:
            Speed multiplier (lower = faster)
        """
        speed = self.get(game_name, 'speed', 'medium')
        difficulty = self.get(game_name, 'difficulty', 'normal')
        
        speed_mult = self.SPEED_MULTIPLIERS.get(speed, 1.0)
        diff_mult = self.DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)
        
        return speed_mult * diff_mult
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self._settings = self.DEFAULT_SETTINGS.copy()
        self._save_settings()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all settings.
        
        Returns:
            Complete settings dictionary
        """
        return self._settings.copy()

