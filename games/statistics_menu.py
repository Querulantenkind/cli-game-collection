"""Statistics viewing menu."""

import curses
from utils.statistics import StatisticsManager
from utils.ui_helpers import center_text, draw_info_panel


class StatisticsMenu:
    """Menu for viewing game statistics."""
    
    def __init__(self):
        self.stats_manager = StatisticsManager()
        self.current_view = 0  # 0 = overview, 1+ = game stats
        self.games = ['snake', 'tetris', 'pacman', 'pong', '2048', 'minesweeper',
                     'space_invaders', 'breakout', 'hangman']
        self.game_names = {
            'snake': 'Snake',
            'tetris': 'Tetris',
            'pacman': 'Pac-Man',
            'pong': 'Pong',
            '2048': '2048',
            'minesweeper': 'Minesweeper',
            'space_invaders': 'Space Invaders',
            'breakout': 'Breakout',
            'hangman': 'Hangman'
        }
    
    def run(self):
        """Display and handle the statistics menu."""
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        try:
            while True:
                if self.current_view == 0:
                    self._draw_overview(stdscr)
                else:
                    game_idx = self.current_view - 1
                    if game_idx < len(self.games):
                        self._draw_game_stats(stdscr, self.games[game_idx])
                
                key = stdscr.getch()
                
                if key == ord('q'):
                    break
                elif key == curses.KEY_UP:
                    if self.current_view > 0:
                        self.current_view -= 1
                elif key == curses.KEY_DOWN:
                    if self.current_view < len(self.games):
                        self.current_view += 1
                elif key == ord('\n') or key == ord('\r'):
                    if self.current_view > 0:
                        # Already viewing game stats, do nothing
                        pass
                    else:
                        # Go to first game
                        self.current_view = 1
        finally:
            curses.endwin()
    
    def _draw_overview(self, stdscr):
        """Draw overview statistics."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "Statistics Overview"
        title_x = center_text(title, width)
        stdscr.addstr(2, title_x, title, curses.A_BOLD)
        
        stats = self.stats_manager.get_all_stats()
        
        y = 5
        
        # Total games
        total_games = self.stats_manager.get_total_games_played()
        stdscr.addstr(y, 5, f"Total Games Played: {total_games}")
        y += 2
        
        # Total play time
        total_time = stats.get('total_play_time', 0)
        time_str = self.stats_manager.format_play_time(total_time)
        stdscr.addstr(y, 5, f"Total Play Time: {time_str}")
        y += 2
        
        # First/last played
        if stats.get('first_played'):
            first = stats['first_played'][:10]  # Just date
            stdscr.addstr(y, 5, f"First Played: {first}")
            y += 1
        if stats.get('last_played'):
            last = stats['last_played'][:10]
            stdscr.addstr(y, 5, f"Last Played: {last}")
            y += 2
        
        # Game list
        stdscr.addstr(y, 5, "Game Statistics:", curses.A_BOLD)
        y += 2
        
        for i, game_key in enumerate(self.games):
            game_name = self.game_names[game_key]
            game_stats = self.stats_manager.get_game_stats(game_key)
            games_played = game_stats.get('games_played', 0)
            
            marker = ">" if (i + 1) == self.current_view else " "
            stdscr.addstr(y, 5, f"{marker} {game_name}: {games_played} games")
            y += 1
        
        # Instructions
        inst_text = "↑↓: Navigate | Enter: View Details | Q: Back"
        inst_x = center_text(inst_text, width)
        stdscr.addstr(height - 2, inst_x, inst_text)
        
        stdscr.refresh()
    
    def _draw_game_stats(self, stdscr, game_key: str):
        """Draw statistics for a specific game."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        game_name = self.game_names[game_key]
        stats = self.stats_manager.get_game_stats(game_key)
        
        # Title
        title = f"{game_name} Statistics"
        title_x = center_text(title, width)
        stdscr.addstr(2, title_x, title, curses.A_BOLD)
        
        y = 5
        
        # Statistics
        items = [
            ("Games Played", stats.get('games_played', 0)),
            ("Games Won", stats.get('games_won', 0)),
            ("Games Lost", stats.get('games_lost', 0)),
            ("Best Score", stats.get('best_score', 0)),
            ("Average Score", stats.get('average_score', 0)),
        ]
        
        draw_info_panel(stdscr, y, 10, items)
        
        # Play time
        play_time = stats.get('total_play_time', 0)
        time_str = self.stats_manager.format_play_time(play_time)
        stdscr.addstr(y + len(items) + 1, 10, f"Total Play Time: {time_str}")
        
        # Instructions
        inst_text = "↑↓: Navigate | Q: Back"
        inst_x = center_text(inst_text, width)
        stdscr.addstr(height - 2, inst_x, inst_text)
        
        stdscr.refresh()

