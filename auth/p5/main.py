from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import auth

app = FastAPI(title = 'Ebby Portal')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    max_age = 600
)

fake_db = {
    "arpita": {
        "username": "arpita",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq" 
    }
}

@app.post('/login')
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_db.get(form_data.username)
    
    if not user_dict:
        raise HTTPException(
            status = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    if not auth.verify_password(form_data.password, user_dict['hashed_password']):
        raise HTTPException(
            status = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    access_token = auth.create_access_token(data = {'sub' : user_dict['username']})
    return {'access_token': access_token, 'token_type': 'bearer'}