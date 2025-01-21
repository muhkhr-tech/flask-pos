from sqlalchemy import Column, Integer, String, Boolean, DATETIME
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

from ..core.db import Base


class User(Base, UserMixin):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    # email = Column(String(100), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    role = Column(String(10))
    created_at = Column(DATETIME)

    def get_id(self):
        return str(self.user_id)
