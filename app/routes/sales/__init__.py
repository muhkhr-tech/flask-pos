from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import current_user, login_required
from sqlalchemy.orm import joinedload

from app.core.db import get_db_session
from app import crud, schemas, models
from app.utils import role_required

sale_bp = Blueprint("sales", __name__, template_folder="templates")


@sale_bp.route("/")
@login_required
@role_required("cashier")
def index():
    with get_db_session() as db:
        rows = db.query(models.Sale).options(joinedload(models.Sale.cashier)).all()

    return render_template("sales/index.html", rows=rows)


@sale_bp.route("/create", methods=["POST"])
async def create_sale():
    user_id = current_user.user_id
    product_id = request.form["product_id"]
    price = request.form["price"]

    get_sale_await = await crud.get_sale("menunggu")

    if get_sale_await:
        await crud.update_sale(user_id, get_sale_await.sale_id, product_id, price)
    else:
        await crud.create_sale(user_id, product_id, price)
    return redirect(url_for("main.index"))


@sale_bp.route("/delete", methods=["POST"])
async def delete_sale():
    user_id = current_user.user_id
    product_id = request.form["product_id"]
    sale_id = request.form["sale_id"]

    await crud.delete_sale(user_id, sale_id, product_id)

    return redirect(url_for("main.index"))
