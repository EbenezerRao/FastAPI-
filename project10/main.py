from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import SessionLocal, engine

# Create the tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Asher Lead Tracker")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ROUTES
# ==========================================

@app.get("/")
def read_root():
    return {"message": "Asher Lead Tracker API is Online"}

# CREATE: Add a new lead
@app.post("/leads", response_model=schemas.LeadResponse)
def create_new_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    db_lead = models.Lead(
        client_name=lead.client_name,
        project_type=lead.project_type,
        budget=lead.budget
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

# READ: Get all leads
@app.get("/leads", response_model=List[schemas.LeadResponse])
def get_all_leads(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    return leads

# DELETE: Remove a lead (to keep the list clean)
@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(db_lead)
    db.commit()
    return {"message": f"Lead for {db_lead.client_name} has been removed."}