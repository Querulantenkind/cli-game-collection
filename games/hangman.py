"""Hangman word game implementation."""

import curses
import random
from typing import Set, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


# Word list
WORDS = [
    'python', 'computer', 'terminal', 'game', 'curses', 'programming',
    'algorithm', 'function', 'variable', 'string', 'integer', 'boolean',
    'dictionary', 'list', 'tuple', 'class', 'object', 'method', 'module',
    'library', 'framework', 'software', 'hardware', 'keyboard', 'mouse',
    'display', 'screen', 'window', 'button', 'menu', 'interface', 'system',
    'operating', 'linux', 'unix', 'command', 'shell', 'script', 'execute',
    'compile', 'debug', 'error', 'exception', 'syntax', 'semantic', 'logic'
]


class HangmanGame(BaseGame):
    """Hangman word game for the terminal."""
    
    def __init__(self):
        super().__init__('hangman', min_height=24, min_width=80)
        
        self.word = random.choice(WORDS).upper()
        self.guessed_letters: Set[str] = set()
        self.wrong_guesses = 0
        self.max_wrong = 6
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize game state."""
        pass  # Already initialized in __init__
    
    def _get_display_word(self) -> str:
        """Get the word with guessed letters revealed."""
        return ' '.join(letter if letter in self.guessed_letters else '_' 
                       for letter in self.word)
    
    def _guess_letter(self, letter: str):
        """Process a letter guess."""
        letter = letter.upper()
        if letter in self.guessed_letters:
            return  # Already guessed
        
        self.guessed_letters.add(letter)
        
        if letter in self.word:
            # Check if won
            if all(l in self.guessed_letters for l in self.word):
                self.won = True
                self.game_over = True
                # Score based on wrong guesses
                self.score = (self.max_wrong - self.wrong_guesses) * 100
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong:
                self.game_over = True
                self.won = False
    
    def _draw_hangman(self, y: int, x: int):
        """Draw the hangman figure."""
        stages = [
            ["  +---+", "  |   |", "      |", "      |", "      |", "      |", "========="],
            ["  +---+", "  |   |", "  O   |", "      |", "      |", "      |", "========="],
            ["  +---+", "  |   |", "  O   |", "  |   |", "      |", "      |", "========="],
            ["  +---+", "  |   |",  "  O   |", " /|   |", "      |", "      |", "========="],
            ["  +---+", "  |   |", "  O   |", " /|\\  |", "      |", "      |", "========="],
            ["  +---+", "  |   |", "  O   |", " /|\\  |", " /    |", "      |", "========="],
            ["  +---+", "  |   |", "  O   |", " /|\\  |", " / \\  |", "      |", "========="],
        ]
        
        stage = min(self.wrong_guesses, len(stages) - 1)
        for i, line in enumerate(stages[stage]):
            self.stdscr.addstr(y + i, x, line)
    
    def _handle_input(self, key: int) -> bool:
        """Handle input."""
        if key == ord('q'):
            return False
        elif ord('a') <= key <= ord('z'):
            self._guess_letter(chr(key))
        return True
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        # Hangman is turn-based, no continuous updates
        pass
    
    def _draw_game(self):
        """Draw the game state."""
        self.stdscr.clear()
        
        # Title
        title = "Hangman"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Draw hangman
        hangman_x = self.width // 4
        hangman_y = 3
        self._draw_hangman(hangman_y, hangman_x)
        
        # Word display
        display_word = self._get_display_word()
        word_x = (self.width - len(display_word)) // 2
        word_y = 12
        self.stdscr.addstr(word_y, word_x, display_word, curses.A_BOLD)
        
        # Guessed letters
        guessed_text = f"Guessed: {', '.join(sorted(self.guessed_letters))}"
        if self.guessed_letters:
            self.stdscr.addstr(word_y + 2, (self.width - len(guessed_text)) // 2, guessed_text)
        
        # Wrong guesses
        wrong_text = f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong}"
        self.stdscr.addstr(word_y + 4, (self.width - len(wrong_text)) // 2, wrong_text)
        
        # Score
        if self.won:
            score_text = f"Score: {self.score}"
            self.stdscr.addstr(word_y + 6, (self.width - len(score_text)) // 2, score_text, 
                            curses.A_BOLD)
        
        # Info bar
        if self.high_score is not None and self.settings.get('general', 'show_high_scores', True):
            high_text = f"High Score: {self.high_score}"
            self.stdscr.addstr(word_y + 7, (self.width - len(high_text)) // 2, high_text)
        
        # Instructions
        inst_y = word_y + 9
        instructions = [
            "Type a letter to guess",
            "Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, (self.width - len(inst)) // 2, inst)
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state['wrong_guesses'] = self.wrong_guesses
        return state
    
    def _save_results(self) -> bool:
        """Save results - only save if won."""
        if self.won:
            return super()._save_results()
        else:
            # Still record stats
            play_time = self.last_frame_time - self.game_start_time if self.game_start_time else 0
            self.stats.record_game_end(self.game_name, self.score, False, play_time)
            return False
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "YOU WIN!"
            extra_info = [
                f"The word was: {self.word}",
                f"Score: {self.score}"
            ]
        else:
            title = "GAME OVER"
            extra_info = [
                f"The word was: {self.word}",
                f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong}"
            ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )
