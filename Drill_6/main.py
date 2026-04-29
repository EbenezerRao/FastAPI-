from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import LocalSession, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- THE SHIELD (Pydantic) ---
class ClientCreate(BaseModel):
    name: str
    deliverable: str
    status: str

# This is the dependency that hands a database connection to your routes!

# --- THE CREATOR ---
@app.post("/api/clients")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = models.Client(
        name=client.name, 
        deliverable=client.deliverable, 
        status=client.status
        )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client

# ==========================================
# 🛠️ THE SOLUTIONS
# ==========================================

# 🔥 CHALLENGE 1: THE FILTER
@app.get("/api/clients/search/{status}")
def get_clients_by_status(status: str, db: Session = Depends(get_db)):
    # Look how clean this is compared to the raw Python loop!
    # "Query the Client table, filter by status, and grab all matches."
    clients = db.query(models.Client).filter(models.Client.status == status).all()
    return clients

# 🔥 CHALLENGE 2: THE ERASER
@app.delete("/api/clients/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    # 1. Find the specific client (.first() stops searching after it finds one)
    target_client = db.query(models.Client).filter(models.Client.id == client_id).first()
    
    # 2. If the client doesn't exist, throw a 404 error back to the user
    if not target_client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    # 3. If they DO exist, delete them and commit to the hard drive
    db.delete(target_client)
    db.commit()
    
    return {"message": f"Client {client_id} successfully deleted"}