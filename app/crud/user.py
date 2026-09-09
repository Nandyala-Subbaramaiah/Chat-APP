from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.user import UserCreate


async def create_user(
    db: AsyncSession,
    user: UserCreate
):

    new_user = User(
        username=user.username,
        email=user.email
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_users(db: AsyncSession):

    result = await db.execute(select(User))
    return result.scalars().all()