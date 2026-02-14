from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import Lead
from services.leads_service import fetch_leads


router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=List[Lead])
async def get_leads():
    """
    Fetch leads from external API.
    
    Returns cleaned list of leads with name, email, and phone.
    """
    try:
        leads = await fetch_leads()
        return leads
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch leads: {str(e)}")
