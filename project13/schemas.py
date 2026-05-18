from pydantic import BaseModel
from typing import List

# --- 1. DELIVERABLE SCHEMAS (The Child) ---
class DeliverableBase(BaseModel):
    task_name: str
    status: str

class DeliverableCreate(DeliverableBase):
    pass

class DeliverableResponse(DeliverableBase):
    id: int
    client_id: int  # Proves which client this belongs to

    class Config:
        from_attributes = True


# --- 2. CLIENT SCHEMAS (The Parent) ---
class ClientBase(BaseModel):
    company_name: str
    budget: int

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    # 🎯 THE MAGIC GATE: Automatically formats the SQLAlchemy relationship into a JSON list!
    deliverables: List[DeliverableResponse] = []

    class Config:
        from_attributes = True