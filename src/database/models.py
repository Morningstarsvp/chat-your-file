import uuid
from typing import Optional, List

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import *


def uuid4_hex() -> str:
    return uuid.uuid4().hex


def uuid1_hex() -> str:
    return uuid.uuid1().hex


class Base(DeclarativeBase):
    pass


class MessageModel(Base):
    """
    聊天记录模型:聊天记录的核心是一个问答对,Human和AI交替进行
    """
    __tablename__ = 'message_tb'
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), default=uuid1_hex, primary_key=True, comment="聊天记录主键ID")
    query: Mapped[str] = mapped_column(String(4096), nullable=True, comment="用户提问")
    response: Mapped[str] = mapped_column(String(4096), nullable=True, comment="AI回答")
    meta_data: Mapped[Optional[str]] = mapped_column(default=None, nullable=True, comment="元数据")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversation_tb.id"), comment="所属会话ID")

    def __repr__(self):
        return (f"<MessageModel(id={self.id}, query={self.query}, response={self.response},"
                f" meta_data={self.meta_data}, conversation_id={self.conversation_id})>")


class ConversationModel(Base):
    __tablename__ = 'conversation_tb'
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), default=uuid4_hex, primary_key=True, comment="会话主键ID")
    name: Mapped[str] = mapped_column(String(32), default="default conversation", comment="对话框名称")
    chat_type: Mapped[str] = mapped_column(String(30), default="llm_chat", comment="聊天类型")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    messages: Mapped[List["MessageModel"]] = relationship(lazy="subquery")

    def __repr__(self):
        return (f"<ConversationModel(id={self.id}, name={self.name}, chat_type={self.chat_type},"
                f" create_time={self.create_time}, messages={self.messages})>")


class VSCollectionModel(Base):
    __tablename__ = 'vs_collection_tb'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="向量库集合主键ID")
    collection_name: Mapped[str] = mapped_column(String, comment="集合名称")
    embedding_function: Mapped[str] = mapped_column(String, comment="嵌入模型")
    persist_directory: Mapped[str] = mapped_column(String, comment="向量库持久化地址")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")
    embed_files: Mapped[List["EmbedFileModel"]] = relationship(lazy="subquery")

    def __repr__(self):
        return (f"<VSCollectionModel(id={self.id}), collection_name={self.collection_name}, "
                f"persist_directory={self.persist_directory}, create_time={self.create_time}, "
                f"embed_files={self.embed_files})>")


class EmbedFileModel(Base):
    __tablename__ = 'embedfile_tb'
    id: Mapped[str] = mapped_column(Uuid(as_uuid=False), default=uuid1_hex, primary_key=True, comment="文件主键ID")
    path: Mapped[Optional[str]] = mapped_column(String, default=None, nullable=True, comment="文件临时存储地址")
    vs_collection_id: Mapped[int] = mapped_column(ForeignKey("vs_collection_tb.id"), comment="所属向量库id")
    embedding_model: Mapped[Optional[str]] = mapped_column(String, default=None, comment="嵌入模型信息")
    split_config: Mapped[Optional[str]] = mapped_column(default=None, nullable=True, comment="分块配置")
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), comment="创建时间")

    def __repr__(self):
        return (f"<EmbedFileModel(id={self.id}, path={self.path}, vs_collection_id={self.vs_collection_id}, "
                f"embedding_model={self.embedding_model}, split_config={self.split_config}, "
                f"create_time={self.create_time})>")
