from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users, authentication, votes
from prometheus_fastapi_instrumentator import Instrumentator


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(authentication.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

