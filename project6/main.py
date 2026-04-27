from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import LocalSession, engine
from sqlalchemy.orm import Session
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class SponsorCreate(BaseModel):
    company_name : str
    tier : str

class SponsorUpdate(BaseModel):
    tier : str

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1/sponsors')
def add_sponser(sponsor_data : SponsorCreate, db : Session = Depends(get_db)):
    new_sponser = models.Sponsors(
        company_name = sponsor_data.company_name,
        tier = sponsor_data.tier
    )
    db.add(new_sponser)
    db.commit()
    db.refresh(new_sponser)
    return new_sponser

@app.get('/api/v1/sponsors')
def get_sponsor(db : Session = Depends(get_db)):
    return db.query(models.Sponsors).all()

@app.put('/api/v1/sponsors/{sponsor_id}')
def update_speaker(speakerdetails : SponsorUpdate, sponsor_id : int , db : Session = Depends(get_db)):
    sponsor = db.query(models.Sponsors).filter(models.Sponsors.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail='Sponsor not found')
    sponsor.tier = speakerdetails.tier
    db.commit()
    db.refresh(sponsor)
    return sponsor

@app.delete('/api/v1/sponsors/{sponsor_id}')
def delete_sponsor(sponsor_id : int, db : Session = Depends(get_db)):
    sponsor = db.query(models.Sponsors).filter(models.Sponsors.id == sponsor_id).first()
    if not sponsor:
        raise HTTPException(status_code=404, detail='Sponsor not found')
    db.delete(sponsor)
    db.commit()
    return {'message' : 'Sponsor deleted successfully'}