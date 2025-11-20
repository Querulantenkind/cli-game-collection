"""Tests for game classes."""

import unittest
from games.snake import SnakeGame
from games.tetris import TetrisGame
from games.tictactoe import TicTacToeGame
from games.wordle import WordleGame


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


if __name__ == '__main__':
    unittest.main()

