from fastapi import Body
from config import CHAT_MODEL, TEMPERATURE
from utils import wrap_done
from langchain.chains import LLMChain
from langchain.callbacks import AsyncIteratorCallbackHandler
from typing import (AsyncIterator, Union, List, Optional)
import asyncio
import json
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

async def base_chat(
        query: str = Body(..., description="Your query"),
        conversation_id: str = Body(..., description="Your conversation id"),
        history_len: int = Body(-1, description="The length of history (in seconds)"),
        history: Union[int, List[BaseChatMessageHistory]] = Body([], description="The history (in seconds)"),
        stream:bool=Body(False, description="Whether to stream or not"),
        model_name: str = Body('glm4', description="The name of the model"),
        temperature: float = Body(..., description="The temperature of the model"),
        max_tokens: Optional[int] = Body(None, description="The maximum number of tokens"),
        prompt_template: str = Body("default", description="The prompt template"),
):
    async def chat_iterator() -> AsyncIterator[str]:
        nonlocal history, max_tokens
        callback = AsyncIteratorCallbackHandler()
        callbacks = [callback]
        memory = None
