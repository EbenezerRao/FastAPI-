from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    max_age = 600
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/reviews', response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db : Session = Depends(get_db)):
    new_review = models.Review(
        restraunt_name = review.restraunt_name,
        dish_type = review.dish_type,
        rating = review.rating
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@app.get('/reviews', response_model=list[schemas.ReviewResponse])
def get_reviews(db : Session = Depends(get_db)):
    reviews = db.query(models.Review).all()
    return reviews

@app.get('/review/top', response_model=list[schemas.ReviewResponse])
def get_top_reviews(db : Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.rating >= 8).all()
    return reviews

@app.put('/reviews/{review_id}', response_model=schemas.ReviewResponse)
def update_review(review_id : int, updated_data : schemas.ReviewCreate, db : Session = Depends(get_db)):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not db_review: 
        raise HTTPException(status_code=404, detail="Review not found")
    db_review.rating = updated_data.rating
    db.commit()
    db.refresh(db_review)
    return db_review

@app.delete('/reviews/{review_id}')
def delete_review(review_id : int, db : Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review: 
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}