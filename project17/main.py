from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import schemas
import models
from database import LocalSession, engine, get_db
from sqlalchemy.orm import Session
from typing import Optional

models.base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

@app.post('/initiatives/{initiative_id}/tasks', response_model=schemas.TaskResponse)
def create_task(task_data : schemas.TaskCreate, initiative_id : int, db : Session = Depends(get_db)):
    if db.query(models.Initiative).filter(models.Initiative.id == initiative_id).first() is None:
        raise HTTPException(status_code=404, detail='Initiative not found')
    new_task = models.Task(
        initiative_id = initiative_id,
        description = task_data.description,
        is_urgent = task_data.is_urgent,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get('/initiatives/{initiative_id}/tasks', response_model=list[schemas.TaskResponse])
def get_tasks(initiative_id : int, urgent_only : Optional[bool] = None, db : Session = Depends(get_db)):
    if db.query(models.Initiative).filter(models.Initiative.id == initiative_id).first() is None:
        raise HTTPException(status_code=404, detail='Initiative not found')
    if urgent_only is not None:
        query = query.filter(models.Task.is_urgent == urgent_only)
    return query.all()