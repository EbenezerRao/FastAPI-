from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

# Assuming you have these files set up perfectly:
import auth
from database import get_db
from models import VaultUser

app = FastAPI()

# 1. The Bouncer
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/login')

# 2. The Upgraded VIP Host (Now talks to PostgreSQL)
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the wristband exactly like before
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={'WWW-Authenticate': 'Bearer'}
            )
            
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={'WWW-Authenticate': 'Bearer'}
        )
        
    # The Real Engine: Query PostgreSQL instead of a dictionary
    user = db.query(VaultUser).filter(VaultUser.username == username).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={'WWW-Authenticate': 'Bearer'}
        )
        
    # user is now a fully loaded SQLAlchemy object, not a dictionary
    return user

# 3. The Upload Gate (With Database Commits)
@app.post('/files/upload')
def upload_file(
    file_size_mb: int, 
    current_user: VaultUser = Depends(get_current_user),
    db: Session = Depends(get_db)  # We inject the database here too!
):
    # Because current_user is an object, we use dot-notation instead of brackets
    available_storage = current_user.storage_limit_mb - current_user.used_storage_mb
    
    if file_size_mb > available_storage:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient storage space. Upgrade your plan."
        )
    
    # Update the Python object
    current_user.used_storage_mb += file_size_mb
    
    # ⚡ THE MAGIC: Push the changes to PostgreSQL permanently
    db.commit()
    db.refresh(current_user)
    
    return {
        "message": f"File uploaded successfully, {current_user.username}!",
        "used_storage_mb": current_user.used_storage_mb
    }