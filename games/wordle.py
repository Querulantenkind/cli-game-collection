"""Wordle word-guessing game."""

import curses
import random
from typing import List, Set, Dict, Any
from utils.base_game import BaseGame
from utils.ui_helpers import draw_game_over_screen


class WordleGame(BaseGame):
    """Wordle game for the terminal."""
    
    # Word list - programming/tech related words
    WORDS = [
        'ARRAY', 'BYTES', 'CACHE', 'CLASS', 'DEBUG',
        'ERROR', 'FLOAT', 'GRAPH', 'HELLO', 'INDEX',
        'LOGIC', 'MERGE', 'QUERY', 'STACK', 'TUPLE',
        'UNION', 'VALUE', 'WHILE', 'YIELD', 'ZONES',
        'AGENT', 'BLOCK', 'CLOUD', 'DATUM', 'EVENT',
        'FIELD', 'GROUP', 'HTTPS', 'INPUT', 'JOINS',
        'KERNEL', 'LINKS', 'MODEL', 'NODES', 'ORDER',
        'PARSE', 'QUEUE', 'ROUTE', 'SCOPE', 'TABLE',
        'USERS', 'VALID', 'WATCH', 'XPATH', 'YIELD',
        'ABORT', 'BUILD', 'CHAIN', 'DEFER', 'EMOJI',
        'FRAME', 'GRANT', 'HOOKS', 'IMAGE', 'JOINS',
    ]
    
    def __init__(self):
        super().__init__('wordle', min_height=24, min_width=80)
        
        # Game state
        self.target_word = ''
        self.guesses = []
        self.current_guess = ''
        self.max_guesses = 6
        self.letter_states = {}  # Track letter colors
        self.cursor_pos = 0
    
    def _get_input_timeout(self) -> int:
        return 100
    
    def _init_game(self):
        """Initialize the game."""
        self.target_word = random.choice(self.WORDS).upper()
        self.guesses = []
        self.current_guess = ''
        self.letter_states = {}
        self.cursor_pos = 0
    
    def _handle_input(self, key: int) -> bool:
        """Handle player input."""
        if key == ord('q'):
            self.game_over = True
            return False
        
        if key == ord('p'):
            self.paused = not self.paused
            return True
        
        if self.paused or self.game_over:
            return True
        
        # Handle letter input
        if key >= ord('a') and key <= ord('z'):
            letter = chr(key).upper()
            if len(self.current_guess) < 5:
                self.current_guess += letter
        elif key >= ord('A') and key <= ord('Z'):
            letter = chr(key)
            if len(self.current_guess) < 5:
                self.current_guess += letter
        
        # Handle backspace
        elif key in [curses.KEY_BACKSPACE, 127, 8, ord('\b')]:
            if len(self.current_guess) > 0:
                self.current_guess = self.current_guess[:-1]
        
        # Handle enter (submit guess)
        elif key in [ord('\n'), ord('\r'), curses.KEY_ENTER]:
            if len(self.current_guess) == 5:
                self._submit_guess()
        
        return True
    
    def _submit_guess(self):
        """Submit the current guess."""
        guess = self.current_guess.upper()
        self.guesses.append(guess)
        
        # Update letter states
        for i, letter in enumerate(guess):
            target_letter = self.target_word[i]
            
            if letter == target_letter:
                self.letter_states[letter] = 'correct'
            elif letter in self.target_word:
                if self.letter_states.get(letter) != 'correct':
                    self.letter_states[letter] = 'present'
            else:
                if letter not in self.letter_states:
                    self.letter_states[letter] = 'absent'
        
        # Check win condition
        if guess == self.target_word:
            self.won = True
            self.game_over = True
            self.score = self._calculate_score()
        elif len(self.guesses) >= self.max_guesses:
            self.won = False
            self.game_over = True
            self.score = 0
        
        self.current_guess = ''
    
    def _calculate_score(self) -> int:
        """Calculate score based on guesses used."""
        # Fewer guesses = higher score
        guesses_used = len(self.guesses)
        return max(100 - (guesses_used - 1) * 15, 10)
    
    def _update_game(self, delta_time: float):
        """Update game state."""
        pass  # Wordle is turn-based, no continuous updates
    
    def _draw_game(self):
        """Draw the game."""
        self.stdscr.clear()
        self.stdscr.border(0)
        
        # Title
        title = "WORDLE"
        title_x = (self.width - len(title)) // 2
        self.stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Subtitle
        subtitle = "Guess the 5-letter word!"
        self.stdscr.addstr(2, (self.width - len(subtitle)) // 2, subtitle)
        
        # Draw guesses
        grid_start_y = 5
        grid_start_x = (self.width - 20) // 2
        
        for i in range(self.max_guesses):
            y = grid_start_y + i * 2
            
            if i < len(self.guesses):
                # Draw completed guess
                guess = self.guesses[i]
                for j, letter in enumerate(guess):
                    x = grid_start_x + j * 4
                    
                    # Determine color/style
                    if letter == self.target_word[j]:
                        attr = curses.A_REVERSE | curses.A_BOLD  # Correct position
                        display = f"[{letter}]"
                    elif letter in self.target_word:
                        attr = curses.A_BOLD  # Present but wrong position
                        display = f" {letter} "
                    else:
                        attr = curses.A_DIM  # Not in word
                        display = f" {letter} "
                    
                    self.stdscr.addstr(y, x, display, attr)
            
            elif i == len(self.guesses):
                # Draw current guess being typed
                for j in range(5):
                    x = grid_start_x + j * 4
                    if j < len(self.current_guess):
                        letter = self.current_guess[j]
                        self.stdscr.addstr(y, x, f" {letter} ", curses.A_UNDERLINE)
                    else:
                        self.stdscr.addstr(y, x, " _ ")
            
            else:
                # Draw empty slots
                for j in range(5):
                    x = grid_start_x + j * 4
                    self.stdscr.addstr(y, x, " _ ")
        
        # Guesses remaining
        guesses_left = self.max_guesses - len(self.guesses)
        guess_text = f"Guesses remaining: {guesses_left}/{self.max_guesses}"
        self.stdscr.addstr(grid_start_y + self.max_guesses * 2 + 1, 
                          (self.width - len(guess_text)) // 2, guess_text)
        
        # Keyboard (show letter states)
        keyboard_y = grid_start_y + self.max_guesses * 2 + 3
        keyboard = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]
        
        for row_idx, row in enumerate(keyboard):
            row_text = ""
            for letter in row:
                state = self.letter_states.get(letter, 'unknown')
                if state == 'correct':
                    row_text += f"[{letter}]"
                elif state == 'present':
                    row_text += f" {letter} "
                elif state == 'absent':
                    row_text += f"·{letter}·"
                else:
                    row_text += f" {letter} "
            
            x = (self.width - len(row_text)) // 2
            self.stdscr.addstr(keyboard_y + row_idx, x, row_text)
        
        # Legend
        legend_y = keyboard_y + 4
        legend = [
            "[X] = Correct position",
            " X  = In word, wrong position",
            "·X· = Not in word"
        ]
        for i, text in enumerate(legend):
            self.stdscr.addstr(legend_y + i, (self.width - len(text)) // 2, text, curses.A_DIM)
        
        # Instructions
        inst_y = legend_y + 4
        instructions = [
            "Type letters to guess",
            "Enter: Submit guess",
            "Backspace: Delete letter",
            "Q: Quit"
        ]
        for i, inst in enumerate(instructions):
            self.stdscr.addstr(inst_y + i, (self.width - len(inst)) // 2, inst, curses.A_DIM)
        
        # Pause message
        self._draw_pause_message()
        
        self.stdscr.refresh()
    
    def _get_game_state(self) -> Dict[str, Any]:
        """Get game state for achievements."""
        state = super()._get_game_state()
        state.update({
            'guesses_used': len(self.guesses),
        })
        return state
    
    def _draw_game_over(self, is_new_high: bool = False):
        """Draw game over screen."""
        if self.won:
            title = "YOU WIN!"
            extra_info = [
                f"Word: {self.target_word}",
                f"Guesses: {len(self.guesses)}/{self.max_guesses}"
            ]
        else:
            title = "GAME OVER"
            extra_info = [
                f"Word was: {self.target_word}",
                f"Better luck next time!"
            ]
        
        draw_game_over_screen(
            self.stdscr, title, self.score,
            self.high_score, is_new_high, extra_info
        )

