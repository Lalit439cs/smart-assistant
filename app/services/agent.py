# app/services/agent.py

from openai import AzureOpenAI
import json
import uuid
from datetime import datetime
from typing import Literal
from app.config import API_KEY, AZURE_ENDPOINT, DEPLOYMENT_NAME
# from app.schemas.event import CalendarEvent
import time

# Initialize client
client = AzureOpenAI(
    api_key=API_KEY,
    api_version="2023-12-01-preview",
    azure_endpoint=AZURE_ENDPOINT
)

# calendar_event_schema = CalendarEvent.schema()  # Pydantic schema
# Tool function schema
# event_tool_schema = {
#     "name": "create_calendar_events",
#     "description": "Create a structured calendar event from user input",
#     "parameters": calendar_event_schema["parameters"]
# }

# Tool function schema to allow list or single event
event_tool_schema = {
    "name": "create_calendar_events",
    "description": "Create one or more structured and sequential calendar events from user input",
    "parameters": {
        "type": "object",
        "properties": {
            "events": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "start_time": {"type": "string", "format": "date-time"},
                        "end_time": {"type": "string", "format": "date-time"},
                        "operation": {
                            "type": "string",
                            "enum": ["add", "delete"],
                            "description": "Type of Operation to be performed in Calendar: 'add' or 'delete'"
                        },
                        "id": {"type": "string", "description": "Id of the event if to be deleted"},
                        "location": {
                            "type": "string",
                            "description": "Event location. Default to 'Online' if not provided."
                        },
                        "category": {"type": "string"},
                        "user_id": {"type": "string"},
                        "user_name": {"type": "string"},
                        "user_email": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time", "description": "Present timestamp of event creation"},
                        "updated_at": {"type": "string", "format": "date-time"},
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Priority level: 'low', 'medium', or 'high'"
                        },
                        "participants": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of user_name of all participants"
                        },
                        "amount": {"type": ["number", "null"]}
                    },
                    "required": ["title", "start_time", "end_time", "location", "user_id", "user_name", "user_email", "operation", "participants", "created_at"]
                }
            }
        },
        "required": ["events"]
    }
}

def safe_llm_call(call_fn, retries=3, delay=1):
    for attempt in range(retries):
        try:
            return call_fn()
        except Exception as e:
            if attempt == retries - 1:
                raise e
            time.sleep(delay)

def plan_task(user_input: str) -> Literal["normal_response", "fetch_info_event", "modify_info_event"]:
    def _call():
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": (
                    "You are a planner for a calendar assistant. Your job is to decide the intent type of the user input.\n"
                    "Choose one of the following task types:\n"
                    "- normal_response: Just reply normally\n"
                    "- fetch_info_event: Retrieve calendar data\n"
                    "- modify_info_event: Add or delete calendar events. Type of 'operation' for event will be also handled here."
                )},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip().lower()

    return safe_llm_call(_call)

def run_agent(user_name: str, agent_request: dict, fetched_info=""):
    user_input = (
        f"Consider the following context:\n"
        f"- User: {user_name}\n"
        f"- Timestamp: {agent_request['timestamp']}\n"
        f"- Other Context: {agent_request}\n\n"
        f"- Fetched Info: {fetched_info}\n\n"
        f"The user's query is:\n\"{agent_request['content']}\"\n\n"
    )

    plan = plan_task(user_input)

    if plan == "normal_response":
        def _call():
            return client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            )

        response = safe_llm_call(_call)
        return {"type": "normal_response", "content": response.choices[0].message.content.strip()}

    elif plan == "fetch_info_event":
        fetched_events = [{"title": "Mock Event", "start_time": "2025-07-23T18:30:00+00:00"}]
        context = f"User ({user_name}) has the following calendar events:-\n {json.dumps(fetched_events)}"
        return run_agent(user_name, agent_request, context)

    elif plan == "modify_info_event":
        def _call():
            return client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "You are a smart calendar assistant. For given user_name, find sequence of calendar events for modifying the calendar"},
                    {"role": "user", "content": user_input}
                ],
                tools=[{"type": "function", "function": event_tool_schema}],
                tool_choice="auto"
            )

        response = safe_llm_call(_call)
        tool_call = response.choices[0].message.tool_calls[0]
        parsed_events = json.loads(tool_call.function.arguments)
        return {"type": "modify_info_event", "event": parsed_events.get("events", [])}

    else:
        return {"type": "error", "message": "Unknown plan"}


# Example
if __name__ == "__main__":

    user_request = {
        "content": "Schedule a meeting called 'Invoice Approval Test' for July 23rd at 6:30 PM UTC for 1 hour.",
        "user_id": "910457a9-96e9-4c5e-b995-30e454d06018",
        "user_name": "Lalit",
        "user_email": "lalit.hyperbots@gmail.com",
        "user_mentions": [
            {
                "id": "910457a9-96e9-4c5e-b995-30e454d06018",
                "name": "Lalit",
                "email": "lalit.hyperbots@gmail.com"
            }
        ],
        "timestamp": "2025-07-23T18:30:00+00:00",
        "location": "4309 Hacienda Dr SUITE 110 PLEASANTON CA United States 94588-2768"
    }
    # simple generate_event_json
    # json_output = generate_event_json(user_prompt, user_id)

    # json_output = generate_event_with_tool(user_prompt)
    # print("title", json_output["title"])
    # print("Structured JSON output:\n", json_output)

    """
        Can be in System prompts
        "- 'priority' must be one of: 'low', 'medium', or 'high'.\n"
        "- If 'location' is not specified or is empty, default to 'Online'.\n"
        "- Return a JSON object following the tool/function schema provided.\n"
    """

    


