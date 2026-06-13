from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Speaker(Base):
    __tablename__ = 'speakers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    expertise = Column(String, nullable=False)
    
    sessions = relationship('Session', back_populates='speaker')
    
class Session(Base):
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    speaker_id = Column(Integer, ForeignKey('speakers.id'))
    
    speakers = relationship('Speaker', back_populates='sessions')