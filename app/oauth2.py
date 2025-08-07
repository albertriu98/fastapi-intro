from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from . import schemas, models
from fastapi import status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


SECRET_KEY = "0f1e36ee5523cb7d39185ddda81797e9bb192df7c497800f083d6f35a6a2b13e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) #convert to schema model
    except JWTError:
        raise credentials_exception


    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token_data =verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.email == token_data.id).first()   
 
    if user is None:
        raise credentials_exception
    
    return user