from fastapi import FastAPI, Depends, HTTPException
import uuid
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import LocalSession, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Usercreate(BaseModel):
    hacker_id : str
    name : str  

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1/hackers')
def add_hacker(user_data: Usercreate, db: Session = Depends(get_db)):
    generated_id = str(uuid.uuid4())[:6]
    new_hacker = models.Hacker(
        generated_id=generated_id,
        name=user_data.name,
        role=user_data.role,
        is_checked_in= False
    )
    db.add(new_hacker)
    db.commit()
    db.refresh(new_hacker)
    return new_hacker

@app.get('/api/v1/hackers/')
def get_hacker(db: Session = Depends(get_db)):
    
    return db.query(models.Hacker).all()

@app.put('/api/v1/hackers/{hacker_id}/checkin')
def checkin(hacker_id: str, db: Session = Depends(get_db)):
    hacker = db.query(models.Hacker).filter(models.Hacker.id == hacker_id).first()
    if not hacker:
        raise HTTPException(status_code=404, detail='Hacker not found')
    hacker.is_checked_in = True
    db.commit()
    db.refresh(hacker)
    return hacker

@app.delete('/api/v1/hackers/{hacker_id}')
def del_hacker(hacker_id: str, db: Session = Depends(get_db)):
    hacker = db.query(models.Hacker).filter(models.Hacker.id == hacker_id).first()
    if not hacker:
        raise HTTPException(status_code=404, detail='Hacker not found')
    db.delete(hacker)
    db.commit()
    return {'message': 'Hacker deleted successfully'}

