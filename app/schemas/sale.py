from datetime import datetime
from optparse import Option
from typing import Set, Union, Optional

from flask import flash
from pydantic import BaseModel, Field, ValidationError
from app.utils import convert_errors, CUSTOM_MESSAGES


class SaleSchema(BaseModel):
    total_amount: float
    payment_method: str
    status: str
    # canceled_by: Optional[int] = Field(None)
    user_id: int
