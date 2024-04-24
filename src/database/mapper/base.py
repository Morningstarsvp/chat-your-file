from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session, joinedload, lazyload, immediateload

from config import SQLALCHEMY_DATABASE_URI

# Database engine
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Create tables
# Base.metadata.create_all(engine)

# Same as the Session(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


@contextmanager
def session_scope() -> Session:
    """上下文管理器用于自动获取 Session,确保线程安全"""
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
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
