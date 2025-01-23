import random, string
from functools import wraps
from flask import flash
from flask_login import current_user

from .validate_schema import *
from ..extensions import bcrypt


def generate_password(password):
    password_hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    return password_hashed


def check_password(password_hashed, password):
    return bcrypt.check_password_hash(password_hashed, password)


def is_valid_password(password, password_confirm):
    if password_confirm != password:
        flash("Password tidak cocok.", "error")
        return False

    if len(password) < 8:
        flash("Password minimal 8 karakter.", "error")
        return False

    return True

def generate_code(length):
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return code

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                return 'User tidak memiliki akses!'

            return func(*args, **kwargs)

        return wrapper
    return decorator

def get_status(status):
    color = ""
    if status == "proses":
        color = "text-bg-primary"
    if status == "sukses":
        color = "text-bg-success"
    if status == "gagal":
        color = "text-bg-secondary"
    if status == "batal":
        color = "text-bg-danger"

    return f"<span class='badge rounded-pill {color}'>{status.upper()}</span>"