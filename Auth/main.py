from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, auth
from database import engine, get_db
from jose import jwt, JWTError

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SHIELDS (PYDANTIC) ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class CentreCreate(BaseModel):
    name: str
    rating: float

# --- OAUTH2 SECURITY SETUP ---
# This creates the "Checkpoint" telling FastAPI where users log in
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """This function acts as the Bouncer checking the JWT Wristband."""
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Wristband")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Wristband")
        
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user

# --- ROUTES ---

@app.post('/api/v1/users', response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username taken")
    
    hashed_pw = auth.get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/api/v1/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Hand them the VIP wristband!
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post('/api/v1/centres')
def create_centre(centre: CentreCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Notice how we automatically attach the currently logged-in user's ID to the new center!
    new_centre = models.Centre(
        name=centre.name, 
        rating=centre.rating, 
        user_id=current_user.id
    )
    db.add(new_centre)
    db.commit()
    db.refresh(new_centre)
    return new_centre