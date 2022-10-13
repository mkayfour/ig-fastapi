from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm.session import Session

from db.db_user import create_user

from routers.schemas import UserBase, UserDisplay

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserDisplay)
def create_new_user(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)
