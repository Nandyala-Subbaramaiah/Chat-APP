from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.chat_db import get_db
from app.models.conversation import Conversation


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post("/")
def create_conversation(
    db:Session=Depends(get_db)
):

    conversation = Conversation()

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation