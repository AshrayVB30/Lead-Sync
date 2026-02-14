"""
Lead Sync + AI Notes API - Main Application Entry Point

This is the main FastAPI application that serves as the backend for the Lead Sync system.
It provides endpoints for:
- Fetching leads from external APIs
- Creating and managing notes for leads
- Generating AI-powered summaries of notes using Ollama

The application uses FastAPI for high-performance async API handling and includes
CORS middleware to allow requests from the Next.js frontend.
"""

# Import FastAPI framework and CORS middleware for handling cross-origin requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route modules that define our API endpoints
from routes import leads, notes


# Initialize the FastAPI application with metadata
# This metadata appears in the auto-generated API documentation at /docs
app = FastAPI(
    title="Lead Sync + AI Notes API",
    description="Backend API for lead management with AI-powered note summaries",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This is essential for allowing our Next.js frontend (running on port 3000)
# to make API requests to this backend (running on port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from Next.js dev server
    allow_credentials=True,                    # Allow cookies and authentication headers
    allow_methods=["*"],                       # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],                       # Allow all headers
)

# Register route handlers from separate modules
# This keeps our code organized by separating concerns into different files
app.include_router(leads.router)  # Handles /leads endpoints
app.include_router(notes.router)  # Handles /notes and /summary endpoints


@app.get("/")
async def root():
    """
    Root endpoint - Health check and API information
    
    This endpoint serves as a simple health check to verify the API is running.
    It also provides a link to the interactive API documentation.
    
    Returns:
        dict: API status information including a link to /docs
    """
    return {
        "message": "Lead Sync + AI Notes API",
        "status": "running",
        "docs": "/docs"  # FastAPI auto-generates interactive docs at this URL
    }
