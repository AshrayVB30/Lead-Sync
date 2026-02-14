"""
Leads Router - API Endpoints for Lead Management

This module handles all API endpoints related to fetching and managing leads.
Currently, it provides a single endpoint to fetch leads from an external API,
but can be extended to include filtering, searching, and pagination.
"""

# Import FastAPI components for routing and error handling
from fastapi import APIRouter, HTTPException
from typing import List

# Import our data models and service functions
from models.schemas import Lead
from services.leads_service import fetch_leads


# Create a router with a prefix and tag for organization
# Prefix: All routes in this file will start with /leads
# Tags: Used to group endpoints in the auto-generated API docs
router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=List[Lead])
async def get_leads():
    """
    Fetch all leads from external CRM/API
    
    This endpoint retrieves leads from an external source (currently JSONPlaceholder
    as a demo API) and returns them in a standardized format. In production, this
    would connect to your actual CRM system (Salesforce, HubSpot, etc.).
    
    The endpoint is async to handle multiple concurrent requests efficiently without
    blocking the server.
    
    Returns:
        List[Lead]: Array of lead objects, each containing name, email, and phone
        
    Raises:
        HTTPException: 500 error if the external API is unreachable or returns invalid data
        
    Example response:
        [
            {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "555-1234"
            },
            ...
        ]
    """
    try:
        # Call the service layer to fetch and process leads
        leads = await fetch_leads()
        return leads
    except Exception as e:
        # If anything goes wrong, return a 500 error with details
        # In production, you might want to log this error to a monitoring service
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to fetch leads: {str(e)}"
        )
