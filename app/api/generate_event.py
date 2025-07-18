from fastapi import APIRouter
from app.schemas.chat import CalendarEventRequest, CalendarEventResponse
from app.services.agent import generate_events_for_users

router = APIRouter()

@router.post("/calendar-events/", response_model=CalendarEventResponse)
def create_calendar_events(request: CalendarEventRequest):
    events = generate_events_for_users(request.content, request.user_mentions)
    return CalendarEventResponse(events=events) 