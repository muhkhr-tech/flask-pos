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
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from ..core.db import Base


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    log_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False, default=0)
    change_type = Column(String(10))
    log_date = Column(TIMESTAMP(timezone=True), nullable=False)
    note = Column(TEXT)
    product_id = Column(INTEGER, ForeignKey("products.product_id"))
    product = relationship("Product", foreign_keys=[product_id])
