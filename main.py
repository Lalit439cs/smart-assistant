from fastapi import FastAPI
from app.api import orchestrator

app = FastAPI(
    title="Smart Assistant Orchestrator",
    description="AI-powered calendar assistant with Supabase integration",
    version="1.0.0"
)

app.include_router(orchestrator.router, prefix="/api/v1", tags=["orchestrator"])

@app.get("/")
async def root():
    return {
        "message": "Smart Assistant Orchestrator API",
        "version": "1.0.0",
        "endpoints": {
            "orchestrator": "/api/v1/orchestrate/",
            "docs": "/docs"
        }
    }

# For local dev: uvicorn main:app --reload --port 8001 