from langchain_core.callbacks import Callbacks


def get_correspond_llm(model_name: str,
                       temperature: float,
                       max_tokens: int = None,
                       streaming: bool = False,
                       callbacks: Callbacks = None):
    if model_name.startswith("glm"):
        from langchain_community.chat_models import ChatZhipuAI
        return ChatZhipuAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
            callbacks=callbacks
        )
