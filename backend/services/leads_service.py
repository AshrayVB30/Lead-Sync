"""
Leads Service - External API Integration for Lead Fetching

This service module handles the business logic for fetching leads from external
sources. It acts as an abstraction layer between the API routes and external
CRM systems, making it easy to swap out data sources without changing the routes.

Currently uses JSONPlaceholder as a demo API, but in production this would
connect to real CRM systems like Salesforce, HubSpot, or Pipedrive.
"""

# Import HTTP client for making async requests to external APIs
import httpx
from typing import List

# Import our Lead model for type safety and validation
from models.schemas import Lead


# External API endpoint - in production, this would be your CRM API
# JSONPlaceholder provides fake user data that's perfect for demos
LEADS_API_URL = "https://jsonplaceholder.typicode.com/users"


async def fetch_leads() -> List[Lead]:
    """
    Fetch leads from external CRM API and transform to our Lead model
    
    This function performs the following steps:
    1. Makes an HTTP GET request to the external API
    2. Validates the response (raises error if API is down)
    3. Extracts only the fields we need (name, email, phone)
    4. Transforms the data into our standardized Lead model
    
    Using async/await allows the server to handle other requests while
    waiting for the external API to respond, improving overall performance.
    
    Returns:
        List[Lead]: Array of Lead objects with validated email addresses
        
    Raises:
        httpx.HTTPStatusError: If the external API returns an error status
        httpx.RequestError: If the network request fails
        
    Note:
        In production, you might want to add:
        - Caching to reduce API calls
        - Retry logic for failed requests
        - Rate limiting to respect API quotas
        - Pagination for large datasets
    """
    # Create an async HTTP client (automatically closed after the 'async with' block)
    async with httpx.AsyncClient() as client:
        # Make GET request to external API
        response = await client.get(LEADS_API_URL)
        
        # Raise an exception if the response status is 4xx or 5xx
        # This ensures we catch API errors early
        response.raise_for_status()
        
        # Parse JSON response into Python list of dictionaries
        users = response.json()
    
    # Transform external API data into our Lead model
    # We only extract the fields we need, ignoring extra data like address, company, etc.
    leads = []
    for user in users:
        # Create a Lead object - Pydantic will validate the email format
        # If email is invalid, Pydantic will raise a validation error
        lead = Lead(
            name=user.get("name", ""),      # Use .get() with default to handle missing fields
            email=user.get("email", ""),    # EmailStr type ensures valid email format
            phone=user.get("phone", "")     # Phone can be any string format
        )
        leads.append(lead)
    
    return leads
