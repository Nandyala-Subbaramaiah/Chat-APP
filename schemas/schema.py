from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    phone: str
    username: str
    profile_pic: Optional[str] = None
    about: Optional[str] = None

class UserOut(UserBase):
    id: str
    is_online: bool
    last_seen: Optional[str]

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    is_group: bool = False
    group_name: Optional[str] = None

class ChatOut(ChatBase):
    id: str
    members: List[str]  # list of user ids
    last_message: Optional[str]

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    chat_id: str
    sender_id: str
    message: Optional[str] = None
    type: Optional[str] = "text"
    file_url: Optional[str] = None

class MessageOut(MessageBase):
    id: str
    status: str
    created_at: str

    class Config:
        orm_mode = True
