from  pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title : str
    status : str
    priority : int = Field(ge= 1, le = 5 , description = "Priority must be between 1 and 5")
    
class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    class Config:
        from_attributes = True