from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Request,HTTPException,status
from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import getdb
from models.usermodel import User
from datetime import datetime
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class myhttpbearer(HTTPBearer):
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    async def __call__(self, request:Request,db: Session = Depends(getdb)):
      
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        token = credentials.credentials

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token not found!")
        
        try:
            payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

            email=payload.get("sub")
            exp=payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        
            if not email:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email id not found!")
        
            user=db.query(User).filter(User.email==email).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found!")
            return user
            

        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        


            
