from typing import List
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException, status
from auth.oauth2 import get_current_user

from db.database import get_db

from sqlalchemy.orm.session import Session

from routers.schemas import PostBase, PostDisplay, UserAuth

from db.db_post import create_post, delete_post, get_posts

import random
import string
import shutil

router = APIRouter(prefix="/post", tags=["posts"])


image_url_types = ["absolute", "relative"]


@router.post("", response_model=PostDisplay)
def create(
    request: PostBase,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    if not request.image_url_type in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter image_url_type can only take values 'absolute' or 'relative'.",
        )
    return create_post(db, request)


@router.get("/all", response_model=List[PostDisplay])
def posts(
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    return get_posts(db)


@router.post("/image")
def upload_file(image: UploadFile = File(...)):
    letter = string.ascii_letters
    rand_str = "".join(random.choice(letter) for i in range(6))
    new = f"_{rand_str}."
    filename = new.join(image.filename.rsplit(".", 1))
    path = f"images/{filename}"

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}


@router.delete("/{id}")
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuth = Depends(get_current_user),
):
    return delete_post(db, id, current_user.id)
