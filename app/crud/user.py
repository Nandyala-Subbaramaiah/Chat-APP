from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.user import UserCreate
from app.auth import hash_password


async def create_user(
    db: AsyncSession,
    user: UserCreate
):

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password) if user.password else None,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_users(db: AsyncSession):

    result = await db.execute(select(User))
    return result.scalars().all()


async def set_password(
    db: AsyncSession,
    user_id: int,
    password: str,
):
    result = await db.execute(select(User).where(User.id == user_id))
    existing_user = result.scalar_one_or_none()

    if existing_user is None:
        return None

    existing_user.password_hash = hash_password(password)
    await db.commit()
    await db.refresh(existing_user)
    return existing_user