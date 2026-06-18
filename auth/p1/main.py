from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Importing the tools you just built in auth.py!
from auth import verify_password, create_access_token

app = FastAPI(title="Asher Portal API")

# Fake database for the drill 
# (In production, you will query your PostgreSQL database here)
fake_db = {
    "ebby": {
        "username": "ebby",
        # This is a sample Bcrypt hash for the password "123asher"
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq" 
    }
}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Grab the user from the database using the username typed in the form
    user_dict = fake_db.get(form_data.username)
    
    # 2. Bouncer Check 1: Does the user exist at all?
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Bouncer Check 2: Use your auth.py function to check the password against the hash
    if not verify_password(form_data.password, user_dict["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 4. They passed! Use your auth.py factory to print the VIP wristband (JWT)
    access_token = create_access_token(data={"sub": user_dict["username"]})
    
    # 5. Hand the wristband back to the frontend
    return {"access_token": access_token, "token_type": "bearer"}