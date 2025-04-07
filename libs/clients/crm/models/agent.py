from pydantic import BaseModel
from datetime import datetime


class Agent(BaseModel):
    id: str
    username: str
    team: str | None = None
    active: bool = False
