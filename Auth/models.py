from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) 
    
    # 1:M Link - One user manages many centers
    centers = relationship("Centre", back_populates="owner")

class Centre(Base):
    __tablename__ = 'coaching_centres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    rating = Column(Float)
    
    # The Anchor - Locks this center to a specific user
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # The Reverse Link
    owner = relationship('User', back_populates='centers')