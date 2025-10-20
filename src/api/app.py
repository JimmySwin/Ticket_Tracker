from fastapi import FastAPI
from src.db_manager import get_all_events, insert_or_update_event, create_table

app = FastAPI(title="Ticket Tracker API")

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    create_table()

@app.get("/")
def root():
    return {"message": "Ticket Tracker API is running 🚀"}

@app.get("/events")
def get_events():
    events = get_all_events()
    return {"events": events}