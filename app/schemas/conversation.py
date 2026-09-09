from datetime import datetime

from pydantic import BaseModel


class ConversationResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationStartResponse(BaseModel):
    conversation_id: int