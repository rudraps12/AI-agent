from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Input format expected
class EmailInput(BaseModel):
    email: str


# RESET endpoint (required)
@app.post("/reset")
def reset():
    return {
        "status": "environment reset",
        "state": {}
    }


# STEP endpoint (required)
@app.post("/step")
def step(data: EmailInput):
    email = data.email.lower()

    tasks = []

    # Simple rule-based extraction (you can improve later)
    if "meeting" in email:
        tasks.append("Schedule meeting")
    if "send" in email:
        tasks.append("Send document")
    if "report" in email:
        tasks.append("Prepare report")
    if "urgent" in email:
        tasks.append("Handle urgent issue")

    return {
        "tasks": tasks,
        "reward": len(tasks),   # simple reward
        "done": True,
        "info": {
            "message": "Processed successfully"
        }
    }