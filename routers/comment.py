from fastapi import APIRouter, Depends

from sqlalchemy.orm.session import Session
from db.database import get_db

from db.db_comment import create_post, get_all
from routers.schemas import CommentsBase, UserAuth

from auth.oauth2 import get_current_user


router = APIRouter(prefix="/comment", tags=["comment"])


@router.get("/all/{post_id}")
def get(post_id: int, db: Session = Depends(get_db)):
    return get_all(db, post_id)


@router.post("/")
def create(
    request: CommentsBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    return create_post(
        db,
        request,
    )
