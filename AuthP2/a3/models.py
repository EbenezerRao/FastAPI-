from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class AsherDeveloper(Base):
    __tablename__ = 'asher_developer'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String, default="Developer")
    hashed_password = Column(String)
    refresh_token = Column(String, nullable=True)

class AsherTask(Base):
    __tablename__ = "asher_tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    assigned_dev_username = Column(String)
    is_completed = Column(Boolean, default=False)