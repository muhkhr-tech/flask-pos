import psycopg2
from flask import flash
from sqlalchemy import func, literal, select, update, text, false
from sqlalchemy.orm import joinedload

from app import models
from app.core.db import get_db_session
from app.utils import generate_code


def get_all_sales():
    with get_db_session() as db:
        rows = db.query(models.Sale).options(joinedload(models.Sale.cashier)).all()
        return rows


def get_sale_by_id(sale_id):
    with get_db_session() as db:
        stmt = text("SELECT * FROM v_get_struct WHERE sale_id=:sale_id")
        result = db.execute(stmt, {"sale_id": sale_id})
        sale = result.fetchone()

        return sale


async def get_sale(status=None):
    with get_db_session() as db:
        sale = (
            db.query(models.Sale)
            .options(joinedload(models.Sale.cashier))
            .filter_by(status=status)
            .first()
        )
        return sale


async def get_struct(status=None):
    with get_db_session() as db:
        stmt = text("SELECT * FROM v_get_struct WHERE status=:status")
        result = db.execute(stmt, {"status": status})
        sale = result.fetchone()
        return sale


async def create_sale(user_id, product_id):
    with get_db_session() as db:
        try:

            stmt = text("SELECT insert_sales(:product_id, :user_id, :code)")
            db.execute(
                stmt,
                {
                    "product_id": product_id,
                    "user_id": user_id,
                    "code": generate_code(15),
                },
            )
            db.commit()
            flash("Berhasil membuat struk.", "success")
            return True
        except Exception as e:
            original_error = e.orig
            if isinstance(original_error, psycopg2.errors.RaiseException):
                error_message = original_error.pgerror
                if "stok kurang" in error_message.lower():
                    flash("Gagal membuat struk: Stok tidak mencukupi.", "error")
                else:
                    flash(f"Gagal membuat struk: {error_message}", "error")
            else:
                flash(f"Gagal membuat struk. {e}", "error")

            db.rollback()


async def update_cart(user_id, sale_id, product_id):
    with get_db_session() as db:
        try:
            stmt = text("SELECT update_cart(:sale_id, :product_id, :user_id)")
            db.execute(
                stmt, {"sale_id": sale_id, "product_id": product_id, "user_id": user_id}
            )
            db.commit()
            flash("Berhasil mengubah struk.", "success")
            return True
        except Exception as e:
            original_error = e.orig
            if isinstance(original_error, psycopg2.errors.RaiseException):
                error_message = original_error.pgerror
                if "stok kurang" in error_message.lower():
                    flash("Gagal membuat struk: Stok tidak mencukupi.", "error")
                else:
                    flash(f"Gagal membuat struk: {error_message}", "error")
            else:
                flash(f"Gagal membuat struk {e}.", "error")

            db.rollback()


def payment(user_id, sale_id, payment_method, amount_paid):
    with get_db_session() as db:
        sale = db.query(models.Sale).get(sale_id)
        print(amount_paid)

        if int(amount_paid) < sale.total_amount:
            flash("Total bayar kurang", "error")
            return False
        try:
            sale.payment_method = payment_method
            sale.amount_paid = amount_paid
            sale.amount_change = int(amount_paid) - sale.total_amount
            sale.status = "sukses"
            sale.user_id = user_id
            db.commit()
            flash("Transaksi berhasil diselesaiakan.", "success")
            return True
        except Exception as e:
            flash(f"Transaksi gagal {e}.", "error")
            db.rollback()


async def delete_sale(user_id, sale_id, product_id):
    with get_db_session() as db:
        try:
            stmt = text(
                "SELECT update_sale_details_and_sales(:sale_id, :product_id, :user_id)"
            )

            db.execute(
                stmt, {"sale_id": sale_id, "product_id": product_id, "user_id": user_id}
            )
            db.commit()
            flash("Berhasil mengubah struk.", "success")
            return True
        except Exception as e:
            flash(f"Gagal mengubah struk. {e}", "error")
            db.rollback()


#
# def update_sale(data: schemas.saleUpdate):
#     with get_db_session() as db:
#         sale = db.query(models.sale).get(data.sale_id)
#
#         sale.name = data.name
#         sale.slug = slugify(data.name)
#         sale.categories = ", ".join(data.categories)
#         sale.phone = data.phone
#         sale.description = data.description
#         sale.open_at = data.open_at
#         sale.close_at = data.close_at
#         sale.google_maps = data.google_maps
#
#         try:
#             db.commit()
#             return True
#         except Exception as e:
#             flash("Gagal mengubah toko.", "error")
#
#
# def update_status_sale(slug):
#     with get_db_session() as db:
#         sale = db.query(models.sale).filter_by(slug=slug).first()
#
#         sale.is_active = not sale.is_active
#         db.commit()
#         db.refresh(sale)
