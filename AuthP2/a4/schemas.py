from pydantic import BaseModel, Field
from typing import Optional

# --------------------------
# USER SCHEMAS
# --------------------------

# Received when registering a new developer
class UserCreate(BaseModel):
    username: str
    password: str

# Returned to the client (Hides password and sensitive tokens)
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Allows Pydantic to read ORM objects directly


# --------------------------
# TASK SCHEMAS
# --------------------------

# Base properties shared across schemas
class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, description="Task title must be at least 3 chars")

# Incoming payload when creating a task
class TaskCreate(TaskBase):
    assigned_dev_id: int

# Outgoing payload when returning task data to the client/React Native app
class TaskOut(TaskBase):
    id: int
    is_completed: bool
    assigned_dev_id: int

    class Config:
        from_attributes = True


# --------------------------
# AUTH / TOKEN SCHEMAS
# --------------------------

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None