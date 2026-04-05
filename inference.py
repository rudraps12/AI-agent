from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class EmailInput(BaseModel):
    email: str


@app.post("/reset")
def reset():
    return {"status": "ok"}


@app.post("/step")
def step(data: EmailInput):
    email = data.email.lower()

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