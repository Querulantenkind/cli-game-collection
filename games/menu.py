"""Main menu for selecting games."""

import curses
from typing import List, Callable
from games.snake import SnakeGame
from games.tetris import TetrisGame
from games.pacman import PacManGame
from games.pong import PongGame
from games.game2048 import Game2048
from games.minesweeper import MinesweeperGame
from games.space_invaders import SpaceInvadersGame
from games.breakout import BreakoutGame
from games.hangman import HangmanGame
from games.tictactoe import TicTacToeGame
from games.wordle import WordleGame
from games.frogger import FroggerGame
from games.sudoku import SudokuGame
from games.settings_menu import SettingsMenu
from games.help_menu import HelpMenu
from games.statistics_menu import StatisticsMenu
from games.achievements_menu import AchievementsMenu
from games.load_menu import LoadMenu
from games.challenges_menu import ChallengesMenu


class GameMenu:
    """Interactive menu for selecting games."""
    
    def __init__(self):
        self.games = [
            ("Snake", self._run_snake),
            ("Tetris", self._run_tetris),
            ("Pac-Man", self._run_pacman),
            ("Pong", self._run_pong),
            ("2048", self._run_2048),
            ("Minesweeper", self._run_minesweeper),
            ("Space Invaders", self._run_space_invaders),
            ("Breakout", self._run_breakout),
            ("Hangman", self._run_hangman),
            ("Tic-Tac-Toe", self._run_tictactoe),
            ("Wordle", self._run_wordle),
            ("Frogger", self._run_frogger),
            ("Sudoku", self._run_sudoku),
            ("Load Game", self._run_load_game),
            ("Settings", self._run_settings),
            ("Statistics", self._run_statistics),
            ("Daily Challenges", self._run_challenges),
            ("Achievements", self._run_achievements),
            ("Help", self._run_help),
            ("Exit", None),
        ]
        self.current_selection = 0
    
    def _run_snake(self):
        """Run the Snake game."""
        game = SnakeGame()
        game.run()
    
    def _run_tetris(self):
        """Run the Tetris game."""
        game = TetrisGame()
        game.run()
    
    def _run_pacman(self):
        """Run the Pac-Man game."""
        game = PacManGame()
        game.run()
    
    def _run_pong(self):
        """Run the Pong game."""
        game = PongGame()
        game.run()
    
    def _run_2048(self):
        """Run the 2048 game."""
        game = Game2048()
        game.run()
    
    def _run_minesweeper(self):
        """Run the Minesweeper game."""
        game = MinesweeperGame()
        game.run()
    
    def _run_space_invaders(self):
        """Run the Space Invaders game."""
        game = SpaceInvadersGame()
        game.run()
    
    def _run_breakout(self):
        """Run the Breakout game."""
        game = BreakoutGame()
        game.run()
    
    def _run_hangman(self):
        """Run the Hangman game."""
        game = HangmanGame()
        game.run()
    
    def _run_tictactoe(self):
        """Run the Tic-Tac-Toe game."""
        game = TicTacToeGame()
        game.run()
    
    def _run_wordle(self):
        """Run the Wordle game."""
        game = WordleGame()
        game.run()
    
    def _run_frogger(self):
        """Run the Frogger game."""
        game = FroggerGame()
        game.run()
    
    def _run_sudoku(self):
        """Run the Sudoku game."""
        game = SudokuGame()
        game.run()
    
    def _run_load_game(self):
        """Run the load game menu."""
        load_menu = LoadMenu()
        result = load_menu.run()
        
        if result:
            game_name, slot = result
            # Load and run the game
            game_classes = {
                'snake': SnakeGame,
                'tetris': TetrisGame,
                'pacman': PacManGame,
                'pong': PongGame,
                '2048': Game2048,
                'minesweeper': MinesweeperGame,
                'space_invaders': SpaceInvadersGame,
                'breakout': BreakoutGame,
                'hangman': HangmanGame,
                'tictactoe': TicTacToeGame,
                'wordle': WordleGame,
                'frogger': FroggerGame,
                'sudoku': SudokuGame,
            }
            
            game_class = game_classes.get(game_name)
            if game_class:
                game = game_class()
                if game._load_game(slot):
                    game.run()
    
    def _run_settings(self):
        """Run the Settings menu."""
        settings = SettingsMenu()
        settings.run()
    
    def _run_statistics(self):
        """Run the Statistics menu."""
        stats = StatisticsMenu()
        stats.run()
    
    def _run_challenges(self):
        """Run the Daily Challenges menu."""
        challenges_menu = ChallengesMenu()
        challenges_menu.run()
    
    def _run_achievements(self):
        """Run the Achievements menu."""
        achievements_menu = AchievementsMenu()
        achievements_menu.run()
    
    def _run_help(self):
        """Run the Help menu."""
        help_menu = HelpMenu()
        help_menu.run()
    
    def run(self):
        """Display and handle the game menu."""
        stdscr = curses.initscr()
        curses.curs_set(0)  # Hide cursor
        curses.noecho()  # Don't echo keys
        curses.cbreak()  # React to keys immediately
        stdscr.keypad(True)  # Enable special keys
        stdscr.timeout(100)  # Non-blocking input
        
        try:
            while True:
                self._draw_menu(stdscr)
                key = stdscr.getch()
                
                if key == curses.KEY_UP:
                    self.current_selection = (self.current_selection - 1) % len(self.games)
                elif key == curses.KEY_DOWN:
                    self.current_selection = (self.current_selection + 1) % len(self.games)
                elif key == ord('\n') or key == ord('\r'):  # Enter key
                    name, game_func = self.games[self.current_selection]
                    if game_func is None:  # Exit
                        break
                    # Restore terminal before running game
                    curses.endwin()
                    game_func()
                    # Reinitialize after game
                    stdscr = curses.initscr()
                    curses.curs_set(0)
                    curses.noecho()
                    curses.cbreak()
                    stdscr.keypad(True)
                    stdscr.timeout(100)
                elif key == ord('q'):
                    break
        finally:
            curses.endwin()
    
    def _draw_menu(self, stdscr):
        """Draw the menu on the screen."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "CLI Game Collection"
        title_x = (width - len(title)) // 2
        stdscr.addstr(2, title_x, title, curses.A_BOLD)
        
        # Instructions
        instructions = "Use ↑↓ to navigate, Enter to select, Q to quit"
        inst_x = (width - len(instructions)) // 2
        stdscr.addstr(4, inst_x, instructions)
        
        # Game list
        start_y = 6
        for i, (name, _) in enumerate(self.games):
            y = start_y + i * 2
            if i == self.current_selection:
                stdscr.addstr(y, width // 2 - 10, f"> {name} <", curses.A_REVERSE)
            else:
                stdscr.addstr(y, width // 2 - 5, name)
        
        stdscr.refresh()

