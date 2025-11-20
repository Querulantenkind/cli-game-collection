"""Tests for manager classes."""

import unittest
import tempfile
import shutil
from pathlib import Path
from utils.high_score import HighScoreManager
from utils.settings import SettingsManager
from utils.statistics import StatisticsManager
from utils.achievements import AchievementManager
from utils.save_manager import SaveManager
from utils.themes import ThemeManager
from utils.daily_challenges import DailyChallengeManager


class TestHighScoreManager(unittest.TestCase):
    """Test HighScoreManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = HighScoreManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_add_score(self):
        """Test adding a score."""
        is_new_high = self.manager.add_score('snake', 100)
        self.assertTrue(is_new_high)
        self.assertEqual(self.manager.get_high_score('snake'), 100)
    
    def test_multiple_scores(self):
        """Test adding multiple scores."""
        self.manager.add_score('snake', 100)
        self.manager.add_score('snake', 200)
        self.manager.add_score('snake', 150)
        
        self.assertEqual(self.manager.get_high_score('snake'), 200)
        top_scores = self.manager.get_top_scores('snake', 3)
        self.assertEqual(len(top_scores), 3)
        self.assertEqual(top_scores[0]['score'], 200)
    
    def test_max_scores_limit(self):
        """Test that only top 10 scores are kept."""
        for i in range(15):
            self.manager.add_score('snake', i * 10)
        
        top_scores = self.manager.get_top_scores('snake')
        self.assertEqual(len(top_scores), 10)


class TestSettingsManager(unittest.TestCase):
    """Test SettingsManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = SettingsManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_default_settings(self):
        """Test default settings are loaded."""
        snake_speed = self.manager.get('snake', 'speed')
        self.assertEqual(snake_speed, 'medium')
    
    def test_set_and_get(self):
        """Test setting and getting values."""
        self.manager.set('snake', 'speed', 'fast')
        self.assertEqual(self.manager.get('snake', 'speed'), 'fast')
    
    def test_speed_multiplier(self):
        """Test speed multiplier calculation."""
        self.manager.set('snake', 'speed', 'slow')
        multiplier = self.manager.get_speed_multiplier('snake')
        self.assertEqual(multiplier, 1.5)


class TestStatisticsManager(unittest.TestCase):
    """Test StatisticsManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = StatisticsManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_record_game(self):
        """Test recording a game."""
        self.manager.record_game_start('snake')
        self.manager.record_game_end('snake', 100, True, 60.0)
        
        stats = self.manager.get_game_stats('snake')
        self.assertEqual(stats['games_played'], 1)
        self.assertEqual(stats['games_won'], 1)
        self.assertEqual(stats['best_score'], 100)
    
    def test_win_rate(self):
        """Test win rate calculation."""
        self.manager.record_game_start('snake')
        self.manager.record_game_end('snake', 100, True, 60.0)
        self.manager.record_game_start('snake')
        self.manager.record_game_end('snake', 50, False, 30.0)
        
        win_rate = self.manager.get_win_rate('snake')
        self.assertEqual(win_rate, 50.0)


class TestAchievementManager(unittest.TestCase):
    """Test AchievementManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = AchievementManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_check_achievements(self):
        """Test achievement checking."""
        game_state = {
            'game': 'snake',
            'score': 150,
            'won': False
        }
        
        unlocked = self.manager.check_achievements('snake', game_state)
        self.assertIn('snake_100', unlocked)
    
    def test_unlock_achievement(self):
        """Test unlocking an achievement."""
        self.manager.unlock('snake_100')
        self.assertTrue(self.manager.is_unlocked('snake_100'))


class TestSaveManager(unittest.TestCase):
    """Test SaveManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = SaveManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load(self):
        """Test saving and loading a game."""
        game_state = {'score': 100, 'level': 5}
        metadata = {'score': 100}
        
        result = self.manager.save_game('snake', 1, game_state, metadata)
        self.assertTrue(result)
        
        loaded = self.manager.load_game('snake', 1)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded['game_state']['score'], 100)
    
    def test_save_slots(self):
        """Test multiple save slots."""
        for slot in range(1, 6):
            self.manager.save_game('snake', slot, {'slot': slot}, {})
        
        saves = self.manager.get_save_list('snake')
        self.assertEqual(len(saves), 5)
        existing_saves = [s for s in saves if s['exists']]
        self.assertEqual(len(existing_saves), 5)


class TestThemeManager(unittest.TestCase):
    """Test ThemeManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.manager = ThemeManager()
    
    def test_get_themes(self):
        """Test getting all themes."""
        themes = self.manager.get_all_themes()
        self.assertGreaterEqual(len(themes), 5)
        self.assertIn('classic', themes)
    
    def test_set_theme(self):
        """Test setting a theme."""
        self.manager.set_theme('dark')
        theme = self.manager.get_current_theme()
        self.assertEqual(theme.id, 'dark')


class TestDailyChallengeManager(unittest.TestCase):
    """Test DailyChallengeManager functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.manager = DailyChallengeManager(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_get_daily_challenges(self):
        """Test getting daily challenges."""
        challenges = self.manager.get_daily_challenges(3)
        self.assertEqual(len(challenges), 3)
    
    def test_mark_completed(self):
        """Test marking a challenge as completed."""
        challenges = self.manager.get_daily_challenges(3)
        challenge_id = challenges[0].id
        
        result = self.manager.mark_completed(challenge_id)
        self.assertTrue(result)
        self.assertTrue(self.manager.is_completed(challenge_id))


if __name__ == '__main__':
    unittest.main()

