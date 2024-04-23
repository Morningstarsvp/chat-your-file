from typing import Optional
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import *
from sqlalchemy import func


class Base(DeclarativeBase):
    pass
