from pydantic import BaseModel, Field
from typing import Optional

class ModelBase(BaseModel):
    version : str
    accuracy_score : str
    
class ModelCreate(ModelBase):
    accuracy_score : str = Field(ge=0, le=100)
    pass

class ModelResponse(ModelBase):
    id : int
    project_id : int
    
    class Config:
        from_attributes = True
        
class ProjectBase(BaseModel):
    title : str
    client : str
    
class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id : int
    ai_project : Optional[list[ModelResponse]] = []
    
    class Config:
        from_attributes = True