from fastapi import FastAPI
from app.api import generate_event

app = FastAPI()

app.include_router(generate_event.router)

# For local dev: uvicorn main:app --reload 