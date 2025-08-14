from pydantic import BaseModel
from typing import List, Dict
from app.schemas.event import CalendarEvent

class CalendarEventRequest(BaseModel):
    content: str
    user_mentions: List[Dict]

class CalendarEventResponse(BaseModel):
    events: List[CalendarEvent]