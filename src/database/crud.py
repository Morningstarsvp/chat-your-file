from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import SQLALCHEMY_DATABASE_URI, DATABASE_ECHO, get_logger
from database import models, schemas

logger = get_logger(__name__)

# Database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=DATABASE_ECHO)

# Create tables
models.Base.metadata.create_all(engine)

# Same as the Session(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


@contextmanager
def session_scope() -> Session:
    """上下文管理器用于自动获取 Session,确保线程安全"""
    session = SessionLocal()
    try:
        yield session
    except Exception:
        raise
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            try:
                result = f(session, *args, **kwargs)
                return result
            except Exception:
                session.rollback()
                raise

    return wrapper


def generate_session() -> SessionLocal:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_session() -> SessionLocal:
    return SessionLocal()


@with_session
def create_conversation(session: Session, conversation: schemas.ConversationBase):
    conversation_model = models.ConversationModel(**conversation.model_dump())
    session.add(conversation_model)
    session.commit()
    return conversation_model.id


@with_session
def get_conversation_by_id(session: Session, conversation_id: str):
    return schemas.Conversation.model_validate(
        session.query(models.ConversationModel).
        filter(models.ConversationModel.id == conversation_id).
        first()
    )


@with_session
def create_message(session: Session, message: schemas.MessageBase, conversation_id: str):
    message_model = models.MessageModel(**message.model_dump(), conversation_id=conversation_id)
    session.add(message_model)
    session.commit()
    return message_model.id


@with_session
def get_message_by_id(session: Session, message_id: str):
    return schemas.Message.model_validate(
        session.query(models.MessageModel).
        filter(models.MessageModel.id == message_id).
        first()
    )


@with_session
def get_message_list_by_conversation_id(session: Session, conversation_id: str):
    message_list = (
        session.query(models.MessageModel).
        filter(models.MessageModel.conversation_id == conversation_id).
        order_by(models.MessageModel.create_time).
        all()
    )
    message_list = [schemas.Message.model_validate(message) for message in message_list]
    return message_list


@with_session
def create_vs_collection(session: Session, vs_collection: schemas.VSCollectionBase):
    vs_collection_model = models.VSCollectionModel(**vs_collection.model_dump())
    session.add(vs_collection_model)
    session.commit()
    return vs_collection_model.id


@with_session
def get_vs_collection_by_id(session: Session, vs_collection_id: int):
    return schemas.VSCollection.model_validate(
        session.query(models.VSCollectionModel).
        filter(models.VSCollectionModel.id == vs_collection_id).
        first()
    )
