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
                     'space_invaders', 'breakout', 'hangman', 'tictactoe', 'wordle']
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
            'wordle': 'Wordle'
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
        x_left = 5
        x_right = width // 2 + 5
        
        # Left column - Basic stats
        stdscr.addstr(y, x_left, "Basic Stats:", curses.A_BOLD)
        y += 1
        
        items = [
            ("Games Played", stats.get('games_played', 0)),
            ("Games Won", stats.get('games_won', 0)),
            ("Games Lost", stats.get('games_lost', 0)),
            ("Best Score", stats.get('best_score', 0)),
            ("Worst Score", stats.get('worst_score', 'N/A')),
            ("Average Score", stats.get('average_score', 0)),
        ]
        
        for label, value in items:
            stdscr.addstr(y, x_left, f"  {label}: {value}")
            y += 1
        
        # Play time
        play_time = stats.get('total_play_time', 0)
        time_str = self.stats_manager.format_play_time(play_time)
        stdscr.addstr(y, x_left, f"  Play Time: {time_str}")
        y += 2
        
        # Win rate and streaks
        win_rate = self.stats_manager.get_win_rate(game_key)
        stdscr.addstr(y, x_left, "Performance:", curses.A_BOLD)
        y += 1
        stdscr.addstr(y, x_left, f"  Win Rate: {win_rate:.1f}%")
        y += 1
        stdscr.addstr(y, x_left, f"  Current Streak: {stats.get('win_streak', 0)}")
        y += 1
        stdscr.addstr(y, x_left, f"  Best Streak: {stats.get('best_win_streak', 0)}")
        y += 1
        
        # Improvement indicator
        improving = self.stats_manager.is_improving(game_key)
        if improving:
            stdscr.addstr(y, x_left, "  Trend: ↗ Improving!", curses.A_BOLD)
        else:
            stdscr.addstr(y, x_left, "  Trend: → Stable")
        
        # Right column - Score graph and best session
        y_right = 6
        score_trend = self.stats_manager.get_score_trend(game_key, 10)
        
        if score_trend and any(score_trend):
            stdscr.addstr(y_right, x_right, "Recent Scores (Last 10):", curses.A_BOLD)
            y_right += 1
            
            # Draw ASCII graph
            graph = self.stats_manager.get_ascii_graph(score_trend, width=20, height=8)
            for line in graph:
                stdscr.addstr(y_right, x_right, line)
                y_right += 1
            
            # Show score scale
            max_score = max(score_trend)
            min_score = min(score_trend)
            stdscr.addstr(y_right, x_right, f"Max: {max_score}")
            y_right += 1
            stdscr.addstr(y_right, x_right, f"Min: {min_score}")
            y_right += 2
        
        # Best session
        best_session = self.stats_manager.get_best_session(game_key)
        if best_session:
            stdscr.addstr(y_right, x_right, "Best Session:", curses.A_BOLD)
            y_right += 1
            stdscr.addstr(y_right, x_right, f"  Score: {best_session['score']}")
            y_right += 1
            if best_session.get('won'):
                stdscr.addstr(y_right, x_right, "  Result: Won", curses.A_BOLD)
            else:
                stdscr.addstr(y_right, x_right, "  Result: Lost")
        
        # Instructions
        inst_text = "↑↓: Navigate | Q: Back"
        inst_x = center_text(inst_text, width)
        stdscr.addstr(height - 2, inst_x, inst_text)
        
        stdscr.refresh()

