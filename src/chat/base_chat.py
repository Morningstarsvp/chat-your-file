import asyncio
import json
from typing import (AsyncIterator, Optional)

from fastapi import Body
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from callback_handler.ConversationCallbackHandler import ConversationCallbackHandler
from database import (ConversationModel, upsert_conversation,
                      MessageModel, upsert_message, )
from memory import ConversationDatabaseBufferMemory
from utils import wrap_done


async def base_chat(
        query: str = Body(..., description="Your query"),
        conversation_id: str = Body(None, description="Your conversation id"),
        # history_len: int = Body(-1, description="The length of history (in seconds)"),
        # history: BaseChatMessageHistory = Body(None, description="The chat message history"),
        stream: bool = Body(False, description="Whether to stream or not"),
        model_name: str = Body('glm-4', description="The name of the model"),
        temperature: float = Body(0.5, description="The temperature of the model"),
        max_tokens: Optional[int] = Body(None, description="The maximum number of tokens"),
        prompt_template: str = Body("default", description="The prompt template"),
):
    async def chat_iterator() -> AsyncIterator[str]:
        nonlocal max_tokens, conversation_id, prompt_template
        callback = AsyncIteratorCallbackHandler()
        callbacks = [callback]

        if conversation_id is None:
            new_conversation = ConversationModel(name="default", chat_type="llm_chat")
            conversation_id = upsert_conversation(new_conversation)
        conversation_callback = ConversationCallbackHandler(
            conversation_id=conversation_id,
            query=query
        )
        callbacks.append(conversation_callback)
        memory = ConversationDatabaseBufferMemory(conversation_id=conversation_id)
        from langchain_community.chat_models import ChatZhipuAI
        import os
        os.environ["ZHIPUAI_API_KEY"] = "5ede9ccf9f7967a2eb082f89657c2297.Zmfr3ej8HAcLs83R"
        chat_model = ChatZhipuAI(
            model_name=model_name, temperature=temperature, max_tokens=max_tokens, streaming=stream)
        if prompt_template == 'default':
            prompt_template = """你是一个人工智能助手\n{chat_history}\nHuman:{query}\nAI:"""
        prompt = PromptTemplate.from_template(prompt_template)
        llm_chat_chain = LLMChain(prompt=prompt, llm=chat_model, memory=memory, callbacks=callbacks)
        task = asyncio.create_task(wrap_done(llm_chat_chain.ainvoke({"query": query}), callback.done))
        if stream:
            async for token in callback.aiter():
                yield json.dumps({"text": token, "conversation_id": conversation_id}, ensure_ascii=False)
        else:
            answer = ""
            async for token in callback.aiter():
                answer += token
            yield json.dumps({"text": answer, "conversation_id": conversation_id}, ensure_ascii=False)
        await task

    from sse_starlette.sse import EventSourceResponse
    return EventSourceResponse(chat_iterator())
