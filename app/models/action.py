from pydantic import BaseModel

class Action(BaseModel):
    action_type: str   # classify / reply / ignore
    content: str