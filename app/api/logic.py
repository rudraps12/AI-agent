from fastapi import FastAPI
from app.env.environment import EmailEnv
from app.models.action import Action

from app.tasks.easy import easy
from app.tasks.medium import medium
from app.tasks.hard import hard
from app.tasks.grader import grade

app = FastAPI()

env = EmailEnv()

@app.get("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: Action):
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
    score = grader(action, task)

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