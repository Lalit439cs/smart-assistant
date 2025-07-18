#!/bin/bash

# Sample request script for the Smart Assistant Orchestrator
# Make sure the server is running: uvicorn main:app --reload --port 8001

echo "🚀 Testing Smart Assistant Orchestrator API"
echo "=========================================="

# Test 1: Single User Meeting
echo ""
echo "📅 Test 1: Single User Meeting"
echo "-------------------------------"
curl -X POST "http://localhost:8001/api/v1/orchestrate/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Schedule a meeting called 'Team Standup' for tomorrow at 9 AM UTC for 30 minutes.",
    "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "user_mentions": [],
    "timestamp": "2025-07-23T18:30:00+00:00",
    "location": "Virtual"
  }' | jq '.'

echo ""
echo ""

# Test 2: Multi-User Meeting
echo "📅 Test 2: Multi-User Meeting"
echo "------------------------------"
curl -X POST "http://localhost:8001/api/v1/orchestrate/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Schedule a meeting with @Alice and @Bob called 'Project Review' for Friday at 2 PM UTC for 1 hour.",
    "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "user_mentions": [
      {
        "user_id": "910457a9-96e9-4c5e-b995-30e454d06019",
        "user_name": "Alice",
        "user_email": "alice@example.com"
      },
      {
        "user_id": "910457a9-96e9-4c5e-b995-30e454d06020",
        "user_name": "Bob",
        "user_email": "bob@example.com"
      }
    ],
    "timestamp": "2025-07-23T18:30:00+00:00",
    "location": "Conference Room A"
  }' | jq '.'

echo ""
echo ""

# Test 3: Invoice Approval Meeting (from your example)
echo "📅 Test 3: Invoice Approval Meeting"
echo "-----------------------------------"
curl -X POST "http://localhost:8001/api/v1/orchestrate/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Schedule a meeting called 'Invoice Approval Test' for July 23rd at 6:30 PM UTC for 1 hour.",
    "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
    "user_name": "Lalit",
    "user_email": "lalit.hyperbots@gmail.com",
    "user_mentions": [],
    "timestamp": "2025-07-23T18:30:00+00:00",
    "location": "4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768"
  }' | jq '.'

echo ""
echo "✅ All tests completed!" 