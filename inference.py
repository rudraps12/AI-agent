from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.post("/reset")
def reset():
    return {"status": "ok"}


@app.post("/step")
def step(data: dict):
    email = data.get("email","").lower()

    tasks = []

    if "meeting" in email:
        tasks.append("Schedule meeting")
    if "send" in email:
        tasks.append("Send document")
    if "urgent" in email:
        tasks.append("Handle urgent issue")

    return {
        "tasks": tasks,
        "reward": len(tasks),
        "done": True
    }