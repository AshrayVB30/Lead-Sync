import json
import os
from typing import Dict, Optional
from pathlib import Path


class JSONStore:
    """Simple JSON file-based storage for notes"""
    
    def __init__(self, filename: str = "notes_data.json"):
        self.filepath = Path(__file__).parent / filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create the JSON file if it doesn't exist"""
        if not self.filepath.exists():
            self._write_data({})
    
    def _read_data(self) -> Dict:
        """Read data from JSON file"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_data(self, data: Dict):
        """Write data to JSON file"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_note(self, email: str, note: str, summary: Optional[str] = None) -> Dict:
        """Save a note for a specific email"""
        data = self._read_data()
        
        # Store note with summary
        data[email] = {
            "note": note,
            "summary": summary
        }
        
        self._write_data(data)
        return data[email]
    
    def get_note(self, email: str) -> Optional[Dict]:
        """Retrieve a note for a specific email"""
        data = self._read_data()
        return data.get(email)
    
    def get_all_notes(self) -> Dict:
        """Retrieve all notes"""
        return self._read_data()


# Singleton instance
store = JSONStore()
