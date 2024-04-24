from database.models.base import *


class ConversationModel(Base):
    __tablename__ = 'conversation_tb'
    id: Mapped[str] = mapped_column(String(32), default=uuid.uuid4().hex, primary_key=True, comment="会话主键ID")
    name: Mapped[str] = mapped_column(String(32), default="default conversation", comment="对话框名称")
    chat_type: Mapped[str] = mapped_column(String(30), default="llm_chat", comment="聊天类型")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    messages: Mapped[List["MessageModel"]] = relationship(lazy="subquery")

    def __repr__(self):
        return (f"<ConversationModel(id={self.id}, name={self.name}, chat_type={self.chat_type},"
                f" create_time={self.create_time}, messages={self.messages})>")
