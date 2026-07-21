from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.database.chat_db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    return user.create_user(
        db,
        user_data
    )


@router.get("/", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):

    return user.get_users(db)