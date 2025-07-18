# smart-assistant
smart AI assistant whcih will manage your calendar and track activities

# project structure
smart-assistant/
├── README.md
├── pyproject.toml              # Optional: if using poetry/pdm
├── requirements.txt            # Dependencies (fastapi, openai, uvicorn, etc.)
├── .env                        # API keys and config (not committed)
├── .gitignore
├── main.py                     # Entrypoint for FastAPI app
├── app/
│   ├── __init__.py
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── chat.py             # POST /chat
│   │   ├── generate_event.py   # POST /generate-event
│   │   └── delete_event.py     # POST /delete-event
│   ├── services/               # Core LLM logic and OpenAI integration
│   │   ├── __init__.py
│   │   └── agent.py            # JSON repair, OpenAI calls, tools, etc.
│   ├── schemas/                # Pydantic models
│   │   ├── __init__.py
│   │   ├── event.py            # Calendar event schema
│   │   └── chat.py             # Chat request/response schema
│   ├── utils/                  # Helpers (e.g. json repair)
│   │   └── json_utils.py
│   └── config.py               # Load env vars, keys, etc.
├── tests/
│   ├── __init__.py
│   ├── test_chat.py
│   └── test_generate_event.py

