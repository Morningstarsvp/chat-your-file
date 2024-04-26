from typing import List, Dict, Any

from langchain.memory import ChatMessageHistory
from langchain.memory.chat_memory import BaseChatMemory

from database import *


class ConversationDatabaseBufferMemory(BaseChatMemory):
    conversation_id: str
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    memory_key: str = "chat_history"

    @property
    def buffer(self):
        messages: list[schemas.Message] = crud.get_message_list_by_conversation_id(self.conversation_id)
        chat_history = ChatMessageHistory()
        for message in messages:
            chat_history.add_user_message(message.query)
            chat_history.add_ai_message(message.response)
        return chat_history

    @property
    def memory_variables(self) -> List[str]:
        """
        :return: The string keys this memory class will add to chain inputs.
        """
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        :return: Return key-value pairs given the text input to the chain.
        """
        return {self.memory_key: self.buffer}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        pass

    def clear(self) -> None:
        """Clear memory contents. Clear DataBase memory is not allowed"""
        pass
