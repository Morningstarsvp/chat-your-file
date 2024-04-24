from database.models.base import *


class MessageModel(Base):
    """
    聊天记录模型:聊天记录的核心是一个问答对,Human和AI交替进行
    """
    __tablename__ = 'message_tb'
    id: Mapped[str] = mapped_column(String(32), default=uuid.uuid1().hex, primary_key=True, comment="聊天记录主键ID")
    query: Mapped[str] = mapped_column(String(4096), nullable=True, comment="用户提问")
    response: Mapped[str] = mapped_column(String(4096), nullable=True, comment="AI回答")
    meta_data: Mapped[Optional[str]] = mapped_column(default=None, nullable=True, comment="元数据")
    feedback_score: Mapped[int] = mapped_column(Integer, default=-1, comment="用户评分")
    feedback_reason: Mapped[str] = mapped_column(String(512), default="", comment="用户反馈")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversation_tb.id"), comment="所属会话ID")

    def __repr__(self):
        return (f"<MessageModel(id={self.id}, query={self.query}, response={self.response},"
                f" meta_data={self.meta_data}, feedback_score={self.feedback_score}, "
                f"conversation_id={self.conversation_id})>")
