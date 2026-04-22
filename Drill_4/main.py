from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import models
from database import LocalSession, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

class Destinations(BaseModel):
    id : str
    name : str
    description : str