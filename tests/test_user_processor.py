#!/usr/bin/env python3
"""
Test script for the processor function
"""

import json
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.services.users_processing import processor

def test_processor():
    """Test the processor function with sample requests"""
    
    # Sample request 1: Single user meeting
    user_request_1 = {
        "content": "Schedule a meeting called 'Invoice Approval Test' for July 23rd at 6:30 PM UTC for 1 hour.",
        "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
        "user_name": "Lalit",
        "user_email": "lalit.hyperbots@gmail.com", 
        "user_mentions": [],
        "timestamp": "2025-07-23T18:30:00+00:00",
        "location": "4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768"
    }

    # Sample request 2: Meeting with mentioned user
    user_request_2 = {
        "content": "Schedule a meeting with @Charan called 'Work Delegation meeting' for July 24th at 6:30 PM UTC for 1 hour.",
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

    print("=" * 80)
    print("TESTING PROCESSOR FUNCTION")
    print("=" * 80)
    
    # Test 1: Single user meeting
    print("\n" + "=" * 40)
    print("TEST 1: Single User Meeting")
    print("=" * 40)
    print("Input Request:")
    print(json.dumps(user_request_1, indent=2))
    
    try:
        response_text, events = processor(user_request_1)
        print("\n" + "-" * 40)
        print("RESPONSE:")
        print("-" * 40)
        print(f"Response Text: {response_text}")
        print(f"Events: {json.dumps(events, indent=2) if events else 'No events'}")
    except Exception as e:
        print(f"Error in Test 1: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Meeting with mentioned user
    print("\n" + "=" * 40)
    print("TEST 2: Meeting with Mentioned User")
    print("=" * 40)
    print("Input Request:")
    print(json.dumps(user_request_2, indent=2))
    
    try:
        response_text, events = processor(user_request_2)
        print("\n" + "-" * 40)
        print("RESPONSE:")
        print("-" * 40)
        print(f"Response Text: {response_text}")
        print(f"Events: {json.dumps(events, indent=2) if events else 'No events'}")
    except Exception as e:
        print(f"Error in Test 2: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_processor()

# python3 -m tests.test_user_processor