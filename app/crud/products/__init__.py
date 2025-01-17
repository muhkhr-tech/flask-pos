from flask import flash

from app import models
from app.core.db import get_db_session
from app.utils import generate_code


async def get_all_products(status=None):
    with get_db_session() as db:
        if status:
            rows = db.query(models.Product).filter_by(is_active=status).all()
        else:
            rows = db.query(models.Product).all()
        return rows


def create_product(name, price):
    product = models.Product()
    product.name = name
    product.code = generate_code(10)
    product.price = price

    with get_db_session() as db:
        db.add(product)
        try:
            db.commit()
            db.refresh(product)
            flash(f"Berhasil menambah produk: {product.name}", "success")
            return product
        except Exception as e:
            flash("Gagal membuat produk.", "error")


def update_stock_product(id, stock):
    with get_db_session() as db:
        try:
            product = db.query(models.Product).get(id)
            product.stock = stock
            db.commit()
            db.refresh(product)
            flash(f"Berhasil mengubah stok produk: {product.name}", "success")
            return product
        except Exception as e:
            flash("Gagal mengubah stok produk.", "error")


def update_status_product(id):
    with get_db_session() as db:
        product = db.query(models.Product).get(id)
        product.is_active = not product.is_active
        db.commit()
        db.refresh(product)
