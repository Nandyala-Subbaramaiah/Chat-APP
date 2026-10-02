from datetime import datetime

from pydantic import BaseModel


class ConversationParticipant(BaseModel):
    user_id: int
    username: str


class ConversationDetailResponse(BaseModel):
    id: int
    participants: list[ConversationParticipant]


class ConversationResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationStartResponse(BaseModel):
    conversation_id: int