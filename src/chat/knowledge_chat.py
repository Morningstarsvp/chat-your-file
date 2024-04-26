from fastapi import Body


async def knowledge_chat(
        query: str = Body(..., description="用户提问"),
        knowledge_base_name: str = Body(..., description="知识库名称"),
        conversation_id: str = Body(None, description="通过会话ID追踪聊天历史,由前端传入"),
        model_name: str = Body('glm-4', description="选用的LLM模型名"),
        temperature: float = Body(0.5, description="模型温度"),
        max_tokens: int | None = Body(None, description="最大token"),
        streaming: bool = Body(False, description="流式输出"),
        template_name: str = Body("default", description="提示模板名"),
):
    ...
