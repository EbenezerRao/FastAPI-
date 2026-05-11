from pydantic import BaseModel
from typing import List

# ==========================================
# 1. PROJECT SCHEMAS (The Child)
# ==========================================
class ProjectBase(BaseModel):
    project_name: str
    price: int

class ProjectCreate(ProjectBase):
    pass # We don't need client_id here, because we will get it from the URL later!

class ProjectResponse(ProjectBase):
    id: int
    client_id: int

    # This tells Pydantic: "It's okay to read data directly from a SQLAlchemy database model"
    class Config:
        from_attributes = True 

# ==========================================
# 2. CLIENT SCHEMAS (The Parent)
# ==========================================
class ClientBase(BaseModel):
    company_name: str
    industry: str

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    # THE MAGIC TRICK: This tells FastAPI to nest all the related projects inside the client response!
    projects: List[ProjectResponse] = [] 

    class Config:
        from_attributes = True