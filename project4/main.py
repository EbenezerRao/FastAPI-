from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import LocalSession, engine
import uuid
from sqlalchemy.orm import Session
import models

models.Base.metadata.create_all(bind=engine)

class SpeakerCreate(BaseModel):
    name : str
    topic : str

class SpeakerUpdate(BaseModel):
    topic : str

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close

app = FastAPI()

@app.post('/api/v1/speakers')
def add_speaker(speaker_data: SpeakerCreate, db : Session = Depends(get_db)):
    speaker_id = str(uuid.uuid4())[:6]
    new_speaker = models.Speaker(
        id = speaker_id,
        name = speaker_data.name,
        topic = speaker_data.topic
    )
    db.add(new_speaker)
    db.commit()
    db.refresh(new_speaker)
    return new_speaker

@app.get('/api/v1/speakers')
def get_speaker(db: Session = Depends(get_db)):
    return db.query(models.Speaker).all()

@app.put('/api/v1/speakers/{speaker_id}')
def update_speaker(speaker_id : str, speaker_data : SpeakerUpdate, db : Session = Depends(get_db)):
    speaker = db.query(models.Speaker).filter(models.Speaker.id == speaker_id).first()
    if not speaker:
        return HTTPException(status_code=404, detail='Speaker not found')
    speaker.topic = speaker_data.topic
    db.commit()
    db.refresh(speaker)
    return speaker

@app.delete('/api/v1/speakers/{speaker_id}')
def delete_speaker(speaker_id : str, db : Session = Depends(get_db)):
    speaker = db.query(models.Speaker).filter(models.Speaker.id == speaker_id).first()
    if not speaker:
        return HTTPException(status_code=404, detail='Speaker not found')
    db.delete(speaker)
    db.commit()
    return {'message' : 'Speaker deleted successfully'}