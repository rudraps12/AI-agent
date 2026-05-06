from app.models.reward import grade_task

def grade(action, task: dict) -> float:
    """Returns score strictly between 0 and 1."""
    task_type = task.get("task_type", "action_decision")
    output = getattr(action, "content", "") or ""
    raw = grade_task(task_type, output)
    return round(max(0.01, min(0.99, raw)), 4)

def grade_all_tasks(action) -> dict:
    from app.tasks.easy import easy
    from app.tasks.medium import medium
    from app.tasks.hard import hard
    tasks = {"easy": easy(), "medium": medium(), "hard": hard()}
    return {
        name: {"score": grade(action, t), "description": t["description"]}
        for name, t in tasks.items()
    }
