from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import leads, notes


app = FastAPI(
    title="Lead Sync + AI Notes API",
    description="Backend API for lead management with AI-powered note summaries",
    version="1.0.0"
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(notes.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Lead Sync + AI Notes API",
        "status": "running",
        "docs": "/docs"
    }
