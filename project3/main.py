import uuid
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import LocalSession, engine
from pydantic import BaseModel
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class ProjectCreate(BaseModel):
    title : str
    tech_stack : str

class ProjectUpdate(BaseModel):
    tech_stack : str

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.post('/api/v1/projects')
def add_project(proj_data: ProjectCreate, db : Session = Depends(get_db)):
    proj_id = str(uuid.uuid4())[:6]
    new_proj = models.Project(
        title = proj_data.title,
        tech_stack = proj_data.tech_stack
    )
    db.add(new_proj)
    db.commit()
    db.refresh(new_proj)
    return new_proj

@app.get('/api/v1/projects')
def get_project(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@app.put('/api/v1/projects/{proj_id}')
def update_project(proj_id : str, proj_data : ProjectUpdate, db : Session = Depends(get_db)):
    proj = db.query(models.Project).filter(models.Project.id == proj_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail='Project not found')
    proj.tech_stack = proj_data.tech_stack
    db.commit()
    db.refresh(proj)
    return proj

@app.delete('/api/v1/projects/{proj_id}')
def delete_project(proj_id : str, db : Session = Depends(get_db)):
    proj = db.query(models.Project).filter(models.Project.id == proj_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail='Project not found')
    db.delete(proj)
    db.commit()
    return {'message' : 'Project deleted successfully'}