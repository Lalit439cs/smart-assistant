from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import orchestrator

app = FastAPI(
    title="Smart Assistant Orchestrator API",
    description="API for orchestrating smart assistant requests",
    version="1.0.0"
)

# CORS middleware must be added before routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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