from fastapi import APIRouter, HTTPException
from app.schemas.orchestrator import OrchestratorRequest, OrchestratorResponse
from app.services.orchestrator import orchestrate_request

router = APIRouter()

@router.post("/orchestrate/", response_model=OrchestratorResponse)
async def orchestrate_calendar_request(request: OrchestratorRequest):
    """
    Main orchestrator endpoint that processes calendar requests and posts events to Supabase
    
    Example request:
    {
        "content": "Schedule a meeting called 'Invoice Approval Test' for July 23rd at 6:30 PM UTC for 1 hour.",
        "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
        "user_name": "Lalit",
        "user_email": "lalit.hyperbots@gmail.com",
        "user_mentions": [
            {
                "user_id": "910457a9-96e9-4c5e-b995-30e454d06019",
                "user_name": "Charan",
                "user_email": "charan.hyperbots@gmail.com"
            }
        ],
        "timestamp": "2025-07-23T18:30:00+00:00",
        "location": "4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768"
    }
    """
    try:
        result = orchestrate_request(request)
        
        if result.status == "error":
            raise HTTPException(status_code=500, detail=result.error)
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 