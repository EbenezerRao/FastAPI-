from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    client = Column(String, index=True)

    ai_project = relationship("AI_Model", back_populates="project", cascade="all, delete-orphan")
    
class AI_Model(Base):
    __tablename__ = 'ai_models'
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, index=True)
    accuracy_score = Column(String, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    
    project = relationship("Project", back_populates="ai_project")

