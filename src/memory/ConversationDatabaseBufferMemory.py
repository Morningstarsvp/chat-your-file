from typing import List, Dict, Any

from langchain.memory import ChatMessageHistory
from langchain.memory.chat_memory import BaseChatMemory

from database import get_conversation_by_id, MessageModel


class ConversationDatabaseBufferMemory(BaseChatMemory):
    human_prefix: str = "Human"
    ai_prefix: str = "AI"
    conversation_id: str
    memory_key: str = "chat_history"

    @property
    def buffer(self):
        conversation = get_conversation_by_id(conversation_id=self.conversation_id)
        messages: list[MessageModel] = conversation.messages
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
