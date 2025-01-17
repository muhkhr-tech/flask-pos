from sqlalchemy import (
    Column,
    Integer,
    String,
    TEXT,
    DATETIME,
    Boolean,
    ForeignKey,
    INTEGER,
    DECIMAL,
)

from ..core.db import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL)
    stock = Column(INTEGER, default=0)
    is_active = Column(Boolean)
    created_at = Column(DATETIME)
    category_id = Column(INTEGER, ForeignKey("categories.category_id"))
