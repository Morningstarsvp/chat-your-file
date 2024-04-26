from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    query: str
    response: str
    meta_data: Optional[str] = None


class Message(MessageBase):
    id: str
    create_time: datetime
    conversation_id: str

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    name: str = "default"
    chat_type: str = "llm_chat"
    messages: list[Message] = []


class Conversation(ConversationBase):
    id: str
    create_time: datetime

    class Config:
        from_attributes = True


class VSCollectionBase(BaseModel):
    collection_name: str
    persist_directory: str
    embedding_function: str


class VSCollection(VSCollectionBase):
    id: int
    create_time: datetime
    embed_files: list = []

    class Config:
        from_attributes = True
