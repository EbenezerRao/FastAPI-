import uuid
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel  

import models
from databse import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GigCreate(BaseModel):
    title: str
    payout_ruppess: int

@app.post('/api/v1/gigs')
def post_gig(gig_data: GigCreate, db: Session = Depends(get_db)):
    gig_id = str(uuid.uuid4())[:6]
    new_gig = models.Gig(
        id=gig_id,
        title=gig_data.title,
        payout_ruppess=gig_data.payout_ruppess
    )   
    db.add(new_gig)
    db.commit()
    db.refresh(new_gig)
    return {
        'message': 'Gig created successfully',
        'gig': {
            'id': new_gig.id,
            'title': new_gig.title,
            'payout_ruppess': new_gig.payout_ruppess
        }
    }

@app.get('/api/v1/gigs/{gig_id}')
def get_gig(gig_id: str, db = Depends(get_db)):
    if not gig_id:
        raise HTTPException(status_code=400, detail='Gig ID is required')
    else:
        return {
            'message': 'Gig retrieved successfully',
            'gig': {
                'id': gig_id,
                'title': 'Sample Gig Title',
            }
        }