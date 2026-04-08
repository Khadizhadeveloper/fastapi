import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User


SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30


from fastapi.security import HTTPBearer
oauth2_scheme = HTTPBearer()

def hash_password(password:str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_token(data: dict) -> str:
    payload=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload["exp"] = expire
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


from fastapi.security import HTTPAuthorizationCredentials
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user=db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user








