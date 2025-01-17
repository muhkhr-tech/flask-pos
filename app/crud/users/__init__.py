import logging
from flask import flash, render_template, request

from app import models
from app import schemas
from app.utils import generate_password, check_password, is_valid_password
from app.core.db import get_db_session
from app.utils.token import create_token


def create_member(data: schemas.UserRegister):
    logger = logging.getLogger("flask")

    user = models.User()
    user.name = data.name
    user.username = data.username
    user.email = data.email
    user.password = generate_password(data.password)
    user.role = "admin"

    if not is_valid_password(data.password, data.password_confirm):
        return False

    with get_db_session() as db:
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            logger.error(e)
            flash("Gagal membuat akun.", "error")


def auth(data: schemas.UserLogin):
    with get_db_session() as db:
        user = db.query(models.User).filter_by(username=data.username).first()

        if not user:
            flash("Username tidak terdaftar", "error")
            return None

        is_valid = check_password(user.password, data.password)

        if not is_valid:
            flash("Password salah", "error")
            return None

    return user
