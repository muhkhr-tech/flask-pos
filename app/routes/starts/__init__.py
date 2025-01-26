from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from app import crud
from app.utils import role_required, get_status, get_formatted_date

start_bp = Blueprint("starts", __name__, template_folder="templates")


@start_bp.route("/create-admin", methods=["GET", "POST"])
def create_admin():

    if request.method == "POST":
        if crud.create_admin(
            username=request.form["username"],
            password=request.form["password"],
            confirmed_password=request.form["confirmed_password"],
        ):
            return redirect(url_for("main.index"))

    return render_template("starts/create-admin.html")


# @master_user_bp.route("/create-cashier", methods=["GET", "POST"])
# @login_required
# def create_cashier():
#     if request.method == "POST":
#         if crud.create_cashier(
#             schemas.CashierCreate(
#                 username=request.form["username"],
#                 password=request.form["password"],
#                 confirmed_password=request.form["confirmed_password"],
#             )
#         ):
#             return redirect(url_for("master_user.index"))
#
#     return render_template("users/create-cashier.html")
