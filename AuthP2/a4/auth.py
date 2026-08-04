from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pswd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def encrypt_password(password : str):
    return pswd_context.hash(password)

def verify_password(password : str, encrypted_password : str):
    return pswd_context.verify(password, encrypted_password)

def create_access_token(data: dict, expires_delta: int = 15):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt