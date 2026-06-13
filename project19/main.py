from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Base, engine
import models
import schemas
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 600
)

models.Base.metadata.create_all(bind=engine)

@app.post('/speakers/{speaker_id}/sessions', response_model = schemas.SessionResponse)
def create_session(speaker_id : int, session : schemas.SessionCreate, db : Session = Depends(get_db)):
    speaker = db.query(models.Speaker).filter(models.Speaker.id == speaker_id).first()
    if not speaker:
        raise HTTPException(status_code=404, detail="Speaker not found")
    new_session = models.Session(
        title = session.title,
        duration = session.duration,
        speaker_id = speaker_id
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.get('/sessions', response_model=list[schemas.SessionResponse])
def get_sessions(min_duration : Optional[int] = None, db : Session = Depends(get_db)):
    sessions = db.query(models.Session)
    
    if min_duration is not None:
        sessions = sessions.filter(models.Session.duration >= min_duration).all()
    return sessions