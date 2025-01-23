from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import crud
from app.utils import role_required, get_status

sale_bp = Blueprint("sales", __name__, template_folder="templates")


@sale_bp.route("/")
@login_required
@role_required("cashier")
def index():
    rows = crud.get_all_sales()
    return render_template("sales/index.html", rows=rows, get_status=get_status)


@sale_bp.route("/create", methods=["POST"])
async def create_sale():
    user_id = current_user.user_id
    product_id = request.form["product_id"]

    get_struct = await crud.get_sale("proses")

    if get_struct:
        await crud.update_cart(user_id, get_struct.sale_id, product_id)
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


@sale_bp.route("/<sale_id>/payment", methods=["GET", "POST"])
@login_required
@role_required("cashier")
def payment(sale_id):
    user_id = current_user.user_id
    sale = crud.get_sale_by_id(sale_id)

    if sale.status != "proses":
        return redirect(url_for("sales.index"))

    if request.method == "POST":
        if crud.payment(
            user_id,
            sale_id,
            request.form["payment_method"],
            request.form["amount_paid"],
        ):
            return redirect(url_for("sales.index"))

    return render_template("sales/payment.html", sale=sale, get_status=get_status)


@sale_bp.route("/<sale_id>/detail")
@login_required
def detail(sale_id):
    sale = crud.get_sale_by_id(sale_id)
    return render_template("sales/detail.html", sale=sale, get_status=get_status)
