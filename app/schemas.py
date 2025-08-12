from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class Post(BaseModel): # create schema
    title: str
    content: str
    published: bool = True #optional value with default value
    #rating: Optional[int] = None # optional field without default value.
    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    name: str
    password: str
    age: int

    class Config:
        orm_mode = True

class ResponseUser(BaseModel):
    email: EmailStr
    name: str

    class Config:
        orm_mode = True

class ReturnPosts(BaseModel):
    title: str
    content: str
    published: bool
    owner_id: str
    owner: ResponseUser

    class Config:
        orm_mode = True

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id : int
    dir: conint(le=1)