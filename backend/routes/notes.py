from fastapi import APIRouter, HTTPException
from models.schemas import NoteCreate, NoteResponse, SummaryRequest, SummaryResponse
from storage.json_store import store
from services.ai_service import generate_summary


router = APIRouter(tags=["notes"])


@router.post("/notes", response_model=NoteResponse)
async def create_note(note_data: NoteCreate):
    """
    Create a new note for a lead.
    
    Automatically generates AI summary and persists both note and summary.
    """
    try:
        # Generate AI summary
        summary = await generate_summary(note_data.note)
        
        # Save to storage
        store.save_note(
            email=note_data.email,
            note=note_data.note,
            summary=summary
        )
        
        return NoteResponse(
            email=note_data.email,
            note=note_data.note,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create note: {str(e)}")


@router.post("/summary", response_model=SummaryResponse)
async def create_summary(request: SummaryRequest):
    """
    Generate AI summary for a given note.
    
    Returns summary with maximum 20 words.
    """
    try:
        summary = await generate_summary(request.note)
        return SummaryResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")
