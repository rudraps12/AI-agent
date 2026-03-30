from pydantic import BaseModel
from typing import List

class Observation(BaseModel):
    email: str
    sender: str
    subject: str
    history: List[str]
    current_tasks: List[str]
    calendar: List[str]