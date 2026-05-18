from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, SessionLocal
import models
import schemas 
from typing import List, Optional

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

@app.post("/tasks/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Tasks(title=task.title, status=task.status, priority=task.priority)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get('/tasks', response_model=List[schemas.TaskResponse])
def get_tasks(filter_status: Optional[str] = None, db: Session = Depends(get_db)):
    
    # 1. If the user provided a status (e.g., ?filter_status=Open)
    if filter_status:
        # Tell the database: "WHERE status = 'Open'"
        tasks = db.query(models.Task).filter(models.Task.status == filter_status).all()
        return tasks
        
    # 2. If they didn't provide anything, give them the whole list
    tasks = db.query(models.Task).all()
    return tasks