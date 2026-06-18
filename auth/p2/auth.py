from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

pswd_context = CryptContext(schemses=['bcrypt'], deprecated='auto')

def get_password_hash(password: str):
    return pswd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pswd_context.verify(plain_password, hashed_password)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data : dict):
    encoded_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({'exp' : expire})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt