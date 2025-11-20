"""Save and load game state system."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class SaveManager:
    """Manages saving and loading game states."""
    
    MAX_SAVES_PER_GAME = 5
    
    def __init__(self, data_dir: str = "data"):
        """Initialize the save manager.
        
        Args:
            data_dir: Directory to store save files
        """
        self.data_dir = Path(data_dir)
        self.saves_dir = self.data_dir / "saves"
        self.saves_dir.mkdir(parents=True, exist_ok=True)
    
    def get_save_path(self, game_name: str, slot: int) -> Path:
        """Get the save file path for a game and slot.
        
        Args:
            game_name: Name of the game
            slot: Save slot number (1-5)
            
        Returns:
            Path to save file
        """
        return self.saves_dir / f"{game_name}_slot{slot}.json"
    
    def save_game(self, game_name: str, slot: int, game_state: Dict[str, Any],
                  metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Save game state to a slot.
        
        Args:
            game_name: Name of the game
            slot: Save slot number (1-5)
            game_state: Game state dictionary
            metadata: Optional metadata (score, progress, etc.)
            
        Returns:
            True if save was successful
        """
        if slot < 1 or slot > self.MAX_SAVES_PER_GAME:
            return False
        
        try:
            save_data = {
                'game_name': game_name,
                'slot': slot,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata or {},
                'game_state': game_state
            }
            
            save_path = self.get_save_path(game_name, slot)
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return True
        except (IOError, TypeError) as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, game_name: str, slot: int) -> Optional[Dict[str, Any]]:
        """Load game state from a slot.
        
        Args:
            game_name: Name of the game
            slot: Save slot number (1-5)
            
        Returns:
            Save data dictionary or None if not found
        """
        if slot < 1 or slot > self.MAX_SAVES_PER_GAME:
            return None
        
        try:
            save_path = self.get_save_path(game_name, slot)
            if not save_path.exists():
                return None
            
            with open(save_path, 'r') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading game: {e}")
            return None
    
    def delete_save(self, game_name: str, slot: int) -> bool:
        """Delete a save file.
        
        Args:
            game_name: Name of the game
            slot: Save slot number (1-5)
            
        Returns:
            True if deletion was successful
        """
        if slot < 1 or slot > self.MAX_SAVES_PER_GAME:
            return False
        
        try:
            save_path = self.get_save_path(game_name, slot)
            if save_path.exists():
                save_path.unlink()
            return True
        except IOError as e:
            print(f"Error deleting save: {e}")
            return False
    
    def get_save_list(self, game_name: str) -> List[Dict[str, Any]]:
        """Get list of all saves for a game.
        
        Args:
            game_name: Name of the game
            
        Returns:
            List of save metadata (without full game state)
        """
        saves = []
        for slot in range(1, self.MAX_SAVES_PER_GAME + 1):
            save_data = self.load_game(game_name, slot)
            if save_data:
                # Return metadata only (not full game state)
                saves.append({
                    'slot': slot,
                    'timestamp': save_data.get('timestamp'),
                    'metadata': save_data.get('metadata', {}),
                    'exists': True
                })
            else:
                saves.append({
                    'slot': slot,
                    'timestamp': None,
                    'metadata': {},
                    'exists': False
                })
        return saves
    
    def has_save(self, game_name: str, slot: int) -> bool:
        """Check if a save exists.
        
        Args:
            game_name: Name of the game
            slot: Save slot number (1-5)
            
        Returns:
            True if save exists
        """
        save_path = self.get_save_path(game_name, slot)
        return save_path.exists()
    
    def get_all_saves(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all saves for all games.
        
        Returns:
            Dictionary mapping game names to their save lists
        """
        all_saves = {}
        
        # Scan saves directory
        if self.saves_dir.exists():
            for save_file in self.saves_dir.glob("*_slot*.json"):
                try:
                    with open(save_file, 'r') as f:
                        save_data = json.load(f)
                        game_name = save_data.get('game_name')
                        if game_name:
                            if game_name not in all_saves:
                                all_saves[game_name] = []
                            all_saves[game_name].append({
                                'slot': save_data.get('slot'),
                                'timestamp': save_data.get('timestamp'),
                                'metadata': save_data.get('metadata', {})
                            })
                except (IOError, json.JSONDecodeError):
                    pass
        
        return all_saves
    
    def format_timestamp(self, iso_timestamp: str) -> str:
        """Format timestamp for display.
        
        Args:
            iso_timestamp: ISO format timestamp
            
        Returns:
            Formatted date/time string
        """
        try:
            dt = datetime.fromisoformat(iso_timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except (ValueError, AttributeError):
            return "Unknown"
    
    def auto_save(self, game_name: str, game_state: Dict[str, Any],
                  metadata: Optional[Dict[str, Any]] = None) -> bool:
        """Auto-save to slot 1 (quick save slot).
        
        Args:
            game_name: Name of the game
            game_state: Game state dictionary
            metadata: Optional metadata
            
        Returns:
            True if save was successful
        """
        return self.save_game(game_name, 1, game_state, metadata)

