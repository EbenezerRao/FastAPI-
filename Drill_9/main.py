from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class CoachingCreate(BaseModel):
    name: str
    subject: str
    rating: float

class CoachingUpdate(BaseModel):
    name: str
    subject: str
    rating: float

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

@app.post('/api/v1/centres')
def create_centre(centre_data : CoachingCreate, db : Session = Depends(get_db)):
    new_centre = models.Centre(
        name = centre_data.name,
        subject = centre_data.subject,
        rating = centre_data.rating
    )
    db.add(new_centre)
    db.commit()
    db.refresh(new_centre)
    return new_centre

@app.get('/api/v1/centres')
def get_centres(db : Session = Depends(get_db)):
    return db.query(models.Centre).all()

@app.get('/api/v1/centres/{centre_id}')
def get_centres_by_id(centre_id : int, db : Session = Depends(get_db)):
    centre = db.query(models.Centre).filter(models.Centre.id == centre_id).first()
    if not centre:
        raise HTTPException(status_code=404, detail='Centre not found')
    return centre

@app.put('/api/v1/centres/{centre_id}')
def update_centre(centre_id : int, centre_data : CoachingUpdate, db : Session = Depends(get_db)):
    centre = db.query(models.Centre).filter(models.Centre.id == centre_id).first()
    if not centre:
        raise HTTPException(status_code=404, detail='Centre not found')
    centre.name = centre_data.name
    centre.subject = centre_data.subject
    centre.rating = centre_data.rating
    db.commit()
    db.refresh(centre)
    return centre

@app.delete('/api/v1/centres/{centre_id}')
def delete_centre(centre_id : int, db : Session = Depends(get_db)):
    centre = db.query(models.Centre).filter(models.Centre.id == centre_id).first()
    if not centre:
        raise HTTPException(status_code=404, detail='Centre not found')
    db.delete(centre)
    db.commit()
    return {'message' : 'Centre deleted successfully'}