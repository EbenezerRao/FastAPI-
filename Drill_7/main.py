from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from  pydantic import BaseModel
from  database import LocalSession, engine
from sqlalchemy.orm import Session
import models
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

class CollegeCreate(BaseModel):
    name : str
    rating : float

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1/colleges')
def create_college(college: CollegeCreate, db : Session = Depends(get_db)):
    new_college = (
        models.Colleges(
            name = college.name,
            rating = college.rating
        )
    )
    db.add(new_college)
    db.commit()
    db.refresh(new_college)
    return new_college

@app.get('/api/v1/colleges')
def get_colleges(db : Session = Depends(get_db)):
    college = db.query(models.Colleges).all()
    return college

@app.get('/api/v1/colleges/{id}')
def get_college_by_id(id : int, db : Session = Depends(get_db)):
    college = db.query(models.Colleges).filter(models.Colleges.id == id).first()
    return college

@app.put('/api/v1/colleges/{id}')
def update_college(id : int, college_data : CollegeCreate, db : Session = Depends(get_db)):
    college = db.query(models.Colleges).filter(models.Colleges.id == id).first()
    if not college:
        raise HTTPException(status_code=404, detail='College not found')
    college.name = college_data.name
    college.rating = college_data.rating
    db.commit()
    db.refresh(college)
    return college

@app.delete('/api/v1/colleges/{id}')
def delete_college(id : int, db : Session = Depends(get_db)):
    college = db.query(models.Colleges).filter(models.Colleges.id == id).first()
    if not college:
        raise HTTPException(status_code=404, detail='College not found')
    db.delete(college)
    db.commit()
    return {'message' : 'College deleted successfully'}