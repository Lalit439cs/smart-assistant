# Smart Assistant Orchestrator

This orchestrator provides a complete solution for processing calendar requests and posting events to Supabase.

## Features

- **Single POST endpoint** for all calendar operations
- **Automatic event processing** using OpenAI GPT-4o Mini
- **Multi-user support** with user mentions
- **Supabase integration** for event storage
- **Comprehensive error handling**

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn main:app --reload --port 8000
```

### 3. Test the API
```bash
python tests/test_simple.py
```

## API Endpoint

### POST `/api/v1/orchestrate/`

Processes calendar requests and posts events to Supabase.

#### Request Format

```json
{
    "content": "Schedule a meeting called 'Invoice Approval Test' for July 23rd at 6:30 PM UTC for 1 hour.",
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
```

#### Response Format

```json
{
    "response_text": "Event is updated in respected calendars successfully!",
    "events": [
        {
            "title": "Invoice Approval Test",
            "description": "Meeting for invoice approval",
            "start_time": "2025-07-23T18:30:00+00:00",
            "end_time": "2025-07-23T19:30:00+00:00",
            "location": "4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768",
            "category": "internal_meeting",
            "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
            "created_at": "2025-07-23T18:30:00+00:00",
            "updated_at": "2025-07-23T18:30:00+00:00",
            "priority": "medium",
            "participants": ["Lalit", "Charan"],
            "amount": null
        }
    ],
    "supabase_results": {
        "total_events": 1,
        "successful": 1,
        "failed": 0,
        "results": [
            {
                "success": true,
                "status_code": 201,
                "event_title": "Invoice Approval Test",
                "data": null,
                "error": null
            }
        ]
    },
    "status": "success",
    "error": null
}
```

## Configuration

The orchestrator uses the following configuration in `app/config.py`:

```python
# OpenAI Configuration
OPENAI_API_KEY = "your-openai-api-key"
MODEL_NAME = "gpt-4o-mini"

# Supabase Configuration
SUPABASE_URL = "https://siydccpivqusbxyhcvbm.supabase.co/rest/v1/events"
SUPABASE_API_KEY = "your-supabase-api-key"
SUPABASE_AUTH_TOKEN = "your-supabase-auth-token"
```

## Usage Examples

### Single User Meeting

```bash
curl -X POST "http://localhost:8001/api/v1/orchestrate/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Schedule a meeting called 'Team Standup' for tomorrow at 9 AM UTC for 30 minutes.",
    "user_id": "user-123",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "user_mentions": [],
    "timestamp": "2025-07-23T18:30:00+00:00",
    "location": "Virtual"
  }'
```

### Multi-User Meeting

```bash
curl -X POST "http://localhost:8001/api/v1/orchestrate/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Schedule a meeting with @Alice and @Bob called 'Project Review' for Friday at 2 PM UTC for 1 hour.",
    "user_id": "user-123",
    "user_name": "John Doe",
    "user_email": "john@example.com",
    "user_mentions": [
      {
        "user_id": "user-456",
        "user_name": "Alice",
        "user_email": "alice@example.com"
      },
      {
        "user_id": "user-789",
        "user_name": "Bob",
        "user_email": "bob@example.com"
      }
    ],
    "timestamp": "2025-07-23T18:30:00+00:00",
    "location": "Conference Room A"
  }'
```

## Testing

### Run Simple Test
```bash
python tests/test_simple.py
```

### Run Full Test Suite
```bash
python tests/test_orchestrator.py
```

### API Documentation
Visit `http://localhost:8001/docs` for interactive API documentation.

## Architecture

The orchestrator consists of several components:

1. **Orchestrator Service** (`app/services/orchestrator.py`): Main coordination logic
2. **Supabase Client** (`app/services/supabase_client.py`): Handles API calls to Supabase
3. **User Processing** (`app/services/users_processing.py`): Processes user requests using OpenAI
4. **Schemas** (`app/schemas/orchestrator.py`): Request/response data models
5. **API Endpoint** (`app/api/orchestrator.py`): FastAPI router for the endpoint

## Error Handling

The orchestrator provides comprehensive error handling:

- **OpenAI API errors**: Retries with exponential backoff
- **Supabase API errors**: Individual event failure tracking
- **Validation errors**: Proper HTTP status codes and error messages
- **Processing errors**: Graceful degradation with fallback responses

## Dependencies

Make sure to install all required packages:

```bash
pip install -r requirements.txt
```

Required packages:
- `fastapi`
- `uvicorn`
- `pydantic`
- `python-dotenv`
- `json-repair`
- `openai`
- `requests` 