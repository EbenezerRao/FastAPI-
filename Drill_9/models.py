from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Centre(Base):
    __tablename__ = 'coaching_centres'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String, index=True)
    rating = Column(Float, index=True)
    
    # THE ANCHOR - The "Many" side wears the nametag pointing to the "One" side
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # THE REVERSE LINK
    owner = relationship('User', back_populates='centers')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) # We NEVER save plain text passwords
    
    # THE MAGIC LINK (1:M) - A user can manage multiple coaching centers
    centers = relationship("Centre", back_populates="owner")