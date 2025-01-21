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


class SaleDetail(Base):
    __tablename__ = "sale_details"

    sale_detail_id = Column(Integer, primary_key=True)
    quantity = Column(INTEGER, nullable=False)
    price = Column(DECIMAL, nullable=False)
    subtotal = Column(DECIMAL, nullable=False)
    sale_id = Column(INTEGER, ForeignKey("sales.sale_id"))
    product_id = Column(INTEGER, ForeignKey("products.product_id"))
