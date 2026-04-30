from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import LocalSession, engine
import models
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

class TaskCreate(BaseModel):
    task : str

class TaskUpdate(BaseModel):
    title : str
    is_completed : bool

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1]tasks')
def create_tasks(tasks : TaskCreate, db : Session = Depends(get_db)):
    new_task = models.Tasks(title = tasks.task, is_completed = False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get('/api/v1/tasks')
def get_tasks(db : Session = Depends(get_db)):
    return db.query(models.Tasks).all()

@app.get('/api/v1/tasks/{task_id}')
def get_task(task_id : int, db : Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

@app.put('/api/v1/tasks/{task_id}')
def update_task(task_id : int, task_data : TaskUpdate, db : Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:    
        raise HTTPException(status_code=404, detail='Task not found')
    task.title = task_data.title
    task.is_completed = task_data.is_completed
    db.commit()
    db.refresh(task)
    return task

@app.delete('/api/v1/tasks/{task_id}')
def delete_task(task_id : int, db : Session = Depends(get_db)):
    task = db.query(models.Tasks).filter(models.Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    db.delete(task)
    db.commit()
    return {'message' : 'Task deleted successfully'}