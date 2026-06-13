from pydantic import BaseModel, Field
from typing import Optional

class ScoreBase(BaseModel):
    subject : str
    score : int
    
class ScoreCreate(ScoreBase): 
    score : int = Field(ge=0, le=100)
    pass

class ScoreResponse(ScoreBase):
    id : int
    student_id : int
    
    class Config:
        from_attributes = True
        
class StudentBase(BaseModel):
    name : str
    enrollment_no : str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id : int
    score : Optional[list[ScoreResponse]] = []
    
    class Config:
        from_attributes = True