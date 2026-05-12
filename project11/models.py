from sqlalchemy import Column, Integer, String
from database import Base

class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(Integer, primary_key=True, index=True)
    restraunt_name = Column(String, index=True)
    dish_type = Column(String, index=True)
    rating = Column(Integer)