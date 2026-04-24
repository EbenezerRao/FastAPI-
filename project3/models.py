from sqlalchemy import Column, Integer, String
from database import Base

class Project(Base):
    __tablename__ = 'Project'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    tech_stack = Column(String, index=True)
