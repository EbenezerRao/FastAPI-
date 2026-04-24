import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import LocalSession, engine
from sqlalchemy.orm import Session
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

class OrganizerCreate(BaseModel):
    username: str
    password : str

@app.post('/api/v1/organizers/signup')
def reg_organizer(org_data: OrganizerCreate, db : Session = Depends(get_db)):
    org_id = str(uuid.uuid4())[:6]
    new_org = models.Organizer(
        id =  org_id,
        username = org_data.username,
        password = org_data.password
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return {
        'message' : 'Organizer successfully registered!',
        'org_id' : org_id
    }

@app.get('/api/v1/organizers/{org_id}')
def get_org(org_id : str, db: Session = Depends(get_db)):
    Req_id = db.query(models.Organizer).filter(models.Organizer.id == org_id).first()
    if not org_id:
        raise HTTPException(status_code=404, detail='Organizer not found')
    else:
        return Req_id
    
@app.put('/api/v1/organizers/{org_id}')
def update_org(org_id : str, org_data : OrganizerCreate, db : Session = Depends(get_db)):
    org = db.query(models.Organizer).filter(models.Organizer.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail='Organizer not found')
    org.username = org_data.username
    org.password = org_data.password
    db.commit()
    db.refresh(org)
    return org

@app.delete('/api/v1/organizers/{org_id}')
def delete_org(org_id : str, db : Session = Depends(get_db)):
    org = db.query(models.Organizer).filter(models.Organizer.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail='Organizer not found')
    db.delete(org)
    db.commit()
    return {'message' : 'Organizer deleted successfully'}