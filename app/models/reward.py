from pydantic import BaseModel

class Reward(BaseModel):
    score: float
    reason: str