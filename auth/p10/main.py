from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
import auth  # Assume your auth file with SECRET_KEY and jwt is here

app = FastAPI()

# Starter Database
vault_db = {
    "user_free": {
        "username": "user_free",
        "storage_limit_mb": 50,
        "used_storage_mb": 45
    },
    "user_pro": {
        "username": "user_pro",
        "storage_limit_mb": 1000,
        "used_storage_mb": 200
    }
}

oauth_scheme = OAuth2PasswordBearer(tokenUrl = '/api/login')

def get_current_user(token : str = Depends(oauth_scheme)):
    try:
        payload = auth.JWT.decode(token, auth.SECRET_KEY, algorithms = [auth.ALGORITHM])
        username : str = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = 'Could not validate credentials',
                headers = {'WWW-Authenticate': 'Bearer'}
            )
            
    except JWTError:
        raise  HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
        
    user_dict = vault_db.get(username)
    
    if user_dict is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
        
    return user_dict

@app.post('/files/upload')
def upload_file(file_size : int, current_user : dict = Depends(get_current_user)):
    available_storage = current_user['storage_limit_mb'] - current_user['used_storage_mb']
    if file_size > available_storage:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'Insufficient storage space. Upgrade your plan.'
        )
    else:
        current_user['used_storage_mb'] += file_size
        return {
            'message': f"File uploaded successfully",
            'used_storage_mb': current_user['used_storage_mb']
        }