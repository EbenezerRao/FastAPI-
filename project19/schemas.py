from pydantic import BaseModel, Field
from typing import Optional

class SessionBase(BaseModel):
    title : str
    duration : int
    
class SessionCreate(SessionBase):
    duration : int = Field(ge=15)
    
class SessionResponse(SessionBase):
    id : int
    speaker_id : Optional[int] = None
    class Config:
        orm_mode = True
        from_attributes = True
        
class SpeakerBase(BaseModel):
    name : str
    expertise : str

class SpeakerCreate(SpeakerBase):
    pass

class SpeakerResponse(SpeakerBase):
    id : int
    sessions : list[SessionResponse] = []
    
    class Config:
        orm_mode = True
        from_attributes = True