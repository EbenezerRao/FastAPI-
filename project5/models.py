from sqlalchemy import Column, Integer, String
from database import Base

class Mentors(Base):
    __tablename__ = 'mentors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    expertise = Column(String, index=True)