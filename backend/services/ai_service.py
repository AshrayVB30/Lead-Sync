"""
AI Service - Ollama-Powered Summary Generation

This module provides AI-powered text summarization using Ollama, a local LLM
(Large Language Model) runtime. It generates concise summaries of notes with
a maximum length of 20 words.

Key Features:
- Uses phi3:mini model (2.2GB) for memory efficiency
- Automatic response cleaning (removes LLM artifacts)
- Word count enforcement (max 20 words)
- Graceful fallback when Ollama is unavailable
- Async operation for non-blocking performance

Ollama Setup:
Before using this service, you must:
1. Install Ollama: https://ollama.ai
2. Pull the model: ollama pull phi3:mini
3. Ensure Ollama is running on localhost:11434
"""

import httpx
from typing import Optional


# ============================================================================
# OLLAMA CONFIGURATION
# ============================================================================

# Base URL for Ollama API - should be running locally
OLLAMA_BASE_URL = "http://localhost:11434"

# Model selection: phi3:mini is chosen for its balance of quality and size
# - Size: 2.2GB (fits in most systems with 8GB RAM)
# - Speed: Fast inference on CPU
# - Quality: Good for summarization tasks
# Alternative models: llama2, mistral, codellama (see Ollama docs)
OLLAMA_MODEL = "phi3:mini"


async def generate_summary(note: str) -> str:
    """
    Generate a concise AI summary of the given note using Ollama
    
    This function sends the note to Ollama's local LLM and processes the response
    to ensure it meets our requirements (max 20 words, clean formatting).
    
    The process:
    1. Send note to Ollama with a specific prompt
    2. Wait for AI to generate summary (1-3 seconds typically)
    3. Clean up the response (remove common LLM artifacts)
    4. Enforce 20-word limit
    5. Add proper punctuation
    6. Return summary or fallback if quality is poor
    
    Args:
        note (str): The note text to summarize (can be any length)
    
    Returns:
        str: A clean, concise summary of maximum 20 words
    
    Raises:
        Exception: If Ollama API call fails (caught internally, returns fallback)
        
    Example:
        Input: "Met with client today. They're interested in our premium package 
                with 50 user licenses. Need to send proposal by Friday. Budget 
                approved for $5000/month."
        Output: "Client interested in premium package, 50 licenses, $5000/month. 
                 Send proposal by Friday."
    """
    
    try:
        # Create async HTTP client with extended timeout
        # Timeout is 60s because first request may need to load the model into memory
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Make POST request to Ollama's generate endpoint
            response = await client.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    
                    # Prompt engineering: Clear, specific instruction
                    # The "max 20 words" constraint is crucial for concise output
                    "prompt": f"Summarize in max 20 words: {note}",
                    
                    # stream=False means we wait for complete response
                    # (streaming would give us partial responses as they're generated)
                    "stream": False,
                    
                    # Model parameters for better summarization
                    "options": {
                        # Low temperature (0.1) = more focused, deterministic output
                        # High temperature (1.0) = more creative, varied output
                        "temperature": 0.1,
                        
                        # num_predict limits the number of tokens generated
                        # 30 tokens ≈ 20-25 words (with some buffer)
                        "num_predict": 30
                    }
                }
            )
            
            # Check if Ollama responded successfully
            if response.status_code == 200:
                result = response.json()
                summary = result.get("response", "").strip()
                
                # ============================================================
                # RESPONSE CLEANING PHASE
                # ============================================================
                # LLMs sometimes add prefixes like "Summary:" or "Here's a summary:"
                # We remove these to get just the actual summary content
                
                prefixes_to_remove = [
                    "Summary:", "Concise summary:", "Here's a summary:",
                    "Here is a summary:", "The summary is:"
                ]
                for prefix in prefixes_to_remove:
                    if summary.lower().startswith(prefix.lower()):
                        summary = summary[len(prefix):].strip()
                
                # Remove surrounding quotes if the entire summary is quoted
                # LLMs sometimes wrap responses in quotes
                if summary.startswith('"') and summary.endswith('"'):
                    summary = summary[1:-1].strip()
                if summary.startswith("'") and summary.endswith("'"):
                    summary = summary[1:-1].strip()
                
                # ============================================================
                # WORD COUNT ENFORCEMENT
                # ============================================================
                # Ensure summary doesn't exceed 20 words
                
                words = summary.split()
                if len(words) > 20:
                    # Truncate to 20 words
                    truncated = ' '.join(words[:20])
                    
                    # Remove trailing punctuation that might be incomplete
                    # (e.g., if we cut off mid-sentence)
                    truncated = truncated.rstrip(',-;:')
                    
                    # Add period to make it a complete sentence
                    summary = truncated + '.'
                    
                elif len(words) > 0 and not summary[-1] in '.!?':
                    # If summary is under 20 words but missing ending punctuation, add period
                    summary = summary + '.'
                
                # Quality check: If summary is too short (< 3 words) or empty,
                # use fallback instead (likely means AI failed to generate good output)
                return summary if summary and len(words) >= 3 else _fallback_summary(note)
            else:
                # Ollama returned an error status code
                # Fall back to simple truncation
                return _fallback_summary(note)
                
    except Exception as e:
        # Catch any errors (network issues, Ollama not running, etc.)
        print(f"Ollama API error: {e}")
        
        # Gracefully degrade to fallback summary
        # This ensures the app keeps working even if AI is unavailable
        return _fallback_summary(note)


def _fallback_summary(note: str) -> str:
    """
    Fallback summary generation when Ollama is unavailable
    
    This is a simple, non-AI approach that just truncates the note to 20 words.
    It's not as intelligent as AI summarization, but ensures the app remains
    functional even when Ollama is down or not installed.
    
    The fallback tries to be smart about truncation:
    - If note is already short (≤20 words), return as-is
    - Otherwise, take first 20 words
    - Try to end at a sentence boundary if possible
    - Add "..." to indicate truncation
    
    Args:
        note (str): The note text to summarize
    
    Returns:
        str: A simple truncated summary
        
    Example:
        Input: "This is a very long note with many sentences. It goes on and on..."
        Output: "This is a very long note with many sentences..."
    """
    words = note.split()
    
    # If note is already short enough, return it unchanged
    if len(words) <= 20:
        return note
    
    # Take first 20 words
    summary = ' '.join(words[:20])
    
    # Try to end at a sentence boundary if there's a period in the first 20 words
    # This makes the summary feel more natural
    if '.' in summary:
        summary = summary.split('.')[0] + '.'
    else:
        # No sentence boundary found, just add ellipsis to show truncation
        summary += '...'
    
    return summary
