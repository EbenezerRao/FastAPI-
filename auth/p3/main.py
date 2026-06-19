from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import auth 

app = FastAPI(title="Ebby doing the first excercise")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

fake_db = {
    "ebby": {
        "username": "ebby",
        # This is a sample Bcrypt hash for the password "123asher"
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq" 
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# 2. The Protected Route
@app.get('/api/dashboard')
def view_dashboard(token: str = Depends(oauth2_scheme)):
    # If they make it inside this function, the bouncer approved them!
    return {
        "message": "Welcome to the secure dashboard!",
        "your_wristband": token
    }