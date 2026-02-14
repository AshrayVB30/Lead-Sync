"""
AI Service for generating note summaries using Ollama.

This module provides an abstraction layer for AI-powered summary generation.
The implementation uses Ollama for local LLM inference.
"""

import httpx
from typing import Optional


# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi3:mini"  # Using phi3:mini (2.2GB) - better for limited memory


async def generate_summary(note: str) -> str:
    """
    Generate a concise summary of the given note using Ollama.
    
    Args:
        note: The note text to summarize
    
    Returns:
        A summary of maximum 20 words
    
    Raises:
        Exception: If Ollama API call fails
    """
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:  # Longer timeout for model loading
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": f"Summarize in max 20 words: {note}",
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_predict": 30
                    }
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get("response", "").strip()
                
                # Clean up the summary
                # Remove common prefixes that LLMs sometimes add
                prefixes_to_remove = [
                    "Summary:", "Concise summary:", "Here's a summary:",
                    "Here is a summary:", "The summary is:"
                ]
                for prefix in prefixes_to_remove:
                    if summary.lower().startswith(prefix.lower()):
                        summary = summary[len(prefix):].strip()
                
                # Remove quotes if the entire summary is quoted
                if summary.startswith('"') and summary.endswith('"'):
                    summary = summary[1:-1].strip()
                if summary.startswith("'") and summary.endswith("'"):
                    summary = summary[1:-1].strip()
                
                # Ensure summary doesn't exceed 20 words
                words = summary.split()
                if len(words) > 20:
                    # Try to cut at a natural boundary (comma, semicolon, etc.)
                    truncated = ' '.join(words[:20])
                    # Remove trailing punctuation that might be incomplete
                    truncated = truncated.rstrip(',-;:')
                    summary = truncated + '.'
                elif len(words) > 0 and not summary[-1] in '.!?':
                    # Add period if missing
                    summary = summary + '.'
                
                return summary if summary and len(words) >= 3 else _fallback_summary(note)
            else:
                # Fallback to simple truncation if Ollama fails
                return _fallback_summary(note)
                
    except Exception as e:
        print(f"Ollama API error: {e}")
        # Fallback to simple truncation if Ollama is not available
        return _fallback_summary(note)


def _fallback_summary(note: str) -> str:
    """
    Fallback summary generation when Ollama is unavailable.
    
    Args:
        note: The note text to summarize
    
    Returns:
        A simple truncated summary
    """
    words = note.split()
    
    if len(words) <= 20:
        return note
    
    # Take first 20 words
    summary = ' '.join(words[:20])
    
    # Try to end at a sentence boundary if possible
    if '.' in summary:
        summary = summary.split('.')[0] + '.'
    else:
        summary += '...'
    
    return summary
