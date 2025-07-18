#!/usr/bin/env python3
"""
Test script for the orchestrator functionality
"""

import sys
import os
# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from app.services.orchestrator import orchestrate_request
from app.schemas.orchestrator import OrchestratorRequest, UserMention

def test_single_user_meeting():
    """Test orchestrator with a single user meeting request"""
    
    request = OrchestratorRequest(
        content="Schedule a meeting called 'Invoice Approval Test' for July 23rd at 6:30 PM UTC for 1 hour.",
        user_id="910457a9-96e9-4c5e-b995-30e454d06018",
        user_name="Lalit",
        user_email="lalit.hyperbots@gmail.com",
        user_mentions=[],
        timestamp="2025-07-23T18:30:00+00:00",
        location="4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768"
    )
    
    print("Testing single user meeting...")
    result = orchestrate_request(request)
    
    print(f"Response Text: {result.response_text}")
    print(f"Status: {result.status}")
    print(f"Number of Events: {len(result.events)}")
    
    if result.supabase_results:
        print(f"Supabase Results: {result.supabase_results.total_events} total, {result.supabase_results.successful} successful, {result.supabase_results.failed} failed")
    
    if result.error:
        print(f"Error: {result.error}")
    
    print("-" * 50)

def test_multi_user_meeting():
    """Test orchestrator with multiple users meeting request"""
    
    request = OrchestratorRequest(
        content="Schedule a meeting with @Charan called 'Work Delegation meeting' for July 24th at 6:30 PM UTC for 1 hour.",
        user_id="910457a9-96e9-4c5e-b995-30e454d06018",
        user_name="Lalit",
        user_email="lalit.hyperbots@gmail.com",
        user_mentions=[
            UserMention(
                user_id="910457a9-96e9-4c5e-b995-30e454d06019",
                user_name="Charan",
                user_email="charan.hyperbots@gmail.com"
            )
        ],
        timestamp="2025-07-23T18:30:00+00:00",
        location="4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768"
    )
    
    print("Testing multi-user meeting...")
    result = orchestrate_request(request)
    
    print(f"Response Text: {result.response_text}")
    print(f"Status: {result.status}")
    print(f"Number of Events: {len(result.events)}")
    
    if result.supabase_results:
        print(f"Supabase Results: {result.supabase_results.total_events} total, {result.supabase_results.successful} successful, {result.supabase_results.failed} failed")
    
    if result.error:
        print(f"Error: {result.error}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("Testing Orchestrator Functionality")
    print("=" * 50)
    
    test_single_user_meeting()
    test_multi_user_meeting()
    
    print("Test completed!") 