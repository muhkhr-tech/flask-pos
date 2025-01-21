from flask import render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.core.db import get_db_session
from app.models import User
from app import crud, schemas
from app.routes.master import master_user_bp


@master_user_bp.route("/")
@login_required
def index():
    with get_db_session() as db:
        rows = db.query(User).all()

    return render_template("users/index.html", rows=rows)


@master_user_bp.route("/create-cashier", methods=["GET", "POST"])
@login_required
def create_cashier():
    if request.method == "POST":
        if crud.create_cashier(
            schemas.CashierCreate(
                username=request.form["username"],
                password=request.form["password"],
                confirmed_password=request.form["confirmed_password"],
            )
        ):
            return redirect(url_for("master_user.index"))

    return render_template("users/create-cashier.html")
