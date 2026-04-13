import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import models
from database import LocalSession, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()

class DestinationCreate(BaseModel):
    city_name : str
    planned_budget : int

@app.post('/api/v1/destinations')
def add_destination(dest_data : DestinationCreate, db = Depends(get_db)):
    id = str(uuid.uuid4())[:6]
    new_dest = models.Destination(
        id=id,
        city_name=dest_data.city_name,
        planned_budget=dest_data.planned_budget
    )
    db.add(new_dest)
    db.commit()
    db.refresh(new_dest)
    return new_dest

class DestinationUpdate(BaseModel):
    city_name : str
    planned_budget : int

@app.put('/api/v1/destinations/{id}')
def update_destination(id : str, dest_data : DestinationUpdate, db = Depends(get_db)):
    dest = db.query(models.Destination).filter(models.Destination.id == id).first()
    if not dest:
        raise HTTPException(status_code=404, detail='Destination not found')
    dest.city_name = dest_data.city_name
    dest.planned_budget = dest_data.planned_budget
    db.commit()
    db.refresh(dest)
    return dest