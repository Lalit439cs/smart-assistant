from typing import List, Dict
from app.schemas.event import CalendarEvent
from app.services.agent import run_agent

def load_user_context(user):
    # Stub: In real use, load from DB or API
    return {"user_id": user.id, "email": user.email, "name": user.name}

def mock_generate_event(content, user_context):
    # Replace with real LLM call
    return CalendarEvent(
        title=f"Event for {user_context['name']}",
        description=content,
        start_time="2024-07-01T10:00:00Z",
        end_time="2024-07-01T11:00:00Z",
        location="Virtual",
        category="Meeting",
        user_id=user_context["user_id"],
        created_at="2024-07-01T09:00:00Z",
        updated_at="2024-07-01T09:00:00Z",
        priority="normal",
        participants=[user_context["email"]],
        amount=None
    )
def process_request(user_request):
    # request user info
        user_id = user_request["user_id"]
        user_name = user_request["user_name"]
        user_email = user_request["user_email"]
        user_mentions = user_request.get("user_mentions", [])

        # create agent_request_base 
        keys_to_remove = ["user_id", "user_name", "user_email", "user_mentions"]

        # Create a copy and remove specified keys
        agent_request_base = {k: v for k, v in user_request.items() if k not in keys_to_remove}
        agent_request_base["user_id"] = user_id
        agent_request_base["user_name"] = user_name
        agent_request_base["user_email"] = user_email
        # chat_user_name can be added 

        agent_requests ={#name id is unique
            user_name: agent_request_base
        }
        for user_mention in user_mentions:
            agent_request_base["user_id"] = user_mention["user_id"]
            agent_request_base["user_name"] = user_mention["user_name"]
            agent_request_base["user_email"] = user_mention["user_email"]
            agent_requests[user_mention["user_name"]] = agent_request_base
        # later may change processing for including interaction among users and their calendars
        participants = list(agent_requests.keys())
        for user in participants:
            agent_requests[user]["participants"] = participants
        return user_name, agent_requests

def post_process_response(response):
    pass

def process_events(events, event):
    if type(event) == list:
        events.extend(event)
    else:# debug
        # events.append(event)
        raise ValueError("Event is not a list")
    return events

def processor_agent(user_name, agent_requests):
     events = []
     response_text = "Request is not able to be processed well. Please try again!"
     try:
        for user, agent_request in agent_requests.items():
            if user!=user_name:
                response = run_agent(user, agent_request)
                if response["type"] == "modify_info_event":
                    events = process_events(events, response["event"])
                elif response["type"] == "normal_response":
                    response_text = response["content"]
                elif response["type"] == "fetch_info_event":
                    events = process_events(events, response["event"])
                else:
                    raise ValueError("Unknown response type")


        response = run_agent(user_name, agent_requests[user_name])

        # later may change processing for including interaction among users and their calendars
        if response["type"] == "normal_response":
            response_text = response["content"]
        elif response["type"] == "fetch_info_event":
            response_text = "Event is updated in respected calendars successfully!"
            events = process_events(events, response["event"])
        elif response["type"] == "modify_info_event":
            response_text = "Event is updated in respected calendars successfully!"
            events = process_events(events, response["event"])
        else:
            raise ValueError("Unknown response type")

        # print("response:", response)
        # print("agent_requests:", agent_requests)
        return response_text, events
     except Exception as e:
        # raise e
        events = []
        response_text = "Request is not able to be processed well. Please try again!"
        print("Error in processing request", e)
        return response_text, events

def processor(user_request):
    user_name, agent_requests = process_request(user_request)
    response_text, events = processor_agent(user_name, agent_requests)
    return response_text, events

def generate_events_for_users(content: str, user_mentions: List[Dict]) -> List[CalendarEvent]:
    events = []
    for user in user_mentions:
        context = load_user_context(user)
        event = mock_generate_event(content, context)
        events.append(event)
    return events

if __name__ == "__main__":
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
    response_text, events = processor(user_request_1)
    print(response_text, events)
    response_text, events = processor(user_request_2)
    print(response_text, events)

# python3 -m app.services.users_processing
