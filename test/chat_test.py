import asyncio

from chat import base_chat


# 测试函数
async def test_base_chat():
    # 设置你的测试参数
    query = "你好！"
    conversation_id = "你的测试会话ID"
    history_len = -1
    history = None  # 或者你可以创建一个测试历史对象
    model_name = 'glm4'
    temperature = 0.5
    max_tokens = None  # 或者你可以设置一个具体的值
    prompt_template = """你是一个人工智能助手。\n
    {history}\n
    Human:{query}\n
    AI:"""

    # 调用 base_chat 函数
    response = await base_chat(
        query=query,
        stream=False,
        model_name=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        prompt_template=prompt_template
    )

    # 打印响应
    for item in response:
        print(item)


# 运行测试函数
asyncio.run(test_base_chat())
