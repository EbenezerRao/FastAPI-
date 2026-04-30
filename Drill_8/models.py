from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Tasks(Base):
    __tablename__ = "tasks"

    id =  Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_completed = Column(Boolean, index=True)