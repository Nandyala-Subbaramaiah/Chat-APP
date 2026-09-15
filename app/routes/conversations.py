from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.chat_db import get_db
from app.models.conversation import Conversation
from app.models.conversation_member import ConversationMember
from app.schemas.conversation import (
    ConversationResponse,
    ConversationStartResponse,
)

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


@router.post("/", response_model=ConversationResponse)
async def create_conversation(
    db: AsyncSession = Depends(get_db)
):

    conversation = Conversation()

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)

    return conversation

@router.post("/start/{user_id}", response_model=ConversationStartResponse)
async def start_chat(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):

    # TEMPORARY:
    # replace this later with the logged-in user
    current_user_id = 1

    conversation = Conversation()
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)

    member1 = ConversationMember(
        conversation_id=conversation.id,
        user_id=current_user_id
    )
    db.add(member1)

    if user_id != current_user_id:
        member2 = ConversationMember(
            conversation_id=conversation.id,
            user_id=user_id
        )
        db.add(member2)

    await db.commit()


    return {
        "conversation_id": conversation.id
    }