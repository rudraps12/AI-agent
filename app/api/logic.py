from fastapi import FastAPI
from pydantic import BaseModel

from app.env.environment import EmailEnv
from app.env.environment import extract_tasks_from_email
from app.models.action import Action

from app.tasks.easy import easy
from app.tasks.medium import medium
from app.tasks.hard import hard
from app.tasks.grader import grade as grade_action

app = FastAPI()

env = EmailEnv()


class EmailRequest(BaseModel):
    email: str
    subject: str = "Inbox message"
    sender: str = "sender@example.com"


def build_triage(email_text: str, subject: str = "Inbox message", sender: str = "sender@example.com"):
    if not env.calendar:
        env.calendar = ["Meeting at 5 PM"]

    tasks = extract_tasks_from_email(email_text)
    priority = env.detect_priority(email_text)
    conflict = env.check_conflict(email_text)

    if priority == "high":
        action_type = "reply"
    elif conflict:
        action_type = "schedule"
    elif tasks:
        action_type = "reply"
    else:
        action_type = "archive"

    task_lines = "\n".join(f"- {task}" for task in tasks) or "- No clear action items found"
    reply = (
        f"Hi,\n\nThanks for your email about {subject}. "
        "I reviewed it and will handle the following:\n"
        f"{task_lines}\n\n"
    )

    if conflict:
        reply += "There may be a scheduling conflict, so I will suggest a new time.\n\n"

    if priority == "high":
        reply += "I will treat this as urgent and share an update as soon as possible.\n\n"

    reply += "Best,\nEmail Triage Assistant"

    return {
        "sender": sender,
        "subject": subject,
        "tasks": tasks,
        "priority": priority,
        "has_conflict": conflict,
        "recommended_action": action_type,
        "suggested_reply": reply,
    }


@app.get("/reset")
def reset(task_name: str | None = None):
    task_map = {
        "easy_task": easy(),
        "medium_task": medium(),
        "hard_task": hard(),
    }
    task = task_map.get(task_name or "", None)
    obs = env.reset(task["email"] if task else None)
    return {
        "observation": obs.dict(),
        "done": False,
        "task_name": task_name,
    }

@app.post("/step")
def step(action: Action):
    if env.current_email is None:
        env.reset()

    obs, reward, done, info = env.step(action)
    
    feedback = "Good response"
    if reward.score < 0.5:
        feedback = "Missing key details"
    elif reward.score < 0.8:
        feedback = "Decent but can improve"


    return {
        "observation": obs.dict(),
        "reward": reward.dict(),
        "done": done,
        "info": info,
        "feedback": feedback
    }
@app.get("/state")
def get_state():
    if env.current_email is None:
        env.reset()

    return env.state().dict()

@app.get("/tasks")
def get_tasks():
    return {
        "easy": {"difficulty": 1, **easy()},
        "medium": {"difficulty": 2, **medium()},
        "hard": {"difficulty": 3, **hard()}
    }

@app.post("/grader")
def grader(action: Action):
    task = hard()
    score = grade_action(action, task)

    return {
        "score": score,
        "evaluation": "Excellent" if score > 0.8 else "Needs improvement"
    }

@app.get("/baseline")
def baseline():
    env.reset()

    action = Action(
        action_type="reply",
        content="I will attend meeting and send report ASAP"
    )

    obs, reward, done, _ = env.step(action)

    return {
        "baseline_score": reward.dict(),
        "done": done
    }
    
@app.post("/simulate")
def simulate(action: Action):
    env.reset()

    results = []
    total_score = 0

    for i in range(3):
        obs, reward, done, info = env.step(action)
        total_score += reward.score

        results.append({
            "step": i + 1,
            "score": reward.score,
            "reason": reward.reason
        })

    return {
        "steps": results,
        "final_score": total_score
    }


@app.post("/triage")
def triage(request: EmailRequest):
    return build_triage(
        email_text=request.email,
        subject=request.subject,
        sender=request.sender,
    )
