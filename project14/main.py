from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Base, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 600
)

@app.post('/clients/', response_model=schemas.ClientResponse)
def create_client(client : schemas.ClientCreate, db : Session = Depends(get_db)):
    new_client = models.Client(
        company_name = client.company_name,
        budget = client.budget
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

@app.delete('/clients/{client_id}', status_code=204)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return {
        'message' : 'Client deleted successfull2                                                                     '
    }