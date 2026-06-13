from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Base, engine
import models
import schemas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 600
)

models.Base.metadata.create_all(bind=engine)


@app.post('/students', response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(
        name=student.name,
        enrollment_no=student.enrollment_no
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post('/students/{student_id}/scores', response_model = schemas.ScoreResponse)
def create_score(student_id : int, score : schemas.ScoreCreate, db : Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    new_score = models.StudentScore(
        student_id = student_id,
        subject = score.subject,
        score = score.score
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score

@app.get('/scores/top-performers', response_model = list[schemas.StudentResponse])
def get_top_performer(subject_name : str, min_score : int, db : Session = Depends(get_db)):
    students = db.query(models.Student).join(models.StudentScore).filter(
        models.StudentScore.subject == subject_name, 
        models.StudentScore.score >= min_score).all()
    return students

@app.put('/students/{student_id}/scores/{score_id}', response_model = schemas.ScoreResponse)
def update_score(student_id : int, score_id : int, score_update : schemas.ScoreCreate, db : Session = Depends(get_db)):
    score = db.query(models.StudentScore).filter(models.StudentScore.id == score_id, models.StudentScore.student_id == student_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    score.subject = score_update.subject
    score.score = score_update.score
    db.commit()
    db.refresh(score)
    return score

@app.delete('/students/{student_id}/scores/{score_id}')
def delete_score(student_id : int, score_id : int, db : Session = Depends(get_db)):
    score = db.query(models.StudentScore).filter(models.StudentScore.id == score_id, models.StudentScore.student_id == student_id).first()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    db.delete(score)
    db.commit()
    return {"detail": "Score deleted successfully"}