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

class UserCreate(BaseModel):
    username: str
    email: str
    stud_id: int

@app.post('/api/v1/users')
def reg_user(user_data: UserCreate, db : Session = Depends(get_db)):
    user_id = str(uuid.uuid4())[:6]
    new_user = models.User(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        stud_id=user_data.stud_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        'message' : 'User successfully registered!',
        'user_id' : user_id
    }