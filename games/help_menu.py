"""Help and tutorial system."""

import curses
from utils.ui_helpers import center_text, draw_text_box


class HelpMenu:
    """Interactive help and tutorial menu."""
    
    GAME_HELP = {
        'snake': {
            'title': 'Snake - Help',
            'description': 'Classic snake game. Eat food to grow and score points!',
            'controls': [
                ('Arrow Keys', 'Move the snake'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Plan your path to avoid trapping yourself',
                'The snake grows each time you eat food',
                'Try to maximize space before eating',
            ]
        },
        'tetris': {
            'title': 'Tetris - Help',
            'description': 'Stack falling blocks to clear lines and score points!',
            'controls': [
                ('← →', 'Move piece left/right'),
                ('↓', 'Soft drop (faster fall)'),
                ('↑ / Space', 'Rotate piece'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Clear multiple lines at once for bonus points',
                'Keep the board clean - don\'t let it fill up',
                'Plan ahead for piece placement',
                'The game speeds up as you level up',
            ]
        },
        'pacman': {
            'title': 'Pac-Man - Help',
            'description': 'Navigate the maze, collect dots, and avoid ghosts!',
            'controls': [
                ('Arrow Keys', 'Move Pac-Man'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Eat power pellets to make ghosts vulnerable',
                'Eat vulnerable ghosts for bonus points',
                'Clear all dots to win',
                'Watch out for ghost patterns',
            ]
        },
        'pong': {
            'title': 'Pong - Help',
            'description': 'Classic paddle game. First to score wins!',
            'controls': [
                ('W/S or ↑↓', 'Move Player 1 paddle'),
                ('I/K', 'Move Player 2 paddle (2-player mode)'),
                ('A', 'Toggle AI/2-player mode'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Hit the ball with the edge of your paddle for more angle',
                'Watch the ball\'s trajectory',
                'First to 5 points wins',
            ]
        },
        '2048': {
            'title': '2048 - Help',
            'description': 'Slide numbered tiles to combine them and reach 2048!',
            'controls': [
                ('Arrow Keys', 'Move tiles in that direction'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Try to keep your highest tile in a corner',
                'Combine tiles of the same number',
                'Plan your moves to avoid blocking yourself',
                'The goal is to reach 2048, but you can keep playing!',
            ]
        },
        'minesweeper': {
            'title': 'Minesweeper - Help',
            'description': 'Find all mines without detonating any!',
            'controls': [
                ('Arrow Keys', 'Move cursor'),
                ('Space/Enter', 'Reveal cell'),
                ('F', 'Toggle flag'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Numbers show how many mines are adjacent',
                'Use flags to mark suspected mines',
                'Start with cells that have fewer adjacent mines',
                'The first click is always safe',
            ]
        },
        'space_invaders': {
            'title': 'Space Invaders - Help',
            'description': 'Shoot down invading aliens before they reach you!',
            'controls': [
                ('← → or A/D', 'Move ship'),
                ('Space', 'Shoot'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Shoot enemies before they reach the bottom',
                'Enemies move faster as you progress',
                'You have 3 lives - use them wisely',
                'Clear all enemies to win',
            ]
        },
        'breakout': {
            'title': 'Breakout - Help',
            'description': 'Break all bricks with the ball and paddle!',
            'controls': [
                ('← → or A/D', 'Move paddle'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Hit the ball with the edge of the paddle for angles',
                'Don\'t let the ball fall',
                'You have 3 lives',
                'Break all bricks to win',
            ]
        },
        'hangman': {
            'title': 'Hangman - Help',
            'description': 'Guess the word before the hangman is drawn!',
            'controls': [
                ('A-Z', 'Guess a letter'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Start with common letters (E, A, R, I, O, T)',
                'You have 6 wrong guesses',
                'Score is based on how few wrong guesses you make',
                'Think of common programming/computer terms',
            ]
        },
        'tictactoe': {
            'title': 'Tic-Tac-Toe - Help',
            'description': 'Classic 3x3 game. Get three in a row to win!',
            'controls': [
                ('Arrow Keys', 'Move cursor'),
                ('Space/Enter', 'Place mark'),
                ('M', 'Toggle AI/2-player mode'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Control the center square for better positioning',
                'Try to create two winning paths at once',
                'Block your opponent\'s winning moves',
                'Corner squares are strategically important',
            ]
        },
        'wordle': {
            'title': 'Wordle - Help',
            'description': 'Guess the 5-letter word in 6 tries!',
            'controls': [
                ('A-Z', 'Type letters'),
                ('Enter', 'Submit guess'),
                ('Backspace', 'Delete letter'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                '[X] means correct letter in correct position',
                ' X  means correct letter in wrong position',
                '·X· means letter is not in the word',
                'Start with words that use common letters',
                'Use the keyboard to see which letters you\'ve tried',
                'All words are programming/tech related',
            ]
        },
        'connect_four': {
            'title': 'Connect Four - Help',
            'description': 'Drop pieces to get four in a row - horizontal, vertical, or diagonal!',
            'controls': [
                ('← →', 'Move cursor'),
                ('Space/Enter', 'Drop piece'),
                ('M', 'Toggle AI/2-Player mode'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Try to control the center columns',
                'Look for opportunities to create multiple threats',
                'Watch for opponent\'s winning moves and block them',
                'Think several moves ahead',
            ]
        },
        'battleship': {
            'title': 'Battleship - Help',
            'description': 'Sink all enemy ships before they sink yours!',
            'controls': [
                ('Arrow Keys', 'Move cursor'),
                ('Space/Enter', 'Fire at position'),
                ('R', 'Rotate ship (during setup)'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'When you hit a ship, try adjacent squares',
                'Spread your ships out during placement',
                'Use a systematic search pattern',
                'Mark your hits and misses mentally',
            ]
        },
        'conway': {
            'title': 'Conway\'s Game of Life - Help',
            'description': 'Watch cellular patterns evolve based on simple rules!',
            'controls': [
                ('Arrow Keys', 'Move cursor'),
                ('Space', 'Toggle cell'),
                ('Enter', 'Start/Stop simulation'),
                ('S', 'Step one generation'),
                ('C', 'Clear grid'),
                ('R', 'Random fill'),
                ('1-5', 'Insert patterns'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Try classic patterns like gliders and blinkers',
                'Experiment with random configurations',
                'Watch for stable, oscillating, or moving patterns',
                'Use patterns 1-5 for pre-made designs',
            ]
        },
        'asteroids': {
            'title': 'Asteroids - Help',
            'description': 'Destroy asteroids and survive as long as possible!',
            'controls': [
                ('← →', 'Rotate ship'),
                ('↑', 'Thrust'),
                ('Space', 'Shoot'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Keep moving to avoid asteroids',
                'Shoot large asteroids from a distance',
                'Use the edges to wrap around',
                'Don\'t spam shots - aim carefully',
            ]
        },
        'centipede': {
            'title': 'Centipede - Help',
            'description': 'Shoot the descending centipede before it reaches you!',
            'controls': [
                ('Arrow Keys', 'Move player'),
                ('Space', 'Shoot'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Shoot mushrooms to clear paths',
                'Target the head of the centipede',
                'Watch out for spiders in your zone',
                'Stay mobile and keep shooting',
            ]
        },
        'missile_command': {
            'title': 'Missile Command - Help',
            'description': 'Defend your cities from incoming missiles!',
            'controls': [
                ('Arrow Keys', 'Move crosshair'),
                ('Space', 'Fire missile'),
                ('1/2/3', 'Select missile base'),
                ('P', 'Pause/Unpause'),
                ('Q', 'Quit to menu'),
            ],
            'tips': [
                'Lead your shots - missiles take time to reach target',
                'Use explosion radius to hit multiple missiles',
                'Preserve ammo - each base has limited missiles',
                'Protect cities and bases equally',
            ]
        }
    }
    
    GENERAL_HELP = {
        'title': 'General Help',
        'sections': [
            ('Navigation', [
                'Use ↑↓ arrow keys to navigate menus',
                'Press Enter to select',
                'Press Q to go back or quit',
            ]),
            ('Settings', [
                'Access Settings from the main menu',
                'Adjust game speed and difficulty',
                'Settings affect all games',
            ]),
            ('High Scores', [
                'High scores are saved automatically',
                'View high scores during gameplay',
                'New high scores are highlighted',
            ]),
            ('Statistics', [
                'View your game statistics',
                'Track total play time',
                'See your best scores',
            ]),
        ]
    }
    
    def __init__(self):
        self.current_game = 0
        self.games = ['snake', 'tetris', 'pacman', 'pong', '2048', 'minesweeper', 
                     'space_invaders', 'breakout', 'hangman', 'tictactoe', 'wordle', 
                     'connect_four', 'battleship', 'conway', 'asteroids', 'centipede',
                     'missile_command', 'general']
        self.game_names = {
            'snake': 'Snake',
            'tetris': 'Tetris',
            'pacman': 'Pac-Man',
            'pong': 'Pong',
            '2048': '2048',
            'minesweeper': 'Minesweeper',
            'space_invaders': 'Space Invaders',
            'breakout': 'Breakout',
            'hangman': 'Hangman',
            'tictactoe': 'Tic-Tac-Toe',
            'wordle': 'Wordle',
            'connect_four': 'Connect Four',
            'battleship': 'Battleship',
            'conway': 'Conway\'s Game of Life',
            'asteroids': 'Asteroids',
            'centipede': 'Centipede',
            'missile_command': 'Missile Command',
            'general': 'General Help'
        }
    
    def run(self):
        """Display and handle the help menu."""
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        try:
            while True:
                self._draw_menu(stdscr)
                key = stdscr.getch()
                
                if key == ord('q'):
                    break
                elif key == curses.KEY_UP:
                    self.current_game = (self.current_game - 1) % len(self.games)
                elif key == curses.KEY_DOWN:
                    self.current_game = (self.current_game + 1) % len(self.games)
                elif key == ord('\n') or key == ord('\r'):
                    self._show_help(stdscr, self.games[self.current_game])
        finally:
            curses.endwin()
    
    def _draw_menu(self, stdscr):
        """Draw the help menu selection."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "Help & Tutorials"
        title_x = center_text(title, width)
        stdscr.addstr(2, title_x, title, curses.A_BOLD)
        
        # Instructions
        instructions = "Select a game to view help, Q to go back"
        inst_x = center_text(instructions, width)
        stdscr.addstr(4, inst_x, instructions)
        
        # Game list
        start_y = 6
        for i, game_key in enumerate(self.games):
            y = start_y + i * 2
            name = self.game_names[game_key]
            if i == self.current_game:
                stdscr.addstr(y, width // 2 - 10, f"> {name} <", curses.A_REVERSE)
            else:
                stdscr.addstr(y, width // 2 - 5, name)
        
        stdscr.refresh()
    
    def _show_help(self, stdscr, game_key: str):
        """Show detailed help for a game."""
        if game_key == 'general':
            self._show_general_help(stdscr)
        else:
            self._show_game_help(stdscr, game_key)
    
    def _show_game_help(self, stdscr, game_key: str):
        """Show help for a specific game."""
        help_data = self.GAME_HELP[game_key]
        height, width = stdscr.getmaxyx()
        
        while True:
            stdscr.clear()
            stdscr.border(0)
            
            y = 2
            
            # Title
            title_x = center_text(help_data['title'], width)
            stdscr.addstr(y, title_x, help_data['title'], curses.A_BOLD)
            y += 2
            
            # Description
            desc_x = center_text(help_data['description'], width)
            stdscr.addstr(y, desc_x, help_data['description'])
            y += 3
            
            # Controls
            stdscr.addstr(y, 5, "Controls:", curses.A_BOLD)
            y += 1
            for control, desc in help_data['controls']:
                stdscr.addstr(y, 8, f"{control:15} - {desc}")
                y += 1
            
            y += 1
            
            # Tips
            stdscr.addstr(y, 5, "Tips:", curses.A_BOLD)
            y += 1
            for tip in help_data['tips']:
                stdscr.addstr(y, 8, f"• {tip}")
                y += 1
            
            # Back instruction
            back_text = "Press Q to go back"
            back_x = center_text(back_text, width)
            stdscr.addstr(height - 2, back_x, back_text)
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == ord('q'):
                break
    
    def _show_general_help(self, stdscr):
        """Show general help information."""
        height, width = stdscr.getmaxyx()
        
        while True:
            stdscr.clear()
            stdscr.border(0)
            
            y = 2
            
            # Title
            title_x = center_text(self.GENERAL_HELP['title'], width)
            stdscr.addstr(y, title_x, self.GENERAL_HELP['title'], curses.A_BOLD)
            y += 2
            
            # Sections
            for section_title, items in self.GENERAL_HELP['sections']:
                stdscr.addstr(y, 5, section_title + ":", curses.A_BOLD)
                y += 1
                for item in items:
                    stdscr.addstr(y, 8, f"• {item}")
                    y += 1
                y += 1
            
            # Back instruction
            back_text = "Press Q to go back"
            back_x = center_text(back_text, width)
            stdscr.addstr(height - 2, back_x, back_text)
            
            stdscr.refresh()
            
            key = stdscr.getch()
            if key == ord('q'):
                break

