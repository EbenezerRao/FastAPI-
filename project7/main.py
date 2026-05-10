from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import LocalSession, engine
import models
from pydantic import BaseModel

app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 600
)

class ScoreCreate(BaseModel):
    stud_name : str
    subject : str
    score : int
    
@app.post('/api/v1/scores')
def create_score(score : ScoreCreate, db : Session = Depends(get_db)):
    new_score = models.Score(
        id = len(db.query(models.Score).all()) + 1,
        stud_name = score.stud_name,
        subject = score.subject,
        score = score.score
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@app.get('/api/v1/scores')
def get_all_scores(db : Session = Depends(get_db)):
    score = db.query(models.Score).all()
    return score

@app.get('/api/v1/scores/{score_id}')
def get_score(score_id : str, db : Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if not score :
        raise HTTPException(status_code=404, detail="Score not found")
    return score

@app.put('/api/v1/scores/{score_id}')
def update_score(score_id : str, score : ScoreCreate, db : Session = Depends(get_db)):
    existing_score =  db.query(models.Score).filter(models.Score.id == score_id).first()
    if not existing_score :
        raise HTTPException(status_code=404, detail="Score not found")
    existing_score.score = score.score
    db.commit()
    db.refresh(existing_score)
    return existing_score

@app.delete('/api/v1/scores/{score_id}')
def delete_score(score_id : str, db : Session = Depends(get_db)):
    score = db.query(models.Score).filter(models.Score.id == score_id).first()
    if not score :
        raise HTTPException(status_code=404, detail="Score not found")
    db.delete(score)
    db.commit()
    return {"detail" : "Score deleted successfully"}