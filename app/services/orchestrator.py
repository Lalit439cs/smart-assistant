from typing import Dict, List, Any
from app.services.users_processing import processor
from app.services.supabase_client import post_events_to_supabase
from app.schemas.orchestrator import OrchestratorRequest, OrchestratorResponse, SupabaseResponse, UserMention
import json
from datetime import datetime, timezone
import uuid

def convert_user_mentions_to_dict(user_mentions: List[UserMention]) -> List[Dict[str, str]]:
    """
    Convert Pydantic UserMention objects to dictionaries for the processor
    """
    return [
        {
            "user_id": mention.user_id,
            "user_name": mention.user_name, 
            "user_email": mention.user_email
        }
        for mention in user_mentions
    ]

def ensure_valid_uuid(user_id: str) -> str:
    """
    Ensure user_id is a valid UUID format
    """
    try:
        # Try to parse as UUID
        uuid.UUID(user_id)
        return user_id
    except ValueError:
        # If not a valid UUID, generate a new one based on the string
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, user_id))

def convert_events_to_supabase_format(events: List[Dict[str, Any]], request: OrchestratorRequest) -> List[Dict[str, Any]]:
    """
    Convert events from processor format to Supabase API format
    """
    supabase_events = []
    current_time = datetime.now(timezone.utc).isoformat()
    
    print(f"DEBUG: Converting {len(events)} events to Supabase format")
    
    for i, event in enumerate(events):
        print(f"DEBUG: Event {i+1} structure: {json.dumps(event, indent=2)}")
        
        # Handle both dict and CalendarEvent objects
        if hasattr(event, 'dict'):  # Pydantic model
            event_dict = event.dict()
        elif isinstance(event, dict):
            event_dict = event
        else:
            print(f"Warning: Unknown event type {type(event)} for event {i+1}")
            continue
        
        # Ensure all required fields have proper values
        start_time = event_dict.get("start_time", "")
        end_time = event_dict.get("end_time", "")
        created_at = event_dict.get("created_at", current_time)
        updated_at = event_dict.get("updated_at", current_time)
        
        # Skip events with empty timestamps
        if not start_time or not end_time:
            print(f"Warning: Skipping event '{event_dict.get('title', 'Unknown')}' due to missing timestamps")
            continue
            
        # Ensure user_id is a valid UUID
        user_id = ensure_valid_uuid(event_dict.get("user_id", ""))
        
        # Get user information from the request
        user_name = event_dict.get("user_name", request.user_name)
        user_email = event_dict.get("user_email", request.user_email)
        
        # Convert event to Supabase format
        supabase_event = {
            "title": event_dict.get("title", "Untitled Event"),
            "description": event_dict.get("description", ""),
            "start_time": start_time,
            "end_time": end_time,
            "location": event_dict.get("location", ""),
            "category": event_dict.get("category", "internal_meeting"),
            "user_id": user_id,
            # "user_name": user_name,  # Include for user creation
            # "user_email": user_email,  # Include for user creation
            "created_at": created_at,
            "updated_at": updated_at,
            # "priority": event_dict.get("priority", "medium"),
            # "participants": event_dict.get("participants", []),
            # "amount": event_dict.get("amount")
        }
        
        # Remove None values to avoid Supabase issues
        supabase_event = {k: v for k, v in supabase_event.items() if v is not None}
        
        print(f"DEBUG: Supabase event {i+1}: {json.dumps(supabase_event, indent=2)}")
        supabase_events.append(supabase_event)
    
    return supabase_events

def orchestrate_request(request: OrchestratorRequest) -> OrchestratorResponse:
    """
    Main orchestrator function that processes the request and posts events to Supabase
    
    Args:
        request: OrchestratorRequest object containing all necessary data
        
    Returns:
        OrchestratorResponse with results
    """
    try:
        # Ensure request user_id is a valid UUID
        request_user_id = ensure_valid_uuid(request.user_id)
        
        # Convert request to the format expected by processor
        user_request = {
            "content": request.content,
            "user_id": request_user_id,
            "user_name": request.user_name,
            "user_email": request.user_email,
            "user_mentions": convert_user_mentions_to_dict(request.user_mentions),
            "timestamp": request.timestamp,
            "location": request.location or ""
        }
        
        # Process the request using the existing processor
        response_text, events = processor(user_request)
        
        print(f"DEBUG: Processor returned {len(events)} events")
        
        # Convert events to Supabase format
        supabase_events = convert_events_to_supabase_format(events, request)
        
        # Post events to Supabase if there are any
        supabase_results = None
        if supabase_events:
            supabase_results = post_events_to_supabase(supabase_events)
        
        return OrchestratorResponse(
            response_text=response_text,
            events=events,
            supabase_results=supabase_results,
            status="success"
        )
        
    except Exception as e:
        return OrchestratorResponse(
            response_text="An error occurred while processing your request.",
            events=[],
            status="error",
            error=str(e)
        ) 