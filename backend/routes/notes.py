"""
Notes Router - API Endpoints for Note Management and AI Summaries

This module handles all note-related operations including:
- Creating notes for leads with automatic AI summary generation
- Standalone AI summary generation for testing/preview purposes

Each note is linked to a lead via email address and stored in JSON format.
The AI service (Ollama) automatically generates concise summaries.
"""

# Import FastAPI components for routing and error handling
from fastapi import APIRouter, HTTPException

# Import our data models for request/response validation
from models.schemas import NoteCreate, NoteResponse, SummaryRequest, SummaryResponse

# Import storage and AI service modules
from storage.json_store import store  # Handles persistent storage in JSON file
from services.ai_service import generate_summary  # Generates AI summaries using Ollama


# Create a router without a prefix (routes defined with full paths)
# Tags help organize endpoints in the auto-generated API documentation
router = APIRouter(tags=["notes"])


@router.post("/notes", response_model=NoteResponse)
async def create_note(note_data: NoteCreate):
    """
    Create a new note for a lead with automatic AI summary generation
    
    This is the main endpoint for creating notes. It performs three operations:
    1. Receives the note text and associated lead email from the frontend
    2. Generates an AI-powered summary using Ollama (max 20 words)
    3. Saves both the original note and summary to persistent storage
    
    The workflow is fully automated - users just write notes and get summaries
    automatically without any additional steps.
    
    Args:
        note_data (NoteCreate): Contains email (lead identifier) and note text
        
    Returns:
        NoteResponse: The created note with email, original text, and AI summary
        
    Raises:
        HTTPException: 500 error if AI service fails or storage fails
        
    Example request:
        {
            "email": "john@example.com",
            "note": "Called customer, interested in premium plan. Follow up next week."
        }
        
    Example response:
        {
            "email": "john@example.com",
            "note": "Called customer, interested in premium plan. Follow up next week.",
            "summary": "Customer interested in premium plan, schedule follow-up next week."
        }
    """
    try:
        # Step 1: Generate AI summary using Ollama
        # This is an async operation that may take 1-3 seconds depending on model
        summary = await generate_summary(note_data.note)
        
        # Step 2: Save to persistent storage (JSON file)
        # The store uses email as the key, so each lead can have one note
        # (In production, you might want to support multiple notes per lead)
        store.save_note(
            email=note_data.email,
            note=note_data.note,
            summary=summary
        )
        
        # Step 3: Return the complete note data to the frontend
        return NoteResponse(
            email=note_data.email,
            note=note_data.note,
            summary=summary
        )
    except Exception as e:
        # If anything fails (AI service down, storage error, etc.), return 500
        # The error message helps with debugging but shouldn't expose sensitive info
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to create note: {str(e)}"
        )


@router.post("/summary", response_model=SummaryResponse)
async def create_summary(request: SummaryRequest):
    """
    Generate an AI summary for a given note (without saving)
    
    This endpoint is useful for:
    - Testing the AI service independently
    - Previewing summaries before saving a note
    - Debugging summary quality issues
    
    Unlike /notes, this endpoint ONLY generates a summary and doesn't persist
    anything to storage. It's a lightweight way to test the AI functionality.
    
    Args:
        request (SummaryRequest): Contains the note text to summarize
        
    Returns:
        SummaryResponse: Just the AI-generated summary (max 20 words)
        
    Raises:
        HTTPException: 500 error if AI service fails
        
    Example request:
        {
            "note": "Customer wants to upgrade to enterprise plan with 100 users"
        }
        
    Example response:
        {
            "summary": "Customer requests enterprise plan upgrade for 100 users."
        }
    """
    try:
        # Generate summary using the AI service
        summary = await generate_summary(request.note)
        return SummaryResponse(summary=summary)
    except Exception as e:
        # Return error if AI service is unavailable or fails
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate summary: {str(e)}"
        )
