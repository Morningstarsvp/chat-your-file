from fastapi import Body
from config import CHAT_MODEL, TEMPERATURE
from utils import wrap_done
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import (AsyncIterator, Union, List, Optional)
import asyncio
import json
from langchain.memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

from database import (
    MessageModel, upsert_message, get_message_by_id,
    ConversationModel, upsert_conversation, get_conversation_by_id,
)
from callback_handler import ConversationCallbackHandler

async def base_chat(
        query: str = Body(..., description="Your query"),
        conversation_id: str = Body(..., description="Your conversation id"),
        history_len: int = Body(-1, description="The length of history (in seconds)"),
        history: BaseChatMessageHistory = Body(None, description="The chat message history"),
        stream:bool=Body(False, description="Whether to stream or not"),
        model_name: str = Body('glm4', description="The name of the model"),
        temperature: float = Body(0.5, description="The temperature of the model"),
        max_tokens: Optional[int] = Body(None, description="The maximum number of tokens"),
        prompt_template: str = Body("default", description="The prompt template"),
):
    async def chat_iterator() -> AsyncIterator[str]:
        nonlocal history, max_tokens
        callback = AsyncIteratorCallbackHandler()
        callbacks = [callback]
        memory = None

        chat_type = 'base_chat'
        user_message = MessageModel(
            conversation_id=conversation_id,
            chat_type=chat_type,
            query=query
        )
        message_id = upsert_message(user_message)
        conversation_callback = ConversationCallbackHandler(
            message_id=message_id,
            conversation_id=conversation_id,
            chat_type=chat_type,
            query=query
        )
        callbacks.append(conversation_callback)

        from langchain_zhipu import ChatZhipuAI
        chat_model = ChatZhipuAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens, streaming=stream)
        if history:
            from langchain.memory import ConversationBufferMemory
