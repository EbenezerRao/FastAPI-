from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import base

class Initiative(base):
    __tablename__ = 'initiatives'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    budget = Column(Integer)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship('Task', back_populates='initiatives', cascade="all, delete-orphan")
    
class Task(base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    is_urgent = Column(Boolean, index=True)
    initiative_id = Column(Integer, ForeignKey('initiatives.id'))
    initiatives = relationship('Initiative', back_populates='task')