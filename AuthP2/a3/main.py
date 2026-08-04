from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError
import auth
import models
import database

app = FastAPI(title = 'Welcome to final project')

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/api/login')

class DeveloperCreate(BaseModel):
    username: str
    password: str
    
def get_current_user(token : str = Depends(oauth_scheme), db : Session = Depends(database.get_db)):
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
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
    
    dev = db.query(models.AsherDeveloper).filter(models.AsherDeveloper.username == username).first()
    if dev is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    return dev

@app.post('/api/register')
def create_developer(dev: DeveloperCreate, db: Session = Depends(database.get_db)):
    # Hash the password before saving
    hashed_pw = auth.encrypt_password(dev.password)
    
    new_dev = models.AsherDeveloper(
        username=dev.username,
        hashed_password=hashed_pw,
        role="Senior Dev"
    )
    db.add(new_dev)
    db.commit()
    return {"message": "Developer created successfully!"}

@app.post('/api/login')
def login(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.AsherDeveloper).filter(models.AsherDeveloper.username == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Incorrect username or password',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    access_token = auth.create_access_token(data = {'sub' : user.username})
    return({'access_token' : access_token, 'token_type' : 'bearer'})

@app.post('/api/refresh')
def refresh_access_token(refresh_token : str, db : Session = Depends(database.get_db)):
    try:
        payload = auth.jwt.decode(refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
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
        
    user = db.query(models.AsherDeveloper).filter(models.AsherDeveloper.username == username).first()
    
    if not user or user.refresh_token != refresh_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Could not validate credentials',
            headers = {'WWW-Authenticate': 'Bearer'}
        )
    
    new_access_token = auth.create_access_token(data = {'sub' : user.username})
    return({'access_token' : new_access_token, 'token_type' : 'bearer'})

@app.get('/api/dashboard')
def get_dashboard(current_dev : models.AsherDeveloper = Depends(get_current_user)):
    return {
        'message' : 'Welcome to the secure dashboard!',
        'your_role' : current_dev.role
    }
    
@app.put('/tasks/{task_id}/complete')
def update_task(task_id : int, current_dev : models.AsherDeveloper = Depends(get_current_user), db : Session = Depends(database.get_db)):
    task = db.query(models.AsherTask).filter(models.AsherTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    if not task.assigned_dev_username == current_dev.username:
        raise HTTPException(status_code=403, detail='You are not authorized to update this task')
    task.is_completed = True
    db.commit()
    db.refresh(task)
    return {
        'message' : 'Task updated successfully',
        'developer' : current_dev.username,
        'task' : task.title
    }