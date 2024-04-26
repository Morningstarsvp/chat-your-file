import logging
from typing import Any, Dict, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult

from database import schemas, crud

from config import get_logger

logger = get_logger(__name__)


class ConversationCallbackHandler(BaseCallbackHandler):
    """
    ConversationCallbackHandler:会话回调处理器
    override:
        on_llm_start
        on_llm_end:将LLM response存入数据库
    """
    raise_error: bool = True

    def __init__(self, conversation_id: str, query: str):
        self.conversation_id = conversation_id
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
        logger.info(f"ConversationCallbackHandler on_llm_start: pass")
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        LLM响应结束时，使用callback将response存入数据库中
        :param response:
        :param kwargs:
        :return:
        """
        logger.info(f"ConversationCallbackHandler on_llm_end: {response}")
        response = response.generations[0][0].text
        new_message = schemas.MessageBase(query=self.query, response=response)
        crud.create_message(new_message, conversation_id=self.conversation_id)
