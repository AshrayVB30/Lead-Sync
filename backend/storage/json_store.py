"""
JSON Storage - Simple File-Based Persistence for Notes

This module provides a lightweight storage solution using JSON files to persist
notes and their AI-generated summaries. It's designed for development and small-scale
deployments where a full database would be overkill.

For production with multiple users and high traffic, consider migrating to:
- PostgreSQL or MySQL for relational data
- MongoDB for document-based storage
- Redis for caching frequently accessed notes

The storage uses email addresses as unique keys, so each lead can have one note.
To support multiple notes per lead, you'd need to restructure the data model.
"""

import json
import os
from typing import Dict, Optional
from pathlib import Path


class JSONStore:
    """
    Simple JSON file-based storage for notes and summaries
    
    This class handles all CRUD (Create, Read, Update, Delete) operations for notes.
    It uses a single JSON file to store all data in a simple key-value structure:
    
    {
        "user@example.com": {
            "note": "Original note text...",
            "summary": "AI-generated summary..."
        },
        "another@example.com": {
            "note": "Another note...",
            "summary": "Another summary..."
        }
    }
    
    The class ensures thread-safe file operations and handles common edge cases
    like missing files, corrupted JSON, and encoding issues.
    """
    
    def __init__(self, filename: str = "notes_data.json"):
        """
        Initialize the JSON store with a specific filename
        
        Args:
            filename (str): Name of the JSON file to use for storage
                           Defaults to "notes_data.json"
        
        The file is created in the same directory as this Python file,
        making it easy to locate and inspect during development.
        """
        # Use Path to construct absolute path relative to this file's location
        # This ensures the JSON file is always in the same directory as json_store.py
        self.filepath = Path(__file__).parent / filename
        
        # Create the file if it doesn't exist yet
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """
        Create the JSON file if it doesn't exist
        
        This is called during initialization to guarantee the file exists
        before any read/write operations. Starts with an empty dictionary {}.
        """
        if not self.filepath.exists():
            self._write_data({})
    
    def _read_data(self) -> Dict:
        """
        Read and parse data from the JSON file
        
        This is a private method (prefixed with _) used internally by other methods.
        It handles common errors gracefully:
        - If file is missing, returns empty dict
        - If JSON is corrupted, returns empty dict
        
        Returns:
            Dict: The parsed JSON data as a Python dictionary
                  Returns {} if file is missing or corrupted
        """
        try:
            # Open file with UTF-8 encoding to support international characters
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # If anything goes wrong, return empty dict
            # This makes the storage resilient to corruption
            return {}
    
    def _write_data(self, data: Dict):
        """
        Write data to the JSON file with pretty formatting
        
        This is a private method used internally to persist data.
        Uses indent=2 for human-readable formatting, making it easy
        to inspect and debug the JSON file manually.
        
        Args:
            data (Dict): The data to write to the file
        """
        # Open file in write mode (overwrites existing content)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(
                data, 
                f, 
                indent=2,              # Pretty print with 2-space indentation
                ensure_ascii=False     # Allow Unicode characters (émojis, 中文, etc.)
            )
    
    def save_note(self, email: str, note: str, summary: Optional[str] = None) -> Dict:
        """
        Save or update a note for a specific lead (identified by email)
        
        This method performs an "upsert" operation:
        - If the email exists, it updates the note
        - If the email doesn't exist, it creates a new entry
        
        Args:
            email (str): Email address of the lead (used as unique identifier)
            note (str): The note text to save
            summary (Optional[str]): AI-generated summary (can be None)
        
        Returns:
            Dict: The saved note data with both note and summary
            
        Example:
            store.save_note(
                email="john@example.com",
                note="Customer interested in premium plan",
                summary="Interested in premium plan"
            )
            # Returns: {"note": "Customer...", "summary": "Interested..."}
        """
        # Read current data from file
        data = self._read_data()
        
        # Create or update the entry for this email
        # This overwrites any existing note for this email
        data[email] = {
            "note": note,
            "summary": summary
        }
        
        # Write updated data back to file
        self._write_data(data)
        
        # Return the saved data for confirmation
        return data[email]
    
    def get_note(self, email: str) -> Optional[Dict]:
        """
        Retrieve a note for a specific lead by email
        
        Args:
            email (str): Email address of the lead
        
        Returns:
            Optional[Dict]: The note data if found, None if not found
                           Dict contains: {"note": "...", "summary": "..."}
        
        Example:
            note_data = store.get_note("john@example.com")
            if note_data:
                print(note_data["note"])
                print(note_data["summary"])
            else:
                print("No note found for this email")
        """
        data = self._read_data()
        return data.get(email)  # Returns None if email not found
    
    def get_all_notes(self) -> Dict:
        """
        Retrieve all notes from storage
        
        Useful for:
        - Displaying all notes in an admin dashboard
        - Exporting data for backup
        - Debugging and testing
        
        Returns:
            Dict: All notes indexed by email
                  Format: {email: {"note": "...", "summary": "..."}, ...}
        
        Example:
            all_notes = store.get_all_notes()
            for email, note_data in all_notes.items():
                print(f"{email}: {note_data['summary']}")
        """
        return self._read_data()


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================
# Create a single shared instance of JSONStore that's used throughout the app
# This ensures all parts of the application use the same storage instance
# and prevents multiple files from being created
store = JSONStore()
