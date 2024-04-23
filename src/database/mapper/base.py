from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import SQLALCHEMY_DATABASE_URI
from database.models.base import Base

# Database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create tables
Base.metadata.create_all(engine)

# Same as the Session(engine)
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def session_scope() -> Session:
    """上下文管理器用于自动获取 Session,确保线程安全"""
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            try:
                result = f(session, *args, **kwargs)
                return result
            except Exception as e:
                session.rollback()

    return wrapper


def generate_session() -> LocalSession:
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()


def get_session() -> LocalSession:
    return LocalSession()
