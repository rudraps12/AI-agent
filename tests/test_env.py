from app.env.environment import EmailEnv
from app.models.action import Action

env = EmailEnv()

obs = env.reset()
print("Step 1 Observation:", obs)

action = Action(
    action_type="reply",
    content="I will attend the meeting and send the report ASAP"
)

for i in range(3):
    obs, reward, done, _ = env.step(action)
    print(f"\nStep {i+2} Observation:", obs)
    print("Reward:", reward)