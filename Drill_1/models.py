from sqlalchemy import Column, Integer, String
from databse import Base
from practice.models import User

class Gig(Base):
    __tablename__ = 'gigs'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    payout_ruppess = Column(Integer, index=True)
