from fastapi import APIRouter, Response, status, HTTPException
from ..database import  get_db
from sqlalchemy.orm import Session
from .. import schemas, oauth2, models
from fastapi.params import  Depends


router = APIRouter(
    prefix="/votes",
    tags=["votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.email)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.email} has already liked this post {found_vote.post_id}")
        new_vote = models.Vote(user_id= current_user.email, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Succesfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote {vote.post_id} does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote deleted"}
