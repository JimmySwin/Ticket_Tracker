from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Event Tracker API is running!"}

