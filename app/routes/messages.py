from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.chat_db import get_db
from app.models.message import Message
from app.routes.websocket import manager
from app.schemas.message import MessageCreate, MessageResponse


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.post("/", response_model=MessageResponse)
async def send_message(
    data: MessageCreate,
    db: AsyncSession = Depends(get_db)
):

    msg = Message(
        conversation_id=data.conversation_id,
        sender_id=data.sender_id,
        message=data.message
    )

    db.add(msg)
    await db.commit()
    await db.refresh(msg)

    payload = {
        "type": "NEW_MESSAGE",
        "message": {
            "id": msg.id,
            "conversation_id": msg.conversation_id,
            "sender_id": msg.sender_id,
            "message": msg.message,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        },
    }

    await manager.broadcast(
        data.conversation_id,
        payload,
        user_id=data.sender_id,
    )

    return msg


@router.get("/{conversation_id}", response_model=list[MessageResponse])
async def get_messages(
    conversation_id:int,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Message).where(Message.conversation_id == conversation_id)
    )
    return result.scalars().all()