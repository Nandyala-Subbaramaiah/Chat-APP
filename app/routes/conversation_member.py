from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.chat_db import get_db
from app.models.conversation_member import ConversationMember


router = APIRouter(
    prefix="/conversation-members",
    tags=["Conversation Members"]
)


@router.post("/")
def add_user_to_conversation(
    conversation_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):

    member = ConversationMember(
        conversation_id=conversation_id,
        user_id=user_id
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member

