from database.models.base import *


class MessageModel(Base):
    """
    聊天记录模型
    """
    __tablename__ = 'message_tb'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="聊天记录主键ID")
    conversation_id: Mapped[str] = mapped_column(String(32), default=None, comment="会话ID")
    chat_type: Mapped[str] = mapped_column(String(30), comment="聊天类型")
    query: Mapped[str] = mapped_column(String(4096), comment="用户提问")
    response: Mapped[str] = mapped_column(String(4096), comment="AI回答")
    meta_data: Mapped[Optional[str]] = mapped_column(default=None, nullable=True, comment="元数据")
    feedback_score: Mapped[int] = mapped_column(Integer, default=-1, comment="用户评分")
    feedback_reason: Mapped[str] = mapped_column(String(512), default="", comment="用户反馈")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")

    def __repr__(self):
        return (f"<message(id='{self.id}', conversation_id='{self.conversation_id}', chat_type='{self.chat_type}', "
                f"query='{self.query}', response='{self.response}',meta_data='{self.meta_data}',feedback"
                f"_score='{self.feedback_score}',feedback_reason='{self.feedback_reason}', create_time='"
                f"{self.create_time}')>")
