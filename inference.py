import os
from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()

# Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)


@app.post("/reset")
def reset():
    print("START: reset called")
    return {"status": "ok"}


@app.post("/step")
def step(data: dict):
    print("STEP: processing input")

    # FIXED LINE 👇
    email = data.get("input", {}).get("email", "")

    tasks = []
    if "meeting" in email.lower():
        tasks.append("Schedule meeting")
    if "send" in email.lower():
        tasks.append("Send document")

    print("END: returning output")

    return {
        "tasks": tasks,
        "reward": len(tasks),
        "done": True
    }