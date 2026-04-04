from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from app.env.environment import EmailEnv, get_task_type
from app.models.action import Action

app = FastAPI()
env = EmailEnv()


# ✅ Request model (NEW ADDITION)
class EmailRequest(BaseModel):
    email_text: str


@app.get("/")
def home():
    return {"message": "Email Triage API running"}


@app.post("/process")
def process(request: EmailRequest):
    try:
        email_text = request.email_text

        # Reset environment
        env.reset()

        # Set email
        env.current_email.email = email_text

        # Detect task
        task_type = get_task_type(email_text)

        # Create action
        action = Action(
            action_type="reply",
            content=email_text
        )

        # Run step
        observation, reward, done, info = env.step(action)

        # Safe response (IMPORTANT)
        return {
            "email": str(email_text),
            "task_type": str(task_type),
            "action": str(action.content),
            "tasks": [str(t) for t in env.tasks],
            "reward": float(reward)
        }

    except Exception as e:
        return {"error": str(e)}
