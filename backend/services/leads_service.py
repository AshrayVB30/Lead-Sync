import httpx
from typing import List
from models.schemas import Lead


LEADS_API_URL = "https://jsonplaceholder.typicode.com/users"


async def fetch_leads() -> List[Lead]:
    """
    Fetch leads from external API and extract relevant fields.
    
    Returns:
        List of Lead objects with name, email, and phone
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(LEADS_API_URL)
        response.raise_for_status()
        users = response.json()
    
    # Extract only the fields we need
    leads = []
    for user in users:
        lead = Lead(
            name=user.get("name", ""),
            email=user.get("email", ""),
            phone=user.get("phone", "")
        )
        leads.append(lead)
    
    return leads
