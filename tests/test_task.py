from app.models.action import Action
from app.tasks.easy import easy
from app.tasks.medium import medium
from app.tasks.hard import hard
from app.tasks.grader import grade


action = Action(
    action_type="reply",
    content="I will attend the meeting and send the report ASAP"
)

tasks = [easy(), medium(), hard()]

for i, task in enumerate(tasks):
    score = grade(action, task)
    print(f"Task {i+1} Score:", score)