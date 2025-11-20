"""Daily challenges menu."""

import curses
from utils.daily_challenges import DailyChallengeManager
from utils.ui_helpers import center_text


class ChallengesMenu:
    """Menu for viewing and tracking daily challenges."""
    
    def __init__(self):
        self.challenge_manager = DailyChallengeManager()
    
    def run(self):
        """Display the daily challenges menu."""
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        try:
            while True:
                self._draw(stdscr)
                key = stdscr.getch()
                
                if key == ord('q') or key == 27:  # Q or ESC
                    break
        finally:
            curses.endwin()
    
    def _draw(self, stdscr):
        """Draw the challenges menu."""
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        # Title
        title = "DAILY CHALLENGES"
        title_x = center_text(title, width)
        stdscr.addstr(1, title_x, title, curses.A_BOLD)
        
        # Streak info
        streak = self.challenge_manager.get_streak()
        best_streak = self.challenge_manager._data.get('best_streak', 0)
        total_points = self.challenge_manager.get_total_points()
        
        y = 3
        stdscr.addstr(y, 5, f"Current Streak: {streak} days", curses.A_BOLD if streak > 0 else curses.A_NORMAL)
        y += 1
        stdscr.addstr(y, 5, f"Best Streak: {best_streak} days")
        y += 1
        stdscr.addstr(y, 5, f"Total Points: {total_points}")
        y += 2
        
        # Today's challenges
        stdscr.addstr(y, 5, "Today's Challenges:", curses.A_BOLD)
        y += 2
        
        challenges = self.challenge_manager.get_daily_challenges(3)
        
        for i, challenge in enumerate(challenges):
            is_completed = self.challenge_manager.is_completed(challenge.id)
            
            # Status indicator
            status = "✓" if is_completed else "○"
            attr = curses.A_BOLD if is_completed else curses.A_NORMAL
            
            # Challenge info
            line1 = f"{status} {challenge.name} ({challenge.game_name.title()})"
            line2 = f"   {challenge.description}"
            line3 = f"   Reward: {challenge.reward_points} points"
            
            stdscr.addstr(y, 5, line1, attr)
            y += 1
            stdscr.addstr(y, 5, line2, attr if not is_completed else curses.A_DIM)
            y += 1
            stdscr.addstr(y, 5, line3, curses.A_DIM)
            y += 2
        
        # Completion stats
        y = height - 8
        completion_rate = self.challenge_manager.get_completion_rate()
        stdscr.addstr(y, 5, "Statistics:", curses.A_BOLD)
        y += 1
        stdscr.addstr(y, 5, f"Overall Completion Rate: {completion_rate:.1f}%")
        y += 1
        total_days = len(self.challenge_manager._data['completions'])
        stdscr.addstr(y, 5, f"Days Participated: {total_days}")
        
        # Instructions
        inst_text = "Q: Back to Menu"
        inst_x = center_text(inst_text, width)
        stdscr.addstr(height - 2, inst_x, inst_text, curses.A_DIM)
        
        # Tip
        tip = "Complete challenges by playing the games and meeting their goals!"
        tip_x = center_text(tip, width)
        stdscr.addstr(height - 4, tip_x, tip, curses.A_DIM)
        
        stdscr.refresh()

