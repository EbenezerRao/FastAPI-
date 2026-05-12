from pydantic import BaseModel
from database import Base

class Lead(BaseModel):
    client_name: str
    project_name: str
    budget: int
    
class LeadCreate(Base):
    pass

class LeadResponse(BaseModel):
    id : int
    client_name: str
    project_name: str
    budget: int
    
    class Config:
        form_attributes = True