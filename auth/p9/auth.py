from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_password(password : str):
    return pswd_context.hash(password)

def verify_password(plain_password : str, encrypted_password : str):
    return pswd_context.verify(plain_password, encrypted_password)

def create_access_token(data : dict):
    encrypted_data = data.copy()
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    encrypted_data.update({'exp' : expiry_time})
    encrypted_jwt = jwt.encode(encrypted_data, SECRET_KEY, algorithm = ALGORITHM)
    return encrypted_jwt