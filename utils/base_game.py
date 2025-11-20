"""Base game class for CLI games."""

import curses
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from utils.high_score import HighScoreManager
from utils.settings import SettingsManager
from utils.statistics import StatisticsManager
from utils.achievements import AchievementManager
from utils.themes import ThemeManager
from utils.terminal import validate_terminal_size, TerminalSizeError, show_terminal_size_error


class BaseGame(ABC):
    """Base class for all CLI games.
    
    Provides common functionality:
    - Manager initialization (high scores, settings, statistics)
    - Curses setup and teardown
    - Game loop structure
    - Statistics tracking
    - High score management
    """
    
    def __init__(self, game_name: str, min_height: int = 24, min_width: int = 80):
        """Initialize base game.
        
        Args:
            game_name: Name of the game (for high scores, settings, stats)
            min_height: Minimum terminal height required
            min_width: Minimum terminal width required
        """
        self.game_name = game_name
        self.min_height = min_height
        self.min_width = min_width
        
        # Game state
        self.score = 0
        self.game_over = False
        self.paused = False
        self.won = False
        
        # Managers
        self.high_score_manager = HighScoreManager()
        self.settings = SettingsManager()
        self.stats = StatisticsManager()
        self.achievements = AchievementManager()
        self.theme_manager = ThemeManager()
        self.high_score = self.high_score_manager.get_high_score(game_name)
        
        # Load theme from settings
        theme_id = self.settings.get('general', 'theme', 'classic')
        self.theme_manager.set_theme(theme_id)
        self.theme = self.theme_manager.get_current_theme()
        
        # Achievement notifications
        self.pending_achievements = []
        self.achievement_notification_time = 0
        
        # Curses window (set in run())
        self.stdscr = None
        self.height = 0
        self.width = 0
        
        # Timing
        self.game_start_time = None
        self.last_frame_time = None
    
    def _init_curses(self):
        """Initialize curses settings."""
        self.stdscr = curses.initscr()
        curses.curs_set(0)  # Hide cursor
        curses.noecho()  # Don't echo keys
        curses.cbreak()  # React to keys immediately
        self.stdscr.keypad(True)  # Enable special keys
        self.stdscr.timeout(self._get_input_timeout())  # Non-blocking input
        
        # Validate terminal size
        try:
            self.height, self.width = validate_terminal_size(
                self.min_height, self.min_width, self.stdscr
            )
        except TerminalSizeError:
            show_terminal_size_error(self.stdscr, self.min_height, self.min_width)
            curses.endwin()
            raise
    
    def _cleanup_curses(self):
        """Clean up curses settings."""
        if self.stdscr:
            curses.endwin()
            self.stdscr = None
    
    def _get_input_timeout(self) -> int:
        """Get input timeout in milliseconds. Override for custom timeout."""
        return 100
    
    def _get_game_speed(self) -> float:
        """Get game speed multiplier. Override for custom speed."""
        return self.settings.get_speed_multiplier(self.game_name)
    
    @abstractmethod
    def _init_game(self):
        """Initialize game-specific state. Called before game loop."""
        pass
    
    @abstractmethod
    def _handle_input(self, key: int) -> bool:
        """Handle input. Returns True if game should continue.
        
        Args:
            key: Key code from getch()
            
        Returns:
            True to continue, False to quit
        """
        pass
    
    @abstractmethod
    def _update_game(self, delta_time: float):
        """Update game state. Called each frame.
        
        Args:
            delta_time: Time since last frame in seconds
        """
        pass
    
    @abstractmethod
    def _draw_game(self):
        """Draw the game. Called each frame."""
        pass
    
    def _draw_pause_message(self):
        """Draw pause message overlay."""
        if self.paused:
            pause_msg = "PAUSED - Press P to resume"
            msg_x = (self.width - len(pause_msg)) // 2
            msg_y = self.height // 2
            self.stdscr.addstr(msg_y, msg_x, pause_msg, 
                             curses.A_BOLD | curses.A_REVERSE)
    
    def _draw_info_bar(self, extra_info: Optional[Dict[str, Any]] = None):
        """Draw info bar with score and high score.
        
        Args:
            extra_info: Optional dict of additional info to display
        """
        # Score
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(0, 2, score_text)
        
        # High score
        if self.high_score is not None and self.settings.get('general', 'show_high_scores', True):
            high_text = f"High: {self.high_score}"
            self.stdscr.addstr(0, self.width - len(high_text) - 2, high_text)
        
        # Extra info
        if extra_info:
            x = 2
            for key, value in extra_info.items():
                info_text = f"{key}: {value}"
                self.stdscr.addstr(1, x, info_text)
                x += len(info_text) + 3
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get current game state for achievement checking.
        
        Override this method to provide game-specific state.
        
        Returns:
            Dictionary of game state
        """
        return {
            'score': self.score,
            'won': self.won,
            'game_over': self.game_over,
        }
    
    def _check_achievements(self):
        """Check for achievements and show notifications."""
        game_state = self._get_game_state()
        
        # Add stats for collection achievements
        all_stats = self.stats.get_all_stats()
        games_played = set()
        games_won = set()
        for game_name, game_stats in all_stats.get('games', {}).items():
            if game_stats.get('games_played', 0) > 0:
                games_played.add(game_name)
            if game_stats.get('games_won', 0) > 0:
                games_won.add(game_name)
        
        game_state['games_played_count'] = len(games_played)
        game_state['games_won_count'] = len(games_won)
        
        newly_unlocked = self.achievements.check_achievements(self.game_name, game_state)
        
        if newly_unlocked:
            self.pending_achievements.extend(newly_unlocked)
            self.achievement_notification_time = time.time()
    
    def _draw_achievement_notification(self):
        """Draw achievement unlock notification."""
        if not self.pending_achievements:
            return
        
        # Show notification for 3 seconds
        if time.time() - self.achievement_notification_time > 3.0:
            self.pending_achievements.pop(0)
            if self.pending_achievements:
                self.achievement_notification_time = time.time()
            return
        
        achievement_id = self.pending_achievements[0]
        achievement = self.achievements.get_achievement(achievement_id)
        
        if achievement:
            # Draw notification box
            lines = [
                "╔════════════════════════════════╗",
                "║   ACHIEVEMENT UNLOCKED!   ║",
                f"║   {achievement.icon} {achievement.name:26} ║",
                f"║   {achievement.description:28} ║",
                "╚════════════════════════════════╝"
            ]
            
            box_width = len(lines[0])
            box_height = len(lines)
            start_y = self.height // 2 - box_height // 2
            start_x = (self.width - box_width) // 2
            
            for i, line in enumerate(lines):
                self.stdscr.addstr(start_y + i, start_x, line, 
                                 curses.A_BOLD | curses.A_REVERSE)
    
    def _save_results(self) -> bool:
        """Save high score and statistics. Returns True if new high score.
        
        Returns:
            True if this is a new high score
        """
        # Record statistics
        play_time = time.time() - self.game_start_time if self.game_start_time else 0
        self.stats.record_game_end(self.game_name, self.score, self.won, play_time)
        
        # Save high score
        is_new_high = self.high_score_manager.add_score(self.game_name, self.score)
        if is_new_high:
            self.high_score = self.score
        
        # Check achievements with final state
        game_state = self._get_game_state()
        game_state['is_new_high'] = is_new_high
        newly_unlocked = self.achievements.check_achievements(self.game_name, game_state)
        if newly_unlocked:
            self.pending_achievements.extend(newly_unlocked)
            self.achievement_notification_time = time.time()
        
        return is_new_high
    
    def run(self):
        """Run the game. Main entry point."""
        try:
            # Initialize curses
            self._init_curses()
            
            # Record game start
            self.stats.record_game_start(self.game_name)
            self.game_start_time = time.time()
            self.last_frame_time = time.time()
            
            # Initialize game
            self._init_game()
            
            # Game loop
            while not self.game_over:
                current_time = time.time()
                delta_time = current_time - self.last_frame_time
                self.last_frame_time = current_time
                
                # Handle input
                key = self.stdscr.getch()
                if not self._handle_input(key):
                    break
                
                if self.paused:
                    self._draw_game()
                    continue
                
                # Update game
                self._update_game(delta_time)
                
                # Check achievements (only once per frame, not every second)
                # We'll check at game end instead
                
                # Draw game
                self._draw_game()
                
                # Draw achievement notifications
                self._draw_achievement_notification()
                
                # Small sleep to prevent excessive CPU usage
                time.sleep(0.01)
            
            # Save results
            is_new_high = self._save_results()
            
            # Show game over screen
            self._draw_game_over(is_new_high)
            self.stdscr.getch()
            
        except TerminalSizeError:
            # Already handled in _init_curses
            pass
        except KeyboardInterrupt:
            # User interrupted
            pass
        finally:
            self._cleanup_curses()
    
    @abstractmethod
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen.
        
        Args:
            is_new_high: Whether this is a new high score
        """
        pass

