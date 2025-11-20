"""Achievement gallery menu."""

import curses
from typing import List, Dict
from utils.achievements import AchievementManager, AchievementCategory


class AchievementsMenu:
    """Menu for viewing achievements."""
    
    def __init__(self):
        self.achievements = AchievementManager()
        self.current_category = None  # None = all categories
        self.scroll_offset = 0
        self.categories = [None] + list(AchievementCategory)
        self.category_index = 0
    
    def run(self):
        """Run the achievements menu."""
        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.timeout(100)
        
        try:
            while True:
                height, width = stdscr.getmaxyx()
                
                key = stdscr.getch()
                
                if key == ord('q') or key == 27:  # Q or ESC
                    break
                elif key == curses.KEY_UP:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif key == curses.KEY_DOWN:
                    self.scroll_offset += 1
                elif key == curses.KEY_LEFT:
                    self.category_index = max(0, self.category_index - 1)
                    self.current_category = self.categories[self.category_index]
                    self.scroll_offset = 0
                elif key == curses.KEY_RIGHT:
                    self.category_index = min(len(self.categories) - 1, self.category_index + 1)
                    self.current_category = self.categories[self.category_index]
                    self.scroll_offset = 0
                
                self._draw(stdscr, height, width)
        finally:
            curses.endwin()
    
    def _draw(self, stdscr, height, width):
        """Draw the achievements menu."""
        stdscr.clear()
        
        # Title
        title = "ACHIEVEMENTS"
        title_x = (width - len(title)) // 2
        stdscr.addstr(0, title_x, title, curses.A_BOLD)
        
        # Category selector
        category_name = "All" if self.current_category is None else self.current_category.value
        cat_text = f"Category: {category_name} (← → to change)"
        stdscr.addstr(1, (width - len(cat_text)) // 2, cat_text)
        
        # Stats
        unlocked = self.achievements.get_unlocked_achievements()
        total = len(self.achievements.get_all_achievements())
        total_points = self.achievements.get_total_points()
        stats_text = f"Unlocked: {len(unlocked)}/{total} | Total Points: {total_points}"
        stdscr.addstr(2, (width - len(stats_text)) // 2, stats_text)
        
        # Get achievements to display
        if self.current_category is None:
            achievements_list = list(self.achievements.get_all_achievements().values())
        else:
            achievements_list = self.achievements.get_achievements_by_category(self.current_category)
        
        # Sort: unlocked first, then by category
        unlocked_ids = set(unlocked.keys())
        achievements_list.sort(key=lambda a: (
            a.id not in unlocked_ids,  # Unlocked first
            a.category.value,
            a.name
        ))
        
        # Display achievements
        start_y = 4
        max_display = height - start_y - 3
        visible_achievements = achievements_list[self.scroll_offset:self.scroll_offset + max_display]
        
        for i, achievement in enumerate(visible_achievements):
            y = start_y + i
            if y >= height - 2:
                break
            
            is_unlocked = achievement.id in unlocked_ids
            attr = curses.A_BOLD if is_unlocked else curses.A_DIM
            
            # Icon and status
            if is_unlocked:
                status = "✓"
                unlock_data = unlocked[achievement.id]
                date_str = unlock_data.get('unlocked_at', '')[:10]  # Just date
                status_text = f"{status} {achievement.icon} {achievement.name}"
            else:
                status = " "
                status_text = f"{status} ? {achievement.name}"
            
            # Truncate if too long
            max_name_len = width - 50
            if len(status_text) > max_name_len:
                status_text = status_text[:max_name_len-3] + "..."
            
            stdscr.addstr(y, 2, status_text, attr)
            
            # Description
            desc = achievement.description
            if len(desc) > width - 25:
                desc = desc[:width-28] + "..."
            
            if is_unlocked:
                stdscr.addstr(y, width - len(desc) - 20, desc)
                points_text = f"{unlock_data.get('points', 0)} pts"
                stdscr.addstr(y, width - len(points_text) - 2, points_text, curses.A_BOLD)
            else:
                stdscr.addstr(y, width - len(desc) - 20, desc, curses.A_DIM)
        
        # Scroll indicator
        if len(achievements_list) > max_display:
            scroll_text = f"Showing {self.scroll_offset + 1}-{min(self.scroll_offset + max_display, len(achievements_list))} of {len(achievements_list)} (↑↓ to scroll)"
            stdscr.addstr(height - 2, (width - len(scroll_text)) // 2, scroll_text, curses.A_DIM)
        
        # Instructions
        instructions = "Q: Quit | ← →: Change Category | ↑ ↓: Scroll"
        stdscr.addstr(height - 1, (width - len(instructions)) // 2, instructions, curses.A_DIM)
        
        stdscr.refresh()

