from pydantic import BaseModel


class Reward(BaseModel):
    score: float
    reason: str


def grade_task(task_type: str, output: str) -> float:
    """Score strictly between 0 and 1 (exclusive). Never 0.0 or 1.0."""
    text = (output or "").lower()

    if task_type == "priority":
        if any(w in text for w in ["urgent", "asap", "immediately", "high"]):
            return 0.92
        elif any(w in text for w in ["medium", "moderate"]):
            return 0.60
        else:
            return 0.25

    elif task_type == "task_extraction":
        if not output or len(output.strip()) == 0:
            return 0.15
        word_count = len(output.split())
        if word_count >= 10:
            return 0.88
        elif word_count >= 5:
            return 0.65
        else:
            return 0.40

    elif task_type == "action_decision":
        if any(w in text for w in ["reply", "escalate", "schedule", "respond"]):
            return 0.85
        elif any(w in text for w in ["ignore", "defer"]):
            return 0.35
        else:
            return 0.50

    elif task_type == "sentiment":
        if any(w in text for w in ["positive", "happy", "great", "excellent"]):
            return 0.82
        elif any(w in text for w in ["negative", "angry", "frustrated"]):
            return 0.78
        else:
            return 0.55

    elif task_type == "summarization":
        if not output:
            return 0.10
        sentences = [s.strip() for s in output.split(".") if s.strip()]
        if len(sentences) >= 3:
            return 0.87
        elif len(sentences) >= 1:
            return 0.60
        else:
            return 0.25

    return 0.50
