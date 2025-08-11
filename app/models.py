from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlmodel import Field, SQLModel, create_engine

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(String, ForeignKey("users.email", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    age = Column(Integer, nullable=False)


# class Heroe(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     secret_name :str
#     age: int | None = None

