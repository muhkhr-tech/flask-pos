from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    current_app,
)
from flask_login import login_user, logout_user, login_required

from app import crud
from app import schemas, models
from app.core.db import get_db_session
from app.utils.token import verify_token

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        is_auth = crud.auth(
            schemas.UserLogin(
                username=request.form["username"], password=request.form["password"]
            )
        )

        if not is_auth:
            return render_template("auth/login.html")

        if not is_auth.is_active:
            flash(f"Akun {request.form['username']} tidak aktif.", "error")
            return render_template("auth/login.html")
        print(is_auth)
        login_user(is_auth)

        return redirect(url_for("main.index"))

    return render_template("auth/login.html", title="Masuk")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
