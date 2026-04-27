from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import LocalSession, engine
import uuid
import models
from  pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class MentorCreate(BaseModel):
    name : str
    expertise : str

class MentorUpdate(BaseModel):
    expertise : str

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1/mentors')
def add_mentor(mentor_data : MentorCreate, db : Session = Depends(get_db)):
    new_mentor = models.Mentors(
        name = mentor_data.name,
        expertise = mentor_data.expertise
    )
    db.add(new_mentor)
    db.commit()
    db.refresh(new_mentor)
    return new_mentor

@app.get('/api/v1/mentors')
def get_speeaker(db : Session = Depends(get_db)):
    return db.query(models.Mentors).all()

@app.put('/api/v1/mentors/{mentor_id}')
def update_speaker(mentor_id : str, mentor_data : MentorUpdate, db : Session = Depends(get_db)):
    mentor = db.query(models.Mentors).filter(models.Mentors.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail='Speaker not found')
    mentor.expertise = mentor_data.expertise
    db.commit()
    db.refresh(mentor)
    return mentor

@app.delete('/api/v1/mentors/{mentor_id}')
def delete_speaker(mentor_id : str, db : Session = Depends(get_db)):
    mentor = db.query(models.Mentors).filter(models.Mentors.id == mentor_id).first()
    if not mentor:
        raise HTTPException(status_code=404, detail='Speaker not found')
    db.delete(mentor)
    db.commit()
    return {'message' : 'Speaker deleted successfully'}