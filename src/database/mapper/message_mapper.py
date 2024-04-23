from database.mapper.base import *
from database.models import MessageModel


@with_session
def upsert_message(session: Session, message: MessageModel) -> int:
    session.add(message)
    session.commit()
    return message.id


@with_session
def get_message_by_id(session: Session, message_id: int):
    return session.query(MessageModel).filter(MessageModel.id == message_id).first()


@with_session
def get_all_message(session: Session):
    return session.query(MessageModel).all()


@with_session
def get_message_by_conversation_id(session: Session, conversation_id: int, limit: int = 10):
    messages = (session.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).
                order_by(MessageModel.create_time).limit(limit).all())
    return messages
