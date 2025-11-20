"""Theme system for visual customization."""

from typing import Dict, Optional
from enum import Enum


class ThemeStyle(Enum):
    """Theme style categories."""
    CLASSIC = "Classic"
    DARK = "Dark"
    NEON = "Neon"
    RETRO = "Retro"
    MINIMAL = "Minimal"


class Theme:
    """Represents a visual theme."""
    
    def __init__(self, theme_id: str, name: str, style: ThemeStyle,
                 border_chars: Dict[str, str] = None,
                 colors: Dict[str, int] = None,
                 description: str = ""):
        """Initialize a theme.
        
        Args:
            theme_id: Unique identifier
            name: Display name
            style: Theme style category
            border_chars: Dictionary of border characters
            colors: Dictionary of color pairs (for future use)
            description: Theme description
        """
        self.id = theme_id
        self.name = name
        self.style = style
        self.description = description
        
        # Default border characters
        default_borders = {
            'horizontal': '─',
            'vertical': '│',
            'corner_tl': '┌',
            'corner_tr': '┐',
            'corner_bl': '└',
            'corner_br': '┘',
            'cross': '┼',
            't_up': '┬',
            't_down': '┴',
            't_left': '├',
            't_right': '┤',
        }
        
        self.border_chars = border_chars or default_borders.copy()
        self.colors = colors or {}
    
    def get_border(self, key: str, default: str = ' ') -> str:
        """Get a border character.
        
        Args:
            key: Border character key
            default: Default if not found
            
        Returns:
            Border character
        """
        return self.border_chars.get(key, default)


class ThemeManager:
    """Manages themes and theme selection."""
    
    def __init__(self):
        """Initialize the theme manager."""
        self._themes = self._define_themes()
        self._current_theme_id = 'classic'
    
    def _define_themes(self) -> Dict[str, Theme]:
        """Define all available themes."""
        themes = {}
        
        # Classic theme (default)
        themes['classic'] = Theme(
            'classic', 'Classic', ThemeStyle.CLASSIC,
            description="Traditional terminal look with standard borders"
        )
        
        # Dark theme
        themes['dark'] = Theme(
            'dark', 'Dark', ThemeStyle.DARK,
            border_chars={
                'horizontal': '═',
                'vertical': '║',
                'corner_tl': '╔',
                'corner_tr': '╗',
                'corner_bl': '╚',
                'corner_br': '╝',
                'cross': '╬',
                't_up': '╦',
                't_down': '╩',
                't_left': '╠',
                't_right': '╣',
            },
            description="Bold double-line borders for a dark aesthetic"
        )
        
        # Neon theme
        themes['neon'] = Theme(
            'neon', 'Neon', ThemeStyle.NEON,
            border_chars={
                'horizontal': '━',
                'vertical': '┃',
                'corner_tl': '┏',
                'corner_tr': '┓',
                'corner_bl': '┗',
                'corner_br': '┛',
                'cross': '╋',
                't_up': '┳',
                't_down': '┻',
                't_left': '┣',
                't_right': '┫',
            },
            description="Heavy borders with a futuristic feel"
        )
        
        # Retro theme
        themes['retro'] = Theme(
            'retro', 'Retro', ThemeStyle.RETRO,
            border_chars={
                'horizontal': '-',
                'vertical': '|',
                'corner_tl': '+',
                'corner_tr': '+',
                'corner_bl': '+',
                'corner_br': '+',
                'cross': '+',
                't_up': '+',
                't_down': '+',
                't_left': '+',
                't_right': '+',
            },
            description="Simple ASCII borders for a retro computing feel"
        )
        
        # Minimal theme
        themes['minimal'] = Theme(
            'minimal', 'Minimal', ThemeStyle.MINIMAL,
            border_chars={
                'horizontal': ' ',
                'vertical': ' ',
                'corner_tl': ' ',
                'corner_tr': ' ',
                'corner_bl': ' ',
                'corner_br': ' ',
                'cross': ' ',
                't_up': ' ',
                't_down': ' ',
                't_left': ' ',
                't_right': ' ',
            },
            description="No borders for a clean, minimal look"
        )
        
        return themes
    
    def get_theme(self, theme_id: Optional[str] = None) -> Theme:
        """Get a theme by ID, or current theme if None.
        
        Args:
            theme_id: Theme ID, or None for current theme
            
        Returns:
            Theme object
        """
        if theme_id is None:
            theme_id = self._current_theme_id
        return self._themes.get(theme_id, self._themes['classic'])
    
    def set_theme(self, theme_id: str):
        """Set the current theme.
        
        Args:
            theme_id: Theme ID to set
        """
        if theme_id in self._themes:
            self._current_theme_id = theme_id
    
    def get_current_theme(self) -> Theme:
        """Get the current theme.
        
        Returns:
            Current theme
        """
        return self.get_theme()
    
    def get_all_themes(self) -> Dict[str, Theme]:
        """Get all available themes.
        
        Returns:
            Dictionary of all themes
        """
        return self._themes.copy()
    
    def get_themes_by_style(self, style: ThemeStyle) -> Dict[str, Theme]:
        """Get themes by style.
        
        Args:
            style: Theme style
            
        Returns:
            Dictionary of themes with that style
        """
        return {tid: theme for tid, theme in self._themes.items() 
                if theme.style == style}

