from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def encrypt_password(password : str):
    return pswd_context.hash(password)

def verify_password(password : str, encrypted_password : str):
    return pswd_context.verify(password, encrypted_password)

def create_access_token(data : dict):
    encoded_data = data.copy()
    token_expiry = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({'exp' : token_expiry})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt 