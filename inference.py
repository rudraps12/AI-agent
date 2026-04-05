from fastapi import FastAPI

app = FastAPI()

@app.post("/reset")
def reset():
    print("START: reset called")
    return {"status": "ok"}

@app.post("/step")
def step(data: dict):
    print("STEP: processing input")

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