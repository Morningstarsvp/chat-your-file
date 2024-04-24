from database.mapper.base import *
from database.models.ConversationModel import ConversationModel


@with_session
def upsert_conversation(session: Session, conversation: ConversationModel) -> str:
    session.add(conversation)
    session.commit()
    return conversation.id


@with_session
def get_conversation_by_id(session: Session, conversation_id: str):
    return session.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()


@with_session
def get_all_conversation(session: Session):
    return session.query(ConversationModel).all()
