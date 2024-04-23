import uuid

from database.models.base import *


class ConversationModel(Base):
    __tablename__ = 'conversation_tb'
    id: Mapped[str] = mapped_column(String(32), default=uuid.uuid4().hex, primary_key=True, comment="会话主键ID")
    name: Mapped[str] = mapped_column(String(32), comment="对话框名称")
    chat_type: Mapped[str] = mapped_column(String(30), comment="聊天类型")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")

    def __repr__(self):
        return (f"<ConversationModel(id={self.id}, name={self.name}), "
                f"chat_type={self.chat_type}, create_time={self.create_time}>")
