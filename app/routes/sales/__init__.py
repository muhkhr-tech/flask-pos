from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import crud
from app.utils import role_required

sale_bp = Blueprint("sales", __name__, template_folder="templates")


@sale_bp.route("/")
@login_required
@role_required("cashier")
def index():
    rows = crud.get_all_sales()
    return render_template("sales/index.html", rows=rows)


@sale_bp.route("/create", methods=["POST"])
async def create_sale():
    user_id = current_user.user_id
    product_id = request.form["product_id"]

    get_sale_await = await crud.get_sale("menunggu")

    if get_sale_await:
        await crud.update_cart(user_id, get_sale_await.sale_id, product_id)
    else:
        await crud.create_sale(user_id, product_id)
    return redirect(url_for("main.index"))


@sale_bp.route("/delete", methods=["POST"])
async def delete_sale():
    user_id = current_user.user_id
    product_id = request.form["product_id"]
    sale_id = request.form["sale_id"]

    await crud.delete_sale(user_id, sale_id, product_id)

    return redirect(url_for("main.index"))
