print("File is running...")
from models.observation import Observation
from models.action import Action
from models.reward import Reward

obs = Observation(
    email="Meeting at 5 PM",
    sender="boss@company.com",
    subject="Urgent meeting",
    history=[]
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