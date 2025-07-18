#!/usr/bin/env python3
"""
Simple test script for the orchestrator functionality
"""

import sys
import os
# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.orchestrator import orchestrate_request
from app.schemas.orchestrator import OrchestratorRequest, UserMention

def test_orchestrator():
    """Test the orchestrator with a simple request"""
    
    # Create a test request with proper UUID
    request = OrchestratorRequest(
        content="Schedule a meeting called 'Test Meeting' for tomorrow at 2 PM UTC for 1 hour.",
        user_id="910457a9-96e9-4c5e-b995-30e454d06018",  # Using a proper UUID
        user_name="Test User",
        user_email="test@example.com",
        user_mentions=[],
        timestamp="2025-07-23T18:30:00+00:00",
        location="Virtual"
    )
    
    print("Testing orchestrator...")
    print(f"Request content: {request.content}")
    print(f"User: {request.user_name} ({request.user_email})")
    print(f"User ID: {request.user_id}")
    print("-" * 50)
    
    try:
        result = orchestrate_request(request)
        
        print(f"Response Text: {result.response_text}")
        print(f"Status: {result.status}")
        print(f"Number of Events: {len(result.events)}")
        
        if result.events:
            print("\nGenerated Events:")
            for i, event in enumerate(result.events, 1):
                print(f"  {i}. {event.get('title', 'No title')}")
                print(f"     Start: {event.get('start_time', 'No time')}")
                print(f"     End: {event.get('end_time', 'No time')}")
                print(f"     Location: {event.get('location', 'No location')}")
        
        if result.supabase_results:
            print(f"\nSupabase Results:")
            print(f"  Total Events: {result.supabase_results.total_events}")
            print(f"  Successful: {result.supabase_results.successful}")
            print(f"  Failed: {result.supabase_results.failed}")
            
            if result.supabase_results.results:
                print("\n  Individual Results:")
                for result_item in result.supabase_results.results:
                    status = "✅ SUCCESS" if result_item.success else "❌ FAILED"
                    print(f"    {status} - {result_item.event_title}")
                    if not result_item.success and result_item.error:
                        print(f"      Error: {result_item.error}")
        
        if result.error:
            print(f"\n❌ Error: {result.error}")
        
        print("\n" + "=" * 50)
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_orchestrator() 