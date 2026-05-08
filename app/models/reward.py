from pydantic import BaseModel


class Reward(BaseModel):
    score: float
    reason: str


def grade_task(task_type: str, output: str) -> float:
    """Return a validator-friendly score strictly between 0 and 1."""
    text = (output or "").lower()

    if task_type == "task_extraction":
        raw = 0.88 if text.strip() else 0.30
    elif task_type == "priority":
        raw = (
            0.92
            if any(word in text for word in ["high", "medium", "low", "urgent", "asap"])
            else 0.20
        )
    elif task_type == "action_decision":
        raw = (
            0.85
            if any(
                word in text
                for word in ["reply", "respond", "schedule", "escalate", "ignore"]
            )
            else 0.20
        )
    else:
        raw = 0.50

    return round(max(0.01, min(0.99, raw)), 4)
