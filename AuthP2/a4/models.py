from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)   
    refresh_token = Column(String, unique=True, index=True)
    
    tasks = relationship("Task", back_populates="owner")
    
class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    
    assigned_dev_id = Column(Integer, ForeignKey('users.id'))
    
    assignee = relationship('User', back_populates='tasks')