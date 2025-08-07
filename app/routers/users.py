from fastapi import APIRouter
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import models, schemas, models
from fastapi.params import  Depends
from ..utils import hash


router = APIRouter(
    tags=["users"]
)

@router.post("/create_user", response_model=schemas.ResponseUser)
def create_user( user : schemas.User, db : Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    hashed_password = hash(new_user.password)
    new_user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user