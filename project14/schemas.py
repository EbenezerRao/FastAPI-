from pydantic import BaseModel
from typing import List

# --- DELIVERABLE SCHEMAS ---
class DeliverableBase(BaseModel):
    task_name: str
    status: str

class DeliverableCreate(DeliverableBase):
    pass

class DeliverableResponse(DeliverableBase):
    id: int
    client_id: int

    class Config:
        from_attributes = True


# --- CLIENT SCHEMAS ---
class ClientBase(BaseModel):
    company_name: str
    budget: int

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    deliverables: List[DeliverableResponse] = []

    class Config:
        from_attributes = True