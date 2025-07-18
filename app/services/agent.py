from typing import List, Dict
from app.schemas.event import CalendarEvent

def load_user_context(user):
    # Stub: In real use, load from DB or API
    return {"user_id": user.id, "email": user.email, "name": user.name}

def mock_generate_event(content, user_context):
    # Replace with real LLM call
    return CalendarEvent(
        title=f"Event for {user_context['name']}",
        description=content,
        start_time="2024-07-01T10:00:00Z",
        end_time="2024-07-01T11:00:00Z",
        location="Virtual",
        category="Meeting",
        user_id=user_context["user_id"],
        created_at="2024-07-01T09:00:00Z",
        updated_at="2024-07-01T09:00:00Z",
        priority="normal",
        participants=[user_context["email"]],
        amount=None
    )

def generate_events_for_users(content: str, user_mentions: List[Dict]) -> List[CalendarEvent]:
    events = []
    for user in user_mentions:
        context = load_user_context(user)
        event = mock_generate_event(content, context)
        events.append(event)
    return events 