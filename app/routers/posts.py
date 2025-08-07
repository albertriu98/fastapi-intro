from fastapi import APIRouter, Response, status, HTTPException
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from fastapi.params import  Depends



router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


@router.get("/")
def get_posts(db : Session = Depends(get_db), get_user : int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    
    return {"data": posts}

@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #saying this URI only admits post method , path /upload
def upload(post: schemas.Post, db: Session = Depends(get_db), get_user: int = Depends(oauth2.get_current_user) ):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(get_user.email)
    return new_post

@router.get("/{id}") #epecting id from the user request
def get_post(id: str, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"post_detail": post}

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first()  != None:
        post.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_posts(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    query = db.query(models.Post).filter(models.Post.id == id) # this is the query
    post_check = query.first() # this returns an object

    if post_check == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No item found")
    
    query.update(post.dict(), synchronize_session=False) #update in db
    db.commit()

    return {"data": "sucess"}