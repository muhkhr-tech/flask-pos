import logging
from flask import flash, render_template, request

from app import models
from app import schemas
from app.utils import generate_password, check_password, is_valid_password
from app.core.db import get_db_session
from app.utils.token import create_token


def create_admin(username, password, confirmed_password):

    user = models.User()
    user.username = username
    user.password = generate_password(password)
    user.role = "admin"

    if not is_valid_password(password, confirmed_password):
        return False

    with get_db_session() as db:
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            flash("Berhasil membuat akun admin.", "success")
            return user
        except Exception as e:
            flash("Gagal membuat akun admin..", "error")


def create_cashier(data: schemas.CashierCreate):

    user = models.User()
    user.username = data.username
    user.password = generate_password(data.password)
    user.role = data.role

    if not is_valid_password(data.password, data.confirmed_password):
        return False

    with get_db_session() as db:
        db.add(user)
        try:
            db.commit()
            db.refresh(user)
            flash("Berhasil membuat akun cashier.", "success")
            return user
        except Exception as e:
            flash("Gagal membuat akun cashier..", "error")


def auth(data: schemas.UserLogin):
    with get_db_session() as db:
        user = db.query(models.User).filter_by(username=data.username).first()

        if not user:
            flash("Username tidak terdaftar", "error")
            return None

        if not user.is_active:
            flash("User tidak aktif", "error")
            return None

        is_valid = check_password(user.password, data.password)

        if not is_valid:
            flash("Password salah", "error")
            return None

    return user


def update_status_user(id):
    with get_db_session() as db:
        user = db.query(models.User).get(id)
        user.is_active = not user.is_active
        db.commit()
        db.refresh(user)
