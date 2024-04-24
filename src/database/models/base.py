from typing import Optional, List, Set, Tuple, Dict
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import *
from sqlalchemy import func, ForeignKey, UniqueConstraint


class Base(DeclarativeBase):
    pass
