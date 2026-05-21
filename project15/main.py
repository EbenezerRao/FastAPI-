from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from typing import Optional
import models
import schemas

models.base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

@app.post('/api/v1/meetup', response_model=schemas.MeetupResponse)
def create_meetup(meet : schemas.MeetupCreate, db : Session = Depends(get_db)):
    new_meetup = models.Meetup(
        title = meet.title,
        city = meet.city,
        max_seats = meet.max_seats
    )
    db.add(new_meetup)
    db.commit()
    db.refresh(new_meetup)
    return new_meetup

@app.get('/api/v1/meetups', response_model=list[schemas.MeetupResponse])
def get_meetups(city_filter: Optional[str] = None, db: Session = Depends(get_db)):
    
    # If the user hits /api/v1/meetups?city_filter=Prayagraj
    if city_filter:
        return db.query(models.Meetup).filter(models.Meetup.city == city_filter).all()
        
    # If they just hit /api/v1/meetups
    return db.query(models.Meetup).all()