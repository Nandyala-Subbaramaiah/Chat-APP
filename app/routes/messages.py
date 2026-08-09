from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.chat_db import get_db
from app.models.message import Message
from app.routes.websocket import manager
from app.schemas.message import MessageCreate


router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)


@router.post("/")
async def send_message(
    data: MessageCreate,
    db: Session = Depends(get_db)
):

    msg = Message(
        conversation_id=data.conversation_id,
        sender_id=data.sender_id,
        message=data.message
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

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


@router.get("/{conversation_id}")
def get_messages(
    conversation_id:int,
    db:Session=Depends(get_db)
):

    return db.query(Message)\
        .filter(
            Message.conversation_id == conversation_id
        ).all()