from pydantic import BaseModel, EmailStr
from typing import Optional


class Lead(BaseModel):
    """Lead model from external API"""
    name: str
    email: EmailStr
    phone: str


class NoteCreate(BaseModel):
    """Request model for creating a note"""
    email: EmailStr
    note: str


class NoteResponse(BaseModel):
    """Response model for note with summary"""
    email: EmailStr
    note: str
    summary: Optional[str] = None


class SummaryRequest(BaseModel):
    """Request model for generating summary"""
    note: str


class SummaryResponse(BaseModel):
    """Response model for summary"""
    summary: str
