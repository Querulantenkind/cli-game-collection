"""Statistics tracking system."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class StatisticsManager:
    """Manages game statistics and player engagement metrics."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the statistics manager.
        
        Args:
            data_dir: Directory to store statistics file
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.stats_file = self.data_dir / "statistics.json"
        self._stats = self._load_stats()
    
    def _load_stats(self) -> Dict[str, Any]:
        """Load statistics from file."""
        if not self.stats_file.exists():
            return {
                'games': {},
                'total_play_time': 0,
                'first_played': None,
                'last_played': None,
            }
        
        try:
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {
                'games': {},
                'total_play_time': 0,
                'first_played': None,
                'last_played': None,
            }
    
    def _save_stats(self):
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self._stats, f, indent=2)
        except IOError:
            pass
    
    def _ensure_game_stats(self, game_name: str):
        """Ensure game statistics entry exists."""
        if 'games' not in self._stats:
            self._stats['games'] = {}
        if game_name not in self._stats['games']:
            self._stats['games'][game_name] = {
                'games_played': 0,
                'games_won': 0,
                'games_lost': 0,
                'total_score': 0,
                'best_score': 0,
                'total_play_time': 0,
                'average_score': 0,
            }
    
    def record_game_start(self, game_name: str):
        """Record that a game has started."""
        self._ensure_game_stats(game_name)
        self._stats['games'][game_name]['games_played'] += 1
        
        if not self._stats.get('first_played'):
            self._stats['first_played'] = datetime.now().isoformat()
        self._stats['last_played'] = datetime.now().isoformat()
        self._save_stats()
    
    def record_game_end(self, game_name: str, score: int, won: bool = False, 
                       play_time: float = 0):
        """Record game completion.
        
        Args:
            game_name: Name of the game
            score: Final score
            won: Whether the player won
            play_time: Time played in seconds
        """
        self._ensure_game_stats(game_name)
        stats = self._stats['games'][game_name]
        
        if won:
            stats['games_won'] += 1
        else:
            stats['games_lost'] += 1
        
        stats['total_score'] += score
        stats['total_play_time'] += play_time
        
        if score > stats['best_score']:
            stats['best_score'] = score
        
        # Calculate average
        if stats['games_played'] > 0:
            stats['average_score'] = stats['total_score'] // stats['games_played']
        
        # Update global play time
        self._stats['total_play_time'] = self._stats.get('total_play_time', 0) + play_time
        
        self._save_stats()
    
    def get_game_stats(self, game_name: str) -> Dict[str, Any]:
        """Get statistics for a specific game.
        
        Args:
            game_name: Name of the game
            
        Returns:
            Dictionary of game statistics
        """
        self._ensure_game_stats(game_name)
        return self._stats['games'][game_name].copy()
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get all statistics.
        
        Returns:
            Complete statistics dictionary
        """
        return self._stats.copy()
    
    def get_total_games_played(self) -> int:
        """Get total number of games played across all games."""
        total = 0
        for game_stats in self._stats.get('games', {}).values():
            total += game_stats.get('games_played', 0)
        return total
    
    def format_play_time(self, seconds: float) -> str:
        """Format play time in a human-readable format.
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

