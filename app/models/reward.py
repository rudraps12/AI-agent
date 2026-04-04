from pydantic import BaseModel

class Reward(BaseModel):
    score: float
    reason: str
    
def grade_task(task_type, output):
    if task_type == "priority":
        if "urgent" in output.lower():
            return 1.0
        else:
            return 0.5

    elif task_type == "task_extraction":
        if len(output) > 0:
            return 1.0
        else:
            return 0.3

    else:
        return 0.5