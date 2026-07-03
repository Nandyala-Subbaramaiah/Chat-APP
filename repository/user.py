from models.model import User
from schemas.schema import UserBase
from sqlalchemy.orm import Session

from uuid import uuid4

def create_user(db: Session, user: UserBase):
    db_user = User(
        id=str(uuid4()),
        phone=user.phone,
        username=user.username,
        profile_pic=user.profile_pic,
        about=user.about,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
