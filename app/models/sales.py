from datetime import datetime

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


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    code = Column(String(15), nullable=False, unique=True)
    total_amount = Column(DECIMAL, nullable=False)
    amount_paid = Column(DECIMAL, nullable=False, default=0)
    amount_change = Column(DECIMAL, nullable=False, default=0)
    payment_method = Column(String(10))
    status = Column(String(7), nullable=False)
    sale_date = Column(TIMESTAMP(timezone=True), nullable=False)
    canceled_by = Column(INTEGER)
    user_id = Column(INTEGER, ForeignKey("users.user_id"))
    cashier = relationship("User", foreign_keys=[user_id])
