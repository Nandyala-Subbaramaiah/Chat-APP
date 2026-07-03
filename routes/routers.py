from schemas.schema import UserOut, UserBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from repository.user import create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
def register_user(request: UserBase, db: Session = Depends(get_db)):
    return create_user(db, request)
