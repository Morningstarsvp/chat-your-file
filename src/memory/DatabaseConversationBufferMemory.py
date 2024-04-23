from typing import List, Dict, Any

from langchain.memory import ChatMessageHistory
from langchain.memory.chat_memory import BaseChatMemory
from langchain_core.language_models import BaseLanguageModel

from database import get_message_by_conversation_id, MessageModel


class DatabaseConversationBufferMemory(BaseChatMemory):
    conversation_id: str
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    llm: BaseLanguageModel
    memory_key: str = "chat_history"
    max_token_limit: int = 4096
    message_limit: int = 10

    @property
    def buffer(self):
        messages: list[MessageModel] = get_message_by_conversation_id(conversation_id=self.conversation_id)
        chat_history = ChatMessageHistory()
        for message in messages:
            chat_history.add_user_message(message.query)
            chat_history.add_ai_message(message.response)
        return chat_history

    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        buffer = self.buffer
