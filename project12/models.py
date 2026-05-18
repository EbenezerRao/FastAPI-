from sqlalchemy import Column, Integer, String
from database import Base

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    priority = Column(Integer, index=True)
    status = Column(String, index=True)