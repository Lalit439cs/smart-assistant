from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class UserMention(BaseModel):
    user_id: str
    user_name: str
    user_email: str

class OrchestratorRequest(BaseModel):
    content: str
    user_id: str
    user_name: str
    user_email: str
    user_mentions: List[UserMention] = []
    timestamp: str
    location: Optional[str] = None

class EventResult(BaseModel):
    success: bool
    status_code: Optional[int] = None
    event_title: str
    data: Optional[Any] = None
    error: Optional[str] = None

class SupabaseResponse(BaseModel):
    total_events: int
    successful: int
    failed: int
    results: List[EventResult]

class OrchestratorResponse(BaseModel):
    response_text: str
    events: List[Dict[str, Any]]
    supabase_results: Optional[SupabaseResponse] = None
    status: str = "success"
    error: Optional[str] = None 