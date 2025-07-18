import requests
import json
from typing import List, Dict, Any, Optional
from app.config import SUPABASE_EVENTS_FETCH_URL, SUPABASE_API_KEY, SUPABASE_AUTH_TOKEN

def get_supabase_headers():
    """Get common headers for Supabase API calls"""
    return {
        'apikey': SUPABASE_API_KEY,
        'Authorization': f'Bearer {SUPABASE_AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }

def fetch_user_events(user_id: str) -> List[Dict[str, Any]]:
    """
    Fetch all events for a specific user from Supabase
    
    Args:
        user_id: The user ID to fetch events for
        
    Returns:
        List of event dictionaries
    """
    try:
        # Construct the URL with user_id filter
        url = f"{SUPABASE_EVENTS_FETCH_URL}?user_id=eq.{user_id}"
        
        response = requests.get(
            url,
            headers=get_supabase_headers(),
            timeout=30
        )
        
        if response.status_code == 200:
            events = response.json()
            print(f"✅ Successfully fetched {len(events)} events for user {user_id}")
            return events
        else:
            print(f"❌ Failed to fetch events for user {user_id}: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error fetching events for user {user_id}: {str(e)}")
        return []

def fetch_user_events_context(user_id: str, user_name: str) -> str:
    """
    Fetch user events and format them as context for the agent
    
    Args:
        user_id: The user ID to fetch events for
        user_name: The user's name for context
        
    Returns:
        Formatted context string with user events
    """
    events = fetch_user_events(user_id)
    
    if not events:
        return f"User ({user_name}) has no calendar events."
    
    # Format events for context
    formatted_events = []
    for event in events:
        formatted_event = {
            "title": event.get("title", "Untitled"),
            "start_time": event.get("start_time", "Unknown"),
            "end_time": event.get("end_time", "Unknown"),
            "location": event.get("location", "No location"),
            "category": event.get("category", "No category"),
            "priority": event.get("priority", "No priority")
        }
        formatted_events.append(formatted_event)
    
    context = f"User ({user_name}) has the following calendar events:\n{json.dumps(formatted_events, indent=2)}"
    return context

def fetch_multiple_users_events(user_events: List[Dict[str, str]]) -> str:
    """
    Fetch events for multiple users and format as context
    
    Args:
        user_events: List of dictionaries with user_id and user_name
        
    Returns:
        Formatted context string with all users' events
    """
    all_contexts = []
    
    for user_info in user_events:
        user_id = user_info.get("user_id", "")
        user_name = user_info.get("user_name", "Unknown User")
        
        if user_id:
            user_context = fetch_user_events_context(user_id, user_name)
            all_contexts.append(user_context)
    
    if not all_contexts:
        return "No user events found."
    
    return "\n\n".join(all_contexts) 