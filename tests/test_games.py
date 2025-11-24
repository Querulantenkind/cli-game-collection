"""Tests for game classes."""

import unittest
from games.snake import SnakeGame
from games.tetris import TetrisGame
from games.tictactoe import TicTacToeGame
from games.wordle import WordleGame
from games.connect_four import ConnectFourGame
from games.battleship import BattleshipGame
from games.conway import ConwayGame
from games.asteroids import Asteroids
from games.centipede import CentipedeGame
from games.missile_command import MissileCommandGame


class TestSnakeGame(unittest.TestCase):
    """Test SnakeGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = SnakeGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'snake')
        # Snake is initialized in _init_game, which requires curses
        # Just verify the game object was created
        self.assertIsNotNone(self.game)


class TestTetrisGame(unittest.TestCase):
    """Test TetrisGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = TetrisGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'tetris')
        # Game state is initialized in _init_game, which requires curses
        # Just verify the game object was created
        self.assertIsNotNone(self.game)


class TestTicTacToeGame(unittest.TestCase):
    """Test TicTacToeGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = TicTacToeGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'tictactoe')
        self.assertEqual(len(self.game.board), 3)
    
    def test_check_winner_row(self):
        """Test winner detection for row."""
        self.game.board = [
            ['X', 'X', 'X'],
            [' ', ' ', ' '],
            [' ', ' ', ' ']
        ]
        winner = self.game._check_winner()
        self.assertEqual(winner, 'X')
    
    def test_check_winner_column(self):
        """Test winner detection for column."""
        self.game.board = [
            ['O', ' ', ' '],
            ['O', ' ', ' '],
            ['O', ' ', ' ']
        ]
        winner = self.game._check_winner()
        self.assertEqual(winner, 'O')
    
    def test_check_winner_diagonal(self):
        """Test winner detection for diagonal."""
        self.game.board = [
            ['X', ' ', ' '],
            [' ', 'X', ' '],
            [' ', ' ', 'X']
        ]
        winner = self.game._check_winner()
        self.assertEqual(winner, 'X')


class TestWordleGame(unittest.TestCase):
    """Test WordleGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = WordleGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'wordle')
        # Game state is initialized in _init_game, which requires curses
        # Just verify the game object was created
        self.assertIsNotNone(self.game)
    
    def test_word_list(self):
        """Test that word list has valid words."""
        # WordleGame.WORDS is a list of valid 5-letter words
        # This test checks the structure is correct
        self.assertTrue(hasattr(WordleGame, 'WORDS'))
        # Most tests would need curses initialization


class TestConnectFourGame(unittest.TestCase):
    """Test ConnectFourGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = ConnectFourGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'connect_four')
        self.assertEqual(len(self.game.board), self.game.ROWS)
        self.assertEqual(len(self.game.board[0]), self.game.COLS)
    
    def test_valid_move(self):
        """Test valid move checking."""
        self.assertTrue(self._is_valid_move(0))
    
    def _is_valid_move(self, col):
        """Helper to check valid moves."""
        return self.game.board[0][col] == ' '


class TestBattleshipGame(unittest.TestCase):
    """Test BattleshipGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = BattleshipGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'battleship')
        self.assertEqual(self.game.GRID_SIZE, 10)
        self.assertEqual(len(self.game.SHIPS), 5)


class TestConwayGame(unittest.TestCase):
    """Test ConwayGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = ConwayGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'conway')
        self.assertIsInstance(self.game.grid, set)
    
    def test_patterns_exist(self):
        """Test that patterns are defined."""
        self.assertTrue(hasattr(ConwayGame, 'PATTERNS'))
        self.assertIn('glider', ConwayGame.PATTERNS)


class TestAsteroids(unittest.TestCase):
    """Test Asteroids functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = Asteroids()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'asteroids')
        self.assertEqual(self.game.lives, 3)


class TestCentipedeGame(unittest.TestCase):
    """Test CentipedeGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = CentipedeGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'centipede')
        self.assertEqual(self.game.lives, 3)


class TestMissileCommandGame(unittest.TestCase):
    """Test MissileCommandGame functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.game = MissileCommandGame()
    
    def test_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.game_name, 'missile_command')
        self.assertEqual(len(self.game.bases), 3)
        self.assertEqual(len(self.game.cities), 6)


if __name__ == '__main__':
    unittest.main()

