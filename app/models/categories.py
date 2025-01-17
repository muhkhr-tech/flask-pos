from sqlalchemy import Column, Integer, String, TEXT, DATETIME, Boolean

from ..core.db import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True)
    code = Column(String(5), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    description = Column(TEXT)
    is_active = Column(Boolean)
    created_at = Column(DATETIME)
