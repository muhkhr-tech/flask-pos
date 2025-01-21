from flask import flash
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func, literal, select, update, text
from sqlalchemy.orm import joinedload

from app import models
from app.core.db import get_db_session
from app.utils import generate_code


async def get_sale(status):
    with get_db_session() as db:
        sale = (
            db.query(models.Sale)
            .options(joinedload(models.Sale.cashier))
            .filter_by(status=status)
            .first()
        )
        return sale


async def get_struct(status):
    with get_db_session() as db:
        stmt = text("SELECT * FROM v_get_struct WHERE status=:status")
        result = db.execute(stmt, {"status": status})
        sale = result.fetchone()
        return sale


async def create_sale(user_id, product_id, price):
    sale = models.Sale()
    detail = models.SaleDetail()

    total_amount = price

    sale.code = generate_code(15)
    sale.user_id = user_id
    sale.total_amount = total_amount
    sale.payment_method = "cash"
    sale.status = "menunggu"

    with get_db_session() as db:
        try:
            db.add(sale)
            db.flush()

            detail.sale_id = sale.sale_id
            detail.product_id = product_id
            detail.quantity = 1
            detail.price = price
            detail.subtotal = total_amount

            db.add(detail)
            db.commit()
            flash("Berhasil membuat struk.", "success")
            return True
        except Exception as e:
            flash(f"Gagal membuat struk. {e}", "error")
            db.rollback()


async def update_sale(user_id, sale_id, product_id, price):
    with get_db_session() as db:
        try:
            stmt = (
                insert(models.SaleDetail)
                .values(
                    sale_id=sale_id,
                    product_id=product_id,
                    quantity=1,
                    price=price,
                    subtotal=price,
                )
                .on_conflict_do_update(
                    index_elements=["sale_id", "product_id"],
                    set_={
                        "quantity": models.SaleDetail.quantity + 1,
                        "subtotal": models.SaleDetail.subtotal + price,
                    },
                )
            )

            db.execute(stmt)

            update_stmt = (
                update(models.Sale)
                .where(models.Sale.sale_id == sale_id)
                .values(
                    user_id=user_id,
                    total_amount=(
                        select(func.sum(models.SaleDetail.subtotal))
                        .where(models.SaleDetail.sale_id == sale_id)
                        .scalar_subquery()
                    ),
                )
            )

            db.execute(update_stmt)
            db.commit()
            flash("Berhasil mengubah struk.", "success")
            return True
        except Exception as e:
            flash(f"Gagal mengubah struk. {e}", "error")
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
