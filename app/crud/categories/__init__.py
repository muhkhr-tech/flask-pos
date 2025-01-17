from flask import flash

from app import models
from app.core.db import get_db_session


async def get_all_categories(status=None):
    with get_db_session() as db:
        if status:
            rows = db.query(models.Category).filter_by(is_active=status).all()
        else:
            rows = db.query(models.Category).all()
        return rows


def create_category(code, name, description):
    category = models.Category()
    category.name = name
    category.code = code
    category.description = description

    with get_db_session() as db:
        db.add(category)
        try:
            db.commit()
            db.refresh(category)
            flash(f"Berhasil menambah kategori: {category.name}", "success")
            return category
        except Exception as e:
            flash("Gagal membuat kategori produk.", "error")


def update_status_category(id):
    with get_db_session() as db:
        category = db.query(models.Category).get(id)
        category.is_active = not category.is_active
        db.commit()
        db.refresh(category)
