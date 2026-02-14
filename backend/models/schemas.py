"""
Pydantic Schemas - Data Validation Models

This module defines Pydantic models that handle data validation and serialization
throughout the application. Pydantic automatically validates incoming data and
provides clear error messages if the data doesn't match the expected format.

These schemas serve three main purposes:
1. Request validation - Ensure incoming API requests have the correct structure
2. Response formatting - Define the structure of API responses
3. Type safety - Provide type hints for better IDE support and fewer bugs
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


# ============================================================================
# LEAD MODELS - For managing lead data from external CRM/API
# ============================================================================

class Lead(BaseModel):
    """
    Lead model representing a potential customer from external API
    
    This model is used when fetching leads from the external CRM system
    (currently using JSONPlaceholder as a demo API). It contains the
    essential contact information for each lead.
    
    Attributes:
        name (str): Full name of the lead
        email (EmailStr): Email address (automatically validated by Pydantic)
        phone (str): Phone number in any format
    """
    name: str
    email: EmailStr  # EmailStr automatically validates email format
    phone: str


# ============================================================================
# NOTE MODELS - For creating and managing notes attached to leads
# ============================================================================

class NoteCreate(BaseModel):
    """
    Request model for creating a new note
    
    When a user creates a note for a lead, the frontend sends this data.
    The email links the note to a specific lead, and the note contains
    the actual text content.
    
    Attributes:
        email (EmailStr): Email of the lead this note is associated with
        note (str): The actual note content written by the user
    """
    email: EmailStr
    note: str


class NoteResponse(BaseModel):
    """
    Response model for note with AI-generated summary
    
    After creating a note, the API returns this model which includes
    the original note plus an AI-generated summary. This is what the
    frontend receives and displays to the user.
    
    Attributes:
        email (EmailStr): Email of the lead this note belongs to
        note (str): The original note text
        summary (Optional[str]): AI-generated summary (max 20 words), may be None if AI fails
    """
    email: EmailStr
    note: str
    summary: Optional[str] = None  # Optional in case AI service is unavailable


# ============================================================================
# AI SUMMARY MODELS - For standalone summary generation
# ============================================================================

class SummaryRequest(BaseModel):
    """
    Request model for generating an AI summary
    
    This is used when you want to generate a summary without saving a note.
    Useful for testing the AI service or previewing summaries before saving.
    
    Attributes:
        note (str): The text to summarize
    """
    note: str


class SummaryResponse(BaseModel):
    """
    Response model for AI-generated summary
    
    Returns just the summary text, typically a concise version of the
    original note (maximum 20 words).
    
    Attributes:
        summary (str): The AI-generated summary text
    """
    summary: str
