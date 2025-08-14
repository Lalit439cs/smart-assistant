import requests
import json
from typing import List, Dict, Any
from app.config import SUPABASE_URL, SUPABASE_API_KEY, SUPABASE_AUTH_TOKEN

def post_event_to_supabase(event_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Post a single event to Supabase API
    
    Args:
        event_data: Dictionary containing event information
        
    Returns:
        Dict containing response status and data
    """
    headers = {
        'apikey': SUPABASE_API_KEY,
        'Authorization': f'Bearer {SUPABASE_AUTH_TOKEN}',
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
    }
    
    try:
        response = requests.post(
            SUPABASE_URL,
            headers=headers,
            json=event_data
        )
        
        if response.status_code in [200, 201]:
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json() if response.content else None,
                "event_title": event_data.get("title", "Unknown")
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "error": response.text,
                "event_title": event_data.get("title", "Unknown")
            }
            
    except Exception as e:
        return {
            "success": False,
            "status_code": None,
            "error": str(e),
            "event_title": event_data.get("title", "Unknown")
        }

def post_events_to_supabase(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Post multiple events to Supabase API
    
    Args:
        events: List of event dictionaries
        
    Returns:
        Dict containing overall results
    """
    results = []
    successful_count = 0
    failed_count = 0
    
    for event in events:
        result = post_event_to_supabase(event)
        results.append(result)
        
        if result["success"]:
            successful_count += 1
        else:
            failed_count += 1
    
    return {
        "total_events": len(events),
        "successful": successful_count,
        "failed": failed_count,
        "results": results
    } 