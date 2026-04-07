from datetime import datetime,timedelta
from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(data:dict):
    to_encode=data.copy()
    expires=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    
