from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    industry = Column(String)
    
    projects = relationship('Project', back_populates='client')
    
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String)
    price = Column(Integer)
    
    client_id = Column(Integer, ForeignKey('clients.id'))
    
    owner = relationship('Client', back_populates='projects')    