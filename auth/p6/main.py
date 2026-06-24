import auth
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import auth

app = FastAPI()

speaker_db = {
    "arpita_j": {
        "username": "arpita_j",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq"
    }
}

@app.post('/speaker/login')
def create_speaker(form_data : OAuth2PasswordRequestForm = Depends()):
    user_dict = speaker_db.get(form_data.username)
    
    if not user_dict:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    if not auth.verify_password(form_data.password, user_dict['hashed_password']):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
        
    access_token = auth.create_access_token(data = {'sub' : user_dict['username']})
    return {'access_token' : access_token,  'token_type' : 'bearer'}