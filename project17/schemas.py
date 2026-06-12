from pydantic import BaseModel, Field
from typing import List

class TaskBase:
    description: str
    is_urgent: bool

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id : int
    initiative_id : int
    from_attributes = True
    
class InitiativeBase:
    title : str

class InitiativeCreate(InitiativeBase):
    budget : int = Field(gt = 5000)

class InitiativeResponse(InitiativeBase):
    id : int
    budget : List[TaskResponse]
    from_attributes = True