from fastapi import Body
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from llm import get_correspond_llm


async def completion(
        query: str = Body(),
        model_name: str = Body(default="glm-4"),
        temperature: float = Body(default=0.5),
        max_tokens: None | int = Body(default=None),
        streaming: bool = Body(default=False),
        prompt: str = Body(default="default")
):
    callback = AsyncIteratorCallbackHandler()
    llm = get_correspond_llm(model_name, temperature, max_tokens, streaming)
    prompt_template = ""
    if prompt == 'default':
        prompt_template = """{query}"""
    prompt = PromptTemplate.from_template(prompt_template)
    completion_chain = LLMChain(prompt=prompt, llm=llm, callbacks=[callback])
    return completion_chain.invoke({"query": query})
