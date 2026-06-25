from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import auth  # Assume your auth file with SECRET_KEY and jwt is here

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = '/login')

stream_db = {
    "user_basic": {
        "username": "user_basic",
        "subscription_tier": "basic"
    },
    "user_premium": {
        "username": "user_premium",
        "subscription_tier": "premium"
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
        
    user_dict = stream_db.get(username)
    
    if user_dict is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    return user_dict

@app.get('/movies/4k-stream')
def get_4k_stream(user : dict = Depends(get_current_user)):
    if user['subscription_tier'] == 'basic':
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'Upgrade to premium to watch in 4K.'
        )
    else:
        return {
            'message' : f"Enjoy the 4K stream, {user['username']}!",
            "stream_url": "https://streamflix.com/play/4k/12345"
        }