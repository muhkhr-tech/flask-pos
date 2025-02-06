import datetime

from flask import flash

from app import models
from app.core.db import get_db_session
from app.utils import generate_code


async def get_all_products(status=None):
    with get_db_session() as db:
        if status:
            rows = (
                db.query(models.Product)
                .filter_by(is_active=status)
                .order_by(models.Product.name)
                .all()
            )
        else:
            rows = db.query(models.Product).order_by(models.Product.name).all()
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
            flash(f"Gagal membuat produk. {e}", "error")


def update_stock_product(id, stock, change_type, note):
    with get_db_session() as db:
        try:
            product = db.query(models.Product).get(id)

            if change_type == "adjustment":
                if product.stock < int(stock):
                    flash("Stok kurang.", "error")
                    return False
                else:
                    product.stock -= int(stock)
            elif change_type == "restock":
                product.stock += int(stock)

            inventory_log = models.InventoryLog()
            inventory_log.product_id = id
            inventory_log.quantity = stock
            inventory_log.change_type = change_type
            inventory_log.log_date = datetime.datetime.now()
            inventory_log.note = note
            db.add(inventory_log)
            db.commit()
            db.refresh(product)
            flash(f"Berhasil mengubah stok produk: {product.name}", "success")
            return product
        except Exception as e:
            flash(f"Gagal mengubah stok produk.{e}", "error")


def update_status_product(id):
    with get_db_session() as db:
        product = db.query(models.Product).get(id)
        product.is_active = not product.is_active
        db.commit()
        db.refresh(product)
