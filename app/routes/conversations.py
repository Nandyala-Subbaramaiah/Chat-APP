from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.chat_db import get_db
from app.models.conversation import Conversation
from app.models.conversation_member import ConversationMember

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

@router.post("/start/{user_id}")
def start_chat(
    user_id: int,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):

    # TEMPORARY:
    # replace this later with logged-in user
    current_user_id = 1


    # create conversation
    conversation = Conversation()

    db.add(conversation)
    db.commit()
    db.refresh(conversation)


    # add current user
    member1 = ConversationMember(
        conversation_id=conversation.id,
        user_id=current_user_id
    )


    # add selected user
    member2 = ConversationMember(
        conversation_id=conversation.id,
        user_id=user_id
    )


    db.add_all([
        member1,
        member2
    ])

    db.commit()


    return {
        "conversation_id": conversation.id
    }

@router.post("/start/{user_id}")
def start_chat(
    user_id: int,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):

    # TEMPORARY:
    # replace this later with logged-in user
    current_user_id = 1


    # create conversation
    conversation = Conversation()

    db.add(conversation)
    db.commit()
    db.refresh(conversation)


    # add current user
    member1 = ConversationMember(
        conversation_id=conversation.id,
        user_id=current_user_id
    )


    # add selected user
    member2 = ConversationMember(
        conversation_id=conversation.id,
        user_id=user_id
    )


    db.add_all([
        member1,
        member2
    ])

    db.commit()


    return {
        "conversation_id": conversation.id
    }