from pydantic import BaseModel
from typing import List, Optional

class CalendarEvent(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: str
    end_time: str
    location: Optional[str] = None
    category: Optional[str] = None
    user_id: str
    created_at: str
    updated_at: str
    priority: Optional[str] = None
    participants: List[str] = []
    amount: Optional[float] = None 