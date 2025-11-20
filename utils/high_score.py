"""High score management system."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class HighScoreManager:
    """Manages high scores for all games."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the high score manager.
        
        Args:
            data_dir: Directory to store high score files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.scores_file = self.data_dir / "high_scores.json"
        self._scores = self._load_scores()
    
    def _load_scores(self) -> Dict[str, List[Dict]]:
        """Load high scores from file."""
        if not self.scores_file.exists():
            return {}
        
        try:
            with open(self.scores_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save_scores(self):
        """Save high scores to file."""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self._scores, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't save
    
    def add_score(self, game_name: str, score: int, **metadata) -> bool:
        """Add a new score for a game.
        
        Args:
            game_name: Name of the game
            score: Score achieved
            **metadata: Additional metadata (level, lines, etc.)
            
        Returns:
            True if this is a new high score, False otherwise
        """
        if game_name not in self._scores:
            self._scores[game_name] = []
        
        entry = {
            'score': score,
            'date': datetime.now().isoformat(),
            **metadata
        }
        
        self._scores[game_name].append(entry)
        # Keep top 10 scores
        self._scores[game_name].sort(key=lambda x: x['score'], reverse=True)
        self._scores[game_name] = self._scores[game_name][:10]
        
        self._save_scores()
        
        # Check if this is a new high score
        return self._scores[game_name][0]['score'] == score
    
    def get_high_score(self, game_name: str) -> Optional[int]:
        """Get the highest score for a game.
        
        Args:
            game_name: Name of the game
            
        Returns:
            Highest score or None if no scores exist
        """
        if game_name not in self._scores or not self._scores[game_name]:
            return None
        return self._scores[game_name][0]['score']
    
    def get_top_scores(self, game_name: str, limit: int = 10) -> List[Dict]:
        """Get top scores for a game.
        
        Args:
            game_name: Name of the game
            limit: Maximum number of scores to return
            
        Returns:
            List of score entries
        """
        if game_name not in self._scores:
            return []
        return self._scores[game_name][:limit]
    
    def get_all_scores(self) -> Dict[str, List[Dict]]:
        """Get all high scores for all games.
        
        Returns:
            Dictionary mapping game names to score lists
        """
        return self._scores.copy()

