from pydantic import BaseModel, Field
from typing import List

class AttendeeBase(BaseModel):
    name : str
    role : str
    
class AttendeeCreate(AttendeeBase):
    pass

class AttendeeResponse(AttendeeBase):
    id : int
    meetup_id : int
    
    class Config:
        form_attributes = True

class MeetupBase(BaseModel):
    title : str
    city : str

class MeetupCreate(MeetupBase):
    max_seats : int = Field(ge = 10)
    
class MeetupResponse(MeetupBase):
    id : int
    max_seats = list[AttendeeResponse] = []
    
    class Config:
        form_attributes = True