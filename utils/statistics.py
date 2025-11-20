"""Statistics tracking system."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
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
                'session_history': {},  # Track last 20 sessions per game
            }
        
        try:
            with open(self.stats_file, 'r') as f:
                data = json.load(f)
                # Ensure session_history exists
                if 'session_history' not in data:
                    data['session_history'] = {}
                return data
        except (json.JSONDecodeError, IOError):
            return {
                'games': {},
                'total_play_time': 0,
                'first_played': None,
                'last_played': None,
                'session_history': {},
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
                'worst_score': None,
                'total_play_time': 0,
                'average_score': 0,
                'win_streak': 0,
                'best_win_streak': 0,
            }
        if 'session_history' not in self._stats:
            self._stats['session_history'] = {}
        if game_name not in self._stats['session_history']:
            self._stats['session_history'][game_name] = []
    
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
        
        # Record session
        session = {
            'score': score,
            'won': won,
            'play_time': play_time,
            'timestamp': datetime.now().isoformat()
        }
        self._stats['session_history'][game_name].append(session)
        
        # Keep only last 20 sessions
        if len(self._stats['session_history'][game_name]) > 20:
            self._stats['session_history'][game_name] = \
                self._stats['session_history'][game_name][-20:]
        
        # Update stats
        if won:
            stats['games_won'] += 1
            stats['win_streak'] = stats.get('win_streak', 0) + 1
            if stats['win_streak'] > stats.get('best_win_streak', 0):
                stats['best_win_streak'] = stats['win_streak']
        else:
            stats['games_lost'] += 1
            stats['win_streak'] = 0
        
        stats['total_score'] += score
        stats['total_play_time'] += play_time
        
        # Update best/worst scores
        if score > stats['best_score']:
            stats['best_score'] = score
        
        if stats['worst_score'] is None or score < stats['worst_score']:
            stats['worst_score'] = score
        
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
    
    def get_session_history(self, game_name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent session history for a game.
        
        Args:
            game_name: Name of the game
            limit: Maximum number of sessions to return
            
        Returns:
            List of session dictionaries
        """
        self._ensure_game_stats(game_name)
        sessions = self._stats['session_history'].get(game_name, [])
        return sessions[-limit:]
    
    def get_win_rate(self, game_name: str) -> float:
        """Get win rate percentage for a game.
        
        Args:
            game_name: Name of the game
            
        Returns:
            Win rate as percentage (0-100)
        """
        stats = self.get_game_stats(game_name)
        games_played = stats.get('games_played', 0)
        if games_played == 0:
            return 0.0
        return (stats.get('games_won', 0) / games_played) * 100
    
    def get_score_trend(self, game_name: str, window: int = 10) -> List[int]:
        """Get recent score trend for a game.
        
        Args:
            game_name: Name of the game
            window: Number of recent sessions to analyze
            
        Returns:
            List of recent scores
        """
        sessions = self.get_session_history(game_name, window)
        return [s['score'] for s in sessions]
    
    def is_improving(self, game_name: str) -> bool:
        """Check if player is improving (recent scores better than average).
        
        Args:
            game_name: Name of the game
            
        Returns:
            True if recent performance is above average
        """
        stats = self.get_game_stats(game_name)
        trend = self.get_score_trend(game_name, 5)
        
        if len(trend) < 3:
            return False
        
        avg_score = stats.get('average_score', 0)
        recent_avg = sum(trend) // len(trend) if trend else 0
        
        return recent_avg > avg_score
    
    def get_best_session(self, game_name: str) -> Optional[Dict[str, Any]]:
        """Get the best scoring session for a game.
        
        Args:
            game_name: Name of the game
            
        Returns:
            Best session dictionary or None
        """
        sessions = self.get_session_history(game_name)
        if not sessions:
            return None
        return max(sessions, key=lambda s: s['score'])
    
    def get_ascii_graph(self, data: List[int], width: int = 40, height: int = 8) -> List[str]:
        """Generate an ASCII bar graph.
        
        Args:
            data: List of values to graph
            width: Width of the graph
            height: Height of the graph
            
        Returns:
            List of strings representing the graph
        """
        if not data:
            return [" " * width for _ in range(height)]
        
        max_val = max(data) if data else 1
        if max_val == 0:
            max_val = 1
        
        # Normalize data to height
        normalized = [(val / max_val) * height for val in data]
        
        # Build graph from top to bottom
        graph = []
        for h in range(height, 0, -1):
            line = ""
            for val in normalized:
                if val >= h:
                    line += "█"
                elif val >= h - 0.5:
                    line += "▄"
                else:
                    line += " "
            graph.append(line)
        
        return graph

