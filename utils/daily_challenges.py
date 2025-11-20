"""Daily challenges system."""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum


class ChallengeType(Enum):
    """Types of challenges."""
    SCORE = "score"
    TIME = "time"
    SPECIAL = "special"
    SURVIVAL = "survival"


class Challenge:
    """Represents a single challenge."""
    
    def __init__(self, challenge_id: str, game_name: str, name: str,
                 description: str, challenge_type: ChallengeType,
                 goal: int, reward_points: int = 10):
        """Initialize a challenge.
        
        Args:
            challenge_id: Unique identifier
            game_name: Game this challenge is for
            name: Challenge name
            description: What the player needs to do
            challenge_type: Type of challenge
            goal: Target value (score, time, etc.)
            reward_points: Points awarded
        """
        self.id = challenge_id
        self.game_name = game_name
        self.name = name
        self.description = description
        self.type = challenge_type
        self.goal = goal
        self.reward_points = reward_points
    
    def check_completion(self, result: Dict[str, Any]) -> bool:
        """Check if challenge is completed.
        
        Args:
            result: Game result dictionary
            
        Returns:
            True if challenge is completed
        """
        if result.get('game') != self.game_name:
            return False
        
        if self.type == ChallengeType.SCORE:
            return result.get('score', 0) >= self.goal
        elif self.type == ChallengeType.TIME:
            return result.get('time', float('inf')) <= self.goal
        elif self.type == ChallengeType.SURVIVAL:
            return result.get('survived', 0) >= self.goal
        
        return False


class DailyChallengeManager:
    """Manages daily challenges."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the daily challenge manager.
        
        Args:
            data_dir: Directory to store challenge data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.challenges_file = self.data_dir / "daily_challenges.json"
        self._data = self._load_data()
        self._challenge_pool = self._define_challenges()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load challenge completion data."""
        if not self.challenges_file.exists():
            return {
                'completions': {},  # date -> list of completed challenge IDs
                'streak': 0,
                'best_streak': 0,
                'total_points': 0,
                'last_completion_date': None
            }
        
        try:
            with open(self.challenges_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {
                'completions': {},
                'streak': 0,
                'best_streak': 0,
                'total_points': 0,
                'last_completion_date': None
            }
    
    def _save_data(self):
        """Save challenge data."""
        try:
            with open(self.challenges_file, 'w') as f:
                json.dump(self._data, f, indent=2)
        except IOError:
            pass
    
    def _define_challenges(self) -> List[Challenge]:
        """Define all possible challenges."""
        challenges = []
        
        # Snake challenges
        challenges.append(Challenge(
            'snake_200', 'snake', 'Snake Sprint',
            'Reach 200 points in Snake', ChallengeType.SCORE, 200, 15
        ))
        challenges.append(Challenge(
            'snake_300', 'snake', 'Snake Master',
            'Reach 300 points in Snake', ChallengeType.SCORE, 300, 20
        ))
        
        # Tetris challenges
        challenges.append(Challenge(
            'tetris_2000', 'tetris', 'Tetris Sprint',
            'Reach 2000 points in Tetris', ChallengeType.SCORE, 2000, 15
        ))
        challenges.append(Challenge(
            'tetris_15_lines', 'tetris', 'Line Clear Master',
            'Clear 15 lines in Tetris', ChallengeType.SPECIAL, 15, 20
        ))
        
        # 2048 challenges
        challenges.append(Challenge(
            '2048_1024', '2048', '1024 Challenge',
            'Reach 1024 in 2048', ChallengeType.SCORE, 1024, 20
        ))
        
        # Pac-Man challenges
        challenges.append(Challenge(
            'pacman_500', 'pacman', 'Pac-Man Marathon',
            'Reach 500 points in Pac-Man', ChallengeType.SCORE, 500, 15
        ))
        
        # Wordle challenges
        challenges.append(Challenge(
            'wordle_4_guess', 'wordle', 'Quick Wordle',
            'Win Wordle in 4 guesses or less', ChallengeType.SPECIAL, 4, 20
        ))
        
        # Minesweeper challenges
        challenges.append(Challenge(
            'minesweeper_90s', 'minesweeper', 'Speed Sweeper',
            'Win Minesweeper in under 90 seconds', ChallengeType.TIME, 90, 25
        ))
        
        # Tic-Tac-Toe challenges
        challenges.append(Challenge(
            'tictactoe_3_wins', 'tictactoe', 'Tic-Tac-Toe Master',
            'Win 3 games of Tic-Tac-Toe in a row', ChallengeType.SPECIAL, 3, 15
        ))
        
        # Space Invaders challenges
        challenges.append(Challenge(
            'space_invaders_300', 'space_invaders', 'Space Ace',
            'Reach 300 points in Space Invaders', ChallengeType.SCORE, 300, 15
        ))
        
        # Breakout challenges
        challenges.append(Challenge(
            'breakout_win', 'breakout', 'Brick Breaker',
            'Complete a level of Breakout', ChallengeType.SPECIAL, 1, 20
        ))
        
        return challenges
    
    def get_today_date(self) -> str:
        """Get today's date string.
        
        Returns:
            Date string in YYYY-MM-DD format
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_daily_challenges(self, count: int = 3) -> List[Challenge]:
        """Get today's challenges.
        
        Uses date-based seeding for consistency.
        
        Args:
            count: Number of challenges to return
            
        Returns:
            List of today's challenges
        """
        today = self.get_today_date()
        
        # Use date as seed for consistent daily challenges
        seed = int(datetime.now().strftime("%Y%m%d"))
        random.seed(seed)
        
        # Select challenges
        challenges = random.sample(self._challenge_pool, min(count, len(self._challenge_pool)))
        
        return challenges
    
    def mark_completed(self, challenge_id: str) -> bool:
        """Mark a challenge as completed.
        
        Args:
            challenge_id: ID of the challenge
            
        Returns:
            True if this is a new completion
        """
        today = self.get_today_date()
        
        if today not in self._data['completions']:
            self._data['completions'][today] = []
        
        if challenge_id in self._data['completions'][today]:
            return False  # Already completed
        
        self._data['completions'][today].append(challenge_id)
        
        # Update points
        challenge = self.get_challenge_by_id(challenge_id)
        if challenge:
            self._data['total_points'] = self._data.get('total_points', 0) + challenge.reward_points
        
        # Update streak
        self._update_streak()
        
        self._save_data()
        return True
    
    def _update_streak(self):
        """Update challenge completion streak."""
        today = datetime.now()
        yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        today_str = today.strftime("%Y-%m-%d")
        
        # Check if completed any challenge today
        completed_today = len(self._data['completions'].get(today_str, [])) > 0
        completed_yesterday = len(self._data['completions'].get(yesterday, [])) > 0
        
        if completed_today:
            if completed_yesterday or self._data.get('streak', 0) == 0:
                self._data['streak'] = self._data.get('streak', 0) + 1
            else:
                # Reset streak if skipped a day
                self._data['streak'] = 1
            
            # Update best streak
            if self._data['streak'] > self._data.get('best_streak', 0):
                self._data['best_streak'] = self._data['streak']
            
            self._data['last_completion_date'] = today_str
    
    def is_completed(self, challenge_id: str) -> bool:
        """Check if a challenge is completed today.
        
        Args:
            challenge_id: ID of the challenge
            
        Returns:
            True if completed
        """
        today = self.get_today_date()
        return challenge_id in self._data['completions'].get(today, [])
    
    def get_challenge_by_id(self, challenge_id: str) -> Optional[Challenge]:
        """Get a challenge by ID.
        
        Args:
            challenge_id: ID of the challenge
            
        Returns:
            Challenge object or None
        """
        for challenge in self._challenge_pool:
            if challenge.id == challenge_id:
                return challenge
        return None
    
    def get_streak(self) -> int:
        """Get current streak.
        
        Returns:
            Current streak count
        """
        return self._data.get('streak', 0)
    
    def get_total_points(self) -> int:
        """Get total points earned.
        
        Returns:
            Total points
        """
        return self._data.get('total_points', 0)
    
    def get_completion_rate(self) -> float:
        """Get overall completion rate.
        
        Returns:
            Completion rate as percentage
        """
        total_days = len(self._data['completions'])
        if total_days == 0:
            return 0.0
        
        total_challenges_available = total_days * 3  # 3 challenges per day
        total_completed = sum(len(challenges) for challenges in self._data['completions'].values())
        
        return (total_completed / total_challenges_available) * 100 if total_challenges_available > 0 else 0.0

