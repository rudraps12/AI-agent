print("File is running...")
from app.models.observation import Observation
from app.models.action import Action
from app.models.reward import Reward
obs = Observation(
    email="Meeting at 5 PM",
    sender="boss@company.com",
    subject="Urgent meeting",
    history=[],
    current_tasks=["attend meeting"],
    calendar=["Meeting at 5 PM"],
)

act = Action(
    action_type="reply",
    content="I will attend the meeting"
)

rew = Reward(
    score=0.9,
    reason="Good reply"
)

print(obs)
print(act)
print(rew)
