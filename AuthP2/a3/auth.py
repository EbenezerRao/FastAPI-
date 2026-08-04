from datetime import timezone, timedelta, datetime
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 30

pswd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def encrypt_password(password : str):
    return pswd_context.hash(password)

def verify_password(plain_pswd : str, encrypted_pswd : str):
    return pswd_context.verify(plain_pswd, encrypted_pswd)

def create_access_token(data : dict):
    encoded_data = data.copy()
    expire_time = datetime.now(timezone.utc) + timezone(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({'exp' : expire_time})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt

def create_refresh_token(data : dict):
    encoded_data = data.copy()
    expire_time = datetime.now(timezone.utc) + timezone(minutes = REFRESH_TOKEN_EXPIRE_MINUTES)
    encoded_data.update({'exp' : expire_time})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt