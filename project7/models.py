from sqlalchemy import Column, Integer, String
from database import base

class Score(base):
    __tablename__ = 'scores'
    
    id = Column(Integer, primary_key=True, index=True)
    stud_name = Column(String, index=True)
    subject = Column(String, index=True)
    score = Column(Integer)