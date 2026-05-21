from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import base

class Meetup(base):
    __tablename__ = "meetups"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    city = Column(String, index=True)
    max_seats = Column(Integer)
    reservations = relationship('Attendee', back_populates='meetup', cascade="all, delete-orphan")
    
class Attendee(base):
    __tablename__ = 'attendees'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String, index=True)
    meetup_id = Column(Integer, ForeignKey('meetups.id'))
    
    meetup = relationship('Meetup', back_populates='reservations')