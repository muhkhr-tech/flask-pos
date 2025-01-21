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

from ..core.db import Base


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    code = Column(String(15), nullable=False, unique=True)
    total_amount = Column(DECIMAL, nullable=False)
    payment_method = Column(String(10), nullable=False)
    status = Column(String(7), nullable=False)
    sale_date = Column(DATETIME, default=datetime.now())
    canceled_by = Column(INTEGER)
    user_id = Column(INTEGER, ForeignKey("users.user_id"))
    cashier = relationship("User", foreign_keys=[user_id])
