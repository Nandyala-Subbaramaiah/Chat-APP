from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.chat_db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.crud import user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    return await user.create_user(
        db,
        user_data
    )


@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):

    return await user.get_users(db)