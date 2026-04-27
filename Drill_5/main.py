from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import LocalSession, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class RoomCreate(BaseModel):
    name : str
    capacity : int

class RoomUpdate(BaseModel):
    capacity : int

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1/rooms')
def add_room(room_data : RoomCreate,  db : Session = Depends(get_db)):
    new_room = models.Rooms(
        name = room_data.name,
        capacity = room_data.capacity
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

@app.get('/api/v1/rooms')
def get_room(db : Session = Depends(get_db)):
    return db.query(models.Rooms).all()

@app.put('/api/v1/rooms/{room_id}')
def update_room(room_id : int, room_data :  RoomUpdate, db : Session = Depends(get_db)):
    room = db.query(models.Rooms).filter(models.Rooms.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')
    room.capacity = room_data.capacity
    db.commit()
    db.refresh(room)
    return room

@app.delete('/api/v1/rooms/{room_id}')
def delete_room(room_id : int, db : Session = Depends(get_db)):
    room = db.query(models.Rooms).filter(models.Rooms.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail='Room not found')
    db.delete(room)
    db.commit()
    return {'message' : 'Room deleted successfully'}