from typing import Any, Dict, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

from database import upsert_message, get_message_by_id, MessageModel


class ConversationCallbackHandler(BaseCallbackHandler):
    raise_error: bool = True

    def __init__(self, message_id: int, conversation_id: str, chat_type: str, query: str):
        self.message_id = message_id
        self.conversation_id = conversation_id
        self.chat_type = chat_type
        self.query = query
        self.start_at = None

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # 如果想存更多信息，则prompts 也需要持久化
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        LLM响应结束时，使用callback将response存入数据库中
        :param response:
        :param kwargs:
        :return:
        """
        response = response.generations[0][0].text
        message: MessageModel = get_message_by_id(message_id=self.message_id)
        message.response = response
        upsert_message(message)
