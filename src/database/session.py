import json

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from functools import wraps
from contextlib import contextmanager
from sqlalchemy.orm import Session
from config import SQLALCHEMY_DATABASE_URI

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


@contextmanager
def session_scope() -> Session:
    """
    使用contextmanager获取session
    :return:
    """
    session = SessionLocal()
    try:
        # 将session对象传递给使用这个上下文管理器的代码块
        yield session
        # 如果代码执行成功则提交
        session.commit()
    except:
        # 执行过程中出现异常则回滚
        session.rollback()
        raise
    finally:
        # 释放数据库session
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            try:
                result = f(session, *args, **kwargs)
                session.commit()
                return result
            except:
                session.rollback()
                raise

    return wrapper


def get_db() -> SessionLocal:
    """
    获取一个数据库session,使用完成后关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db0() -> SessionLocal:
    """
    获取一个数据库session
    :return: SessionLocal
    """
    db = SessionLocal()
    return db
