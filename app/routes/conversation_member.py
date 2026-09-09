from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.chat_db import get_db
from app.models.conversation_member import ConversationMember
from app.schemas.conversation_member import ConversationMemberResponse


router = APIRouter(
    prefix="/conversation-members",
    tags=["Conversation Members"]
)


@router.post("/", response_model=ConversationMemberResponse)
async def add_user_to_conversation(
    conversation_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
):

    member = ConversationMember(
        conversation_id=conversation_id,
        user_id=user_id
    )

    db.add(member)
    await db.commit()
    await db.refresh(member)

    return member

