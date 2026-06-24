import auth
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'client/login')

client_db = {
    "client_01": {
        "username": "client_01",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq",
        "is_active": False  # This client hasn't paid!
    }
}

def get_current_user(token : str = Depends(oauth2_scheme)):
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms = [auth.ALGORITHM])
        username : str = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = 'Could not validate credentials',
                headers = {'WWW-Authenticate': 'Bearer'}
            )
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    user_dict = client_db.get(username)
    
    if user_dict is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
        
    return user_dict

@app.post('/client/login')
def login(form_data : OAuth2PasswordRequestForm = Depends()):
    user_dict = client_db.get(form_data.username)
    
    if not user_dict:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
        
    if not auth.verify_password(form_data.password, user_dict['hashed_password']):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
        
    if user_dict['is_active'] == False:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Inactive User'
        )
        
    access_token = auth.create_access_token(data = {'sub' : user_dict['username']})
    return {'access_token' : access_token, 'token_type' : 'bearer'}

@app.get('/api/dashboard')
def view_dashboard(current_client: dict = Depends(get_current_user)):
    return {
        "message": f"Welcome to the secure dashboard, {current_client['username']}!",
        "billing_status": "Active" if current_client['is_active'] else "Suspended",
        "client_data": current_client
    }