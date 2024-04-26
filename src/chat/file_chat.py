from fastapi import Body
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from callback_handler import ConversationCallbackHandler
from config import get_logger, PROMPT_TEMPLATES
from database import crud, schemas
from llm import get_correspond_llm
from memory import ConversationDatabaseBufferMemory
from rag import get_temp_vectorstore

logger = get_logger(__name__)


async def file_chat(
        query: str = Body(..., description="用户输入"),
        file_vs_id: str = Body(..., description="包含文件数据的临时知识库ID"),
        conversation_id: str = Body(None, description="通过会话ID追踪聊天历史,由前端传入"),
        model_name: str = Body('glm-4', description="选用的LLM模型名"),
        temperature: float = Body(0.5, description="模型温度"),
        max_tokens: int | None = Body(None, description="最大token"),
        streaming: bool = Body(False, description="流式输出"),
        template_name: str = Body("default", description="提示模板名"),
):
    chat_type = "file_chat"
    vs = get_temp_vectorstore(file_vs_id)
    docs = vs.similarity_search(query=query)
    context = "\n".join([doc.page_content for doc in docs])
    if conversation_id is None:
        # 如果传入的conversation_id为空，表明当前为新建会话，创建conversation
        new_conversation = schemas.ConversationBase(name="file_conversation", chat_type=chat_type)
        conversation_id = crud.create_conversation(new_conversation)
    # 获取会话历史
    memory = ConversationDatabaseBufferMemory(conversation_id=conversation_id)
    chat_history = memory.load_memory_variables({}).get(memory.memory_key)
    logger.info(f"get history from conversation: {conversation_id}, chat_history: \n{chat_history}")
    # 获取提示模板
    prompt_template = PROMPT_TEMPLATES.get(chat_type).get(template_name)
    prompt = PromptTemplate.from_template(prompt_template)
    logger.info(f"load prompt template: {prompt.template}")
    # 创建会话回调管理器，实现会话持久化
    conversation_callback = ConversationCallbackHandler(
        conversation_id=conversation_id,
        query=query
    )
    callbacks = [conversation_callback]
    # 获取聊天模型
    chat_model = get_correspond_llm(model_name, temperature, max_tokens, streaming)
    file_chat_chain = prompt | chat_model | StrOutputParser()
    response = file_chat_chain.invoke(
        {"question": query, "chat_history": chat_history, "context": context},
        config={
            "callbacks": callbacks
        }
    )
    return {
        "conversation_id": conversation_id,
        "chat_history": str(chat_history),
        "question": query,
        "response": response
    }
