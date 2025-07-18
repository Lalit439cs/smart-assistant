#!/usr/bin/env python3
"""
Test script for event fetching functionality
"""

import sys
import os
# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.event_fetcher import fetch_user_events, fetch_user_events_context

def test_event_fetching():
    """Test the event fetching functionality"""
    
    # Test user ID (use a valid UUID that exists in your database)
    test_user_id = "910457a9-96e9-4c5e-b995-30e454d06018"
    test_user_name = "John Doe"
    
    print("🔍 Testing Event Fetching Functionality")
    print("=" * 50)
    
    # Test 1: Fetch raw events
    print(f"\n📅 Test 1: Fetching raw events for user {test_user_name} ({test_user_id})")
    print("-" * 50)
    
    try:
        events = fetch_user_events(test_user_id)
        print(f"Found {len(events)} events")
        
        if events:
            print("\nRaw events:")
            for i, event in enumerate(events, 1):
                print(f"  {i}. {event.get('title', 'No title')}")
                print(f"     Start: {event.get('start_time', 'No time')}")
                print(f"     End: {event.get('end_time', 'No time')}")
                print(f"     Location: {event.get('location', 'No location')}")
        else:
            print("No events found for this user.")
            
    except Exception as e:
        print(f"❌ Error fetching raw events: {str(e)}")
    
    # Test 2: Fetch formatted context
    print(f"\n📅 Test 2: Fetching formatted context for user {test_user_name}")
    print("-" * 50)
    
    try:
        context = fetch_user_events_context(test_user_id, test_user_name)
        print("Formatted context:")
        print(context)
        
    except Exception as e:
        print(f"❌ Error fetching formatted context: {str(e)}")
    
    # Test 3: Test with non-existent user
    print(f"\n📅 Test 3: Testing with non-existent user")
    print("-" * 50)
    
    try:
        non_existent_user_id = "00000000-0000-0000-0000-000000000000"
        context = fetch_user_events_context(non_existent_user_id, "Non-existent User")
        print("Result for non-existent user:")
        print(context)
        
    except Exception as e:
        print(f"❌ Error testing non-existent user: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Event fetching tests completed!")

if __name__ == "__main__":
    test_event_fetching() 