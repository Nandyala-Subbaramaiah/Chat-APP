from pydantic import BaseModel


class ConversationMemberResponse(BaseModel):
    id: int
    conversation_id: int
    user_id: int

    class Config:
        from_attributes = True